load "template.gnuplot"

fakeweeknum(x) = 12 + (x - 1584316800)/(7*86400)

# x-axis setup
set xdata
set xrange [ 10 : 54 < * < 120 ]
set xtics 4 out nomirror rotate by 90 offset 0, -1.8 scale 1.2
set mxtics 4
set xlabel "Kalenderwoche" offset 0.0, +0.55

# y-axis setup
set yrange [ 0 : 100 < * < 100000 ]
unset ylabel

# key
unset key

# grid
unset grid 
set grid ytics ls 21 lc rgb '#aaaaaa'

# bars
set style fill solid 1.00
set style data boxes
set boxwidth 0.67 rel

set xtics rotate by 0 offset 0, +0.50
set xtics ( "12" 12, "16" 16, "20" 20, "24" 24, "28" 28, "32" 32, "36" 36, "40" 40, "44" 44, "48" 48, "52" 52, "1" 54, "4" 57, "8" 61, "12" 65, "16" 69, "20" 73, "24" 77, "28" 81, "32" 85, "36" 89, "40" 93, "44" 97, "48" 101, "52" 105 )

set offsets graph 0.01, graph 0.01, graph 0.20, 0.00
