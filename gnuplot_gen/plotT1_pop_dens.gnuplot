set terminal pngcairo enhanced background rgb "#f8f8f8" truecolor font "Linux Libertine O,16" size 800, 600 dl 2.0 
set encoding utf8
set minussign

set fit quiet logfile '/dev/null'
set fit errorvariables

# margins
set lmargin 12.25
set rmargin 2.80
set tmargin 0.75
set bmargin 3.75

# colors and plot style
set style line  1 lc rgb '#0000FF' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  2 lc rgb '#800000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  3 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50
set style line  4 lc rgb '#005000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  5 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  6 lc rgb '#000080' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  10 lc rgb '#000000' lw 1 lt 1 dt "  .  "
set style line  11 lc rgb '#aaaaaa' lw 1 lt 1 dt "  .  "
set style line  12 lc rgb '#FF0000' lw 2
set style line  21 dt 3

# grid
set grid xtics ls 21 lc rgb '#aaaaaa'
set grid ytics ls 21 lc rgb '#aaaaaa'

# misc
set samples 30
set style increment default
 set style fill transparent solid 0.20 border

# axes
set xtics out nomirror scale 1.2
set mxtics 2

set format y '%6.0f'
set ytics out nomirror scale 1.2
set mytics 2

set key opaque
set border back

set object 1 rectangle from screen -0.1,-0.1 to screen 1.1,1.1 fc rgb "#f2f2f2" behind

# filter negative values
filter_neg(x)=(x>=0)?(x):(1/0)

# latest update
update_str = "{/*0.75 (Stand: " . system("date +%d.%m.,\\ %H\\:%M") . " Uhr)}"

set output '../plotT1_pop_dens.png'

set xrange [ 0 : 1000 ]

# stats for y
stats "<awk -F, '{ print $5 }' ./th_dens_vs_cases.dat" using 1 nooutput
set yrange [ 0 : int(4/3.0*STATS_max) ]

# x-axis setup
set xlabel "Einwohnerdichte (EW/km²)"

# y-axis setup
set ylabel sprintf("Zahl bestätigter Coronavirus-Fälle %s", update_str)

# key
set key at graph 0.50, 0.98 center top invert spacing 1.2 box ls 3 maxrows 1
# unset key

# data
plot  \
  1/0 notitle, \
  "<awk -F, '{if ($3 == 0) print $4, $5}' ./th_dens_vs_cases.dat" u 1:2 w p ls 2 title "Landkreise", \
  "<awk -F, '{if ( ($3 == 0) && ( $4 > 0 ) ) print $4, $5, $2}' ./th_dens_vs_cases.dat" u 1:2:($3) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 2 notitle, \
  "<awk -F, '{if ($3 == 1) print $4, $5}' ./th_dens_vs_cases.dat" u 1:2 w p ls 1 title "kreisfreie Städte", \
  "<awk -F, '{if ($3 == 1) print $4, $5, $2}' ./th_dens_vs_cases.dat" u 1:2:($3) with labels point pt 7 ps 0 center offset char -0.3, 0.8 tc ls 1 notitle
  
