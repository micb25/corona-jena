load "template.gnuplot"

set output '../plotT3_Germany_RKI.png'

# stats for x
stats "<awk -F, '!_[$2]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1}'" using 1 nooutput
xmin = 1583884800 + 5.9 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 18 * 86400
xmax = xmin + (22 + 18) * 86400

fitmin = int(STATS_max) - 7 * 86400
fitmax = int(STATS_max)

fitmino = (fitmin - xmin_o) / 86400
fitmaxo = (fitmax - xmin_o) / 86400

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit [fitmino:fitmaxo] f(x) "<awk -F, '!_[$2]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1, $2}'" using (($1 - xmin_o) / 86400):2 via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

ymin = 9000
ymax = 10000000

gA(x) = ymin * exp( log(2) / 1 * x)
gB(x) = ymin * exp( log(2) / 2 * x)
gC(x) = ymin * exp( log(2) / 3 * x)
gD(x) = ymin * exp( log(2) / 4 * x)
gE(x) = ymin * exp( log(2) / 5 * x)
gF(x) = ymin * exp( log(2) / 6 * x)
gG(x) = ymin * exp( log(2) / 7 * x)
gH(x) = ymin * exp( log(2) / 14 * x)

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Deutschland'
set yrange [ymin:ymax]
set logscale y
set mytics 10

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# label_trend = sprintf("f({/Arial-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f) {/Arial-Italic x}}", a, a_err, b, b_err)
set label 2 at graph 0.99, 0.04 right "Hilfslinien entsprechen Fallzahl-Verdopplung alle {/Linux-Libertine-O-Italic N} Tage" textcolor ls 0

set label 3 at first 7.2*86400 + xmin, first gA(8.2) right "täglich" textcolor ls 0
set label 4 at first 20*86400 + xmin, first gB(16) right "2 Tage" textcolor ls 0
set label 5 at first xmax - 0.5 * 86400, first gC( ((xmax-xmin)/86400) - 5.0) right "3 Tage" textcolor ls 0
set label 6 at first xmax - 0.5 * 86400, first gD( ((xmax-xmin)/86400) - 5.5) right "4 Tage" textcolor ls 0
set label 7 at first xmax - 0.5 * 86400, first gG( ((xmax-xmin)/86400) - 6.5) right "7 Tage" textcolor ls 0
set label 8 at first xmax - 0.5 * 86400, first gH( ((xmax-xmin)/86400) - 8.5) right "14 Tage" textcolor ls 0

label_double = log(2) / b > 21 ? sprintf(" Verdopplungszeit\n >21 Tage") : sprintf(" Verdopplungszeit\n ≈%.f Tage", log(2) / b )
set label 9 at first fitmin, first f((fitmin - xmin_o - 4 * 86400) / 86400) label_double left textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Robert Koch-Institut}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  gA((x - xmin)/86400) w l ls 2 notitle, \
  gB((x - xmin)/86400) w l ls 2 notitle, \
  gC((x - xmin)/86400) w l ls 2 notitle, \
  gD((x - xmin)/86400) w l ls 2 notitle, \
  gG((x - xmin)/86400) w l ls 2 notitle, \
  gH((x - xmin)/86400) w l ls 2 notitle, \
  1/0 w l ls 12 title  "exponentieller Fit (letzte 7 Tage)", \
  "<awk -F, '!_[$2]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1, $2}'" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  [fitmin:fitmax] f((x - xmin_o)/86400) w l ls 12 notitle
  
  # [xmin:] '+' using 1:(fmin(($1 - xmin_o)/86400)):(fmax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "Fehlerbereich Trend", \
  # f((x - xmin_o)/86400) w l ls 2 title "exponentieller Trend", \
