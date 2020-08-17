load "template.gnuplot"

set output '../plotT7_RKI_A.png'

# stats for x
stats "<awk -F, '{if (NR>1) print int($1/86400)*86400}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1 nooutput
set xrange [ 1583712000 - 0.5 * 86400 : STATS_max + 0.5 * 86400 ]
set yrange [0:50 < * < 100000]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+7200}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m." -d`")
update_str = "{/*0.75 (letztes Update: " . date_cmd . "; Quelle: Robert Koch-Institut)}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Gesamtzahl der Fälle in Thüringen'

# key
set key at graph 0.02, 0.98 left top spacing 1.1 box ls 3

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlen in Thüringen nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

set offsets 0.00, 0.00, graph 0.425, 0.00

plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$3}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$4}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$5}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$6}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$7}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$8}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title "80+ Jahre"
  
set output '../plotT7_RKI_F.png'
  
set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlen (weiblich) nach Altersgruppe}" right textcolor ls 0
  
plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$3}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$4}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$5}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$6}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$7}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$8}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title "80+ Jahre"
  
set output '../plotT7_RKI_M.png'
  
set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlen (männlich) nach Altersgruppe}" right textcolor ls 0
  
plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$3}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$4}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$5}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$6}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$7}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$8}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title "80+ Jahre"
