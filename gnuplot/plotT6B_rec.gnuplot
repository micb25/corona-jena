load "template_weekly.gnuplot"

set output '../plotT6B_rec.png'

# get last update
date_cmd = sprintf("%s", "`awk -F, '{print "@"$1+86400}' ../data/cases_rki_db_th.csv | tail -n 1 | xargs date +"%d.%m.%Y" -d`")
update_str = "{/*0.75 Stand: " . date_cmd . "; Quelle: TMASGFF}"

set label 1 at graph 0.98, 0.95 "{/Linux-Libertine-O-Bold Genesungen pro Kalenderwoche in Thüringen}" right textcolor ls 0
set label 2 at graph 0.98, 0.90 update_str right textcolor ls 0

# data
plot  \
  "<awk -F, 'BEGIN{d=0;w=0;tmin=1584316800}{if((NR>1)&&($1>=1584316800)){if ($1<=tmin+7*86400){w+=$3-d;d=$3;}else{print tmin,w;tmin=tmin+7*86400;w=0;}}}END{if (w>0) print tmin, w}' ../data/cases_th_sums.csv" using (fakeweeknum($1)):($2) with boxes lt rgb "#006000" notitle
  
