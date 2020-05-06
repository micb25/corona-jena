load "template.gnuplot"

set output '../plot1_Weimar.png'

# stats for x
stats "<awk -F, '{ print $1 }' ../data/cases_weimar.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max + 8.0 * 86400 ]

# stats for y
stats "<awk -F, '{ print $2 }' ../data/cases_weimar.csv" using 1 nooutput
ymax_we = int(1.45*STATS_max)
set yrange [ 0 : ymax_we ]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_weimar.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Weimar'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: Stadt Weimar}" right textcolor ls 0

# data
plot  \
  \
  "<awk -F, '{if ($2 >= 0) print $1,$2,$3,$4}' ../data/cases_weimar.csv | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 left offset char +0.3,  0.2 tc ls 1 notitle, \
  "<awk -F, '{if ($3 >= 0) print $1,$2,$3,$4}' ../data/cases_weimar.csv | awk 'BEGIN{ov=0}{dv=$3-ov;ov=$3;print $1,$3,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 left offset char +0.3, -0.2 tc ls 4 notitle, \
  \
  "<awk -F, '{if ($3 >= 0) print $1,$2,$3,$4}' ../data/cases_weimar.csv" using 1:(filter_neg($3)) with linespoints ls 4 title "Genesene", \
  "<awk -F, '{if (( $2 >= 0 ) && ( $3 >= 0 ) ) print $1,$2-$3-($4>=0?$4:0)}' ../data/cases_weimar.csv" using 1:(filter_neg($2)) with lines lt 1 lw 1.5 lc '#007af2' title "aktive Fälle", \
  "<awk -F, '{if ($2 >= 0) print $1,$2,$3,$4}' ../data/cases_weimar.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
