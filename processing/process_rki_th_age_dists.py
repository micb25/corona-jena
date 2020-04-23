#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv, json, time, re

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

def writeTotalCSV( valueType ) :
    global gender
    global ages
    global regions

    with open('../data/rki_th/total_' + valueType + '.csv', 'w', newline='') as csvfile:
        fieldnames = []
        fieldnames.append( 'region' )
        for ageKey in ages:
                for genderKey in gender:
                    fieldnames.append( genderKey + '_' + ageKey )
            #fieldnames.append( 'T_' + ageKey )

        datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(fieldnames)
        
        # fixes the key order in old Python 3 versions
        sorted_keys = sorted(regions.keys())
        sorted_keys.remove("TH")
        sorted_keys.append("TH")
        
        for regionKey in sorted_keys:
            row = []
            row.append( regionKey )
            for ageKey in ages:
                for genderKey in gender:
                    if isinstance(regions[regionKey][genderKey + ageKey][valueType], float):
                        row.append( "{:.2f}".format(regions[regionKey][genderKey + ageKey][valueType]) )
                    else:
                        row.append( regions[regionKey][genderKey + ageKey][valueType] )
            datawriter.writerow(row)

def writeTotalJSON( valueType, dt ) :
    global types
    global regions
    values = {}
    for regionKey in regions:
        if regionKey != "TH":
            values[regionKey] = {} 
            for genderKey in gender:
                for ageKey in ages:
                    values[regionKey][genderKey + ageKey] = regions[regionKey][genderKey + ageKey][valueType]

    resultArray = {
        "ts" : dt,
        "types": types,
        "values": values
    }

    f = open('../data/rki_th/total_' + valueType + '.json', 'w')
    f.write( json.dumps( resultArray ) ) 
    f.close()
    return True

def writeCSVThuringia(cases_total, cases_dec):
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_thuringia_rki.csv"
    URL = "cases_thuringia_rki.csv"
    num_latest = (cases_total, cases_dec)
    
    # get old values
    with open(DATAFILE, 'r') as df:
        raw_data = df.read().splitlines()
    last_values = raw_data[-1].split(",")[1:2]
    
    # check for changes
    value_changed = False        
    for i in enumerate(last_values):
        if ( int(i[1]) != num_latest[i[0]] ):
            if ( num_latest[i[0]] != -1 ):
                value_changed = True
                
    if value_changed:
        # write new csv data
        f = open(DATAFILE, 'a')
        f.write("%i,%i,%i,%s\n" % (int(time.time()), num_latest[0], num_latest[1], URL))
        f.close()

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    gender = ( "W", "M" )

    ages = (
        "A00-A04",
        "A05-A14",
        "A15-A34",
        "A35-A59",
        "A60-A79",
        "A80+"
    )    

    regions = {
        "ABG": { "t": "L", "name": "Altenburger Land", "res": 90118, "area": 569.40 },
        "EIC": { "t": "L", "name": "Eichsfeld", "res": 100380, "area": 943.07 },
        "EA":  { "t": "S", "name": "Eisenach", "res": 42370, "area": 104.17 },
        "EF":  { "t": "S", "name": "Erfurt", "res": 213699, "area": 269.91 },
        "G":   { "t": "S", "name": "Gera", "res": 94152, "area": 152.18 },
        "GTH": { "t": "L", "name": "Gotha", "res": 135452, "area": 936.08 },
        "GRZ": { "t": "L", "name": "Greiz", "res": 98159, "area": 845.98 },
        "HBN": { "t": "L", "name": "Hildburghausen", "res": 63553, "area": 938.42 },
        "IK":  { "t": "L", "name": "Ilm-Kreis", "res": 108742, "area": 843.71 },
        "J":   { "t": "S", "name": "Jena", "res": 111407, "area": 114.77 },
        "KYF": { "t": "L", "name": "Kyffhäuserkreis", "res": 75009, "area": 1037.91 },
        "NDH": { "t": "L", "name": "Nordhausen", "res": 83822, "area": 713.90 },
        "SHK": { "t": "L", "name": "Saale-Holzland-Kreis", "res": 83051, "area": 815.24 },
        "SOK": { "t": "L", "name": "Saale-Orla-Kreis", "res": 80868, "area": 1151.30 },
        "SLF": { "t": "L", "name": "Saalfeld-Rudolstadt", "res": 106356, "area": 1036.03 },
        "SM":  { "t": "L", "name": "Schmalkalden-Meiningen", "res": 122347, "area": 1210.73 },
        "SOM": { "t": "L", "name": "Sömmerda", "res": 69655, "area": 806.86 },
        "SON": { "t": "L", "name": "Sonneberg", "res": 56196, "area": 433.61 },
        "SHL": { "t": "S", "name": "Suhl", "res": 34835, "area": 103.03 },
        "UH":  { "t": "L", "name": "Unstrut-Hainich-Kreis", "res": 102912, "area": 979.69 },
        "WAK": { "t": "L", "name": "Wartburgkreis", "res": 123025, "area": 1307.44 },
        "WE":  { "t": "S", "name": "Weimar", "res": 65090, "area": 84.48 },
        "AP":  { "t": "L", "name": "Weimarer Land", "res": 81947, "area": 804.48 },
        "TH":  { "t": "-", "name": "Thüringen" }
    }

    types = {}
    i = 0
    for genderKey in gender:
        for ageKey in ages:
            types[genderKey + ageKey] = {}
            types[genderKey + ageKey]["id"] = i
            types[genderKey + ageKey]["de"] = genderKey + ': ' + ageKey
            types[genderKey + ageKey]["color"] = "#0000d3"
            types[genderKey + ageKey]["unit"] = "Fälle"
            types[genderKey + ageKey]["unit1"] = "Fall"
            types[genderKey + ageKey]["showSum"] = 1
            i = i + 1
            

    # prepare result array
    for regionKey in regions:
        for genderKey in gender:
            for ageKey in ages:
                regions[regionKey][genderKey + ageKey] = { 'cases_by_age': 0, 'deceased_by_age': 0, 'recovered_by_age': 0, 'active_cases_by_age': 0, 'cfr_by_age': 0 }
    
    # fill result array, count cases and casulties
    lines = 0
    cases = 0
    death = 0
    recovered = 0
    with open('../data/cases_rki_db_th.csv', newline='', encoding="utf8") as csvfile:
        datareader = csv.reader( csvfile, delimiter=',', quotechar='"' )
        for row in datareader:
            lines = lines + 1
            if ( lines > 1 ):
                dt = strToTimestamp(row[1])
                for regionKey in regions:
                    if ( row[2] == regions[regionKey]['t'] + 'K ' + regions[regionKey]['name'] ):
                        
                        # skip corrections
                        cases = cases + ( int( row[3] ) if int( row[3] ) > 0 else 0)
                        death = death + ( int( row[4] ) if int( row[4] ) > 0 else 0)
                        recovered = recovered + ( int( row[10] ) if int( row[4] ) > 0 else 0)
                        
                        if (row[7] in gender) and (row[8] in ages):
                            regions["TH"][row[7] + row[8]]['cases_by_age'] += (int( row[3] ) if int( row[3] ) > 0 else 0)
                            regions["TH"][row[7] + row[8]]['deceased_by_age'] += (int( row[4] ) if int( row[4] ) > 0 else 0)
                            regions["TH"][row[7] + row[8]]['recovered_by_age'] += (int( row[10] ) if int( row[10] ) > 0 else 0)
                            
                            regions[regionKey][row[7] + row[8]]['cases_by_age'] += (int( row[3] ) if int( row[3] ) > 0 else 0)
                            regions[regionKey][row[7] + row[8]]['deceased_by_age'] += (int( row[4] ) if int( row[4] ) > 0 else 0)
                            regions[regionKey][row[7] + row[8]]['recovered_by_age'] += (int( row[10] ) if int( row[10] ) > 0 else 0)
                    
    for regionKey in regions:
        for genderKey in gender:
            for ageKey in ages:
                regions[regionKey][genderKey + ageKey]['cfr_by_age'] = 100.0 * regions[regionKey][genderKey + ageKey]['deceased_by_age'] / regions[regionKey][genderKey + ageKey]['cases_by_age'] if regions[regionKey][genderKey + ageKey]['cases_by_age'] > 0 else 0.0
                regions[regionKey][genderKey + ageKey]['active_cases_by_age'] = regions[regionKey][genderKey + ageKey]['cases_by_age'] - regions[regionKey][genderKey + ageKey]['deceased_by_age'] - regions[regionKey][genderKey + ageKey]['recovered_by_age']
               
    # CSV data
    writeCSVThuringia(cases, death)
    
    writeTotalCSV( 'cases_by_age' )
    writeTotalCSV( 'deceased_by_age' )
    writeTotalCSV( 'recovered_by_age' )
    writeTotalCSV( 'active_cases_by_age' )
    writeTotalCSV( 'cfr_by_age' )
    
    # JSON data
    writeTotalJSON( 'cases_by_age', dt )
    writeTotalJSON( 'deceased_by_age', dt )
    writeTotalJSON( 'recovered_by_age', dt )
    writeTotalJSON( 'active_cases_by_age', dt )
    
    #print( 'lines: ' + str( lines ) )
    # print( 'case count: ' + str( cases ) )
    # print( 'death count: ' + str( death ) )