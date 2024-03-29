set terminal pngcairo enhanced background rgb "#f8f8f8" truecolor font "Linux Libertine O,16" size 800, 600 dl 2.0 
set encoding utf8
set minussign

set fit quiet logfile '/dev/null'
set fit errorvariables

# margins
set lmargin 13.60
set rmargin 1.45
set tmargin 0.75
set bmargin 3.75

# colors and plot style
set style line  1 lc rgb '#0000FF' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  2 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50 dt "."
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
set style line  31 lc rgb '#0000FF' lt 1 lw 1 pt 7 ps 1.50
set style line  32 lc rgb '#0000A0' lt 1 lw 1 pt 7 ps 1.50
set style line  33 lc rgb '#A000A0' lt 1 lw 1 pt 7 ps 1.50
set style line  34 lc rgb '#600060' lt 1 lw 1 pt 7 ps 1.50
set style line  35 lc rgb '#0060c0' lt 1 lw 1 pt 7 ps 1.50
set style line  36 lc rgb '#008080' lt 1 lw 1 pt 7 ps 1.50
set style line  40 lc rgb '#137e6d' lt 1 lw 3 pt 7 ps 1.50
set style line  41 lc rgb '#0b4008' lt 1 lw 3 pt 7 ps 1.50
set style line  42 lc rgb '#0d9419' lt 1 lw 3 pt 7 ps 1.50
set style line  43 lc rgb '#0d9419' lt 1 lw 3 pt 7 ps 1.50 dt "."

# grid
set grid xtics ls 21 lc rgb '#aaaaaa'
set grid ytics ls 21 lc rgb '#aaaaaa'

# misc
set samples 30
set style increment default
set style fill transparent solid 0.20 border

# axes
set xtics 3*365*86400/12 out nomirror rotate by 90 offset 0, -2.6 scale 1.0
set mxtics 3

set format y '%6.0f'
set ytics out nomirror scale 1.2 offset +0.5, 0.0
set mytics 2

set key opaque
set border back

set object 1 rectangle from screen -0.1,-0.1 to screen 1.1,1.1 fc rgb "#f2f2f2" behind

# filter negative values
filter_neg(x)=(x>=0)?(x):(1/0)

# latest update
update_str = "{/*0.75 letztes Update: " . system("date +%d.%m.,\\ %H\\:%M") . " Uhr}"
