load "template.gnuplot"

set output '../plotT4.png'

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max ]
set yrange [0:50 < * < 100000]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Zahl der Fälle in Thüringen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# date
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 letzte Aktualisierung: " . date_cmd . "}"

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: TMASGFF}" right textcolor ls 0

set offsets graph 0.01, graph 0.12, graph 0.20, 0.00

# data
plot  \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$4}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$7}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 7 title "schwere Verläufe", \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$5}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 8 title "stationäre Fälle", \
  \
  "<awk -F, '{print int($1/86400)*86400,$5}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.5, +0.3 tc ls 8 notitle, \
  "<awk -F, '{print int($1/86400)*86400,$7}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.5, +0.5 tc ls 7 notitle, \
  "<awk -F, '{print int($1/86400)*86400,$4}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.5, +0.5 tc ls 5 notitle
