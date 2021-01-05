#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os, sys


def getWENumbersRKI():
    RKIFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/rki_th/current_cases_by_region.csv"
    try:
        with open(RKIFILE, 'r') as df:
            raw_data = df.read().splitlines()
        for l in raw_data:
            if ( l[0:2] == 'WE' ):
                current_values = l.split(",")[1:6]
                return (int(current_values[2]), int(current_values[3]))
        
        return (-1, -1)
    except:
        return (-1, -1)
    

def getWENumbers(url):
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    num_pattern1 = re.compile(r"positiv getesteten: ([0-9]{1,})")
    num_pattern2 = re.compile(r"genesenen: ([0-9]{1,})")
    num_pattern3 = re.compile(r"verstorbenen: ([0-9]{1,})")
    num_pattern4 = re.compile(r"kliniken behandelten: ([0-9]{1,})")
    
    n = getWENumbersRKI()
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.lower().replace('.', '')
                
        ps1 = num_pattern1.findall( s )
        ps2 = num_pattern2.findall( s )
        ps3 = num_pattern3.findall( s )
        ps4 = num_pattern4.findall( s )
        
        num_t = int(ps1[0]) if len(ps1) >= 1 else -1
        num_r = int(ps2[0]) if len(ps2) >= 1 else -1
        num_d = int(ps3[0]) if len(ps3) >= 1 else n[1] # RKI number
        num_h = int(ps4[0]) if len(ps4) >= 1 else -1
        num_s = -1
    
        return [num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False

    
if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_weimar.csv"
    URL = "https://stadt.weimar.de/aktuell/coronavirus/"
    
    # do the request
    num_latest = getWENumbers(URL)
    
    # sanity checks
    if (num_latest[1] > num_latest[0]) or (num_latest[2] > num_latest[0]):
        sys.exit(0)
    
    if (num_latest != False) and (num_latest[0] > -1):
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        current_values = raw_data[-1].split(",")[1:6]
        source = raw_data[-1].split(",")[-1]
        
        # check for changes and manually added numbers
        value_changed = False        
        for i in enumerate(current_values):
            if source == URL:
                if ( int(i[1]) != num_latest[i[0]] ):
                    if ( num_latest[i[0]] != -1 ): 
                        value_changed = True
            else:
                if ( num_latest[i[0]] > int(i[1]) ):
                    value_changed = True
            
        if value_changed:
            # timestamp
            timestamp = int(datetime.datetime.now().timestamp())
            
            # write new csv data
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (timestamp, num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], URL))
            f.close()
