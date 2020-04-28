#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv, json, datetime, re


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEFILE = SCRIPTPATH + '/../data/cases_th_rki_sums.csv'
    DATAFILE1  = SCRIPTPATH + '/../data/rki_th/cases_by_date.csv'
    DATAFILE2  = SCRIPTPATH + '/../data/rki_th/current_cases_by_region.csv'
    DATAFILE3  = SCRIPTPATH + '/../data/rki_th/current_cases_by_region.json'
    
    array_dates = []
    data_array = []
    last_date = 0
    current_data_per_region = {}
    yesterdays_data_per_region = {}
    current_region = ""
    fallback_calc_increments = False
    
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
        
        # additional CSV filenames
        last_date_label = datetime.datetime.fromtimestamp(last_date + 86400).strftime("%d.%m.%Y")
        last_date_minus_one_label = datetime.datetime.fromtimestamp(last_date).strftime("%d.%m.%Y")
        DATAFILE4  = SCRIPTPATH + '/../data/rki_th_by_date/cases_by_region_' + last_date_label + '.csv'
        DATAFILE5  = SCRIPTPATH + '/../data/rki_th_by_date/cases_by_region_' + last_date_minus_one_label + '.csv'
                
        # read yesterdays data
        if not os.path.isfile(DATAFILE5):
            fallback_calc_increments = True
        else:
            with open(DATAFILE5, encoding="utf8") as oldcsvfile:
                olddatareader = csv.reader(oldcsvfile, delimiter=',', quotechar='"' )
                for row in enumerate(olddatareader):
                    if (row[0] > 0):
                        row_array = [int(row[1][2]), int(row[1][3]), int(row[1][4]), int(row[1][5]), int(row[1][6]), int(row[1][7]) ]
                        yesterdays_data_per_region[row[1][0]] = row_array
        
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
                        
                        if fallback_calc_increments:
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
                
        # calculate increments based on yesterdays data
        if not fallback_calc_increments:
            for idx in current_data_per_region.keys():
                current_data_per_region[idx][3] = current_data_per_region[idx][0] - yesterdays_data_per_region[idx][0]
                current_data_per_region[idx][4] = current_data_per_region[idx][1] - yesterdays_data_per_region[idx][1]
                current_data_per_region[idx][5] = current_data_per_region[idx][2] - yesterdays_data_per_region[idx][2]
        
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
                
        # copy new CSV to folder with daily tables
        os.system("cp {} {} > /dev/null".format(DATAFILE2, DATAFILE4))
                
        # add date for JSON
        current_data_per_region["Timestamp"] = last_date
        current_data_per_region["DateLabel"] = "Stand: " + datetime.datetime.fromtimestamp(last_date + 86400).strftime("%d.%m.%Y") + ", 0 Uhr"
                
        # write JSON with latest results per region
        with open(DATAFILE3, "w") as df:
            df.write(json.dumps(current_data_per_region))
            
        # update JSON list with available data        
        DATAPATH  = SCRIPTPATH + '/../data/rki_th_by_date/' # cases_by_region_' + last_date_minus_one_label + '.csv'
        DATAFILE6 = SCRIPTPATH + '/../data/rki_th_by_date/cases_by_region_list.json'
        fnpattern = re.compile(r"cases_by_region_([0-9]{2}).([0-9]{2}).([0-9]{4}).csv");
        
        dates_tmp_arr = []
        dates_list = []
        i = 0
        csvfiles = [f for f in os.listdir(DATAPATH) if os.path.isfile(os.path.join(DATAPATH, f))]
        for f in csvfiles:
            pm = fnpattern.findall(f)
            if ( len(pm) == 1 ) and ( len(pm[0]) == 3 ):                
                dt = datetime.date(int(pm[0][2]), int(pm[0][1]), int(pm[0][0]))
                
                date_entry = {}
                date_entry["date"] = dt.strftime("%d.%m.%Y") + ", 0 Uhr"
                date_entry["timestamp"] = int(dt.strftime("%s"))
                date_entry["file"] = f
                dates_tmp_arr.append(date_entry)
                dates_list.append(date_entry["timestamp"])
                
        dates_arr = sorted(dates_tmp_arr, key=lambda k: k['timestamp']) 
        with open(DATAFILE6, "w") as df:
            df.write(json.dumps(dates_arr))
            