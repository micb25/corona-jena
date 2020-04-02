#!/bin/bash

rm cases_erfurt.csv
curl -O https://www.michael-böhme.de/corona/data/cases_erfurt.csv

rm cases_gera.dat
curl -O https://www.michael-böhme.de/corona/data/cases_gera.dat

rm cases_jena.dat
curl -O https://www.michael-böhme.de/corona/data/cases_jena.dat

rm cases_thuringia.dat
curl -O https://www.michael-böhme.de/corona/data/cases_thuringia.dat

rm cases_thuringia_recovered.dat
curl -O https://www.michael-böhme.de/corona/data/cases_thuringia_recovered.dat

rm cases_thuringia_rki.dat
curl -O https://www.michael-böhme.de/corona/data/cases_thuringia_rki.dat

rm cases_weimar.dat
curl -O https://www.michael-böhme.de/corona/data/cases_weimar.dat

