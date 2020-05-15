#!/bin/bash

rm cases_abg.csv
curl -O https://www.michael-böhme.de/corona/data/cases_abg.csv

rm cases_ea.csv
curl -O https://www.michael-böhme.de/corona/data/cases_ea.csv

rm cases_eic.csv
curl -O https://www.michael-böhme.de/corona/data/cases_eic.csv

rm cases_erfurt.csv
curl -O https://www.michael-böhme.de/corona/data/cases_erfurt.csv

rm cases_gera.csv
curl -O https://www.michael-böhme.de/corona/data/cases_gera.csv

rm cases_grz.csv
curl -O https://www.michael-böhme.de/corona/data/cases_grz.csv

rm cases_hbn.csv
curl -O https://www.michael-böhme.de/corona/data/cases_hbn.csv

rm cases_jena_opendata.csv
curl -O https://www.michael-böhme.de/corona/data/cases_jena_opendata.csv

rm cases_ndh.csv
curl -O https://www.michael-böhme.de/corona/data/cases_ndh.csv

rm cases_rki_db_th.csv
curl -O https://www.michael-böhme.de/corona/data/cases_rki_db_th.csv

rm cases_shk.csv
curl -O https://www.michael-böhme.de/corona/data/cases_shk.csv

rm cases_sok.csv
curl -O https://www.michael-böhme.de/corona/data/cases_sok.csv

rm cases_som.csv
curl -O https://www.michael-böhme.de/corona/data/cases_som.csv

rm cases_son.csv
curl -O https://www.michael-böhme.de/corona/data/cases_son.csv

rm cases_thuringia.csv
curl -O https://www.michael-böhme.de/corona/data/cases_thuringia.csv

rm cases_th_rki_sums.csv
curl -O https://www.michael-böhme.de/corona/data/cases_th_rki_sums.csv

rm cases_th_sums.csv
curl -O https://www.michael-böhme.de/corona/data/cases_th_sums.csv

rm cases_germany_total_rki.csv
curl -O https://www.michael-böhme.de/corona/data/cases_germany_total_rki.csv

rm cases_thuringia_rki.csv
curl -O https://www.michael-böhme.de/corona/data/cases_thuringia_rki.csv

rm cases_uh.csv
curl -O https://www.michael-böhme.de/corona/data/cases_uh.csv

rm cases_weimar.csv
curl -O https://www.michael-böhme.de/corona/data/cases_weimar.csv

rm cases_wak.csv
curl -O https://www.michael-böhme.de/corona/data/cases_wak.csv


cd divi_db_th

rm divi_data_germany.csv
curl -O https://www.michael-böhme.de/corona/data/divi_db_th/divi_data_germany.csv

rm divi_data_th.csv
curl -O https://www.michael-böhme.de/corona/data/divi_db_th/divi_data_th.csv

cd ..


cd rki_th

rm cases_by_date.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/cases_by_date.csv

rm current_cases_by_region.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/current_cases_by_region.csv

rm current_cases_by_region.json
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/current_cases_by_region.json

rm reproduction_rates_th.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/reproduction_rates_th.csv

rm total_active_cases_by_age.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_active_cases_by_age.csv

rm total_active_cases_by_age.json
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_active_cases_by_age.json

rm total_cases_by_age.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_cases_by_age.csv

rm total_cases_by_age.json
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_cases_by_age.json

rm total_cfr_by_age.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_cfr_by_age.csv

rm total_deceased_by_age.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_deceased_by_age.csv

rm total_deceased_by_age.json
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_deceased_by_age.json

rm total_recovered_by_age.csv
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_recovered_by_age.csv

rm total_recovered_by_age.json
curl -O https://www.xn--michael-bhme-djb.de/corona/data/rki_th/total_recovered_by_age.json

cd ..
