#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getSOKNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
        
    num_pattern_T = re.compile(r"Infektionen\s(?:gesamt|insgesamt): ([0-9]{1,})")
    num_pattern_D = re.compile(r"Verstorbene: ([0-9]{1,})")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        ps1 = num_pattern_T.findall( s )
        ps3 = num_pattern_D.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_sok.csv"
    URL = 'https://www.saale-orla-kreis.de/sok/'
    
    num_latest = getSOKNumbers(URL)
        
    if num_latest[0] > -1:
        f = open(DATAFILE, 'a')
        f.write("%i,%i,%i,%i,%i,%i,%s\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
        f.close()
