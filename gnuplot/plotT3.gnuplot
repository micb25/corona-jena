load "template.gnuplot"

set output '../plotT3.png'

# stats for x
stats "<awk -F, '{if (NR > 1) print int($1/86400)*86400,$2}' ../data/cases_th_sums.csv" using 1 nooutput
xmin = 1583884800 + 8 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 2 * 86400
# xmax = xmin + (50 + 18) * 86400

fitmin = int(STATS_max) - 7 * 86400
fitmax = int(STATS_max)

fitmino = (fitmin - xmin_o) / 86400
fitmaxo = (fitmax - xmin_o) / 86400

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit [fitmino:fitmaxo] f(x) "<awk -F, '{if (NR > 1) print int($1/86400)*86400,$2}' ../data/cases_th_sums.csv" using (($1 - xmin_o) / 86400):2 via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

gA(x) = 100 * exp( log(2) / 1 * x)
gC(x) = 100 * exp( log(2) / 3 * x)
gE(x) = 100 * exp( log(2) / 5 * x)
gF(x) = 100 * exp( log(2) / 6 * x)
gG(x) = 100 * exp( log(2) / 7 * x)
gH(x) = 100 * exp( log(2) / 14 * x)
gD(x) = 100 * exp( log(2) / 21 * x)
gB(x) = 100 * exp( log(2) / 28 * x)

ymin = 100
ymax = 100000

# x-axis setup

unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Thüringen'
set yrange [ymin:ymax]
set logscale y
set mytics 10

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 2 at graph 0.99, 0.04 right "Hilfslinien entsprechen Fallzahl-Verdopplung alle {/Linux-Libertine-O-Italic N} Tage" textcolor ls 0

set label 3 at graph 0.13, first 10000 right "täglich" offset 2.0, 0.0 textcolor ls 0
set label 5 at graph 0.18, first 10000 left  "3 Tage" offset 2.0, 0.0 textcolor ls 0
set label 6 at graph 0.56, first 10000 right "7 Tage" offset 2.0, 0.0 textcolor ls 0
set label 7 at first xmax - 0.5 * 86400, first gH( ((xmax-xmin)/86400) ) right "14 Tage" offset 0, +1.0 textcolor ls 0
set label 8 at first xmax - 0.5 * 86400, first gD( ((xmax-xmin)/86400) ) right "21 Tage" offset 0, -1.5 textcolor ls 0
set label 4 at first xmax - 0.5 * 86400, first gB( ((xmax-xmin)/86400) ) right "28 Tage" offset 0, -1.5 textcolor ls 0

label_double = log(2) / b > 21 ? sprintf(" Verdopplungszeit\n >21 Tage") : sprintf(" Verdopplungszeit\n ≈%.f Tage", log(2) / b )
set label 9 at first fitmax, first f((fitmin - xmin_o) / 86400) label_double right offset 0.0, 2.0 textcolor ls 0

# date
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "letztes Update: " . date_cmd . " Uhr"

# data
plot  \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Thüringer Landesregierung}", \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 " . update_str . "}", \
  gA((x - xmin)/86400) w l ls 2 notitle, \
  gC((x - xmin)/86400) w l ls 2 notitle, \
  gD((x - xmin)/86400) w l ls 2 notitle, \
  gG((x - xmin)/86400) w l ls 2 notitle, \
  gH((x - xmin)/86400) w l ls 2 notitle, \
  gB((x - xmin)/86400) w l ls 2 notitle, \
  1/0 w l ls 12 title  "exponentieller Fit (letzte 7 Tage)", \
  "<awk -F, '{if (NR > 1) print int($1/86400)*86400,$2}' ../data/cases_th_sums.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle", \
  [fitmin:fitmax] f((x - xmin_o)/86400) w l ls 12 notitle
  
