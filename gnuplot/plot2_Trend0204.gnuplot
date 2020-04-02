load "template.gnuplot"

set output '../plot2_Trend0204.png'

# stats for x
stats "<awk '!_[$2]++' ../data/cases_jena.dat" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmin_f = 1585332622 # 28.03.2020
xmax = int(STATS_max) + 1 * 86400
xmax_f = int(STATS_max)

# fit
ao = 1.0
bo = 0.30
co = 100
fo(x) = ao * exp( bo * x ) + co
fit fo(x) "<awk '!_[$2]++' ../data/cases_jena.dat | awk '{if ($1 >= 1585353600) print $0 }'" using (($1 - xmin_f)/86400):2 via ao, bo, co

foerr(x) = sqrt( (ao_err*exp(bo*x))*(ao_err*exp(bo*x)) + (bo_err*ao*bo*exp(bo*x))*(bo_err*ao*bo*exp(bo*x)) + (co_err*co_err) )
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
set ylabel 'Gesamtzahl der Fälle in Jena'
set yrange [ymin:ymax]

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

label_trend = sprintf("f({/Arial-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f) {/Arial-Italic x}} + (%.1f±%.1f)", ao, ao_err, bo, bo_err, co, co_err)
set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title update_str, \
  [xmin_f:xmax_f] '+' using 1:(fomin(($1 - xmin_f)/86400)):(fomax((x - xmin_f)/86400)) with filledcurves closed ls 2 title "Fehlerbereich Trend (seit 28.03.)", \
  [xmin_f:xmax_f] fo((x - xmin_f)/86400) w l ls 2 title "exponentieller Trend (seit 28.03.)", \
  "<awk '!_[$2]++' ../data/cases_jena.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle"
  
