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
    # https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2018%7C%7Cs1
    residents_array  = {
        "ABG": 90118,
        "EIC":  100380,
        "EA": 42370,
        "EF":  213699,
        "G": 94152,
        "GTH":  135452,
        "GRZ": 98159,
        "HBN": 63553,
        "IK":  108742,
        "J": 111407,
        "KYF": 75009,
        "NDH": 83822,
        "SHK": 83051,
        "SOK": 80868,
        "SLF":  106356,
        "SM": 122347,
        "SOM": 69655,
        "SON": 56196,
        "SHL": 34835,
        "UH":  102912,
        "WAK":  123025,
        "WE": 65090,
        "AP": 81947,
        "TH": 2143145
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
            