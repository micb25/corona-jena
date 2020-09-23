#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def getUHNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"aktuell infizierter personen(?:<\/strong>)?(?:<\/span>)?</td><td.*?>.*?(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?(?:<\/span>)?<\/td>")
    num_pattern_R = re.compile(r"genesene.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?(?:<\/span>)?<\/td>")
    num_pattern_D = re.compile(r"verstorbene.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?(?:<\/span>)?<\/td>")
    num_pattern_H = re.compile(r"stationäre.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?(?:<\/span>)?<\/td>")
    num_pattern_S = re.compile(r"schwere verläufe.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?(?:<\/span>)?<\/td>")
            
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.replace("\n", "").replace("\r", "").replace("\t", "").lower()
        
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
        
        if ( num_t > -1 ) and ( num_r > -1 ) and ( num_d > -1 ):
            return (num_t + num_r + num_d, num_r, num_d, num_h, num_s)
        else:
            return False
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_uh.csv"
    URL = "https://www.unstrut-hainich-kreis.de/index.php/informationen-zum-neuartigen-coronavirus"
    
    # do the request
    num_latest = getUHNumbers(URL)
    
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
            timestamp = int(datetime.datetime.now().timestamp()) 
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (timestamp, num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
            f.close()
            