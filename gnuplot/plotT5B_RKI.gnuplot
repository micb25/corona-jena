load "template.gnuplot"

set output '../plotT5B_RKI.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 (Stand: " . date_cmd . ")}"

# get maximum y value
stats "<awk -F, '{if (NR>1) {a[$10]+=$6; if ($9==\"W\") b[$10]+=$6}}END{for (i in a) print i,a[i]-b[i],b[i]}' ../data/cases_rki_db_th.csv | sort -k 1" using 2 name "M" nooutput
stats "<awk -F, '{if (NR>1) {a[$10]+=$6; if ($9==\"W\") b[$10]+=$6}}END{for (i in a) print i,a[i]-b[i],b[i]}' ../data/cases_rki_db_th.csv | sort -k 1" using 3 name "W" nooutput
ymax = 1.3 * (W_max > M_max ? W_max : M_max)

# get maximum values by gender
stats "<awk -F, '{if ($9==\"M\") s+=$6} END{print s}' ../data/cases_rki_db_th.csv" using 1 name "MM" nooutput
stats "<awk -F, '{if ($9==\"W\") s+=$6} END{print s}' ../data/cases_rki_db_th.csv" using 1 name "WW" nooutput

# x-axis setup
set xrange [-0.5:5.5]
set xtics rotate by 0 offset 0, 0
set xtics ("0-4\nJahre" 0, "5-14\nJahre" 1, "15-34\nJahre" 2, "35-59\nJahre" 3, "60-79\nJahre" 4, "80+\nJahre" 5)

# y-axis setup
set ylabel "bestätigte Coronavirus-Todesfälle in Thüringen"
set yrange [0:ymax]

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

set mytics 1

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Verstorbene nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

M_title = sprintf("Männlich {/*0.75 (insgesamt: %i)}", MM_max)
W_title = sprintf("Weiblich {/*0.75 (insgesamt: %i)}", WW_max)

# data
plot  \
  "<awk -F, 'BEGIN{a[\"A00-A04\"]=0;a[\"A05-A14\"]=0;a[\"A05-A14\"]=0;a[\"A15-A34\"]=0;a[\"A35-A59\"]=0;a[\"A60-A79\"]=0;a[\"A80+\"]=0;}{if (NR>1) {a[$10]+=$6; if ($9==\"W\") b[$10]+=$6}}END{c=0; for (i in a) { c++; print i,c,a[i]-b[i],b[i]}}' ../data/cases_rki_db_th.csv | sort -k 1" using 3 with histograms lt rgb "#72777e" title M_title, \
  "" using 4 with histograms lt rgb "#32373e" title W_title, \
  \
  1/0 lc rgb '#f2f2f2' title "{/*0.75 Quelle: Robert Koch-Institut}"
  
