#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os
import pandas as pd

if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/RKI_COVID19_Impfquotenmonitoring.csv"
    URL = 'https://raw.githubusercontent.com/micb25/RKI_COVID19_DATA/master/Impfquotenmonitoring/RKI_COVID19_Impfquotenmonitoring.csv'
    
    # do the request
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    r = requests.get(URL, headers=headers, allow_redirects=True, timeout=5.0)
    
    if r.ok:            
        # write new data
        f = open(DATAFILE, 'w')
        f.write(r.text)
        f.close()
    
    DATAFILE2 = os.path.dirname(os.path.realpath(__file__)) + "/../data/RKI_BL_Impfquotenmonitoring.csv"
    DATAFILE3 = os.path.dirname(os.path.realpath(__file__)) + "/../data/RKI_TH_Impfquotenmonitoring.csv"
    URL2 = 'https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Landkreise_COVID-19-Impfungen.csv'
            
    r = requests.get(URL2, headers=headers, allow_redirects=True, timeout=5.0)
    if r.ok:            
        # write new data
        f = open(DATAFILE2, 'w')
        f.write(r.text)
        f.close()
        
        df = pd.read_csv(DATAFILE2, encoding='utf-8');
        df.drop(df[ df.LandkreisId_Impfort == 'u' ].index, inplace=True);
        df['LandkreisId_Impfort'] = df['LandkreisId_Impfort'].astype(int);
        df.drop(df[ df.LandkreisId_Impfort < 16000 ].index, inplace=True);
        df.to_csv(DATAFILE3, sep=',', index=False);
        