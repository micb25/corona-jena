load "template.gnuplot"

set output '../plotTR_RKI.png'

# stats for x
stats "<awk -F, '{ print $1 }' ../data/rki_th/reproduction_rates_th.csv" using 1 nooutput
set xrange [ STATS_min + 86400 : STATS_max + 1.0 * 86400 ]

# stats for y
stats "<awk -F, '{ print $4 }' ../data/rki_th/reproduction_rates_th.csv | tail -n 1" using 1 name "R" nooutput
set yrange [ 0 : 3.5 ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."
set format y "%.1f"

# y-axis setup
unset ylabel

# key
unset key

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold geschätzte Reproduktionsrate {/Linux-Libertine-O-Italic R} für Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.89 ("(siehe Hinweis, " . update_str . ")") right textcolor ls 0

watermark = "michael-böhme.de/corona"
set label 3 at graph 0.02, 0.04 watermark left textcolor rgb '#999999'

last_value = sprintf("aktueller Wert: %.1f", R_max)
set label 4 at graph 0.98, 0.04 last_value right textcolor ls 5

f(x) = 1.0

# data
plot  \
  f(x) with lines ls 1 notitle, \
  "<awk -F, '{print $1, $4}' ../data/rki_th/reproduction_rates_th.csv" using 1:(filter_neg($2)) with lines ls 12 notitle
