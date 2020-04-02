load "template.gnuplot"

set output '../plotT2_RKI_Trend2603.png'

# stats for x
stats "<awk '!_[$2]++' ../data/cases_thuringia_rki.dat" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 1 * 86400
xmax_o = int(STATS_max)

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit f(x) "<awk '!_[$2]++' ../data/cases_thuringia_rki.dat | awk '{if ($1 <= 1585094400) print $0 }'" using (($1 - xmin_o) / 86400):(filter_neg($2)) via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

# R2
stats "<awk '!_[$2]++' ../data/cases_thuringia_rki.dat" using (f(($1 - xmin_o) / 86400)):(filter_neg($2)) name "A" nooutput

ymin = 0
ymax = f( (xmax - xmin_o) / 86400 )

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Thüringen'
set yrange [ymin:ymax]

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

label_trend = sprintf("f({/Arial-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f) {/Arial-Italic x}}", a, a_err, b, b_err)
set label 2 at graph 0.02, 0.40 label_trend left textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Robert Koch-Institut}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  [xmin_o:xmax_o]'+' using 1:(fmin(($1 - xmin_o)/86400)):(fmax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (bis 26.03.)}", \
  [xmin_o:xmax_o] f((x - xmin_o)/86400) w l ls 2 title "exponentieller Trend (bis 26.03.)", \
  "<awk '!_[$2]++' ../data/cases_thuringia_rki.dat" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
  
