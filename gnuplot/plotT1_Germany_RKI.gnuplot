load "template.gnuplot"

set output '../plotT1_Germany_RKI.png'

# stats for y
stats "<awk -F, '{ print $1 }' ../data/cases_germany_total_rki.csv" using 1 nooutput
set xrange [ STATS_min - 86400 : STATS_max + 3.0 * 86400 ]

# stats for y
stats "<awk -F, '{ print $2 }' ../data/cases_germany_total_rki.csv" using 1 nooutput
set yrange [ 0 : int(4.5/3.0*STATS_max) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Deutschland'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# data
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Robert Koch-Institut}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  "<awk -F, '!_[$4]++' ../data/cases_germany_total_rki.csv | awk -F, '{if ($4 >= 0) print $1, $4}' | tail -n 1" using 1:2:($2) with labels point pt 7 center offset char -0.3, 0.8 tc ls 5 notitle, \
  "<awk -F, '!_[$2]++' ../data/cases_germany_total_rki.csv | awk -F, '{if ($2 >= 0) print $1, $2}' | tail -n 1" using 1:2:($2) with labels point pt 7 center offset char -0.3, 0.8 tc ls 1 notitle, \
  "<awk -F, '!_[$4]++' ../data/cases_germany_total_rki.csv | awk -F, '{if ($4 >= 0) print $1, $4}'" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '!_[$2]++' ../data/cases_germany_total_rki.csv | awk -F, '{if ($2 >= 0) print $1, $2}'" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
