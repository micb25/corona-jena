load "template.gnuplot"

set output '../plot1_Jena.png'

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
set ylabel 'Gesamtzahl der Fälle in Jena'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: Stadt Jena}" right textcolor ls 0

set offsets 0.00, 0.00, graph 0.40, 0.00

plot  \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_jena_opendata.csv | awk '{if ($4 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$4-ov;ov=$4;print $1,$4,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 0.0,  1.8 tc ls 5 notitle, \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_jena_opendata.csv | awk '{if ($3 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$3-ov;ov=$3;print $1,$3,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 0.0, -1.8 tc ls 4 notitle, \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_jena_opendata.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 0.0,  1.8 tc ls 1 notitle, \
  \
  "<awk -F, '{print $1,$4}' ../data/cases_jena_opendata.csv" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{print $1,$3}' ../data/cases_jena_opendata.csv" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene", \
  "<awk -F, '{print $1,$2}' ../data/cases_jena_opendata.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
