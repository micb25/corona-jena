#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def getWAKNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"Infektionen im Wartburgkreis:\s?([0-9]{1,})")
    num_pattern_R = re.compile(r"[dD]avon mit aktiver Infektion in:?\s?\(?([0-9]{1,})\)?")
    num_pattern_D = re.compile(r"[0-9]{1,}\s?\([0-9]{1,}\sPersonen\sin\sEisenach\sund\s([0-9]{1,})\sPersonen\sim\sWartburgkreis\)")
    
    remove_array = { "<em>", "</em>", "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>"  }
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.replace("&nbsp;", " ")
        
        for entry in remove_array:
            s = s.replace(entry, "")
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        ps3 = num_pattern_D.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = -1
        num_s = -1
    
        if (len(ps2) >= 1) and (num_t > 0) and (num_d > 0):
            num_r = num_t - num_d - int(ps2[0])
        else:
            num_r = -1
    
        return [num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_wak.csv"
    URL = 'https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus'
    
    num_latest = getWAKNumbers(URL)
        
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
