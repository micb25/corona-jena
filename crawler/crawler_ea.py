#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def getEANumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"Infektionen in der kreisfreien Stadt Eisenach:\s?([0-9]{1,})")
    
    remove_array = { "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>"  }
    
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
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_ea.csv"
    URL = 'https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus'
    
    num_latest = getEANumbers(URL)
        
    if (num_latest != False) and (num_latest[0] > -1):
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        last_values = raw_data[-1].split(",")[1:5]
        
        # check for changes
        value_changed = False        
        for i in enumerate(last_values):
            if ( int(i[1]) != num_latest[i[0]] ):
                if ( num_latest[i[0]] != -1 ):
                    value_changed = True
        
        if value_changed:
            # timestamp
            timestamp = int(datetime.datetime.now().timestamp())      
            
            # write new csv data
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (timestamp, num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
            f.close()
