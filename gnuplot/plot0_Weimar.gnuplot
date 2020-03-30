set terminal pngcairo enhanced transparent truecolor font "Linux Libertine O,16" size 800, 400 dl 2.0 
set encoding utf8
set minussign

set output '../plot0_Weimar.png'

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

# gets sum of infected people
stats "<cat ../data/cases_weimar.dat | awk '{print $2, $2}'" u 2 prefix "A" nooutput

# gets maximum number of recovered people
stats "<cat ../data/cases_weimar.dat | awk '{print $2, $3}'" u 2 prefix "B" nooutput

# gets maximum number of deceased
stats "<cat ../data/cases_weimar.dat | awk '{print $2, $4}'" u 2 prefix "C" nooutput

angle(x)=x*360/A_max

centerX=0
centerY=0
radius=0.8

yposmin = 0.0
yposmax = 0.95*radius
xpos = 1.35*radius
ypos(i) = yposmax - i*(yposmax-yposmin)/(4)

set style fill solid 1
set size ratio -1
set xrange [-1.75*radius:3.3*radius]
set yrange [-radius:radius]

pos = 90

plot \
     "<echo 0" u (xpos):(ypos(1)):(sprintf("%i bestätigte Fälle in Weimar", A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(A_max-B_max-C_max)) w circle fc rgb "#0241b5", \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#0241b5", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf("%i aktive Fälle (%.1f%%)", A_max - B_max - C_max, 100*(A_max-B_max-C_max)/A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(B_max)) w circle fc rgb "#006000", \
     "<echo 0" u (xpos):(ypos(3)) w p pt 5 ps 4 lc rgb "#006000", \
     "<echo 0" u (xpos):(ypos(3)):(sprintf("%i Genesene (%.1f%%)", B_max, 100*B_max/A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(C_max)) w circle fc rgb "#000000", \
     "<echo 0" u (xpos):(ypos(4)) w p pt 5 ps 4 lc rgb "#000000", \
     "<echo 0" u (xpos):(ypos(4)):(sprintf("%i Verstorbene (%.1f%%)", C_max, 100*C_max/A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: Stadt Weimar") w labels font ", 12" left offset 2.5, 0
