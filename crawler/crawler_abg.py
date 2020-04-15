#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getABGNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"zahl der infizierten: ([0-9]{1,})")
    num_pattern_R = re.compile(r"([0-9]{1,})\sperson.*?genesen")
    num_pattern_H = re.compile(r"([0-9]{1,})\spatient.*?in stationärer behandlung")
    
    remove_array = [ "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>", "<b>", "</b>", "<br>", "<br />" ]
    
    number_array  = {
                "eine": "1", "zwei": "2","drei": "3",
                "vier": "4", "fünf": "5", "sechs": "6",
                "sieben": "7", "acht": "8", "neun": "9",
                "zehn": "10", "elf": "11", "zwölf": "12"
        }
        
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.lower()
        
        for entry in remove_array:
            s = s.replace(entry, "")
            
        for k, r in number_array.items():
            s = s.replace(k, r)
        
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
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_abg.csv"
    URL = 'https://www.altenburgerland.de/sixcms/detail.php?&_nav_id1=2508&_lang=de&id=371691'

    # do the request    
    num_latest = getABGNumbers(URL)
    
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
