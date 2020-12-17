set terminal pngcairo enhanced background rgb "#f2f2f2" truecolor font "Linux Libertine O,16" size 800, 400 dl 2.0 
set encoding utf8
set minussign

set output '../plot0_edu_k.png'

set datafile separator ","

# pie chart inspired by:
# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

# setup
unset xlabel
unset ylabel
unset key
unset tics
unset border

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1}' ../data/schools/TH_schools.csv | tail -n 1 | xargs date +"%d.%m.%Y, %H:%M" -d`")
update_str = "letzte Aktualisierung: " . date_cmd . " Uhr"

# Kitas grün
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $3}'" u 1 prefix "A" nooutput

# Kitas gelb
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $4}'" u 1 prefix "B" nooutput

# Kitas rot
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $5}'" u 1 prefix "C" nooutput

# Schulen grün
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $6}'" u 1 prefix "D" nooutput

# Schulen gelb
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $7}'" u 1 prefix "E" nooutput

# Schulen rot
stats "<cat ../data/schools/TH_schools.csv | tail -n 1 | awk -F, '{print $8}'" u 1 prefix "F" nooutput

sum_K = A_max + B_max + C_max
sum_S = D_max + E_max + F_max

angleK(x)=x*360/sum_K - 0.001
angleS(x)=x*360/sum_S - 0.001

centerX=-0.20
centerY=0
radius=0.8

yposmin = 0.0
yposmax = 0.95*radius
xpos = 1.25*radius
ypos(i) = yposmax - i*(yposmax-yposmin)/(4)

set style fill solid 1
set size ratio -1
set xrange [-1.45*radius:3.6*radius]
set yrange [-radius:radius]

pos = 90

plot \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(A_max)) w circle fc rgb "#06470c", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(B_max)) w circle fc rgb "#fec615", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(C_max)) w circle fc rgb "#e50000", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos - 0.23):(ypos(0.6)):(sprintf("aktuelle Situation in Thüringer Kitas")) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#e50000", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf(C_max != 1 ? "Stufe ROT: %i Kitas (%.1f%%)" : "Stufe ROT: %i Kita (%.1f%%)", C_max, 100*(C_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(3.5)) w p pt 5 ps 4 lc rgb "#fec615", \
     "<echo 0" u (xpos):(ypos(3.5)):(sprintf(B_max != 1 ? "Stufe GELB: %i Kitas (%.1f%%)" : "Stufe GELB: %i Kita (%.1f%%)", B_max, 100*(B_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5)) w p pt 5 ps 4 lc rgb "#06470c", \
     "<echo 0" u (xpos):(ypos(5)):(sprintf(A_max != 1 ? "Stufe GRÜN: %i Kitas (%.1f%%)" : "Stufe GRÜN: %i Kita (%.1f%%)", A_max, 100*(A_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: TMBJS") w labels font ", 12" left offset 2.5, 0

     
set output '../plot0_edu_s.png'

pos = 90

plot \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(D_max)) w circle fc rgb "#06470c", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(E_max)) w circle fc rgb "#fec615", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(F_max)) w circle fc rgb "#e50000", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos - 0.23):(ypos(0.6)):(sprintf("aktuelle Situation in Thüringer Schulen")) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#e50000", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf(C_max != 1 ? "Stufe ROT: %i Schulen (%.1f%%)" : "Stufe ROT: %i Schule (%.1f%%)", F_max, 100*(F_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(3.5)) w p pt 5 ps 4 lc rgb "#fec615", \
     "<echo 0" u (xpos):(ypos(3.5)):(sprintf(B_max != 1 ? "Stufe GELB: %i Schulen (%.1f%%)" : "Stufe GELB: %i Schule (%.1f%%)", E_max, 100*(E_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5)) w p pt 5 ps 4 lc rgb "#06470c", \
     "<echo 0" u (xpos):(ypos(5)):(sprintf(A_max != 1 ? "Stufe GRÜN: %i Schulen (%.1f%%)" : "Stufe GRÜN: %i Schule (%.1f%%)", D_max, 100*(D_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: TMBJS") w labels font ", 12" left offset 2.5, 0
     
set terminal pngcairo enhanced background rgb "#f2f2f2" truecolor font "Linux Libertine O,16" size 800, 600 dl 2.0 
set output '../plot0_edu.png'
set multiplot layout 2, 1

pos = 90

plot \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(A_max)) w circle fc rgb "#06470c", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(B_max)) w circle fc rgb "#fec615", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleK(C_max)) w circle fc rgb "#e50000", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos - 0.23):(ypos(0.6)):(sprintf("aktuelle Situation in Thüringer Kitas")) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#e50000", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf(C_max != 1 ? "Stufe ROT: %i Kitas (%.1f%%)" : "Stufe ROT: %i Kita (%.1f%%)", C_max, 100*(C_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(3.5)) w p pt 5 ps 4 lc rgb "#fec615", \
     "<echo 0" u (xpos):(ypos(3.5)):(sprintf(B_max != 1 ? "Stufe GELB: %i Kitas (%.1f%%)" : "Stufe GELB: %i Kita (%.1f%%)", B_max, 100*(B_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5)) w p pt 5 ps 4 lc rgb "#06470c", \
     "<echo 0" u (xpos):(ypos(5)):(sprintf(A_max != 1 ? "Stufe GRÜN: %i Kitas (%.1f%%)" : "Stufe GRÜN: %i Kita (%.1f%%)", A_max, 100*(A_max)/sum_K)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: TMBJS") w labels font ", 12" left offset 2.5, 0

pos = 90

plot \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(D_max)) w circle fc rgb "#06470c", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(E_max)) w circle fc rgb "#fec615", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angleS(F_max)) w circle fc rgb "#e50000", \
     "<echo 0" u (centerX):(centerY):(radius/2.2) w circle fc rgb "#f2f2f2", \
     \
     "<echo 0" u (xpos - 0.23):(ypos(0.6)):(sprintf("aktuelle Situation in Thüringer Schulen")) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(2)) w p pt 5 ps 4 lc rgb "#e50000", \
     "<echo 0" u (xpos):(ypos(2)):(sprintf(C_max != 1 ? "Stufe ROT: %i Schulen (%.1f%%)" : "Stufe ROT: %i Schule (%.1f%%)", F_max, 100*(F_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(3.5)) w p pt 5 ps 4 lc rgb "#fec615", \
     "<echo 0" u (xpos):(ypos(3.5)):(sprintf(B_max != 1 ? "Stufe GELB: %i Schulen (%.1f%%)" : "Stufe GELB: %i Schule (%.1f%%)", E_max, 100*(E_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5)) w p pt 5 ps 4 lc rgb "#06470c", \
     "<echo 0" u (xpos):(ypos(5)):(sprintf(A_max != 1 ? "Stufe GRÜN: %i Schulen (%.1f%%)" : "Stufe GRÜN: %i Schule (%.1f%%)", D_max, 100*(D_max)/sum_S)) w labels left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(5.5)):(" ") w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(6.5)):(update_str) w labels font ", 12" left offset 2.5, 0, \
     "<echo 0" u (xpos):(ypos(7.5)):("Quelle: TMBJS") w labels font ", 12" left offset 2.5, 0
     
