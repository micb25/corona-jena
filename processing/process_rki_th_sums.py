#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEFILE = SCRIPTPATH + '/../data/cases_th_rki_sums.csv'
    DATAFILE   = SCRIPTPATH + '/../data/rki_th/cases_by_date.csv'
    
    array_dates = []
    data_array = []
    current_region = ""
    
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
        
        # go back to start
        csvfile.seek(0)
        
        # set initial values
        for date in array_dates:
            row_array = { "Datum": date, "SummeFall": 0, "SummeGenesen": 0, "SummeTodesfall": 0, "AnzahlFall": 0, "AnzahlGenesen": 0, "AnzahlTodesfall": 0 }
            data_array.append(row_array)
            
        # count cases
        for row in enumerate(datareader):
            if (row[0] > 0):
                for entry in data_array:
                    if ( entry["Datum"] == int(row[1][0]) ):
                        
                        entry["SummeFall"] += int(row[1][2])
                        entry["SummeGenesen"] += int(row[1][3])
                        entry["SummeTodesfall"] += int(row[1][4])
                        
                        entry["AnzahlFall"] += int(row[1][5])
                        entry["AnzahlGenesen"] += int(row[1][6])
                        entry["AnzahlTodesfall"] += int(row[1][7])
            
        # write CSV data with sums
        with open(DATAFILE, "w") as df:
            df.write("%s,%s,%s,%s,%s,%s,%s\n" % ("Datum", "SummeFall", "SummeGenesen", "SummeTodesfall", "AnzahlFall", "AnzahlGenesen", "AnzahlTodesfall"))
            for entry in data_array:
                df.write("%i,%i,%i,%i,%i,%i,%i\n" % (entry["Datum"], entry["SummeFall"], entry["SummeGenesen"], entry["SummeTodesfall"], entry["AnzahlFall"], entry["AnzahlGenesen"], entry["AnzahlTodesfall"]))
        
                
    