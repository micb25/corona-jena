load "../gnuplot/template.gnuplot"

set output '../plotT6B_rec.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: Thüringer Landesregierung)}"

# stats for x
stats "<awk -F, '{if ( NR > 1 ) print int($1/86400)*86400}' ../data/cases_th_sums.csv" using 1 nooutput
set xrange [ 1584316800 - 2.5 * 86400 : STATS_max + 86400/2 ]

# get maximum value
stats "<awk -F, 'BEGIN{d=0;w=-51;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$3-d;d=$3;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using 2 name "A" nooutput
set yrange [0 : int(1.4*A_max/10)*10 ]

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
set xtics ( "12\n{/*0.75 16.03.-}\n{/*0.75 22.03.}" 1584316800, \
            "13\n{/*0.75 23.03.-}\n{/*0.75 29.03.}" 1584921600, \
            "14\n{/*0.75 30.03.-}\n{/*0.75 05.04.}" 1585526400, \
            "15\n{/*0.75 06.04.-}\n{/*0.75 12.04.}" 1586131200, \
            "16\n{/*0.75 13.04.-}\n{/*0.75 19.04.}" 1586736000, \
            "17\n{/*0.75 20.04.-}\n{/*0.75 26.04.}" 1587340800, \
            "18\n{/*0.75 27.04.-}\n{/*0.75 03.05.}" 1587945600, \
            "19\n{/*0.75 04.05.-}\n{/*0.75 10.05.}" 1588550400, \
            "20\n{/*0.75 11.05.-}\n{/*0.75 17.05.}" 1589155200, \
            "21\n{/*0.75 18.05.-}\n{/*0.75 24.05.}" 1589760000, \
            "22\n{/*0.75 25.05.-}\n{/*0.75 31.05.}" 1590364800, \
            "23\n{/*0.75 01.06.-}\n{/*0.75 07.06.}" 1590969600, \
            "24\n{/*0.75 08.06.-}\n{/*0.75 14.06.}" 1591574400, \
            "25\n{/*0.75 15.06.-}\n{/*0.75 21.06.}" 1592179200, \
            "26\n{/*0.75 22.06.-}\n{/*0.75 28.06.}" 1592784000, \
            "27\n{/*0.75 29.06.-}\n{/*0.75 05.07.}" 1593388800, \
            "28\n{/*0.75 06.07.-}\n{/*0.75 12.07.}" 1593993600, \
            "29\n{/*0.75 13.07.-}\n{/*0.75 19.07.}" 1594598400, \
            "30\n{/*0.75 20.07.-}\n{/*0.75 26.07.}" 1595203200 )

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Genesungen pro Kalenderwoche in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, 'BEGIN{d=0;w=0;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$3-d;d=$3;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using 1:2 with boxes lt rgb "#006000" notitle, \
  "<awk -F, 'BEGIN{d=0;w=0;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$3-d;d=$3;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using 1:2:2 with labels point pt 7 ps 0 center offset char -0.5, 0.5 tc ls 4 notitle, \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Thüringer Landesregierung}"
  
