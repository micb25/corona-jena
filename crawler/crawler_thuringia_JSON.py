#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os, json

DATAFILE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_thuringia.json"

def strToTimestamp(datetimestr):    
    s = datetimestr.replace("Uhr", "").strip()
    
    # fix for dates, since 25.03.
    if re.search(",", s) is None:
        s += ", 10"
            
    months = {"Januar": "1", "Februar": "2", "März": "3", "April": "4", "Mai": "5", "Juni": "6", "Juli": "7", "August": "8", "September": "9", "Oktober": "10", "November": "11", "Dezember": "12" }    
    for key in months.keys():
        s = s.replace(key, months[key])
            
    try:    
        struct_time = time.strptime(s, "%d. %m %Y, %H")
        return int(time.mktime(struct_time))
    except:
        return False

def writeAsJSON( pd, num_patterns ):
    global DATAFILE_JSON
    
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
            "id": 0,
            "de": "Fallzahlen",
            "color": "#0000d3",
            "unit": "Fälle",
            "unit1": "Fall",
            "showSum": 1
        },
        "diff": {
            "id": 1,
            "de": "Entwicklung zum Vortag",
            "color": "#A000FFFF",
            "unit": "Fälle",
            "unit1": "Fall",
            "pm" : 1,
            "showSum": 1
        },
        "diffweek": {
            "id": 2,
            "de": "Entwicklung zur Vorwoche",
            "color": "#A000FFFF",
            "unit": "Fälle",
            "unit1": "Fall",
            "pm" : 1,
            "showSum": 1
        },
        "reldiffweek": {
            "id": 3,
            "de": "rel. Entwicklung zur Vorwoche",
            "color": "#A000FFFF",
            "unit": "Fälle / 100&thinsp;000 EW",
            "unit1": "Fall / 100&thinsp;000 EW",
            "pm" : 1
        },
        "hospinf": {
            "id": 4,
            "de": "stationäre Fälle mit COVID19",
            "color": "#EBE800",
            "unit": "Fälle",
            "unit1": "Fall",
            "showSum": 1
        },
        "hosp": {
            "id": 5,
            "de": "stationäre Fälle wegen COVID19",
            "color": "#FFAD00",
            "unit": "Fälle",
            "unit1": "Fall",
            "showSum": 1
        },
        "severe": {
            "id": 6,
            "de": "schwere Verläufe",
            "color": "#D30000",
            "unit": "Fälle",
            "unit1": "Fall",
            "showSum": 1
        },
        "deceased": {
            "id": 7,
            "de": "Todesfälle",
            "color": "#333333",
            "unit": "Verstorbene",
            "unit1": "Verstorbene(r)",
            "showSum": 1
        },
        "caseres" : {
            "id": 8,
            "de": 'relative Fallzahlen',
            "color": '#0000D3',
            "unit": 'Fälle / 100&thinsp;000 EW'
        },
        "casedens" : { 
            "id": 9,
            "de": 'flächenbezogene Fälle',
            "color": '#0000D3',
            "unit": 'Fälle / km²'
        },
        "res" : {
            "id": 10,
            "de": 'Einwohner',
            "color": '#00A000',
            "unit": 'EW',
            "showSum": 1
        },
        "area" : {
            "id": 11,
            "de": 'Fläche',
            "color": '#00A000',
            "unit": 'km²',
            "showSum": 1
        },
        "dens" : {
            "id": 12,
            "de": 'Einwohnerdichte',
            "color": '#00A000',
            "unit": 'EW / km²'
        }
    }
        


    p = pd
    if True:
        dt = strToTimestamp(p[0])
                        
        if dt is not False:            
            # get numbers one week ago
            last_week = dt - 7 * 86400
            DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_thuringia.csv"    
            with open(DATAFILE, 'r') as df:
                raw_data = df.read().splitlines()
                
            for line in raw_data:
                cols = line.split(",")
                if ( int(cols[0]) == last_week ):
                    for key in regions:
                        if ( regions[key]["name"] == cols[1] ):
                            regions[key]["diffweek"]  = -int(cols[3])
            
            ps = num_patterns[1].findall( p[1].replace("&nbsp;", "0") )
            for d in ps:
                for key in regions:
                    if ( regions[key]["name"] == d[0] ):
                        regions[key]["cases"] = int(d[2])
                        regions[key]["diff"]  = int(d[3])
                        regions[key]["diffweek"] += int(d[2])
                        regions[key]["hospinf"]  = int(d[4])
                        regions[key]["hosp"]  = int(d[5])
                        regions[key]["severe"]  = int(d[6])
                        regions[key]["deceased"] = int(d[7])
                        regions[key]["casedens"] = regions[key]["cases"] / regions[key]["area"]
                        regions[key]["caseres"] = regions[key]["cases"] / regions[key]["res"]*100000
                        regions[key]["reldiffweek"] = regions[key]["diffweek"] / regions[key]["res"]*100000
                        regions[key]["dens"] = regions[key]["res"] / regions[key]["area"]
    
    resultArray = {
        "ts" : dt,
        "types": types,
        "values": regions
    }
    
    f = open(DATAFILE_JSON, 'w')
    f.write( json.dumps( resultArray ) ) 
    f.close()
    return True

def parseNumbers():
    url          = "https://www.landesregierung-thueringen.de/corona-bulletin"
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }

    date_pattern = re.compile(r"(?:<strong>)?.*?\s\(Stand: (.*?)\)(?:<\/strong>)?.*?\<table.*?\<\/table\>.*?<table.*?\<tbody\>(.*?)\<\/tbody\>")
    num_pattern0 = re.compile(r"\<tr\>\<th scope=\"row\">([A-Za-z\s\-äöüÄÖÜ]{1,})\<\/th\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\><\/tr\>") # 
    # new layout, since 21.03.2020
    num_pattern1 = re.compile(r"\<tr\>\<th scope=\"row\">([A-Za-z\s\-äöüÄÖÜ]{1,})\<\/th\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>(?:[\-0,-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\><\/tr\>") # 
    num_patterns = [ num_pattern0, num_pattern1 ]
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        pd = date_pattern.findall( r.text.replace("\n", "").replace("\r", "").replace("<p>", "").replace("</p>", "") )
        
        writeAsJSON( pd[0], num_patterns )
        
    except:
        return False


if __name__ == "__main__":

    parseNumbers()
