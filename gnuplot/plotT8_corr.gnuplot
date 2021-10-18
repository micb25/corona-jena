load "template.gnuplot"

set lmargin 10.25
set rmargin 2.95
set tmargin 2.75
set bmargin 3.75

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+7200}' ../data/RKI_TH_Inc_Hosp_Correlation.csv | tail -n 1 | xargs date +"%d.%m." -d`")
update_str = "{/*0.75 (letztes Update: " . date_cmd . "; Quellen: RKI und eigene Berechnung)}"

# x-axis setup
set xlabel '7-Tage-Inzidenz in Altersgruppe' 
set format x '%.0f'
set xrange [0:800]
set xtics out nomirror 
set mxtics 2

# y-axis setup −
set ylabel '7-Tage-Hospitalisierungsinzidenz in Altersgruppe'  #offset -0.5, 0 
set format y '%3.0f'
set yrange [0: 50 < * ]
set ytics out nomirror 
set mytics 2

# set key at graph 0.01, graph 0.88 left Left reverse spacing 1.20 font ",12" width 2.0 samplen 1.5 maxrows 3
set key at graph 0.02, 0.98 left top spacing 1.1 box ls 3

set xtics 100 out nomirror rotate by 0 offset 0, 0 scale 1.2
set mxtics 2

set offsets 0.00, 0.00, graph 0.425, 0.00

#set fit quiet logfile '/dev/null'
set fit errorvariables
set datafile separator ","

h = 10
hosp(x) = h/100 * x

NUM_AGS = 6
age_groups(n) = word("00-04 05-14 15-34 35-59 60-79 80+", n)

fns(n) = word("plotT8_Corr_A plotT8_Corr_B plotT8_Corr_C plotT8_Corr_D plotT8_Corr_E plotT8_Corr_F", n)

set label 3 at graph 0.98, 0.80 update_str right textcolor ls 0

# colorbox
set palette rgb 33,13,10
set cbrange [1585699200:1640995200]
set cbtics ("04/2020" 1585699200, "07/2020" 1593561600, "10/2020" 1601510400, "01/2021" 1609459200, "04/2021" 1617235200, "07/2021" 1625097600, "10/2021" 1633046400, "01/2022" 1640995200)
set colorbox front

do for [i=0:NUM_AGS-1] {
	
	set output sprintf("../%s.png", fns(i+1) )
	
	h = 10
	fit hosp(x) "<awk -F, '{if ($2==\"" . age_groups(i+1) . "\") print $0}' ../data/RKI_TH_Inc_Hosp_Correlation.csv" using ($4):($3) via h

	set label 1 at graph 0.98, 0.95 "Hospitalisierungswahrscheinlichkeit" right textcolor ls 0 
	set label 2 at graph 0.98, 0.88 sprintf("pro Fall: %.2f%% ± %.2f%%", h, h_err) right textcolor ls 0 
	set title sprintf("{/Arial-Bold 7-Tage-Inzidenz und -Hospitalisierungsinzidenz in TH (%s Jahre)}", age_groups(i+1))

	plot  \
	"<awk -F, '{if ($2==\"" . age_groups(i+1) . "\") print $0}' ../data/RKI_TH_Inc_Hosp_Correlation.csv" using ($4):($3):($1) with points pt 7 ps 1 palette title "Daten", \
	hosp(x) ls 5 dt "-" title "linearer Fit"
}
  
