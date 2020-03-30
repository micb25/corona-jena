load "template.gnuplot"

set output '../plot2_Trend2103.png'

# stats for x
stats "<awk '!_[$2]++' ../data/cases_jena.dat" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmax = int(STATS_max) + 1 * 86400
xmax_o = int(STATS_max)
xmax_t = int(STATS_max) - 3 * 86400

# fit 
a = 1.0
b = 0.30
f(x) = a * exp( b * x )
fit f(x) "<awk '!_[$2]++' ../data/cases_jena.dat" using (($1 - xmin_o) / 86400):2 via a, b

ferr(x) = sqrt( (a_err*exp(b*x))*(a_err*exp(b*x)) + (b_err*a*b*exp(b*x))*(b_err*a*b*exp(b*x)) )
fmin(x) = f(x) - ferr(x)
fmax(x) = f(x) + ferr(x)

ao = 1.0
bo = 0.30
fo(x) = ao * exp( bo * x )
fit fo(x) "<awk '!_[$2]++' ../data/cases_jena.dat | awk '{if ($1 <= 1584900002) print $0 }'" using (($1 - xmin_o) / 86400):2 via ao, bo

foerr(x) = sqrt( (ao_err*exp(bo*x))*(ao_err*exp(bo*x)) + (bo_err*ao*bo*exp(bo*x))*(bo_err*ao*bo*exp(bo*x)) )
fomin(x) = fo(x) - foerr(x)
fomax(x) = fo(x) + foerr(x)

# R2
stats "<awk '!_[$2]++' ../data/cases_jena.dat" using (f(($1 - xmin_o) / 86400)):2 name "A" nooutput

ymin = 0
ymax = 0.75 * f( (xmax - xmin_o) / 86400 )
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
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3

label_trend = sprintf("f({/Arial-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f) {/Arial-Italic x}}", ao, ao_err, bo, bo_err)
set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0

# data
plot  \
  [xmin:xmax] 1/0 notitle, \
  1/0 lc rgb '#f2f2f2' title update_str, \
  '+' using 1:(fomin(($1 - xmin_o)/86400)):(fomax((x - xmin_o)/86400)) with filledcurves closed ls 2 title "Fehlerbereich Trend (21.03.)", \
  fo((x - xmin_o)/86400) w l ls 2 title "exponentieller Trend (21.03.)", \
  "<awk '!_[$2]++' ../data/cases_jena.dat" using 1:2 with linespoints ls 1 title "bestätigte Fälle"
  
