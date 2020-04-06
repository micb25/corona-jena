#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getRKINumbers(url):    
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_DA = re.compile(r"\>Stand: ([0-9]{1,}\.[0-9]{1,}\.[0-9]{4})")
    num_pattern_TH = re.compile(r"Gesamt</strong></td><td>([0-9]{1,})</td><td>([0-9]{1,})</td><td>([0-9]{1,})</td><td>([0-9]{1,})</td>")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = re.sub(r"(rowspan|colspan|class)=\"[A-Za-z0-9]*\"", "", r.text)
        
        pd1 = num_pattern_DA.findall( s )
        if ( len(pd1) < 1 ):
            return False
        
        struct_time = time.strptime(pd1[0], "%d.%m.%Y")
        date = int(time.mktime(struct_time))
        
        s = re.sub(r"[\.\+\s]", "", s)
        ps1 = num_pattern_TH.findall( s )
        if len(ps1) != 1:
            return False
                
        num_t = int(ps1[0][0]) if (len(ps1[0]) >= 1) else 0
        num_d = int(ps1[0][3]) if (len(ps1[0]) >= 4) else 0
        
        return (date, num_t, -1, num_d, -1, -1)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_germany_total_rki.csv"
    URL = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
    
    n = getRKINumbers(URL)
    
    if (n != False):
        
        last_update = 0        
        with open(DATAFILE, "r") as df:
            rawdata = df.read().splitlines()
            
        dl = rawdata[-1].split(",")
        if len(dl) > 1:
            if int(dl[0]) > last_update:
                last_update = int(dl[0])
                  
        if ( n[0] > last_update ):
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%i,%s\n" % (int(n[0]), n[1], n[2], n[3], n[4], n[5], -1, URL))
            f.close()
