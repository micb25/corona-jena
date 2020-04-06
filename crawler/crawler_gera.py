#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getGeraNumbers(url):
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern1 = re.compile(r"Infizierte\s([0-9]{1,})")
    num_pattern2 = re.compile(r"([0-9]{1,})\sPerson.*?\sgenesen")
    
    try:
    
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        
        ps1 = num_pattern1.findall( r.text )
        ps2 = num_pattern2.findall( r.text )
        
        num_t = int(ps1[0]) if ( len(ps1) >= 1 ) else -1
        num_r = int(ps2[0]) if ( len(ps2) >= 1 ) else -1
        num_d = -1
        num_h = -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False
    
    
if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_gera.csv"
    URL = "https://corona.gera.de/"
    
    n = getGeraNumbers(URL)
    
    if (n != False) and ( n[0] > -1 ):
        f = open(DATAFILE, 'a')
        f.write("%i,%i,%i,%i,%i,%i,%s\n" % (int(time.time()), n[0], n[1], n[2], n[3], n[4], URL))
        f.close()
