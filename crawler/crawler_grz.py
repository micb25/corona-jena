#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getGRZNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"esamt\<td\srowspan=\"1\"\>([0-9]{1,})")
    
    remove_array = { "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>", "<b>", "</b>", "<br>", "<br />" }
        
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        for entry in remove_array:
            s = s.replace(entry, "")
        
        ps1 = num_pattern_T.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = -1
        num_d = -1
        num_h = -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_grz.csv"
    URL = 'https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/?tx_ttnews[tt_news]=224&cHash=74595518f951c32f22d04b7591d643fe'
    
    num_latest = getGRZNumbers(URL)
            
    if num_latest[0] > -1:
        f = open(DATAFILE, 'a')
        f.write("%i,%i,%i,%i,%i,%i,%s\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
        f.close()
