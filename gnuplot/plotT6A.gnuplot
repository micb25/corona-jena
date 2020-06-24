load "../gnuplot/template.gnuplot"

set output '../plotT6A.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: Thüringer Landesregierung)}"

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ STATS_min + 86400/2 : STATS_max + 86400/2 ]

# get maximum value
stats "<awk -F, 'BEGIN{d=0;}{if ((NR>1)&&($1>1584230400)) {print int($1/86400)*86400,$2-d;d=$2;}}' ../data/cases_th_sums.csv" using 2 name "A" nooutput
set yrange [0 : int(1.30*A_max/10)*10 ]

# x-axis setup
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
unset ylabel

# key
unset key

# grid
unset grid 
set grid ytics ls 21 lc rgb '#aaaaaa'

# bars
set style fill solid 1.00 
set style data boxes
set boxwidth 0.4 relative

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold bestätigte Neuinfektionen pro Tag in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, 'BEGIN{d=0;}{if (NR>1) {if ($1>=1584352800) print int($1/86400)*86400,$2-d;d=$2;}}' ../data/cases_th_sums.csv" using 1:2 with boxes lt rgb "#0000FF" title "bestätigte Neuinfektionen in Thüringen pro Tag", \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Thüringer Landesregierung}"
  
