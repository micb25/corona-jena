set terminal pngcairo enhanced background rgb "#f2f2f2" truecolor font "Linux Libertine O,16" size 800, 400 dl 2.0 
set encoding utf8
set minussign

set output '../plotD0_Germany.png'

# pie chart inspired by:
# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

# setup
unset xlabel
unset ylabel
unset key
unset tics
unset border

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1 | xargs date +"%d.%m., %H:%M" -d`")
update_str = "letztes Update: " . date_cmd . " Uhr"

# get sum beds
stats "<awk -F, '{print $2}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1" u 1 prefix "A" nooutput

# get occupied beds
stats "<awk -F, '{print $3}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1" u 1 prefix "B" nooutput

# get free beds
stats "<awk -F, '{print $4}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1" u 1 prefix "C" nooutput

# get number of covid 19 patients
stats "<awk -F, '{print $5}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1" u 1 prefix "E" nooutput

# get number of covid 19 patients with ventilation treatment
stats "<awk -F, '{print $6}' ../data/divi_db_th/divi_data_germany.csv | tail -n 1" u 1 prefix "F" nooutput

diff_c = F_max - F_min

angle(x)=x*360/A_max

centerX=-0.27
centerY=0
radius=0.8

yposmin = 0.0
yposmax = 0.95*radius
xpos = 0.98*radius
ypos(i) = yposmax - i*(yposmax-yposmin)/(4)

set style fill solid 1
set size ratio -1
set xrange [-1.45*radius:3.6*radius]
set yrange [-radius:radius]

pos = 90

filter_inf(x, y)= (y >= 0) ? (x/y) : 0

plot \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(B_max-E_max)) w circle fc rgb "#5c5c5c", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(C_max)) w circle fc rgb "#006000", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(E_max-F_max)) w circle fc rgb "#ff8a1e", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(F_max)) w circle fc rgb "#ff2020", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos - 0.2):(ypos(-0.20)):(sprintf("Intensivbetten in Deutschland: %i", A_max)) w labels left offset 2.5, 0, \
     \
     '+' u (xpos):(ypos(1.20)) w p pt 5 ps 4 lc rgb "#006000", \
     "<echo 0" u (xpos):(ypos(1.20)):(sprintf("%i freie Intensivbetten (%.1f%%)", C_max, 100*C_max/A_max)) w labels left offset 2.5, 0, \
     \
     "<echo 0" u (xpos):(ypos(2.20)):(sprintf("%i belegte Intensivbetten (%.1f%%), davon:", B_max, 100*B_max/A_max)) w labels left offset 2.5, 0, \
     \
     '+' u (xpos + 0.21):(ypos(3.20)) w p pt 5 ps 4 lc rgb "#5c5c5c", \
     "<echo 0" u (xpos + 0.21):(ypos(3.20)):(sprintf("%i sonstige Fälle (%.1f%%)", B_max-E_max, 100*(B_max-E_max)/B_max)) w labels left offset 2.5, 0, \
     \
     '+' u (xpos + 0.21):(ypos(4.20)) w p pt 5 ps 4 lc rgb "#ff2020", \
     "<echo 0" u (xpos + 0.21):(ypos(4.20)):(sprintf("%i beatmete COVID19-Fälle (%.1f%%)", F_max, 100*(F_max)/B_max)) w labels left offset 2.5, 0, \
     \
     '+' u (xpos + 0.21):(ypos(5.20)) w p pt 5 ps 4 lc rgb "#ff8a1e", \
     "<echo 0" u (xpos + 0.21):(ypos(5.20)):(sprintf("%i weitere COVID19-Fälle (%.1f%%)", E_max-F_max, 100*(E_max-F_max)/B_max)) w labels left offset 2.5, 0, \
     \
     "<echo 0" u (xpos-0.21):(ypos(6.30)):("Quelle: DIVI-Intensivregister") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos-0.21):(ypos(7.00)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos-0.21):(ypos(7.70)):("Zahlen basieren auf den eigenständigen Meldungen der Kliniken\nin Deutschland in den vergangenen 60 Stunden.") w labels font ", 12" left offset 2.5, 0
