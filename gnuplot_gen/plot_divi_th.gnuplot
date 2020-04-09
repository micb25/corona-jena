load "../gnuplot/template.gnuplot"

set output '../plot_divi_th.png'

set datafile separator ","

# stats for x
stats "../data/divi_db_th/divi_db_th_sums.csv" using 1 nooutput
set xrange [ STATS_min - 1.0 * 86400 : STATS_max + 1.0 * 86400 ]

# stats for y
stats "../data/divi_db_th/divi_db_th_sums.csv" using 2 nooutput
set yrange [ 0 : int(1.5*STATS_max) ]

# x-axis setup

set xtics 1*86400 out nomirror rotate by 90 offset 0, -1.8 scale 1.2

unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Einträge im DIVI-Intensivregister für Thüringen'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

# data
plot  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: DIVI Intensivregister}", \
  1/0 lc rgb '#f2f2f2' title update_str, \
  "../data/divi_db_th/divi_db_th_sums.csv" u 1:2 with lines lc rgb '#ff8a1e' lt 1 lw 2 title "aktuelle Einträge im DIVI-Intensivregister" #, \
  
  
  #"<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center #offset char +0.8, 0.4 tc ls 5 notitle, \
  #"<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center #offset char -0.3, 0.8 tc ls 8 notitle, \
  #"<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 1 notitle

#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 4 notitle, \
#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene (bis 25.03.)", \
#  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$6}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 7 title "schwere Verläufe", \
