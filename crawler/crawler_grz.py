#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getGRZNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"esamt</td><td\srowspan=\"1\"\>([0-9]{1,})")
    num_pattern_R = re.compile(r"genesen.*?([0-9]{1,})\sPerson")
    num_pattern_D = re.compile(r"([0-9]{1,})\sverstorbenen")
    
    remove_array = { "<p>", "</p>", "<td>", "<strong>", "</strong>", "<b>", "</b>", "<br>", "<br />" }
        
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        for entry in remove_array:
            s = s.replace(entry, "")
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        ps3 = num_pattern_D.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = -1
        num_s = -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_grz.csv"
    URL = 'https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/?tx_ttnews[tt_news]=224&cHash=74595518f951c32f22d04b7591d643fe'

    # do the request    
    num_latest = getGRZNumbers(URL)
    
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
