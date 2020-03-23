load "template.gnuplot"

set output 'plot1_Weimar.png'

# stats for x
stats "<awk -F, '{a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' cases_thuringia.dat" using 1 nooutput
xmin_th = STATS_min - 1.5 * 86400
xmax_th = STATS_max + 1.5 * 86400

stats "<awk '{ print $1 }' ./cases_weimar.dat" using 1 nooutput
xmin_we = STATS_min - 1.5 * 86400
xmax_we = STATS_max + 1.5 * 86400

set xrange [ xmin_th < xmin_we ? xmin_th : xmin_we : xmax_th > xmax_we ? xmax_th : xmax_we ]

# stats for y
stats "<awk -F, '{if ($2==\"Weimar\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' cases_thuringia.dat" using 2 nooutput
ymax_th = int(5.0/3.0*STATS_max)

stats "<awk '{ print $2 }' ./cases_weimar.dat" using 1 nooutput
ymax_we = int(5.0/3.0*STATS_max)

set yrange [ 0 : ymax_th > ymax_we ? ymax_th : ymax_we ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Weimar'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

# latest update
update_str = "letztes Update: " . system("date +%d.%m.\\ %H\\:%M")

# data
plot  \
  1/0 notitle, \
  "<awk -F, '{if ($2==\"Weimar\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' cases_thuringia.dat" using 1:2 with linespoints ls 6 title "bestätigte Fälle (Land)", \
  "<awk '!_[$2]++' ./cases_weimar.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle (Stadt Weimar)", \
  1/0 lc rgb '#f2f2f2' title update_str
