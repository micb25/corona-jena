#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/cases_jena.dat"

def getNumber():
    url         = "https://gesundheit.jena.de/de/coronavirus"
    headers     = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_A = re.compile(r"\<strong\>\s?([0-9]{1,})\s?\<\/strong\>\s?Meldungen")
    num_pattern_G = re.compile(r"([0-9]{1,})\sPerson.*\sgenesen")
    num_pattern_T = re.compile(r"([0-9]{1,})\sTodesf")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        ps1 = num_pattern_A.findall( r.text )
        ps2 = num_pattern_G.findall( r.text )
        ps3 = num_pattern_T.findall( r.text )
        
        if ( len(ps1) == 1 ) and ( len(ps2) == 0 ) and ( len(ps3) == 0 ):
            return (int(ps1[0]), 0, 0)
        
        if ( len(ps1) == 1 ) and ( len(ps2) == 1 ) and ( len(ps3) == 0 ):
            return (int(ps1[0]), int(ps2[0]), 0)
        
        if ( len(ps1) == 1 ) and ( len(ps2) == 0 ) and ( len(ps3) == 1 ):
            return (int(ps1[0]), 0, int(ps3[0]))
    
        if ( len(ps1) == 1 ) and ( len(ps2) == 1 ) and ( len(ps3) == 1 ):
            return (int(ps1[0]), int(ps2[0]), int(ps3[0]))
        
        return False
    
    except:
        return False  
    
if __name__ == "__main__":

    n = getNumber()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i %-8i %-8i\n" % (int(time.time()), n[0], n[1], n[2])) 
        f.close()
