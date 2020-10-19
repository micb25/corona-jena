set terminal pngcairo enhanced background rgb "#f8f8f8" truecolor font "Linux Libertine O,14" size 600, 450 dl 2.0 
set encoding utf8
set minussign

set fit quiet logfile '/dev/null'
set fit errorvariables

# margins
set lmargin 9.00
set rmargin 1.45
set tmargin 0.75
set bmargin 3.75

# colors and plot style
set style line  1 lc rgb '#ff8a1e' lt 1 lw 4 pt 7 ps 1.50 dt "."
set style line  2 lc rgb '#FF0000' lt 1 lw 4 pt 7 ps 1.50 dt "."
set style line  3 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50
set style line  4 lc rgb '#005000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  5 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  6 lc rgb '#000080' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  7 lc rgb '#800000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  8 lc rgb '#ff8a1e' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  10 lc rgb '#000000' lw 1 lt 1 dt "  .  "
set style line  11 lc rgb '#aaaaaa' lw 1 lt 1 dt "  .  "
set style line  12 lc rgb '#FF0000' lw 1.5
set style line  16 lc rgb '#800080' lt 1 lw 2
set style line  17 lc rgb '#FF0000' lt 1 lw 2
set style line  18 lc rgb '#ff8a1e' lt 1 lw 2
set style line  19 lc rgb '#5c5c5c' lt 1 lw 2
set style line  21 dt 3

# grid
set grid xtics ls 21 lc rgb '#aaaaaa'
set grid ytics ls 21 lc rgb '#aaaaaa'

# misc
set samples 30
set style increment default
 set style fill transparent solid 0.20 border

# axes
set xtics 14*86400 out nomirror rotate by 90 offset 0, -1.8 scale 1.2
set mxtics 2

set format y '%3.0f'
set ytics out nomirror scale 1.2
set mytics 2

set key opaque
set border back

set object 1 rectangle from screen -0.1,-0.1 to screen 1.1,1.1 fc rgb "#f2f2f2" behind

# filter negative values
filter_neg(x)=(x>=0)?(x):(1/0)

set output '../plot8_RKI_%FILENAME%.png'

# stats for x
stats "<awk -F, '{print $1}' ../data/cases_rki_7day_incidence.csv" using 1 nooutput
set xrange [ STATS_min - 2.0 * 86400 : STATS_max + 2.0 * 86400 ]
set yrange [0:100 < * < 100000]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/cases_rki_7day_incidence.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 letzte Aktualisierung: " . date_cmd . "; Quelle: RKI}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Neuinfektionen in 7 Tagen pro 100 000 EW'
#unset ylabel

# key
set key at graph 0.02, 0.98 left top invert spacing 1.2 box ls 3

set label 1 at graph 0.98, 0.94 "{/Linux-Libertine-O-Bold %SNAME%}" right textcolor ls 0
set label 2 at graph 0.98, 0.87 update_str right textcolor ls 0

set offsets 0.00, 0.00, graph 0.25, 0.00

set datafile separator ","

threshold_low(x) = 35.0
threshold_high(x) = 50.0

plot  \
  \
  threshold_low(x) with lines ls 1 notitle, \
  threshold_high(x) with lines ls 2 notitle, \
  "../data/cases_rki_7day_incidence.csv" using 1:(column(%COLIDX%)) with lines lt 1 lw 3 lc '#047495' title "7-Tages-Inzidenz"
  
