set terminal pngcairo enhanced transparent truecolor font "Linux Libertine O,16" size 64, 64 dl 2.0 
set encoding utf8

set output '../icons/pie_chart_mini_%NAME%.png'

# pie chart inspired by:
# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

# setup
unset xlabel
unset ylabel
unset key
unset tics
unset border

# gets sum of infected people
stats "<cat ../data/rki_th/current_cases_by_region.csv | awk -F, '{if ($1==\"%NAME%\") print $3}'" u 1 prefix "A" nooutput

# gets maximum number of recovered people
stats "<cat ../data/rki_th/current_cases_by_region.csv | awk -F, '{if ($1==\"%NAME%\") print $4}'" u 1 prefix "B" nooutput

# gets maximum number of deceased
stats "<cat ../data/rki_th/current_cases_by_region.csv | awk -F, '{if ($1==\"%NAME%\") print $5}'" u 1 prefix "C" nooutput

angle(x)=x*360/A_max

centerX=-0.01
centerY=0
radius=0.8

set lmargin 0.0
set rmargin 0.0
set tmargin 0.0
set bmargin 0.0

set style fill solid 1
set size ratio -1
set xrange [-1.1*radius:1.*1*radius]
set yrange [-1.1*radius:1.*1*radius]

pos = 90

plot \
     1/0 notitle, \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(A_max-B_max-C_max)) w circle fc rgb "#007af2", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(B_max)) w circle fc rgb "#006000", \
     "<echo 0" u (centerX):(centerY):(radius):(pos):(pos=pos+angle(C_max)) w circle fc rgb "#000000"
