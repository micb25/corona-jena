load "template.gnuplot"

set output '../plot2_Erfurt_Trend2703.png'

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$2}' ../data/cases_erfurt.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# stats for x
stats "<awk -F, '{print $2,$3}' ../data/cases_erfurt.csv" using 1 nooutput
xmin = int(STATS_min) - 1 * 86400
xmin_o = int(STATS_min)
xmin_f = int(STATS_max) - 7 * 86400
xmax = int(STATS_max) + 1 * 86400
xmax_f = int(STATS_max)

# fit
filterx(x)=(x>=xmin_f)?(x):(1/0)
ao = 110.0
bo = 0.15
fo(x) = ao * exp( bo * x )

# stats for y
stats "<awk -F, '{print $3}' ../data/cases_erfurt.csv | tail -n 7" using 1 prefix "A" nooutput

ymin = 0
if ( A_max - A_min < 2.0 ) {
	fit_performed = 0;
	ymax = 1.3 * A_max
} else {
	fit_performed = 1;
	fit fo(x) "<awk -F, '{print $2,$3}' ../data/cases_erfurt.csv" using ((filterx($1) - xmin_f)/86400):(filter_neg($2)) via ao, bo;
	
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
set ylabel 'Gesamtzahl der Fälle in Erfurt'
set yrange [ymin:ymax]

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3 opaque
set border back

if ( fit_performed == 1 ) {
label_trend = sprintf("f({/Linux-Libertine-O-Italic x}) = (%.3f±%.3f) e^{(%.3f±%.3f){/Linux-Libertine-O-Italic x}}", ao, ao_err, bo, bo_err)
set label 2 at graph 0.02, 0.60 label_trend left textcolor ls 0
}

if ( fit_performed == 1 ) {
	label_double = log(2) / bo > 21 ? sprintf("aktuelle Verdopplungszeit: >21 Tage") : sprintf("aktuelle Verdopplungszeit: ≈%.0f Tage",log(2) / bo );
} else {
	label_double = sprintf("aktuelle Verdopplungszeit: nicht bestimmbar");
}
set label 3  at graph 0.99, 0.04 label_double right textcolor ls 0

set label 4 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 5 at graph 0.98, 0.90 "{/*0.75 Quelle: Stadt Erfurt}" right textcolor ls 0

# data
if ( fit_performed == 1 ) {
plot  \
  [xmin:xmax] 1/0 notitle, \
  [xmin_f:xmax_f] '+' using 1:(fomin(($1 - xmin_f)/86400)):(fomax((x - xmin_f)/86400)) with filledcurves closed ls 2 title "{/*0.75 stat. Fehlerbereich Trend (letzte 7 Tage)}", \
  [xmin_f:xmax_f] fo((x - xmin_f)/86400) w l ls 12 title "exp. Trend (letzte 7 Tage)", \
  "<awk -F, '{print $2,$3}' ../data/cases_erfurt.csv" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  [xmin_f:xmax_f] fo((x - xmin_f)/86400) w l ls 12 notitle
} else {
plot  \
  [xmin:xmax] 1/0 notitle, \
  "<awk -F, '{print $2,$3}' ../data/cases_erfurt.csv" using 1:2 with linespoints ls 1 title "bestätigte Fälle"
}
  
