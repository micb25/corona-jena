set terminal pngcairo enhanced background rgb "#f2f2f2" truecolor font "Linux Libertine O,16" size 800, 400 dl 2.0 
set encoding utf8
set minussign

set output '../plot0_Erfurt.png'

# pie chart inspired by:
# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

# setup
unset xlabel
unset ylabel
unset key
unset tics
unset border

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$2}' ../data/cases_erfurt.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "letztes Update: " . date_cmd . " Uhr"

# gets sum of infected people
stats "<cat ../data/cases_erfurt.csv | awk -F, '{print $2, $3}'" u 2 prefix "A" nooutput

# gets maximum number of recovered people
stats "<cat ../data/cases_erfurt.csv | awk -F, '{print $2, $4}'" u 2 prefix "B" nooutput

# gets maximum number of dead people
stats "<cat ../data/cases_erfurt.csv | awk -F, '{print $2, $5}'" u 2 prefix "C" nooutput

# calculate diffs
stats "<awk -F, '!_[$2]++' ../data/cases_erfurt.csv | awk -F, '{if ($3 >= 0) print $2,$3}' | tail -n 2" u 2 prefix "G" nooutput

# get 7-day incidence
stats "<awk -F, '{print $6}' ../data/cases_rki_7day_incidence.csv | tail -n 1" using 1 prefix "I" nooutput

diff_c = G_max - G_min

angle(x)=x*360/A_max

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

if ( I_max < 0 ) {
        sdi_str = "%s"
        sdi = "?"
} else {
        sdi_str = "%.1f"
        sdi = I_max
} 

plot \
     "<echo 0" u (xpos):(ypos(1)):(sprintf("%i bestätigte Fälle in Erfurt", A_max)) w labels left offset 2.5, 0, \
     \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(B_max)) w circle fc rgb "#006000", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(A_max-B_max-C_max)) w circle fc rgb "#007af2", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(C_max)) w circle fc rgb "#000000", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#007af2", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf(A_max - B_max - C_max != 1 ? "%i aktive Fälle (%.1f%%), davon" : "%i aktiver Fall (%.1f%%), davon", A_max - B_max - C_max, 100*(A_max-B_max-C_max)/A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(3)) w p pt 5 ps 4 lc rgb "#006000", \
     "<echo 0" u (xpos):(ypos(3)):(sprintf("%i Genesene (%.1f%%)", B_max, 100*B_max/A_max)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(4)) w p pt 5 ps 4 lc rgb "#000000", \
     "<echo 0" u (xpos):(ypos(4)):(sprintf("%i Verstorbene (%.1f%%)", C_max, 100*C_max/A_max)) w labels left offset 2.5, 0, \
     \
     "<echo 0" u (centerX):(centerY):("7-Tages-\nInzidenz:") w labels center offset 0.0, +1.2, \
     "<echo 0" u (centerX):(centerY):(sprintf(sdi_str, sdi)) w labels font ",24" center offset 0.0, -1.00, \
     \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: Stadt Erfurt") w labels font ", 12" left offset 2.5, 0
