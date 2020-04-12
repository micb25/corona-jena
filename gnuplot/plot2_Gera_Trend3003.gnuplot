load "template.gnuplot"

set output '../plot2_Gera_Trend3003.png'

# stats for x
stats "<awk -F, '!_[$2]++' ../data/cases_gera.csv | awk -F, '{print $1, $2}'" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmin_f = int(STATS_max) - 7 * 86400
xmax = int(STATS_max) + 1 * 86400
xmax_f = int(STATS_max)

# fit
filterx(x)=(x>=xmin_f)?(x):(1/0)
ao = 20.0
bo = 0.15
fo(x) = ao * exp( bo * x )
fit fo(x) "<awk -F, '!_[$2]++' ../data/cases_gera.csv | awk -F, '{print $1, $2}'" using ((filterx($1) - xmin_f)/86400):(filter_neg($2)) via ao, bo

foerr(x) = sqrt( (ao_err*exp(bo*x))*(ao_err*exp(bo*x)) + (bo_err*ao*bo*exp(bo*x))*(bo_err*ao*bo*exp(bo*x)) )
fomin(x) = fo(x) - foerr(x)
fomax(x) = fo(x) + foerr(x)

ymin = 0
ymax = 1.75 * fo( (xmax - xmin_f) / 86400 )

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Gera'
set yrange [ymin:ymax]

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3 opaque
set border back

label_trend = sprintf("f({/Linux-Libertine-O-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f){/Linux-Libertine-O-Italic x}}", ao, ao_err, bo, bo_err)
set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0

label_double = log(2) / bo > 14 ? sprintf("aktuelle Verdopplungsrate: >14 Tage") : sprintf("aktuelle Verdopplungsrate: ≈%.0f Tage",log(2) / bo )
set label 3  at graph 0.99, 0.04 label_double right textcolor ls 0

# data
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Stadt Gera}", \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title update_str, \
  [ xmin_f < xmin_o ? xmin_o : xmin_f :xmax_f] '+' using 1:(fomin(($1 - xmin_f)/86400)):(fomax((x - xmin_f)/86400)) with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (letzte 7 Tage)}", \
  [ xmin_f < xmin_o ? xmin_o : xmin_f :xmax_f] fo((x - xmin_f)/86400) w l ls 12 title "exponentieller Trend (letzte 7 Tage)", \
  "<awk -F, '!_[$2]++' ../data/cases_gera.csv | awk -F, '{print $1, $2}'" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
  
