load "../gnuplot/template.gnuplot"

set output '../plotT9_icu.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: DIVI Intensivregister)}"

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

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold mit COVID-19 belegte Intensivbetten in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

set offsets graph 0.00, graph 0.00, graph 0.20, 0.00

# data
plot  \
  "<awk -F, '{if (NR>1) {print $1,$5}}' ../data/divi_db_th/divi_data_th.csv" using ($1-365*86400):2 with lines lw 2 lt rgb "#ff8a1e" title " 2021/2022", \
  "<awk -F, '{if (NR>1) {print $1,$5}}' ../data/divi_db_th/divi_data_th.csv" using 1:2 with lines lw 2 lt rgb "#b66215" title " 2020/2021"
  
