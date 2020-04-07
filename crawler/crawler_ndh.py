#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getNDHNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    remove_array = ["<strong>", "</strong>", "<td>", "</td>", "&nbsp;", "\n"]
    
    num_pattern_T = re.compile(r"Infektionen:([0-9]{1,})")
    num_pattern_R = re.compile(r"gelten als genesen:([0-9]{1,})")
    num_pattern_H = re.compile(r"stationär\sbehandelt:([0-9]{1,})")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        for entry in remove_array:
            s = s.replace(entry, "")
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        ps4 = num_pattern_H.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = -1
        num_h = int(ps4[0]) if (len(ps4) >= 1) else -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_ndh.csv"
    URL = 'https://www.landratsamt-nordhausen.de/informationen-coronavirus.html'
    
    num_latest = getNDHNumbers(URL)
    
    if num_latest[0] > -1:
        f = open(DATAFILE, 'a')
        f.write("%i,%i,%i,%i,%i,%i,%s\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
        f.close()
