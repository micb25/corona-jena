#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json


def readTHdata(data_folder):
    
    timestamp_array    = []
    timestamp_last     = -1
    timestamp_lastweek = -1
    
    regions = {
        "ABG": { "name": "Altenburger Land", "res": 90118, "area": 569.40 },
        "EIC": { "name": "Eichsfeld", "res": 100380, "area": 943.07 },
        "EA":  { "name": "Eisenach", "res": 42370, "area": 104.17 },
        "EF":  { "name": "Erfurt", "res": 213699, "area": 269.91 },
        "G":   { "name": "Gera", "res": 94152, "area": 152.18 },
        "GTH": { "name": "Gotha", "res": 135452, "area": 936.08 },
        "GRZ": { "name": "Greiz", "res": 98159, "area": 845.98 },
        "HBN": { "name": "Hildburghausen", "res": 63553, "area": 938.42 },
        "IK":  { "name": "Ilm-Kreis", "res": 108742, "area": 843.71 },
        "J":   { "name": "Jena", "res": 111407, "area": 114.77 },
        "KYF": { "name": "Kyffhäuserkreis", "res": 75009, "area": 1037.91 },
        "NDH": { "name": "Nordhausen", "res": 83822, "area": 713.90 },
        "SHK": { "name": "Saale-Holzland-Kreis", "res": 83051, "area": 815.24 },
        "SOK": { "name": "Saale-Orla-Kreis", "res": 80868, "area": 1151.30 },
        "SLF": { "name": "Saalfeld-Rudolstadt", "res": 106356, "area": 1036.03 },
        "SM":  { "name": "Schmalkalden-Meiningen", "res": 122347, "area": 1210.73 },
        "SOM": { "name": "Sömmerda", "res": 69655, "area": 806.86 },
        "SON": { "name": "Sonneberg", "res": 56196, "area": 433.61 },
        "SHL": { "name": "Suhl", "res": 34835, "area": 103.03 },
        "UH":  { "name": "Unstrut-Hainich-Kreis", "res": 102912, "area": 979.69 },
        "WAK": { "name": "Wartburgkreis", "res": 123025, "area": 1307.44 },
        "WE":  { "name": "Weimar", "res": 65090, "area": 84.48 },
        "AP":  { "name": "Weimarer Land", "res": 81947, "area": 804.48 }
    }

    types = {
        "cases": {
            "id": 4,
            "de": "Fallzahlen (Summe)",
            "color": "#0000d3",
            "unit": "Fälle",
            "unit1": "Fall",
            "showSum": 1,
            "source": "RKI"
        },
        "caseres" : {
            "id": 3,
            "de": "Fälle / 100&thinsp;000 EW",
            "color": "#0000D3",
            "unit": "Fälle / 100&thinsp;000 EW",
            "source": "RKI"
        },
        "diff": {
            "id": 2,
            "de": "Entwicklung zum Vortag",
            "color": "#A000FFFF",
            "unit": "Neuinfektionen",
            "unit1": "Neuinfektion",
            "pm" : 1,
            "showSum": 1,
            "source": "RKI"
        },
        "diffweek": {
            "id": 1,
            "de": "Entwicklung zur Vorwoche",
            "color": "#A000FFFF",
            "unit": "Neuinfektionen",
            "unit1": "Neuinfektion",
            "pm" : 1,
            "showSum": 1,
            "source": "RKI; eigene Berechnung"
        },
        "incidence": {
            "id": 0,
            "de": "7-Tages-Inzidenz",
            "color": "#A000FFFF",
            "unit": "Fälle / 100&thinsp;000 EW",
            "unit1": "Fall / 100&thinsp;000 EW",
            "source": "RKI; eigene Berechnung"
        },
        #"active": {
        #    "id": 1,
        #    "de": "aktive Fälle",
        #    "color": "#0000d3",
        #    "unit": "aktive Fälle",
        #    "unit1": "aktiver Fall",
        #    "showSum": 1,
        #    "source": "RKI; eigene Berechnung"
        #},
        #"hospinf": {
        #    "id": 5,
        #    "de": "stationäre Fälle mit COVID-19",
        #    "color": "#FF891D",
        #    "unit": "Fälle",
        #    "unit1": "Fall",
        #    "showSum": 1,
        #    "source": "TMASGFF"
        #},
        #"severe": {
        #    "id": 6,
        #    "de": "schwere Verläufe",
        #    "color": "#D30000",
        #    "unit": "Fälle",
        #    "unit1": "Fall",
        #    "showSum": 1,
        #    "source": "TMASGFF"
        #},
        "deceased": {
            "id": 5,
            "de": "Todesfälle (Summe)",
            "color": "#333333",
            "unit": "Verstorbene",
            "unit1": "Verstorbene(r)",
            "showSum": 1,
            "source": "RKI"
        },
        "deceasedrel": {
            "id": 6,
            "de": "Todesfälle / 100&thinsp;000 EW",
            "color": "#333333",
            "unit": "Verstorbene / 100&thinsp;000 EW",
            "unit1": "Verstorbene(r)",
            "source": "RKI; eigene Berechnung"
        },
        "deceaseddiffweek": {
            "id": 7,
            "de": "Todesfälle (letzte 7 Tage)",
            "color": "#333333",
            "unit": "Verstorbene",
            "unit1": "Verstorbene(r)",
            "showSum": 1,
            "pm" : 1,
            "source": "RKI; eigene Berechnung"
        },
        "cfr": {
            "id": 8,
            "de": "Fallsterblichkeit",
            "color": "#333333",
            "unit": "%",
            "source": "RKI; eigene Berechnung"
        },
        "casedens" : { 
            "id": 9,
            "de": "flächenbezogene Fallzahlen",
            "color": "#0000D3",
            "unit": "Fälle / km²",
            "source": "RKI, statistik.thueringen.de"
        },
        "res" : {
            "id": 10,
            "de": 'Einwohner',
            "color": '#00A000',
            "unit": 'EW',
            "showSum": 1,
            "source": "statistik.thueringen.de"
        },
        "area" : {
            "id": 11,
            "de": 'Fläche',
            "color": '#00A000',
            "unit": 'km²',
            "showSum": 1,
            "source": "statistik.thueringen.de"
        },
        "dens" : {
            "id": 12,
            "de": 'Einwohnerdichte',
            "color": '#00A000',
            "unit": 'EW / km²',
            "source": "statistik.thueringen.de"
        }
    }
    
    try:                        
        # 7-day incidence (RKI data)
        with open(data_folder + "cases_rki_7day_incidence.csv", "r") as df:
            rawdata = df.read().splitlines()
            
        columns = rawdata[0].split(",")[2:]
        last_line = rawdata[-1].split(",")[2:]
        
        # convert to float
        for i, entry in enumerate(last_line):
            last_line[i] = float(entry)
        
        for key in regions:
            col_idx = columns.index(key)
            regions[key]["incidence"] = last_line[col_idx]
            
            
        # RKI data
        with open(data_folder + "rki_th_by_date/cases_by_day_and_region.csv", "r") as df:
            rawdata = df.read().splitlines()[-192:]
            
        th_data = []
        for line in rawdata:
            line_data = line.split(",")
            for i, e in enumerate(line_data):
                if i != 1:
                    line_data[i] = int(e)
                    
            th_data.append( line_data )
        
        cases_total = [th_data[i][1:5] for i in range(168, len(th_data))]
        cases_yesterday = [th_data[i][1:5] for i in range(144, 168)]
        cases_week_ago = [th_data[i][1:5] for i in range(0, 24)]
        
        for i, [key, cases, recovered, deceased] in enumerate(cases_total):
            if key != 'TH':
                regions[key]["dens"] = regions[key]["res"] / regions[key]["area"]
                regions[key]["cases"] = cases
                # regions[key]["active"] = cases - recovered - deceased
                regions[key]["casedens"] = cases / regions[key]["area"]
                regions[key]["caseres"] = cases / regions[key]["res"]*100000
                regions[key]["deceased"] = deceased
                regions[key]["deceasedrel"] = deceased / regions[key]["res"]*100000
                regions[key]["cfr"] = 100.0 * deceased / cases
                
                regions[key]["diff"] = cases - cases_yesterday[i][1]
                regions[key]["diffweek"] = cases - cases_week_ago[i][1]
                regions[key]["deceaseddiffweek"] = deceased - cases_week_ago[i][3]
        
        timestamp_last = th_data[-1][0]
        
    except:
        return False
    
    resultArray = {
        "ts" : timestamp_last,
        "types": types,
        "values": regions
    }
        
    return resultArray


if __name__ == "__main__":
    
    ###########################################################################
    # Filenames
    ###########################################################################

    DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../data/"
       
    JSON_FILE = DATA_FOLDER + "cases_thuringia.json"
    
    data = readTHdata(DATA_FOLDER)
    
    if data != False:
        f = open(JSON_FILE, 'w')
        f.write( json.dumps( data ) ) 
        f.close()
