#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv

def writeTotalCSV( valueType ) :
    global gender
    global ages
    global regions

    with open('../data/rki_th/total_' + valueType + '.csv', 'w', newline='') as csvfile:
        fieldnames = []
        fieldnames.append( 'region' )
        for ageKey in ages:
            fieldnames.append( 'W_' + ageKey )
            fieldnames.append( 'M_' + ageKey )
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
                row.append( regions[regionKey]['W'][ageKey][valueType] )
                row.append( regions[regionKey]['M'][ageKey][valueType] )
                #row.append( regions[regionKey]['W'][ageKey][valueType] + regions[regionKey]['M'][ageKey][valueType] )
            datawriter.writerow(row)

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    gender = ( "M", "W" )

    ages = (
        "A00-A04",
        "A05-A14",
        "A15-A34",
        "A35-A59",
        "A60-A79",
        "A80+"
    )

    regions = {
        "ABG": { "t": "L", "n": "Altenburger Land" },
        "EIC": { "t": "L", "n": "Eichsfeld" },
        "EA":  { "t": "S", "n": "Eisenach" },
        "EF":  { "t": "S", "n": "Erfurt" },
        "G":   { "t": "S", "n": "Gera" },
        "GTH": { "t": "L", "n": "Gotha" },
        "GRZ": { "t": "L", "n": "Greiz" },
        "HBN": { "t": "L", "n": "Hildburghausen" },
        "IK":  { "t": "L", "n": "Ilm-Kreis" },
        "J":   { "t": "S", "n": "Jena" },
        "KYF": { "t": "L", "n": "Kyffhäuserkreis" },
        "NDH": { "t": "L", "n": "Nordhausen" },
        "SHK": { "t": "L", "n": "Saale-Holzland-Kreis" },
        "SOK": { "t": "L", "n": "Saale-Orla-Kreis" },
        "SLF": { "t": "L", "n": "Saalfeld-Rudolstadt" },
        "SM":  { "t": "L", "n": "Schmalkalden-Meiningen" },
        "SOM": { "t": "L", "n": "Sömmerda" },
        "SON": { "t": "L", "n": "Sonneberg" },
        "SHL": { "t": "S", "n": "Suhl" },
        "UH":  { "t": "L", "n": "Unstrut-Hainich-Kreis" },
        "WAK": { "t": "L", "n": "Wartburgkreis" },
        "WE":  { "t": "S", "n": "Weimar" },
        "AP":  { "t": "L", "n": "Weimarer Land" },
        "TH":  { "t": "-", "n": "Thüringen" }
    }
    
    # prepare result array
    for regionKey in regions:
        for genderKey in gender:
            regions[regionKey][genderKey] = {}
            for ageKey in ages:
                regions[regionKey][genderKey][ageKey] = { 'cases_by_age': 0, 'deceased_by_age': 0 }
    
    # fill result array, count cases and casulties
    lines = 0
    #cases = 0
    #death = 0
    with open('../data/cases_rki_db_th.csv', newline='', encoding="utf8") as csvfile:
        datareader = csv.reader( csvfile, delimiter=',', quotechar='"' )
        for row in datareader:
            lines = lines + 1
            if ( lines > 1 ):
                for regionKey in regions:
                    if ( row[2] == regions[regionKey]['t'] + 'K ' + regions[regionKey]['n'] ):
                        #cases = cases + int( row[3] )
                        #death = death + int( row[4] )
                        regions["TH"][row[7]][row[8]]['cases_by_age'] = regions["TH"][row[7]][row[8]]['cases_by_age'] + int( row[3] )
                        regions["TH"][row[7]][row[8]]['deceased_by_age'] = regions["TH"][row[7]][row[8]]['deceased_by_age'] + int( row[4] )
                        regions[regionKey][row[7]][row[8]]['cases_by_age'] = regions[regionKey][row[7]][row[8]]['cases_by_age'] + int( row[3] )
                        regions[regionKey][row[7]][row[8]]['deceased_by_age'] = regions[regionKey][row[7]][row[8]]['deceased_by_age'] + int( row[4] )
                    
    writeTotalCSV( 'cases_by_age' )
    writeTotalCSV( 'deceased_by_age' )

    #print( 'lines: ' + str( lines ) )
    #print( 'case count: ' + str( cases ) )
    #print( 'death count: ' + str( death ) )