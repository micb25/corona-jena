#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEFILE = SCRIPTPATH + '/../data/cases_thuringia_rki.csv'
    DATAFILE1  = SCRIPTPATH + '/../data/rki_th/reproduction_rates_th.csv'
    
    # COVID19, generation time: https://www.rki.de/DE/Content/Infekt/EpidBull/Archiv/2020/Ausgaben/17_20.pdf
    generation_time = 7 # 4 days, as assumed by the RKI
    
    # 7 day trend
    average_time    = 7 
    
    data_array = []
    r_array = []
    idx = 0
        
    # read RKI dashboard dump file
    with open(SOURCEFILE, encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"' )
        
        # read data
        for row in enumerate(datareader):
            if (row[0] > 0):
                data_array.append( [int(row[1][0]), int(row[1][1])] )
                
        # write CSV header
        with open(DATAFILE1, "w") as df:
            df.write("%s,%s,%s,%s\n" % ("Datum", "SummeA", "SummeB", "R"))
        
            # calculate reproduction rates
            while ( idx + generation_time +  average_time < len(data_array) ):
                sum_cases1 = data_array[idx + average_time][1] - data_array[idx][1]
                sum_cases2 = data_array[idx + average_time + generation_time][1] - data_array[idx + generation_time][1]
                
                if (sum_cases1 > 0):
                    rep_rate = pow(sum_cases2 / sum_cases1, 4.0/7.0)
                else:
                    rep_rate = -1 # R not available
                    
                df.write("%i,%i,%i,%.3f\n" % (data_array[idx + average_time + generation_time][0], sum_cases2, sum_cases1, rep_rate) )
                idx += 1                
