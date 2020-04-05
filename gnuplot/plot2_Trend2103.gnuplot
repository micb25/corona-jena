load "template.gnuplot"

set output '../plot2_Trend2103.png'

# stats for x
stats "<awk '!_[$2]++' ../data/cases_jena.dat" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 1 * 86400
xmax_o = int(STATS_max)

# fit
ao = 1.0
bo = 0.30
fo(x) = ao * exp( bo * x )
fit fo(x) "<awk '!_[$2]++' ../data/cases_jena.dat | awk '{if ($1 <= 1584900002) print $0 }'" using (($1 - xmin_o) / 86400):(filter_neg($2)) via ao, bo

foerr(x) = sqrt( (ao_err*exp(bo*x))*(ao_err*exp(bo*x)) + (bo_err*ao*bo*exp(bo*x))*(bo_err*ao*bo*exp(bo*x)) )
fomin(x) = fo(x) - foerr(x)
fomax(x) = fo(x) + foerr(x)

ymin = 0
ymax = 0.75 * fo( (xmax - xmin_o) / 86400 )
ymax = 500

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
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3 opaque
set border back

label_trend = sprintf("f({/Linux-Libertine-O-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f){/Linux-Libertine-O-Italic x}}", ao, ao_err, bo, bo_err)
set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0

label_double = sprintf("Verdopplungsrate vor dem 21.03.: ≈%.0f Tage",log(2) / bo )
set label 3  at graph 0.99, 0.04 label_double right textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title update_str, \
  [xmin_o:xmax_o] '+' using 1:(fomin(($1 - xmin_o)/86400)):(fomax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (bis 21.03.)}", \
  [xmin_o:xmax_o] fo((x - xmin_o)/86400) w l ls 12 title "exponentieller Trend (bis 21.03.)", \
  "<awk '!_[$2]++' ../data/cases_jena.dat" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
  
