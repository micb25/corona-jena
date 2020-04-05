#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    DATAFILE = SCRIPTPATH + "/../data/cases_thuringia.csv"
    DATFILE  = SCRIPTPATH + "/th_dens_vs_cases.dat"
    GPFILE   = SCRIPTPATH + "/plotT1_pop_dens.gnuplot"
    
    replace_array  = {
        "Altenburger Land": "ABG",
        "Eichsfeld": "EIC",
        "Eisenach": "EA",
        "Erfurt": "EF",
        "Gera": "G",
        "Gotha": "GTH",
        "Greiz": "GRZ",
        "Hildburghausen": "HBN",
        "Ilm-Kreis": "IK",
        "Jena": "J",
        "Kyffhäuserkreis": "KYF",
        "Nordhausen": "NDH",
        "Saale-Holzland-Kreis": "SHK",
        "Saale-Orla-Kreis": "SOK",
        "Saalfeld-Rudolstadt": "SLF",
        "Schmalkalden-Meiningen": "SM",
        "Sömmerda": "SÖM",
        "Sonneberg": "SON",
        "Suhl": "SHL",
        "Unstrut-Hainich-Kreis": "UH",
        "Wartburgkreis": "WAK",
        "Weimar": "WE",
        "Weimarer Land": "AP"
    }
   
    # density per city/county; values taken from:
    # https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=GG000101%7C%7C
    area_array  = {
        "Altenburger Land": 90118.0 / 569.40,
        "Eichsfeld":  100380.0 / 943.07,
        "Eisenach": 42370.0 / 104.17,
        "Erfurt":  213699.0 / 269.91,
        "Gera": 94152.0 / 152.18,
        "Gotha":  135452.0 / 936.08,
        "Greiz": 98159.0 / 845.98,
        "Hildburghausen": 63553.0 / 938.42,
        "Ilm-Kreis":  108742.0 / 843.71,
        "Jena": 111407.0 / 114.77,
        "Kyffhäuserkreis": 75009.0 / 1037.91,
        "Nordhausen": 83822.0 / 713.90,
        "Saale-Holzland-Kreis": 83051.0 / 815.24,
        "Saale-Orla-Kreis": 80868.0 / 1151.30,
        "Saalfeld-Rudolstadt":  106356.0 / 1036.03,
        "Schmalkalden-Meiningen": 122347.0 / 1210.73,
        "Sömmerda": 69655.0 / 806.86,
        "Sonneberg": 56196.0 / 433.61,
        "Suhl": 34835.0 / 103.03,
        "Unstrut-Hainich-Kreis":  102912.0 / 979.69,
        "Wartburgkreis": 123025.0 / 1307.44,
        "Weimar": 65090.0 / 84.48,
        "Weimarer Land": 81947.0 / 804.48
    }
    
    cities = ["Eisenach", "Erfurt", "Gera", "Jena", "Suhl", "Weimar"]
        
    try:
        
        # read data file
        with open(DATAFILE, "r") as df:
            rawdata = df.read().splitlines()

        # get latest timestamp
        timestamp = int(rawdata[-1].split(",")[0])
        
        # generate and write data
        with open(DATFILE, "w") as dat:
            for l in rawdata:
                ds = l.split(",")
                if ( len(ds) == 8 ):
                    if ( int(ds[0]) == timestamp ):
                        dat.write("%s,%s,%i,%.3f,%i\n" % (ds[1], replace_array[ds[1]], 1 if ds[1] in cities else 0, float(area_array[ds[1]]), float(ds[3])) )
            
            dat.close()            

        # create diagram
        os.system( "gnuplot {} > /dev/null".format( GPFILE ) )
        
    except:
        print("Error occured!")
