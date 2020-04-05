set terminal pngcairo enhanced background rgb "#f2f2f2" truecolor font "Linux Libertine O,16" size 800, 400 dl 2.0 
set encoding utf8
set minussign

set output '../plotT0.png'

# pie chart inspired by:
# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

# setup
unset xlabel
unset ylabel
unset key
unset tics
unset border

# latest update
update_str = "letztes Update: " . system("date +%d.%m.,\\ %H\\:%M") . " Uhr"

# get sum
stats "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u 2 prefix "A" nooutput

# get recovered
stats "<cat ../data/cases_thuringia_recovered.dat | sort -n -k1 | tail -n 1" u 2 prefix "B" nooutput

# get number of hospitalized
stats "<awk -F, '{a[$1]+=$5}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u 2 prefix "E" nooutput

# get number of severe
stats "<awk -F, '{a[$1]+=$6}END{for(i in a) print int(i/86400)*86400,a[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u 2 prefix "F" nooutput

angle(x)=x*360/A_sum

centerX=-0.15
centerY=0
radius=0.8

yposmin = 0.0
yposmax = 0.95*radius
xpos = 1.35*radius
ypos(i) = yposmax - i*(yposmax-yposmin)/(4)

set style fill solid 1
set size ratio -1
set xrange [-1.45*radius:3.6*radius]
set yrange [-radius:radius]

pos = 90

filter_inf(x, y)= (y >= 0) ? (x/y) : 0

plot \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(-0.15)):(sprintf("%i bestätigte Fälle in Thüringen", $2)) w labels left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (centerX):(centerY):(radius):(pos):(pos=pos+angle($2-B_max-$4)) w circle fc rgb "#0241b5", \
     '+' u (xpos):(ypos(1.75)) w p pt 5 ps 4 lc rgb "#0241b5", \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(1.75)):(sprintf("%i aktive Fälle* (%.1f%%), davon", $2 - B_max - $4, 100*($2-B_max-$4)/A_sum)) w labels left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(B_max)) w circle fc rgb "#006000", \
     '+' u (xpos):(ypos(4.75)) w p pt 5 ps 4 lc rgb "#006000", \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(4.75)):(sprintf("%i Genesene* (%.1f%%)", B_max, 100*B_max/A_sum)) w labels left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (centerX):(centerY):(radius):(pos):(pos=pos+angle($4)) w circle fc rgb "#000000", \
     '+' u (xpos):(ypos(5.75)) w p pt 5 ps 4 lc rgb "#000000", \
     \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos + 0.19):(ypos(2.75)):(sprintf("stationäre Fälle: %i (%.1f\%)", E_max, 100*filter_inf(E_max, $2 - B_max - $4))) w labels left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos + 0.19):(ypos(3.75)):(sprintf("schwere Verläufe: %i (%.1f\%)", F_max, 100*filter_inf(F_max, $2 - B_max - $4))) w labels left offset 2.5, 0, \
     \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(5.75)):(sprintf("%i Verstorbene (%.1f%%)", $4, 100*$4/A_sum)) w labels left offset 2.5, 0, \
     \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos + 0.20):(ypos(0.70)):(sprintf("≈ %.0f Fälle pro 100.000 EW", $2 / 21.34393 )) w labels left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(6.75)):("* geschätzt ab dem 26.03.") w labels font ", 12" left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(7.35)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<awk -F, '{a[$1]+=$4;b[$1]+=$8;c[$1]+=$7}END{for(i in a) print int(i/86400)*86400,a[i],b[i],c[i]}' ../data/cases_thuringia.csv | sort -n -k1 | tail -n 1" u (xpos):(ypos(7.95)):("Quelle: Thüringer Landesregierung") w labels font ", 12" left offset 2.5, 0

