#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/cases_jena.dat"

def getNumber():
    url         = "https://gesundheit.jena.de/de/coronavirus"
    headers     = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern = re.compile(r"\<strong\>\s?([0-9]{1,})\s?\<\/strong\>\s?Meldungen")
    
    r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
    ps = num_pattern.findall( r.text )
    if ( len(ps) == 1 ):
        return ps[0]
    else:
        return False  
    
if __name__ == "__main__":

    n = getNumber()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i\n" % (int(time.time()), int(n))) 
        f.close()
