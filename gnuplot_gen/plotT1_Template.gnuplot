load "../gnuplot/template.gnuplot"

set output '../plotT1_%FILENAME%.png'

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_thuringia.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 letztes Update: " . date_cmd . "}"

# stats for x
stats "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1 nooutput
set xrange [ STATS_min : STATS_max + 10.0 * 86400 ]

# stats for y
stats "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1" using 2 nooutput

if ( STATS_max > 200 ) {
	set yrange [ 0 : 100*int(1+int(1.40*STATS_max)/100.0) ]
} else {
	if ( STATS_max > 50 ) {
		set yrange [ 0 : 50*int(1+int(1.40*STATS_max)/50.0) ]
	} else {
		set yrange [ 0 : 10*int(1+int(1.40*STATS_max)/10.0) ]
	}
}


# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Zahl der Fälle %NAMEYLABEL%'

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.95 update_str right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 Quelle: Thüringer Landesregierung}" right textcolor ls 0

# data
plot  \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 5 title "Verstorbene", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 8 title "stationäre Fälle", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 1 title "bestätigte Fälle", \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 left offset char +0.8, 0.25 tc ls 5 notitle, \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 left offset char +0.8, 0.45 tc ls 8 notitle, \
  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$4}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | awk 'BEGIN{ov=0}{dv=$2-ov;ov=$2;print $1,$2,dv}' | tail -n 1" using 1:2:(sprintf("%i (%+i)", $2, $3)) with labels point pt 7 ps 0 left offset char +0.8, 0.25 tc ls 1 notitle

#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | awk '{if ($2 >= 0) print $0}' | sort -n -k1 | tail -n 1" using 1:2:($2) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 4 notitle, \
#  "<awk -F, '{if ($1 < 1585180800 && $2==\"%NAME%\")a[$1]+=$8}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 4 title "Genesene (bis 25.03.)", \
#  "<awk -F, '{if ($2==\"%NAME%\")a[$1]+=$6}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1" using 1:(filter_neg($2)) with linespoints ls 7 title "schwere Verläufe", \
