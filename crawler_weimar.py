#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/cases_weimar.dat"

def getNumber():
    url          = "https://stadt.weimar.de/aktuell/coronavirus/"
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern  = re.compile(r"sind\s([0-9]{1,})\sPerson.*positiv.*")
    num_pattern2 = re.compile(r"von\s([0-9]{1,})\spositiv.*\sF.*")
    
    r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
    ps = num_pattern.findall( r.text )
    if ( len(ps) == 1 ):
        return ps[0] 
    ps = num_pattern2.findall( r.text )
    return ps[0] if len(ps) == 1 else False
    
if __name__ == "__main__":

    n = getNumber()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i\n" % (int(time.time()), int(n))) 
        f.close()
