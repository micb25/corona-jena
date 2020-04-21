#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getGeraNumbers(url):
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern1 = re.compile(r"Infizierte\s([0-9]{1,})")
    num_pattern2 = re.compile(r"([0-9]{1,})\s(?:Person)?.*?\s?genesen")
    
    try:
    
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        
        ps1 = num_pattern1.findall( r.text )
        ps2 = num_pattern2.findall( r.text )
        
        num_t = int(ps1[0]) if ( len(ps1) >= 1 ) else -1
        num_r = int(ps2[0]) if ( len(ps2) >= 1 ) else -1
        num_d =  2 # manually set
        num_h = -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False
    
    
if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_gera.csv"
    URL = "https://corona.gera.de/"
    
    # do the request    
    num_latest = getGeraNumbers(URL)
    
    if (num_latest != False) and (num_latest[0] > -1):
        
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        last_values = raw_data[-1].split(",")[1:6]
        
        # check for changes
        value_changed = False
        for i in enumerate(last_values):
            if ( int(i[1]) != num_latest[i[0]] ):
                if ( num_latest[i[0]] != -1 ):
                    value_changed = True
                    
        if value_changed:
            # write new csv data
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
            f.close()
