load "../gnuplot/template.gnuplot"

set output '../plotT1_%FILENAME%.png'

# stats for x
stats "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1 nooutput
set xrange [ STATS_min - 1.0 * 86400 : STATS_max + 1.5 * 86400 ]

# stats for y
stats "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1" using 2 nooutput
set yrange [ 0 : int(2*STATS_max) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Zahl der Fälle %NAMEYLABEL%'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# data
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Thüringer Landesregierung}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 8 title "aktuelle stationäre Fälle", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char +0.8, 0.4 tc ls 5 notitle, \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 8 notitle, \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 1 notitle

#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 4 notitle, \
#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene (bis 25.03.)", \
#  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$6}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 7 title "schwere Verläufe", \
