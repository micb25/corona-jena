load "template.gnuplot"

set output '../plotD2.png'

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print $1}' ../data/divi_db_th/divi_data_th.csv" using 1 nooutput
set xrange [ STATS_min - 0.5 * 86400 : STATS_max + 16.0 * 86400 ]

# stats for y
stats "<awk -F, '{if ( NR > 1 ) print $2}' ../data/divi_db_th/divi_data_th.csv" using 1 nooutput
set yrange [ 0 : 100*(1+int(int(1.40*STATS_max)/100.0)) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Intensivbetten in Thüringen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# date
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/divi_db_th/divi_data_th.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: DIVI-Intensivregister}" right textcolor ls 0

# data
plot  \
  "<awk -F, '{if ( NR > 1 ) print $1,$5}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines ls 18 title "belegt mit COVID19", \
  "<awk -F, '{if ( NR > 1 ) print $1,$3}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines ls 19 title "belegte Intensivbetten", \
  "<awk -F, '{if ( NR > 1 ) print $1,$2}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines ls 16 title "Intensivbetten in Thüringen", \
  \
  "<awk -F, '{if ( NR>1) {a=$1;c=b;b=$5}}END{print a, b, b-c}' ../data/divi_db_th/divi_data_th.csv | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point ls 18 ps 0.0 left offset char  0.3, +0.3 tc ls 18 notitle, \
  "<awk -F, '{if ( NR>1) {a=$1;c=b;b=$3}}END{print a, b, b-c}' ../data/divi_db_th/divi_data_th.csv | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point ls 18 ps 0.0 left offset char  0.3, +0.0 tc ls 19 notitle, \
  "<awk -F, '{if ( NR>1) {a=$1;c=b;b=$2}}END{print a, b, b-c}' ../data/divi_db_th/divi_data_th.csv | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point ls 18 ps 0.0 left offset char  0.3, +0.0 tc ls 16 notitle
