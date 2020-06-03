#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def getSONNumbers_A(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"([0-9]{1,})\sInfektionen\snachgewiesen")
    num_pattern_R = re.compile(r"\s([\d]{1,})\s[gG]enesene")
    
    remove_array = { "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>"  }
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        for entry in remove_array:
            s = s.replace(entry, "")
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = -1
        num_h = -1
        num_s = -1
        
        return [num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False  
    
    
def getSONNumbers_B(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_date = re.compile(r"([0-9]{1,2}\.\s[0-9A-Za-z]{1,10}\s[0-9]{1,4}.*?)---")
    
    num_pattern_T = re.compile(r"Infektionen\**?:?\s([0-9]*)")
    num_pattern_R = re.compile(r"genesen\**?:?\s([0-9]*)")
    num_pattern_D = re.compile(r"verstorben\**?:?\s([0-9]*)")
    
    remove_array = { "<p style=\"margin: 0cm 0cm 0pt;\">", "<p>", "</p>", "<td>", "</td>", "<strong>", "</strong>", "<u>", "</u>", "\r"  }
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text
        
        for entry in remove_array:
            s = s.replace(entry, "")
            
        s = s.replace("&nbsp;", " ")
        s = s.replace("\n", "")
        
        pd = num_pattern_date.findall( s )
        
        if ( len(pd) < 1 ):
            return False
        
        s = pd[1]
        
        ps1 = num_pattern_T.findall( s )
        ps2 = num_pattern_R.findall( s )
        ps3 = num_pattern_D.findall( s )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = -1
        num_s = -1
        
        return [num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_son.csv"
    URL = 'https://www.kreis-sonneberg.de/news/wichtige-hinweise-zum-coronavirus-1'
    URL_B = 'https://www.kreis-sonneberg.de/news/information-zum-infektionsgeschehen-im-landkreis-sonneberg'
    
    # do the requests
    num_latest = getSONNumbers_A(URL)    
    num_latest_B = getSONNumbers_B(URL_B)
    
    # take the higher numbers
    if ( num_latest == False ):
        num_latest = num_latest_B
    else:
        if ( num_latest_B != False ):
            for i in enumerate(num_latest_B):
                if ( i[1] != -1 ):
                    if ( i[1] > num_latest[i[0]] ):
                        num_latest[i[0]] = i[1]
                        
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
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (timestamp, num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL_B))
            f.close()
