load "../gnuplot/template.gnuplot"

set output '../plotT9.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: TMASGFF)}"

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ 1593554400 : 1593554400 + 365*86400 ]

# x-axis setup
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
unset ylabel

# key
# unset key
set key at graph 0.02, 0.85 left top spacing 1.2 box ls 3

# grid
unset grid 
set grid ytics ls 21 lc rgb '#aaaaaa'

# bars
set style fill solid 1.00 
set style data boxes
set boxwidth 1.0 relative

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Neuinfektionen pro Tag in Thüringen (7-Tage-Mittelwert)}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

set offsets graph 0.00, graph 0.00, graph 0.20, 0.00

# data
plot  \
  "<awk -F, 'BEGIN{d=0;for(i=0;i<7;i++){a[i]=0}}{if (NR>1) {if ($1>=1584352800) {for(i=0; i<6; i++){a[i]=a[i+1]};a[6]=$2-d;b=0;for(i=0;i<7; i++){b=b+a[i]};print int($1/86400)*86400,b/7;d=$2;}}}' ../data/cases_th_sums.csv" using ($1-365*86400):2 with lines lw 2 lt rgb "#0000FF" title " 2021/2022", \
  "<awk -F, 'BEGIN{d=0;for(i=0;i<7;i++){a[i]=0}}{if (NR>1) {if ($1>=1584352800) {for(i=0; i<6; i++){a[i]=a[i+1]};a[6]=$2-d;b=0;for(i=0;i<7; i++){b=b+a[i]};print int($1/86400)*86400,b/7;d=$2;}}}' ../data/cases_th_sums.csv" using 1:2 with lines lw 2 lt rgb "#000060" title " 2020/2021"
  
