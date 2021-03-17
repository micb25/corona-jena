load "template.gnuplot"

set output '../plot1_Gera.png'

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
set ylabel 'Gesamtzahl der Fälle in Gera'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.99, 0.98 update_str right textcolor ls 0
set label 2 at graph 0.99, 0.93 "{/*0.75 Quelle: Stadt Gera}" right textcolor ls 0

set offsets graph 0.01, graph 0.12, graph 0.20, 0.00

plot  \
  "<cat ../data/cases_gera.csv | awk -F, '{if ($4 >= 0) print $0}' | awk -F, 'BEGIN{ov=0}{dv=$4-ov;ov=$4;print $1,$4,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.0, 0.8 tc ls 5 notitle, \
  "<cat ../data/cases_gera.csv | awk -F, '{if ($3 >= 0) print $0}' | awk -F, 'BEGIN{ov=0}{dv=$3-ov;ov=$3;print $1,$3,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.0,-0.2 tc ls 4 notitle, \
  "<cat ../data/cases_gera.csv | awk -F, '{if ($2 >= 0) print $0}' | awk -F, 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 5.0, 0.8 tc ls 1 notitle, \
  \
  "<awk -F, '{if ((NR>1)&&($4>=0)) print $1,$4}' ../data/cases_gera.csv" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ((NR>1)&&($3>=0)) print $1,$3}' ../data/cases_gera.csv | awk -F, '{print $1, $2}'" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene", \
  "<awk -F, '{if ((NR>1)&&($2>=0)) print $1,$2}' ../data/cases_gera.csv | awk -F, '{print $1, $2}'" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
