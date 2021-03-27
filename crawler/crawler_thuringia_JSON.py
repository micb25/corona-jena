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
            "source": "TMASGFF"
        },
        "caseres" : {
            "id": 3,
            "de": "Fälle / 100&thinsp;000 EW",
            "color": "#0000D3",
            "unit": "Fälle / 100&thinsp;000 EW",
            "source": "TMASGFF"
        },
        "diff": {
            "id": 2,
            "de": "Entwicklung zum Vortag",
            "color": "#A000FFFF",
            "unit": "Fälle",
            "unit1": "Fall",
            "pm" : 1,
            "showSum": 1,
            "source": "TMASGFF"
        },
        "diffweek": {
            "id": 1,
            "de": "Entwicklung zur Vorwoche",
            "color": "#A000FFFF",
            "unit": "Fälle",
            "unit1": "Fall",
            "pm" : 1,
            "showSum": 1,
            "source": "TMASGFF"
        },
        "reldiffweek": {
            "id": 0,
            "de": "7-Tages-Inzidenz",
            "color": "#A000FFFF",
            "unit": "Fälle / 100&thinsp;000 EW",
            "unit1": "Fall / 100&thinsp;000 EW",
            "pm" : 1,
            "source": "eigene Berechnung mit RKI-Rohdaten"
        },
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
            "source": "TMASGFF"
        },
        "deceasedrel": {
            "id": 6,
            "de": "Todesfälle / 100&thinsp;000 EW",
            "color": "#333333",
            "unit": "Verstorbene / 100&thinsp;000 EW",
            "unit1": "Verstorbene(r)",
            "source": "TMASGFF"
        },
        "deceaseddiffweek": {
            "id": 7,
            "de": "Todesfälle (letzte 7 Tage)",
            "color": "#333333",
            "unit": "Verstorbene",
            "unit1": "Verstorbene(r)",
            "showSum": 1,
            "pm" : 1,
            "source": "TMASGFF"
        },
        "cfr": {
            "id": 8,
            "de": "Fallsterblichkeit",
            "color": "#333333",
            "unit": "%",
            "source": "TMASGFF"
        },
        "casedens" : { 
            "id": 9,
            "de": "flächenbezogene Fallzahlen",
            "color": "#0000D3",
            "unit": "Fälle / km²",
            "source": "TMASGFF, statistik.thueringen.de"
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
        with open(data_folder + "cases_thuringia.csv", 'r') as df:
            raw_data = df.read().splitlines()[1:]
            
        for line in raw_data:
            timestamp = int(line.split(",")[0])
            if timestamp not in timestamp_array:
                timestamp_array.append(timestamp)
                
        if len(timestamp_array) > 0:
            timestamp_last = timestamp_array[-1]
            
            for line in raw_data:
                line_data = line.split(",")
                if int(line_data[0]) == timestamp_last:
                    for key in regions:
                        if regions[key]["name"] == line_data[1]:
                            regions[key]["cases"]    = int(line_data[3])
                            regions[key]["diff"]     = int(line_data[2])
                            regions[key]["diffweek"] = int(line_data[3])
                            regions[key]["hospinf"]  = int(line_data[4])
                            regions[key]["severe"]   = int(line_data[5])
                            regions[key]["deceased"] = int(line_data[6])
                            regions[key]["deceaseddiffweek"] = int(line_data[6])
                            regions[key]["casedens"] = regions[key]["cases"] / regions[key]["area"]
                            regions[key]["caseres"] = regions[key]["cases"] / regions[key]["res"]*100000
                            regions[key]["dens"] = regions[key]["res"] / regions[key]["area"]
                            regions[key]["deceasedrel"] = regions[key]["deceased"] / regions[key]["res"]*100000 
                            regions[key]["cfr"] = 100.0* regions[key]["deceased"] / int(line_data[3])
                    
        else:
            return False
        
        for ts in timestamp_array:
            timestamp_delta = (timestamp_last - ts) / 86400
            if ( timestamp_delta >= 6.5 ) and ( timestamp_delta < 7.5 ):
                timestamp_lastweek = ts
                break
            
        if timestamp_lastweek > 0:
            for line in raw_data:
                line_data = line.split(",")
                if int(line_data[0]) == timestamp_lastweek:
                    for key in regions:
                        if regions[key]["name"] == line_data[1]:
                            regions[key]["diffweek"] -= int(line_data[3])
                            regions[key]["deceaseddiffweek"] -= int(line_data[6])
                            
        else:
            for key in regions:
                regions[key]["diffweek"] = 0
                
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
            regions[key]["reldiffweek"] = last_line[col_idx]
            
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
