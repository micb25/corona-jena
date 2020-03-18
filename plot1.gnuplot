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
set xtics out nomirror
set mxtics 1

# y-axis setup
set ylabel 'bestätigte Fälle in Jena'
set format y '%6.0f'
set ytics out nomirror
set mytics 2

# key
unset key

# latest update
update_str = "letztes Update: " . system("date +%d.%m.%Y\\ %H\\:%M")
set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0 font ",12"

# data
plot  \
  './cases_jena.dat' using 1:2 with linespoints ls 1 title "Bestätigte Fälle"
