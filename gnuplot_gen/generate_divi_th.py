#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, datetime
   

if __name__ == "__main__":

    # data folder
    DATAFOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../data/divi_db_th/"
    DATASUMFILE = DATAFOLDER + "divi_db_th_sums.csv"    
    FILE_PATTERN = re.compile(r"divi_db_th_([0-9]{2}).([0-9]{2}).([0-9]{4})_([0-9]{2}).csv")
    
    # gnuplot file
    PLOTFILE = os.path.dirname(os.path.realpath(__file__)) + "/plot_divi_th.gnuplot"
    
    header = ["datum", "summe_faelle" ]
    
    data_records = []    
    
    # read files and calculate sum
    datafiles = [f for f in os.listdir(DATAFOLDER)]
    for file in datafiles:
        file_date = FILE_PATTERN.findall(file)
        if ( len(file_date) == 1 ) and ( len(file_date[0]) == 4 ):
            data_row = {}
            data_cont = ""
            data_sum = 0
            data_row[0] = int(datetime.datetime(year=int(file_date[0][2]), month=int(file_date[0][1]), day=int(file_date[0][0]), hour=int(file_date[0][3])).strftime('%s'))
            
            with open(DATAFOLDER + file, "r") as df:
                data_cont = df.read().splitlines()
                
            if ( data_cont != "" ):
                for l in data_cont[1:]:
                    s = l.split("\",")
                    c = s[1].split(",")
                    data_sum += int(c[0])
                
                data_row[1] = data_sum
                data_records.append(data_row)

    # sort data by time
    sorted_data = sorted(data_records, key=lambda i: i[0])

    # add a last entry with the current time and data
    last_entry = sorted_data[-1]
    last_entry[0] = int(datetime.datetime.now().strftime('%s'))
    sorted_data.append(last_entry)
    
    # generate sum file    
    data_str = ""        
    
    # write header
    for column in header:
        data_str += ("," if column != header[0] else "" ) + column     
    data_str += "\n"
    
    # write data
    for row in sorted_data:
        for i in range(len(row)):
            data_str += ("" if i == 0 else "," ) + (row[i] if isinstance(row[i], str) else str(row[i]))
        data_str += "\n"
            
    # write everything to the csv file
    with open(DATASUMFILE, "w") as nf:
        nf.write(data_str)
        
    # create diagram
    os.system( "gnuplot \"{}\" > /dev/null".format(PLOTFILE) )
    