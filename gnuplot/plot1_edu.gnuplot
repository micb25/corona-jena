load "template.gnuplot"

set output '../plot1_edu_k.png'

set xtics 7*86400 out nomirror rotate by 90 offset 0, -1.8 scale 1.2
set mxtics 7

# stats for x
stats "<awk -F, '{print $1}' ../data/schools/TH_schools.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max ]
set yrange [0:*]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/schools/TH_schools.csv | tail -n 1 | xargs date +"%d.%m.%Y, %H:%M" -d`")
update_str = "{/*0.75 letzte Aktualisierung: " . date_cmd . " Uhr}"

set style line 81 lc rgb '#fec615' lt 1 lw 2 pt 9 ps 1.00 #dt "."
set style line 82 lc rgb '#e50000' lt 1 lw 2 pt 9 ps 1.00 #dt "."
set style line 83 lc rgb '#fec615' lt 1 lw 2 pt 7 ps 1.00 #dt "."
set style line 84 lc rgb '#e50000' lt 1 lw 2 pt 7 ps 1.00 #dt "."

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Zahl an Bildungseinrichtungen'

# key
set key at graph 0.02, 0.98 left top spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: TMBJS}" right textcolor ls 0

set offsets graph 0.02, graph 0.15, graph 0.15, 0.00

# data
#   "<awk -F, '{print $1, $4}' ../data/schools/TH_schools.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 7.0, 0.3 tc ls 81 notitle, \

plot  \
  "<awk -F, '{print $1, $5}' ../data/schools/TH_schools.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 7.0, 0.3 tc ls 82 notitle, \
  \
  "<awk -F, '{print $1, $5}' ../data/schools/TH_schools.csv" using 1:(filter_neg($2)) with linespoints ls 82 title "    Kitas Stufe ROT", \
  "<awk -F, '{print $1, $4}' ../data/schools/TH_schools.csv" using 1:(filter_neg($2)) with linespoints ls 81 title "    Kitas Stufe GELB", \

set output '../plot1_edu_s.png'

# data
#   "<awk -F, '{print $1, $7}' ../data/schools/TH_schools.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 7.0, 0.3 tc ls 83 notitle, \

plot  \
  "<awk -F, '{print $1, $8}' ../data/schools/TH_schools.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i\n(%+i)", $2, $3)) with labels point pt 7 ps 0 right offset char 7.0, 0.3 tc ls 84 notitle, \
  \
  "<awk -F, '{print $1, $8}' ../data/schools/TH_schools.csv" using 1:(filter_neg($2)) with linespoints ls 84 title "    Schulen Stufe ROT", \
  "<awk -F, '{print $1, $7}' ../data/schools/TH_schools.csv" using 1:(filter_neg($2)) with linespoints ls 83 title "    Schulen Stufe GELB", \
