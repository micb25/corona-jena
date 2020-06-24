load "template.gnuplot"

set output '../plotT2_RKI_Trend2603.png'

# stats for x
stats "<awk -F, '{ print $1 }' ../data/cases_thuringia_rki.csv" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 1 * 86400
xmax_o = int(STATS_max)
xmax_a = xmin_o + 42 * 86400

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit f(x) "<awk -F, '{ print $1,$2,$3 }' ../data/cases_thuringia_rki.csv | awk '{if ($1 <= 1585094400) print $0 }'" using (($1 - xmin_o) / 86400):(filter_neg($2)) via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

ymin = 0
ymax = 5000

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
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

label_trend = sprintf("f({/Linux-Libertine-O-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f){/Linux-Libertine-O-Italic x}}", a, a_err, b, b_err)
set label 2 at graph 0.98, 0.12 label_trend right textcolor ls 0

label_double = sprintf("Verdopplungszeit bis zum 26.03.: ≈%.0f Tage",log(2) / b )
set label 3  at graph 0.98, 0.05 label_double right textcolor ls 0

set label 4 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 5 at graph 0.98, 0.90 "{/*0.75 Quelle: Robert Koch-Institut}" right textcolor ls 0

# data
plot  \
  1/0 notitle, \
  1/0 w l ls 12 lw 3 title "exponentieller Trend (bis 26.03.)", \
  1/0 with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (bis 26.03.)}", \
  "<awk -F, '{ print $1,$2,$3 }' ../data/cases_thuringia_rki.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle", \
  [xmin_o:xmax_a]'+' using 1:(fmin(($1 - xmin_o)/86400)):(fmax((x - xmin_o)/86400)) with filledcurves closed ls 2 notitle, \
  [xmin_o:xmax_a] f((x - xmin_o)/86400) w l ls 12 lw 3 notitle
  
