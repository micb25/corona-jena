load "template.gnuplot"

set output '../plot3_Gera.png'

# stats for x
stats "<awk -F, '{ print $1 }' ../data/cases_gera.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max ]
set yrange [0:50 < * < 100000]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_gera.csv | tail -n 1 | xargs date +"%d.%m.%Y, %H:%M" -d`")
update_str = "{/*0.75 letzte Aktualisierung: " . date_cmd . " Uhr}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'aktive Coronavirus-Fälle in Gera'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: Stadt Gera}" right textcolor ls 0

set offsets graph 0.01, graph 0.01, graph 0.175, 0.00

plot  \
  "<awk -F, '{if ($5>=0) print $1,$5}' ../data/cases_gera.csv" using 1:(filter_neg($2)) with lines lt 1 lw 3 lc '#ff8a1e' title "davon stationäre Fälle", \
  "<awk -F, '{if ( (NR > 1) && ( $2 >= 0 ) && ( $3 >= 0 ) ) print $1,$2-$3-($4>=0?$4:0)}' ../data/cases_gera.csv" using 1:(filter_neg($2)) with lines lt 1 lw 3 lc '#007af2' title "aktive Fälle"
  
