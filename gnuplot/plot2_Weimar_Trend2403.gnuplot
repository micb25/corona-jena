load "template.gnuplot"

set output '../plot2_Weimar_Trend2403.png'

# stats for x
stats "<awk -F, '{print $1}' ../data/cases_weimar.csv" using 1 nooutput
xmin = int(STATS_min) 
xmin_o = int(STATS_min)
xmin_f = int(STATS_max) - 7 * 86400
xmax = int(STATS_max) + 1 * 86400
xmax_f = int(STATS_max)

stats "<awk -F, '{print $2}' ../data/cases_weimar.csv | tail -n 7" using 1 prefix "A" nooutput

# fit
filterx(x)=(x>=xmin_f)?(x):(1/0)
ao = 110.0
bo = 0.15

ymin = 0
if ( A_max - A_min < 2.0 ) {
	fit_performed = 0;
	ymax = 1.35 * A_max
} else {
	fit_performed = 1;
	
	fo(x) = ao * exp( bo * x )
	fit fo(x) "<awk -F, '{print $1, $2}' ../data/cases_weimar.csv" using ((filterx($1) - xmin_f)/86400):(filter_neg($2)) via ao, bo

	foerr(x) = sqrt( (ao_err*exp(bo*x))*(ao_err*exp(bo*x)) + (bo_err*ao*bo*exp(bo*x))*(bo_err*ao*bo*exp(bo*x)) )
	fomin(x) = fo(x) - foerr(x)
	fomax(x) = fo(x) + foerr(x)
	
	ymax = 1.75 * fo( (xmax - xmin_f) / 86400 )
}

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set xrange [xmin:xmax]

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Weimar'
set yrange [ymin:ymax]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_weimar.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3 opaque
set border back

if ( fit_performed == 1 ) {
	label_trend = sprintf("f({/Linux-Libertine-O-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f){/Linux-Libertine-O-Italic x}}", ao, ao_err, bo, bo_err)
	set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0
}

if ( fit_performed == 1 ) {
	label_double = log(2) / bo > 21 ? sprintf("aktuelle Verdopplungszeit: >21 Tage") : sprintf("aktuelle Verdopplungszeit: ≈%.0f Tage",log(2) / bo )
} else {
	label_double = sprintf("aktuelle Verdopplungszeit: nicht bestimmbar");
}
set label 3  at graph 0.99, 0.04 label_double right textcolor ls 0

# data
if ( fit_performed == 1 ) {
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Stadt Weimar}", \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title update_str, \
  [xmin_f:xmax_f] '+' using 1:(fomin(($1 - xmin_f)/86400)):(fomax((x - xmin_f)/86400)) with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (letzte 7 Tage)}", \
  [xmin_f:xmax_f] fo((x - xmin_f)/86400) w l ls 12 title "exponentieller Trend (letzte 7 Tage)", \
  "<awk -F, '{print $1, $2}' ../data/cases_weimar.csv" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  [xmin_f:xmax_f] fo((x - xmin_f)/86400) w l ls 12 notitle
} else {
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Stadt Weimar}", \
  [xmin:xmax] 1/0 lc rgb '#f2f2f2' title update_str, \
  "<awk -F, '{print $1, $2}' ../data/cases_weimar.csv" using 1:2 with linespoints ls 1 title "bestätigte Fälle"
}
