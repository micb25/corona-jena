load "template.gnuplot"

set output '../plotT1.png'

# stats for x
stats "<awk -F, '{a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 1 nooutput
set xrange [ STATS_min - 1.5 * 86400 : STATS_max + 1.5 * 86400 ]

# stats for y
stats "<awk -F, '{a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 2 nooutput
set yrange [ 0 : int(5.0/3.0*STATS_max) ]

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Thüringen'

# key
set key at graph 0.02, 0.98 left top spacing 1.5 box ls 3

# latest update
update_str = "letztes Update: " . system("date +%d.%m.\\ %H\\:%M")

# data
plot  \
  1/0 notitle, \
  1/0 lc rgb '#f2f2f2' title update_str, \
  "<awk -F, '{a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 1:2 with linespoints ls 1 title "bestätigte Fälle", \
  "<awk -F, '{if ( $1 < 1585213200 ) a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 1:2 with linespoints ls 4 title "Genesene (bis 25.03.)", \
  "<awk '{if ($1 >= 1585213200) print int($1/86400)*86400, $2}' ../data/cases_thuringia_recovered.dat | sort -n -k1" using 1:2 with linespoints ls 4 pt 5 title "Genesene (ab 26.03. geschätzt)", \
  "<awk -F, '{a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.dat | sort -n -k1" using 1:2 with linespoints ls 5 title "Verstorbene"
