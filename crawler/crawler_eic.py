#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getEICNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"Infizierten\s?:?\s?([0-9]{1,})")
    num_pattern_R = re.compile(r"(?:Genesenen?|Genesungen):\s?([0-9]{1,})")
    num_pattern_D = re.compile(r"(?:Todesfälle|Verstorbene|Tote)\:\s?([0-9]{1,})")
    num_pattern_H = re.compile(r"(?:stationäre?)\:\s?([0-9]{1,})")
    num_pattern_S = re.compile(r"(?:Verlauf|Verläufe)\:\s?([0-9]{1,})")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.replace('.', '')
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        ps3 = num_pattern_D.findall( s )
        ps4 = num_pattern_H.findall( s )
        ps5 = num_pattern_S.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = int(ps4[0]) if (len(ps4) >= 1) else -1
        num_s = int(ps5[0]) if (len(ps5) >= 1) else -1
        
        return [num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_eic.csv"
    URL = 'https://www.kreis-eic.de/aktuelle-fallzahlen-im-landkreis-eichsfeld.html'
    
    num_latest = getEICNumbers(URL)
    
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
