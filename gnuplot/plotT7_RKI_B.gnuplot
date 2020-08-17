load "template.gnuplot"

set output '../plotT7B_RKI_A.png'

# stats for x
stats "<awk -F, '{if (NR>1) print int($1/86400)*86400}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1 nooutput
set xrange [ 1583712000 - 0.5 * 86400 : STATS_max + 0.5 * 86400 ]
set yrange [0:0.1 < * < 100]

# latest update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+7200}' ../data/cases_th_sums.csv | tail -n 1 | xargs date +"%d.%m." -d`")
update_str = "{/*0.75 (letztes Update: " . date_cmd . "; Quelle: Robert Koch-Institut)}"

# x-axis setup
unset xlabel
set xdata time
set timefmt "%s"
set format x "%d.%m."

# y-axis setup
set ylabel 'Fallzahlenverhältnis zur Bevölkerungszahl in Thüringen'
set format y "%.2f%%"

# key
set key at graph 0.02, 0.98 left top spacing 1.1 box ls 3

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlenverhältnis nach Altersgruppe}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 "{/*0.75 in Relation zur Bevölkerungszahl in dieser Altersgruppe}" right textcolor ls 0
set label 3 at graph 0.98, 0.85 update_str right textcolor ls 0

set offsets 0.00, 0.00, graph 0.425, 0.00

plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$3/90338*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$4/181978*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$5/397268*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$6/733338*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$7/560974*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"A\") print $1,$8/169482*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title ">80 Jahre"
  
set output '../plotT7B_RKI_F.png'
  
set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlenverhältnis (w) nach Altersgruppe}" right textcolor ls 0
  
plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$3/44119*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$4/88419*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$5/187832*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$6/353489*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$7/296464*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"F\") print $1,$8/107059*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title ">80 Jahre"
  
set output '../plotT7B_RKI_M.png'
  
set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Fallzahlenverhältnis (m) nach Altersgruppe}" right textcolor ls 0
  
plot  \
  \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$3/46219*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 title "0-4 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$4/93559*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 1 lw 3 dt "-" title "5-14 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$5/209436*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 31 lw 3 title "15-34 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$6/379849*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 32 lw 3 title "35-59 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$7/264510*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 33 lw 3 title "60-79 Jahre", \
  "<awk -F, '{if (NR>1&&$2==\"M\") print $1,$8/62423*100}' ../data/rki_th_by_date/cases_by_day_and_age.csv" using 1:(filter_neg($2)) with lines ls 34 lw 3 title ">80 Jahre"
