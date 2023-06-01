load "template.gnuplot"

set output '../plotT3B_Germany_RKI.png'

# stats for x
stats "<awk -F, '!_[$4]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1}'" using 1 nooutput
xmin = 1583884800 + 5.9 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 10 * 86400

fitmin = int(STATS_max) - 7 * 86400
fitmax = int(STATS_max)

fitmino = (fitmin - xmin_o) / 86400
fitmaxo = (fitmax - xmin_o) / 86400

# fit 
a = 2000000.0
b = 0.050
f(x) = a * exp( b * x )
fit [fitmino:fitmaxo] f(x) "<awk -F, '!_[$4]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1, $4}'" using (($1 - xmin_o) / 86400):2 via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

ymin = 100
ymax = 1000000

gB(x) = ymin * exp( log(2) / 2 * x)
gD(x) = ymin * exp( log(2) / 4 * x)
gE(x) = ymin * exp( log(2) / 5 * x)
gF(x) = ymin * exp( log(2) / 6 * x)
gG(x) = ymin * exp( log(2) / 7 * x)
gH(x) = ymin * exp( log(2) / 14 * x)
gA(x) = ymin * exp( log(2) / 21 * x)
gC(x) = ymin * exp( log(2) / 28 * x)

# x-axis setup
unset xlabel
set xtics 14*86400
set mxtics 2
set xdata time
set timefmt "%s"
set format x "%m.%Y"
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Summe der Todesfälle mit/wegen COVID-19 in Deutschland' offset 0, -0.3
set yrange [ymin:ymax]
set logscale y
set mytics 10

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# label_trend = sprintf("f({/Arial-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f) {/Arial-Italic x}}", a, a_err, b, b_err)
set label 2 at graph 0.99, 0.04 right "Hilfslinien entsprechen Verdopplung alle {/Linux-Libertine-O-Italic N} Tage." textcolor ls 0

# set label 4 at first (xmin+86400*10), first gB( 12 - 0 ) right "2 Tage" textcolor ls 0
# set label 6 at first (xmin+86400*24), first gD( 24 - 2 ) left "4 Tage" textcolor ls 0
# set label 7 at first xmax - 0.5 * 86400, first gG( ((xmax-xmin)/86400) -  8) right "7 Tage" textcolor ls 0
# set label 8 at first xmax - 0.5 * 86400, first gH( ((xmax-xmin)/86400) - 11) right "14 Tage" textcolor ls 0
set label 3 at first xmax - 0.5 * 86400, first gA( ((xmax-xmin)/86400) - 11) right "21 Tage" textcolor ls 0
set label 5 at first xmax - 0.5 * 86400, first gC( ((xmax-xmin)/86400) - 13) right "28 Tage" textcolor ls 0

label_double = log(2) / b > 28 ? sprintf(" aktuelle Verdopplungszeit:\n >28 Tage") : sprintf(" aktuelle Verdopplungszeit:\n ≈%.f Tage", log(2) / b )

set label 6 at graph 0.99, 0.08 update_str . "{/*0.75 ; Quelle: Robert Koch-Institut}" font ",12" right textcolor ls 0
set label 9 at graph 0.99, 0.15 label_double right offset 0, 2.0 textcolor ls 0

set offsets graph 0.02, graph 0.02, graph 0.00, 0.00

# gB((x - xmin)/86400) w l ls 2 notitle, \
# gD((x - xmin)/86400) w l ls 2 notitle, \
# gG((x - xmin)/86400) w l ls 2 notitle, \
# gH((x - xmin)/86400) w l ls 2 notitle, \

plot  \
  gA((x - xmin)/86400) w l ls 2 notitle, \
  gC((x - xmin)/86400) w l ls 2 notitle, \
  1/0 w l ls 12 title  "exponentieller Fit (letzte 7 Tage)", \
  "<awk -F, '!_[$4]++' ../data/cases_germany_total_rki.csv | awk -F, '{if (NR > 1) print $1, $4}'" using 1:2 with linespoints ls 5 title "Todesfälle mit/wegen COVID-19", \
  [fitmin:fitmax] f((x - xmin_o)/86400) w l ls 12 lw 3 notitle
  
  # [xmin:] '+' using 1:(fmin(($1 - xmin_o)/86400)):(fmax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "Fehlerbereich Trend", \
  # f((x - xmin_o)/86400) w l ls 2 title "exponentieller Trend", \
