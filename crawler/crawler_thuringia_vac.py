#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os

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
            
