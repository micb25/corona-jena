load "template.gnuplot"

set output '../plot3_Jena.png'

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_jena_opendata.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# stats for x
stats "<awk -F, '{print $1}' ../data/cases_jena_opendata.csv" using 1 nooutput
set xrange [ STATS_min - 2.0 * 86400 : STATS_max + 2.0 * 86400 ]
set yrange [0:50 < * < 100000]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'aktive Coronavirus-Fälle in Jena'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: Stadt Jena}" right textcolor ls 0

set offsets 0.00, 0.00, graph 0.20, 0.00

plot  \
  "<awk -F, '{if ($5>=0) print $1,$5}' ../data/cases_jena_opendata.csv" using 1:(filter_neg($2)) with lines lt 1 lw 3 lc '#ff8a1e' title "davon stationäre Fälle", \
  "<awk -F, '{print $1,$2-$3-$4}' ../data/cases_jena_opendata.csv" using 1:(filter_neg($2)) with lines lt 1 lw 3 lc '#007af2' title "aktive Fälle"
  
