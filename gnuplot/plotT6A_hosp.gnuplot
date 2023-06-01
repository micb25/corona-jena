load "../gnuplot/template.gnuplot"

set output '../plotT6A_hosp.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/RKI_TH_Hospitalisierung.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: RKI; ggf. Nachmeldungen möglich)}"

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ STATS_min : STATS_max ]

# x-axis setup
set xdata time
set timefmt "%s"
set format x "%m.%Y"

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
set boxwidth 1.0 relative

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold gemeldete Hospitalisierungen pro Tag in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

set offsets graph 0.01, graph 0.01, graph 0.20, 0.00

# data
plot  \
    "<awk -F, '{if (NR>1&&$2==\"00+\") print $1,$5}' ../data/RKI_TH_Hospitalisierung.csv" using 1:(filter_neg($2)) with boxes lt rgb "#ff8a1e" title "Hospitalisierungen"
  
