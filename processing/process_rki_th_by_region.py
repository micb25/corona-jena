#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEPATH = SCRIPTPATH + '/../data/rki_th_by_date/'
    SOURCEFILE = SOURCEPATH + 'cases_by_region_list.json'
    OUTPUTFILE = SOURCEPATH + 'cases_by_day_and_region.csv'
    
    json_list = []
    entries = []
    
    regions = {
        "LK Altenburger Land": "ABG",
        "LK Eichsfeld": "EIC",
        "SK Eisenach": "EA",
        "SK Erfurt": "EF",
        "SK Gera": "G",
        "LK Gotha": "GTH",
        "LK Greiz": "GRZ",
        "LK Hildburghausen": "HBN",
        "LK Ilm-Kreis": "IK",
        "SK Jena": "J",
        "LK Kyffhäuserkreis": "KYF",
        "LK Nordhausen": "NDH",
        "LK Saale-Holzland-Kreis": "SHK",
        "LK Saale-Orla-Kreis": "SOK",
        "LK Saalfeld-Rudolstadt": "SLF",
        "LK Schmalkalden-Meiningen": "SM",
        "LK Sömmerda": "SOM",
        "LK Sonneberg": "SON",
        "SK Suhl": "SHL",
        "LK Unstrut-Hainich-Kreis": "UH",
        "LK Wartburgkreis": "WAK",
        "SK Weimar": "WE",
        "LK Weimarer Land": "AP",
        "Thüringen": "TH"
    }
    
    csv_header = "Datum,Region,SummeFall,SummeGenesen,SummeTodesfall,AnzahlFall,AnzahlGenesen,AnzahlTodesfall\n"
    
    with open(SOURCEFILE, 'r') as jsonfile:
        tmp_date_list = json.loads(jsonfile.read())
        
    for entry in tmp_date_list:
        json_list.append( [entry['timestamp'], entry['file'] ] )
        
    sorted_json_list = sorted(json_list, key=lambda t: t[0])
        
    for timestamp, jsonfile in sorted_json_list:
        filename = SOURCEPATH + jsonfile
        with open(filename, 'r') as jsonfile:
            daily_data = json.loads(jsonfile.read())
            
        for region in regions:
            region_name = regions[region]
            rd = daily_data[region_name]
            entries.append( [timestamp, region_name, rd[0], rd[1], rd[2], rd[3], rd[4], rd[5] ] )
    
    csv_data = csv_header
    for e in entries:
        csv_data += "{},{},{},{},{},{},{},{}\n".format(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7])
    
    with open(OUTPUTFILE, 'w') as csvfile:
        csvfile.write(csv_data)
        csvfile.close()
            