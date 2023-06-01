load "template.gnuplot"

set output '../plotTR_RKI.png'

# stats for x
stats "<awk -F, '{ print $1 }' ../data/rki_th/reproduction_rates_th.csv" using 1 nooutput
set xrange [ STATS_min + 86400 : STATS_max + 1.0 * 86400 ]

# stats for y
stats "<awk -F, '{ print $4 }' ../data/rki_th/reproduction_rates_th.csv | tail -n 1" using 1 name "R" nooutput
set yrange [ 0 : 4.0 ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%m.%Y"
set format y "%.1f"

# y-axis setup
unset ylabel

# key
set key at graph 0.98, 0.825  spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold geschätzte Reproduktionsrate {/Linux-Libertine-O-Bold-Italic R} für Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.89 ("(siehe Hinweis, " . update_str . ")") right textcolor ls 0

watermark = "michael-böhme.de/corona"
set label 3 at graph 0.02, 0.04 watermark left textcolor rgb '#999999'

last_value = sprintf("aktueller {/Linux-Libertine-O-Italic R}-Wert: %.1f", R_max)
set label 4 at graph 0.98, 0.04 last_value right textcolor ls 5

f(x) = 1.0

# data
plot  \
  f(x) with lines ls 1 notitle, \
  "<awk -F, '{print $1, $4}' ../data/rki_th/reproduction_rates_th.csv" using 1:(filter_neg($2)) with lines ls 12 lw 1.0 title "{/Linux-Libertine-O-Italic R}", \
  "<awk -F, 'BEGIN{for(i=0;i<7;i++){a[i]=0}} { if (NR > 1) {for(i=0; i<6; i++){a[i]=a[i+1]};a[6]=$4;b=0;for(i=0;i<7; i++){b=b+a[i]};print $1,b/7}}' ../data/rki_th/reproduction_rates_th.csv" using ($1-3.5*86400):(filter_neg($2)) with lines ls 12  lc rgb "#800000" lw 3.0 title "7-Tage-Mittelwert von {/Linux-Libertine-O-Italic R}"
