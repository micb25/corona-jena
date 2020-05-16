load "template.gnuplot"

set output '../plotD1.png'

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print $1}' ../data/divi_db_th/divi_data_th.csv" using 1 nooutput
set xrange [ STATS_min - 0.5 * 86400 : STATS_max + 3.0 * 86400 ]

# stats for y
stats "<awk -F, '{if ( NR > 1 ) print $5}' ../data/divi_db_th/divi_data_th.csv" using 1 nooutput
set yrange [ 0 : 10*(1+int(int(1.25*STATS_max)/10.0)) ]

set xtics 4*86400
set mxtics 4

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'belegte Intensivbetten mit COVID19 in Thüringen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# date
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/divi_db_th/divi_data_th.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: DIVI Intensivregister}" right textcolor ls 0

# data
plot  \
  "<awk -F, '{if ( NR > 1 ) print $1,$6}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines ls 17 title "davon beatmet ", \
  "<awk -F, '{if ( NR > 1 ) print $1,$5}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines ls 18 title "COVID19-Fälle auf Intensivstation", \
  \
  "<awk -F, '{if ( NR>1) {a=$1;c=b;b=$6}}END{print a, b, b-c}' ../data/divi_db_th/divi_data_th.csv | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point ls 17 left offset char  0.3, -0.1 tc ls 17 notitle, \
  "<awk -F, '{if ( NR>1) {a=$1;c=b;b=$5}}END{print a, b, b-c}' ../data/divi_db_th/divi_data_th.csv | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point ls 18 left offset char  0.3, -0.1 tc ls 18 notitle
