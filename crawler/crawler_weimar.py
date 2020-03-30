#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_weimar.dat"

def getNumber():
    url          = "https://stadt.weimar.de/aktuell/coronavirus/"
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern1 = re.compile(r"von\s(?:insgesamt\s)([0-9]{1,})\spositiv.*\sf.*")
    num_pattern2 = re.compile(r"([0-9]{1,})\sperson.*?geheilt")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.lower()
        
        replace_array  = {
                "eine": "1",
                "zwei": "2",
                "drei": "3",
                "vier": "4",
                "fünf": "5",
                "sechs": "6",
                "sieben": "7",
                "acht": "8",
                "neun": "9",
                "zehn": "10",
                "elf": "11",
                "zwölf": "12"
        }
        
        for k, r in replace_array.items():
            s = s.replace(k, r)
        
        ps1 = num_pattern1.findall( s )
        ps2 = num_pattern2.findall( s )
    
        num_t = int(ps1[0]) if len(ps1) >= 1 else 0
        num_r = int(ps2[0]) if len(ps2) >= 1 else 0
        num_d = 0
    
        return (num_t, num_r, num_d)
    
    except:
        return False
    
if __name__ == "__main__":

    n = getNumber()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i %-8i %-8i\n" % (int(time.time()), n[0], n[1], n[2]))
        f.close()
