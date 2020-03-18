set terminal pngcairo enhanced font "./fonts/Vollkorn-Regular.ttf,14" fontscale 1.0 size 800, 600 background rgb '#f2f2f2' dl 2.0
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
set style line  2 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  3 lc rgb '#000000' lt 1 lw 1 pt 7 ps 1.50
set style line  10 lc rgb '#000000' lw 1 lt 1 dt "  .  "
set style line  11 lc rgb '#aaaaaa' lw 1 lt 1 dt "  .  "

# grid
set grid xtics mxtics ls 10, ls 11
set grid ytics mytics ls 10, ls 11

# misc
set samples 30
set style increment default
set style fill transparent solid 0.20 border
