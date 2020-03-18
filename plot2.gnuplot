load "template.gnuplot"

set output 'plot2.png'

# stats for y
stats "<awk '!_[$2]++' ./cases_jena.dat" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 8 * 86400
xmax_o = int(STATS_max)

# stats for y
stats "<awk '!_[$2]++' ./cases_jena.dat" using 1 nooutput
ymin = 0
ymax = int(4.0/3.0*STATS_max)

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit f(x) "<awk '!_[$2]++' ./cases_jena.dat" using (($1 - xmin_o) / 86400):2 via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

# R2
stats "<awk '!_[$2]++' ./cases_jena.dat" using (f(($1 - xmin_o) / 86400)):2 name "A" nooutput

ymax = f( (xmax - xmin_o) / 86400 )

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]
set xtics out nomirror
set mxtics 2

# y-axis setup
set ylabel 'kumulierte Fälle in Jena'
set format y '%6.0f'
set yrange [ymin:ymax]
set ytics out nomirror
set mytics 2

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

# latest update
update_str = "letztes Update: " . system("date +%d.%m.\\ %H\\:%M")
# label_trend = sprintf("\\~&{/*0.5 .}e^{%.3f{/Arial-Italic x}} mit {/Arial-Italic R}^2 = %.3f", b, A_correlation)
label_trend = sprintf("\\~&{/*0.5 .}%.3f e^{%.3f{/Arial-Italic x}}", a, b)
set label 2 at graph 0.50, 0.50 label_trend center textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 notitle, \
  [xmax_o:] '+' using 1:(fmin(($1 - xmin_o)/86400)):(fmax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "Fehlerbereich Trend", \
  [xmax_o:] f((x - xmin_o)/86400) w l ls 2 title "exponentieller Trend", \
  "<awk '!_[$2]++' ./cases_jena.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  1/0 lc rgb '#f2f2f2' title update_str
  
