load "template.gnuplot"

set output '../plot1_Weimar.png'

# stats for x
stats "<awk '{ print $1 }' ../data/cases_weimar.dat" using 1 nooutput
xmin_we = STATS_min - 1.5 * 86400
xmax_we = STATS_max + 1.5 * 86400

set xrange [ xmin_we : xmax_we ]

# stats for y
stats "<awk -F, '{if ($2==\"Weimar\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 2 nooutput
ymax_th = int(5.0/3.0*STATS_max)

stats "<awk '{ print $2 }' ../data/cases_weimar.dat" using 1 nooutput
ymax_we = int(5.0/3.0*STATS_max)

set yrange [ 0 : ymax_we ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Weimar'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

# data
plot  \
  1/0 notitle, \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Stadt Weimar}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  "<awk '!_[$3]++' ../data/cases_weimar.dat | tail -n 1" using 1:3:($3) with labels point pt 7 center offset char -0.3, 0.8 tc ls 4 notitle, \
  "<awk '!_[$2]++' ../data/cases_weimar.dat | tail -n 1" using 1:2:($2) with labels point pt 7 center offset char -0.3, 0.8 tc ls 1 notitle, \
  "<awk '!_[$3]++' ../data/cases_weimar.dat" using 1:3 with linespoints ls 4 title "Genesene", \
  "<awk '!_[$2]++' ../data/cases_weimar.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle"
