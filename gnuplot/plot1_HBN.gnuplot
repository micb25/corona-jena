load "template.gnuplot"

set output '../plot1_HBN.png'

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_hbn.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . " Uhr}"

# stats for x
stats "<awk -F, '{if (NR>1) print $1}' ../data/cases_hbn.csv" using 1 nooutput
set xrange [ STATS_min - 0.5 * 86400 : STATS_max + 3.5 * 86400 ]

# stats for y
stats "<awk -F, '{print $2}' ../data/cases_hbn.csv" using 1 nooutput
set yrange [ 0 : int(6.0/3.0*STATS_max) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle im Landkreis Hildburghausen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# data
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Landkreis Hildburghausen}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_hbn.csv | awk '{if ($4 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$4-ov;ov=$4;print $1,$4,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 5 notitle, \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_hbn.csv | awk '{if ($3 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$3-ov;ov=$3;print $1,$3,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 4 notitle, \
  "<awk -F, '{print $1,$2,$3,$4,$5,$6}' ../data/cases_hbn.csv | awk '{if ($2 >= 0) print $0}' | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 1 notitle, \
  \
  "<awk -F, '{if ($4 >= 0) print $1,$4}' ../data/cases_hbn.csv" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ($3 >= 0) print $1,$3}' ../data/cases_hbn.csv" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene", \
  "<awk -F, '{if (NR>1) print $1,$2-($3>=0?$3:0)-($4>=0?$4:0)}' ../data/cases_hbn.csv" using 1:(filter_neg($2)) with lines lt 1 lw 1.5 lc '#007af2' title "aktive Fälle", \
  "<awk -F, '{print $1,$2}' ../data/cases_hbn.csv" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle"
