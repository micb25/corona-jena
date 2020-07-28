load "../gnuplot/template.gnuplot"

set output '../plot5B_RKI_%FILENAME%.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: Robert Koch-Institut)}"

# get maximum y value
stats "<awk -F, '{if ($1==\"%FILENAME%\") {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13+0;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_deceased_by_age.csv | sort -k 1" using 2 name "MM" 
stats "<awk -F, '{if ($1==\"%FILENAME%\") {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13+0;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_deceased_by_age.csv | sort -k 1" using 3 name "WW" nooutput

ymax = 1.3 * (WW_max > MM_max ? WW_max : MM_max)
ymax = ymax > 5 ? ymax : 5

# x-axis setup
set xrange [-0.5:5.5]
set xtics rotate by 0 offset 0, 0
set xtics ("0-4\nJahre" 0, "5-14\nJahre" 1, "15-34\nJahre" 2, "35-59\nJahre" 3, "60-79\nJahre" 4, "80+\nJahre" 5)

# y-axis setup
set ylabel "COVID19-Todesfälle %REGION%"
set yrange [0:ymax]

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

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Verstorbene nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

M_title = sprintf("Männlich {/*0.75 (insgesamt: %i)}", MM_sum)
W_title = sprintf("Weiblich {/*0.75 (insgesamt: %i)}", WW_sum)

# data
plot  \
  "<awk -F, '{if ($1==\"%FILENAME%\") {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13+0;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_deceased_by_age.csv | sort -k 1" using 2 with histograms lt rgb "#72777e" title M_title, \
  "" using 3 with histograms lt rgb "#32373e" title W_title, \
  \
  "<awk -F, '{if ($1==\"%FILENAME%\") {a[\"A00-A04\"]=$2;b[\"A00-A04\"]=$3;a[\"A05-A14\"]=$4;b[\"A05-A14\"]=$5;a[\"A15-A34\"]=$6;b[\"A15-A34\"]=$7;a[\"A35-A59\"]=$8;b[\"A35-A59\"]=$9;a[\"A60-A79\"]=$10;b[\"A60-A79\"]=$11;a[\"A80+\"]=$12;b[\"A80+\"]=$13+0;}}END{ for (i in a) { print i, b[i], a[i] }}' ../data/rki_th/total_deceased_by_age.csv | sort -k 1" using (column(0) - 0.17):($2):($2>0?sprintf("{/*0.85 %.0f}", $2):"") with labels center offset 0, 0.7 notitle, \
  "" using (column(0) + 0.17):($3):($3>0?sprintf("{/*0.85 %.0f}", $3):"") with labels center offset 0, 0.7 notitle  
