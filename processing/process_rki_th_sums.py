#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEFILE = SCRIPTPATH + '/../data/cases_th_rki_sums.csv'
    DATAFILE1  = SCRIPTPATH + '/../data/rki_th/cases_by_date.csv'
    DATAFILE2  = SCRIPTPATH + '/../data/rki_th/current_cases_by_region.csv'
    
    array_dates = []
    data_array = []
    last_date = 0
    current_data_per_region = {}
    current_region = ""
    
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
    
    # initial values
    for region in regions:
        current_data_per_region[regions[region]] = ()
    
    # open RKI dashboard dump file
    with open(SOURCEFILE, encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"' )
        
        # add all individual dates to date_array
        for row in enumerate(datareader):
            if (row[0] > 0):
                if (row[0] == 1):
                    current_region = row[1][1]
                elif (current_region != row[1][1]):
                    break
                array_dates.append(int(row[1][0]))
        
        last_date = array_dates[-1]
        
        # go back to start
        csvfile.seek(0)
        
        # set initial values
        for date in array_dates:
            row_array = { "Datum": date, "SummeFall": 0, "SummeGenesen": 0, "SummeTodesfall": 0, "AnzahlFall": 0, "AnzahlGenesen": 0, "AnzahlTodesfall": 0 }
            data_array.append(row_array)
            
        # count cases
        for row in enumerate(datareader):            
            if (row[0] > 0):
                
                the_date = int(row[1][0])
                
                for entry in data_array:
                    
                    if ( entry["Datum"] == the_date ):
                        
                        entry["SummeFall"] += int(row[1][2])
                        entry["SummeGenesen"] += int(row[1][3])
                        entry["SummeTodesfall"] += int(row[1][4])
                        
                        entry["AnzahlFall"] += int(row[1][5])
                        entry["AnzahlGenesen"] += int(row[1][6])
                        entry["AnzahlTodesfall"] += int(row[1][7])
                        
                if ( the_date == last_date ):
                    index = regions[row[1][1]]
                    current_data_per_region[index] = [int(row[1][2]), int(row[1][3]), int(row[1][4]), int(row[1][5]), int(row[1][6]), int(row[1][7])]
                    
        # add sum for TH
        for entry in data_array:
            if ( entry["Datum"] == last_date ):
                current_data_per_region["TH"] = [entry["SummeFall"], entry["SummeGenesen"], entry["SummeTodesfall"], entry["AnzahlFall"], entry["AnzahlGenesen"], entry["AnzahlTodesfall"]]
                                    
        # write CSV data with sums per region
        with open(DATAFILE1, "w") as df:
            df.write("%s,%s,%s,%s,%s,%s,%s\n" % ("Datum", "SummeFall", "SummeGenesen", "SummeTodesfall", "AnzahlFall", "AnzahlGenesen", "AnzahlTodesfall"))
            for entry in data_array:
                df.write("%i,%i,%i,%i,%i,%i,%i\n" % (entry["Datum"], entry["SummeFall"], entry["SummeGenesen"], entry["SummeTodesfall"], entry["AnzahlFall"], entry["AnzahlGenesen"], entry["AnzahlTodesfall"]))
        
        # write CSV data with latest results per region
        with open(DATAFILE2, "w") as df:
            df.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % ("Region", "Datum", "SummeFall", "SummeGenesen", "SummeTodesfall", "AnzahlFall", "AnzahlGenesen", "AnzahlTodesfall"))
            
            # fixes the key order in old Python 3 versions
            sorted_keys = sorted(current_data_per_region.keys())
            sorted_keys.remove("TH")
            sorted_keys.append("TH")
            
            for entry in sorted_keys:
                df.write("%s,%i,%i,%i,%i,%i,%i,%i\n" % ( entry, last_date, current_data_per_region[entry][0], current_data_per_region[entry][1], current_data_per_region[entry][2], current_data_per_region[entry][3], current_data_per_region[entry][4], current_data_per_region[entry][5]))
                
    