load "template.gnuplot"

set xtics 14*86400 out nomirror rotate by 90 offset 0, -1.8 scale 1.2
set mxtics 2

set output '../plotTV_TH.png'

# stats for x
stats "<awk -F, '{if (NR>1) print int($1/86400)*86400}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1 nooutput
set xrange [ STATS_min - 0.5 * 86400 : STATS_max + 0.5 * 86400 ]
set yrange [ 0: * ]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+7200}' ../data/RKI_COVID19_Impfquotenmonitoring.csv | tail -n 1 | xargs date +"%d.%m." -d`")
update_str = "{/*0.75 (letztes Update: " . date_cmd . "; Quelle: RKI)}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# fit
m = 1
n = -STATS_min
f(x) = m * x + n
fit [ STATS_max - 14 * 86400 : STATS_max ] f(x) "<awk -F, '{if (NR>1&&$3==16) print $1,100*$5/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1:(filter_neg($2)) via m, n

vac_per_day_rel = m * 86400
vac_per_day = vac_per_day_rel * 2133378 / 100.0

# y-axis setup
set ylabel 'Bevölkerungsanteil'
set format y "%.0f%%"

# grid
set grid xtics ls 21 lc rgb '#cccccc'
set grid ytics ls 21 lc rgb '#cccccc'

# key
set key at graph 0.02, 0.98 left top spacing 1.08 box ls 3

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold geimpfte Bevölkerung in}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/Linux-Libertine-O-Bold Thüringen}" right textcolor ls 0
set label 10 at graph 0.98, 0.85 update_str right textcolor ls 0

set label 3 at graph 0.03, 0.65 "{/Linux-Libertine-O-Bold*0.9 14-Tage-Trend (Erstimpfungen):}" left textcolor ls 0

if ( vac_per_day_rel > 0 ) {
	set label 4 at graph 0.04, 0.60 sprintf("{/*0.8 %+.0f Impfungen pro Tag}", vac_per_day) left textcolor ls 0
	set label 5 at graph 0.04, 0.55 sprintf("{/*0.8 %+.2f%% geimpfter Anteil pro Tag}", vac_per_day_rel) left textcolor ls 0

	line = 0.50
	achievement_25 = (25 - f(STATS_max) ) / vac_per_day_rel
	achievement_50 = (50 - f(STATS_max) ) / vac_per_day_rel
	achievement_75 = (75 - f(STATS_max) ) / vac_per_day_rel
	
	if ( achievement_25 > 0 ) {
		set label 6 at graph 0.04, line sprintf("{/*0.8 25%% erreicht in %.0f Tagen}", achievement_25) left textcolor ls 0
		line = line - 0.05
	}
	if ( achievement_50 > 0 ) {
		set label 7 at graph 0.04, line sprintf("{/*0.8 50%% erreicht in %.0f Tagen}", achievement_50) left textcolor ls 0
		line = line - 0.05
	}
	if ( achievement_75 > 0 ) {
		set label 8 at graph 0.04, line sprintf("{/*0.8 75%% erreicht in %.0f Tagen}", achievement_75) left textcolor ls 0
		line = line - 0.05
	}
}

set offsets 0.00, graph 0.10, graph 0.30, 0.00

plot  \
  \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$5/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1:(filter_neg($2)) with lines ls 40  lw 3 title "Erstimpfungen", \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$11/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1:(filter_neg($2)) with lines ls 41 lw 3 title "Zweitimpfungen", \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$13/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1:(filter_neg($2)) with lines ls 42 lw 3 title "Auffrischimpfungen", \
  "<awk -F, '{if (NR>1&&$3==16) print 86400*30*6+$1,100*$11/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv" using 1:(filter_neg($2)) with lines ls 43 title "{/*0.9 Auffrischimpfungen (theoretisch)}", \
  1/0 title "{/*0.9 Zweitimpfungen + 6 Monate}" lc rgb "#f2f2f2", \
  \
  [ STATS_max - 14 * 86400 : STATS_max ] f(x) with lines ls 12 notitle, \
  \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$5/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv | tail -n 1" using 1:2:(sprintf("%.1f%%", $2)) with labels point pt 7 ps 0 right offset char 5, +0.3 tc ls 40 notitle, \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$11/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv | tail -n 1" using 1:2:(sprintf("%.1f%%", $2)) with labels point pt 7 ps 0 right offset char 5, -0.3 tc ls 41 notitle, \
  "<awk -F, '{if (NR>1&&$3==16) print 86400*30*6+$1,100*$11/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv | tail -n 1" using 1:2:(sprintf("%.1f%%", $2)) with labels point pt 7 ps 0 right offset char 5, +0.3 tc ls 43 notitle, \
  "<awk -F, '{if (NR>1&&$3==16) print $1,100*$13/2133378}' ../data/RKI_COVID19_Impfquotenmonitoring.csv | tail -n 1" using 1:2:(sprintf("%.1f%%", $2)) with labels point pt 7 ps 0 right offset char 5, 0.0 tc ls 42 notitle
