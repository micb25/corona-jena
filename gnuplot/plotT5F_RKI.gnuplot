load "template.gnuplot"

set output '../plotT5F_RKI.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/RKI_TH_Hospitalisierung.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . "; Quelle: RKI; ggf. Nachmeldungen möglich)}"

# x-axis setup
set xrange [-0.5:5.5]
set xtics rotate by 0 offset 0, 0
set xtics ("0-4\nJahre" 0, "5-14\nJahre" 1, "15-34\nJahre" 2, "35-59\nJahre" 3, "60-79\nJahre" 4, "80+\nJahre" 5)

# y-axis setup
set ylabel "Summe an Hospitalisierungen in Thüringen"
set yrange [0:*]
set mytics 2

# key
set key at graph 0.02, 0.98 left top spacing 1.2 box ls 3

# grid
unset grid 
set grid ytics ls 21 lc rgb '#aaaaaa'

# bars
set boxwidth 0.9
set style fill solid 1.00 
set style data histograms
set style histogram clustered gap 1

set offsets 0.00, 0.00, graph 0.20, 0.00

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Hospitalisierungen nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

plot  \
  "<awk -F, '{if (NR>1) { print $2, $6 }}' ../data/RKI_TH_Hospitalisierung.csv | tail -n 6" using 2 with histograms lt rgb "#ff8a1e" title "  Summe   ", \
  "" using (column(0)):($2):($2>0?(sprintf("{/*0.85 %.0f}", $2)):"") with labels center offset 0.0, 0.7 notitle, \
