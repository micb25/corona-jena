load "template.gnuplot"

set output '../plotT5C_RKI.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . ")}"

# get maximum y value
stats "<awk -F, '{if (NR>1) {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_cfr_by_age.csv | sort -k 1" using 2 name "M" nooutput
stats "<awk -F, '{if (NR>1) {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_cfr_by_age.csv | sort -k 1" using 3 name "W" nooutput

# x-axis setup
set xrange [-0.5:5.5]
set xtics rotate by 0 offset 0, 0
set xtics ("0-4\nJahre" 0, "5-14\nJahre" 1, "15-34\nJahre" 2, "35-59\nJahre" 3, "60-79\nJahre" 4, "80+\nJahre" 5)

# y-axis setup
set ylabel "Fallsterblichkeit in Thüringen"
set yrange [0:100]
set format y '%5.0f%%'
set ytics 0, 25, 100
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


set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallsterblichkeit nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, '{if (NR>1) {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_cfr_by_age.csv | sort -k 1" using 2 with histograms lt rgb "#72777e" title "Männlich", \
  "" using 3 with histograms lt rgb "#32373e" title "Weiblich", \
  "<awk -F, '{if (NR>1) {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_cfr_by_age.csv | sort -k 1" using (column(0) - 0.17):($2):($2>0?(sprintf("{/*0.85 %.1f%%}", $2)):"") with labels center offset 0.2, 0.7 notitle, \
  "" using (column(0) + 0.17):($3):($3>0?(sprintf("{/*0.85 %.1f%%}", $3)):"") with labels center offset 0.2, 0.7 notitle, \
  \
  1/0 lc rgb '#f2f2f2' title "{/*0.65 Quelle: Robert Koch-Institut}"
  
