#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, pandas as pd, numpy as np, datetime


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEPATH = SCRIPTPATH + '/../data/'
    SOURCEFILE = SOURCEPATH + 'cases_rki_db_th.csv'
    OUTPUTFILE = SOURCEPATH + 'cases_rki_7day_incidence.csv'
        
    regions = {
        "Thüringen": "TH",
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
        "LK Weimarer Land": "AP"
    }
    
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
        "AP": 81947
    }
    
    df = pd.read_csv(SOURCEFILE, sep=",", decimal=".", encoding='utf-8')
    dates_df = sorted(list(df.Meldedatum.unique()))
    dates = [ ]
    today = int(datetime.datetime.now().strftime("%s"))
    
    date = dates_df[0]
    while ( date < today ):
        dates.append(date)
        date += 86400
    
    columns = ['Meldedatum']
    columns.extend( [ regions[x] for x in regions ] )
    data = np.zeros((len(dates), len(columns)), dtype=float)

    for i, date in enumerate(dates):
        data[i][0] = date
        
        for j, district in enumerate(regions):
            
            last_week = date - 7 * 86400
            
            if district != 'Thüringen':
                num_cases = 100000 / residents_array[regions[district]] * df.loc[ (df.Meldedatum >= last_week) & (df.Meldedatum <= date) & (df.Landkreis == district) ]['AnzahlFall'].sum()
            else:
                num_cases = 100000 / 2143145 * df.loc[ (df.Meldedatum >= last_week) & (df.Meldedatum <= date) ]['AnzahlFall'].sum()
                
            data[i][j+1] = num_cases
    
    dfB = pd.DataFrame(columns=columns, data=data)
    dfB['Meldedatum'] = dfB['Meldedatum'].astype(int)
    dfB.to_csv(OUTPUTFILE, sep=",", decimal=".", encoding='utf-8', float_format='%.2f', index=False)
            