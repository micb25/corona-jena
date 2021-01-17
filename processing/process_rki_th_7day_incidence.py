#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, pandas as pd, numpy as np, datetime


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEPATH = SCRIPTPATH + '/../data/rki_th_by_date/'
    SOURCEFILE = SOURCEPATH + 'cases_by_day_and_region.csv'
    OUTPUTFILE = SCRIPTPATH + '/../data/cases_rki_7day_incidence.csv'
        
    regions = [ 'TH', 'ABG', 'EIC', 'EA', 'EF', 'G', 'GTH', 'GRZ', 'HBN', 'IK', 'J', 'KYF', 'NDH', 'SHK', 'SOK', 'SLF', 'SM', 'SOM', 'SON', 'SHL', 'UH', 'WAK', 'WE', 'AP' ]
    
    # number of residents per city/county; values taken from:
    # https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2019%7C%7Cs1
    residents_array  = {
        "ABG":    89393,
        "EIC":   100006,
        "EA":     42250,
        "EF":    213981,
        "G":      93125,
        "GTH":   134908,
        "GRZ":    97398,
        "HBN":    63197,
        "IK":    106249,
        "J":     111343,
        "KYF":    74212,
        "NDH":    83416,
        "SHK":    82950,
        "SOK":    80312,
        "SLF":   103199,
        "SM":    124916,
        "SOM":    69427,
        "SON":    57717,
        "SHL":    36789,
        "UH":    102232,
        "WAK":   118974,
        "WE":     65228,
        "AP":     82156,
        "TH":   2133378
    }
    
    df = pd.read_csv(SOURCEFILE, sep=",", decimal=".", encoding='utf-8')
    df['Datum'] = df.apply(lambda r: int(r['Datum']/86400)*86400, axis=1)
    dates_df = sorted(list(df.Datum.unique()))
    dates = [ ]
        
    date = dates_df[0]
    while ( date <= dates_df[-1] ):
        dates.append(date)
        date += 86400
    
    columns = ['Datum']
    columns.extend( [ x for x in regions ] )
    data = np.zeros((len(dates), len(columns)), dtype=float)
    
    for i, date in enumerate(dates):
        data[i][0] = date
        
        for j, district in enumerate(columns[1:]):
            
            num_cases = -1
            last_week = date - 7 * 86400
            
            cases = df.loc[ (df.Datum >= last_week) & (df.Datum <= date) & (df.Region == district) ]
            if len(cases) == 8:
                num_cases = 100000 / residents_array[district] * ( int(cases.iloc[-1]['SummeFall']) - int(cases.iloc[0]['SummeFall']) )
                
            data[i][j+1] = num_cases
    
    dfB = pd.DataFrame(columns=columns, data=data)
    dfB['Datum'] = dfB['Datum'].astype(int)
    dfB.to_csv(OUTPUTFILE, sep=",", decimal=".", encoding='utf-8', float_format='%.2f', index=False)
            
