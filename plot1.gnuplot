load "template.gnuplot"

set output 'plot1.png'

# stats for y
stats "<awk '{ print $1 }' ./cases_jena.dat" using 1 nooutput
set xrange [ STATS_min - 86400 : STATS_max + 86400 ]

# stats for y
stats "<awk '{ print $2 }' ./cases_jena.dat" using 1 nooutput
set yrange [ 0 : int(4.0/3.0*STATS_max) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'kumulierte Fälle in Jena'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

# latest update
update_str = "letztes Update: " . system("date +%d.%m.\\ %H\\:%M")

# data
plot  \
  1/0 notitle, \
  "<awk '!_[$2]++' ./cases_jena.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  1/0 lc rgb '#f2f2f2' title update_str
