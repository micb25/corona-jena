load "../gnuplot/template.gnuplot"

set output '../plotT6B_dec.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: Thüringer Landesregierung)}"

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ 1584316800 - 2.5 * 86400 : STATS_max + 86400/2 ]

# get maximum value
stats "<awk -F, 'BEGIN{d=0;w=-51;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$4-d;d=$4;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using 2 name "A" nooutput
set yrange [0 : int(1.4*A_max/10+1)*10 ]

# x-axis setup
set xdata time
set timefmt "%s"

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
set boxwidth 0.2 rel

set xtics rotate by 0 offset 0, +0.50
set xtics ( "KW 12\n{/*0.85 16.03.-}\n{/*0.85 22.03.}" 1584316800, \
            "KW 13\n{/*0.85 23.03.-}\n{/*0.85 29.03.}" 1584921600, \
            "KW 14\n{/*0.85 30.03.-}\n{/*0.85 05.04.}" 1585526400, \
            "KW 15\n{/*0.85 06.04.-}\n{/*0.85 12.04.}" 1586131200, \
            "KW 16\n{/*0.85 13.04.-}\n{/*0.85 19.04.}" 1586736000, \
            "KW 17\n{/*0.85 20.04.-}\n{/*0.85 26.04.}" 1587340800, \
            "KW 18\n{/*0.85 27.04.-}\n{/*0.85 03.05.}" 1587945600, \
            "KW 19\n{/*0.85 04.05.-}\n{/*0.85 10.05.}" 1588550400, \
            "KW 20\n{/*0.85 11.05.-}\n{/*0.85 17.05.}" 1589155200 )

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Coronavirus-Todesfälle pro Kalenderwoche in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, 'BEGIN{d=0;w=0;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$4-d;d=$4;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using 1:2 with boxes lt rgb "#52555e" notitle, \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Thüringer Landesregierung}"
  
