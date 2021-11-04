load "template.gnuplot"

set output '../plotTV_TH_Age.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/RKI_COVID19_Impfquotenmonitoring_Thuringia.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: RKI)}"

# x-axis setup
set xrange [-0.5:3.5]
set xtics rotate by 0 offset 0, 0
set xtics ("Gesamt" 0, "12-17\nJahre" 1, "18-59\nJahre" 2, "60+\nJahre" 3)

# y-axis setup
set ylabel "Impfquote in Thüringen"
set yrange [0:130]
set ytics 0, 20, 100
set format y "%.0f%%"
set mytics 2

# key
set key at graph 0.02, 0.98 left top spacing 1.2 box ls 3

# grid
unset grid 
set grid ytics ls 21 lc rgb '#aaaaaa'

# bars
set boxwidth 0.9
set style fill solid 1.00 
set style data histograms
set style histogram clustered gap 1


set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Impfquote nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, '{if (NR>1) {a[\"A00\"]=($6+$7)/2120237;a[\"A12-A17\"]=$4/105509;a[\"A18-A59\"]=$5/1057819;a[\"A60+\"]=$7/738544;b[\"A00\"]=($10+$11)/2120237;b[\"A12-A17\"]=$8/105509;b[\"A18-A59\"]=$9/1057819;b[\"A60+\"]=$11/738544;c[\"A00\"]=($14+$15)/2120237;c[\"A12-A17\"]=$12/105509;c[\"A18-A59\"]=$13/1057819;c[\"A60+\"]=$15/738544;}}END{ for (i in a) { print i, a[i], b[i], c[i] }}' ../data/RKI_COVID19_Impfquotenmonitoring_Thuringia.csv | sort -k 1" using (100*$2) with histograms lt rgb "#137e6d" title "Erstimpfung", \
  "" using (100*$3) with histograms lt rgb "#0b4008" title "Zweitimpfung", \
  "" using (100*$4) with histograms lt rgb "#0d9419" title "Auffrischimpfung", \
  \
  "<awk -F, '{if (NR>1) {a[\"A00\"]=($6+$7)/2120237;a[\"A12-A17\"]=$4/105509;a[\"A18-A59\"]=$5/1057819;a[\"A60+\"]=$7/738544;b[\"A00\"]=($10+$11)/2120237;b[\"A12-A17\"]=$8/105509;b[\"A18-A59\"]=$9/1057819;b[\"A60+\"]=$11/738544;c[\"A00\"]=($14+$15)/2120237;c[\"A12-A17\"]=$12/105509;c[\"A18-A59\"]=$13/1057819;c[\"A60+\"]=$15/738544;}}END{ for (i in a) { print i, a[i], b[i], c[i] }}' ../data/RKI_COVID19_Impfquotenmonitoring_Thuringia.csv | sort -k 1" using (column(0) - 0.30):(100*$2):($2>0?(sprintf("{/*0.85 %.1f%%}", 100*$2)):"") with labels center offset 0.0, 0.7 notitle, \
  "" using (column(0) + 0.0):(100*$3):($3>0?(sprintf("{/*0.85 %.1f%%}", 100*$3)):"") with labels center offset 0.0, 0.7 notitle, \
  "" using (column(0) + 0.28):(100*$4):($3>0?(sprintf("{/*0.85 %.1f%%}", 100*$4)):"") with labels center offset 0.0, 0.7 notitle
  
  
