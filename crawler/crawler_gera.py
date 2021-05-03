#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os
  

def getGeraNumbers(url):
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern1 = re.compile(r"\s([0-9]{1,})\s{1,}\([+-]?\s?([0-9]{1,})\)\s{1,}([0-9]{1,})\s{1,}\([+-]?\s?([0-9]{1,})\)\s{1,}([0-9]{1,})\s{1,}\([+-]?\s?([0-9]{1,})\)\s{1,}([0-9]{1,})\s{1,}\([+-]?\s?([0-9]{1,})\)\s{1,}([0-9]{1,})\s{1,}\([+-]?\s?([0-9]{1,})\)\s{1,}")
    num_pattern2 = re.compile(r"aus gera.*?\s([0-9]{1,})\s")
    
    try:
    
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.lower().replace('.', '').replace('\n', ' ')
        s = re.sub(r"<td[^>]*>", ' ', s)
        s = re.sub(r"<p[^>]*>", ' ', s)
        s = re.sub(r"</p>", ' ', s)
        s = re.sub(r"</td>", ' ', s)
        
        ps1 = num_pattern1.findall( s )
        ps2 = num_pattern2.findall( s )
                
        num_t = int(ps1[0][4]) if ( len(ps1) >= 1 ) else -1
        num_r = int(ps1[0][6]) if ( len(ps1) >= 1 ) else -1
        num_d = int(ps1[0][8]) if ( len(ps1) >= 1 ) else -1
        num_h = int(ps2[0]) if ( len(ps2) >= 1 ) else -1
        num_s = -1
        
        return [num_t, num_r, num_d, num_h, num_s]
    
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
