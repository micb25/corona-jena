load "template.gnuplot"

set output '../plotT1.png'

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max + 24.0 * 86400 ]

# stats for y
stats "<awk -F, '{if ( NR > 1 ) print $2}' ../data/cases_th_sums.csv" using 1 nooutput
set yrange [ 0 : int(1.5*STATS_max) ]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Thüringen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: TMASGFF}" right textcolor ls 0

# data
plot  \
  \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$4}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 left offset char  0.3, -0.1 tc ls 5 notitle, \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$3}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 left offset char  0.3, -0.1 tc ls 4 notitle, \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$2}' ../data/cases_th_sums.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 left offset char  0.3, -0.1 tc ls 1 notitle, \
  \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$4}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$3}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene", \
  "<echo 0" using 1:(filter_neg($2)) with lines lt 1 lw 1.5 lc '#007af2' title "aktive Fälle", \
  "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400,$2}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle", \
  "<awk -F, '{if ( NR > 1 ) print $1,$2-$3-$4}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with lines lt 1 lw 3.0 lc '#007af2' notitle
