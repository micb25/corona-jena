#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getJenaNumbers_OpenData():
    url = 'https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:
        lines = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text.splitlines()
        data  = lines[-1].split(',')
        return  [
                    int(data[1]) if (len(data) >= 2) else -1,
                    int(data[2]) if (len(data) >= 3) else -1,
                    int(data[3]) if (len(data) >= 4) else -1,
                    int(data[4]) if (len(data) >= 5) else -1,
                    int(data[5]) if (len(data) >= 6) else -1
                ]
    except:
        return False


def getJenaNumbers_Website():
    url = 'https://gesundheit.jena.de/de/coronavirus'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"\s([0-9]{1,})\s?(?:Meldungen|bestätigte\ Fälle)")
    num_pattern_R = re.compile(r"Genesene:\s([0-9]{1,})")
    num_pattern_D = re.compile(r"Todesfälle\:\s([0-9]{1,})")
    num_pattern_H = re.compile(r"stationärer Aufenthalt\:\s([0-9]{1,})")
    num_pattern_S = re.compile(r"schwerer\sVerlauf\:\s([0-9]{1,})")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        ps1 = num_pattern_T.findall( r.text )
        ps2 = num_pattern_R.findall( r.text )
        ps3 = num_pattern_D.findall( r.text )
        ps4 = num_pattern_H.findall( r.text )
        ps5 = num_pattern_S.findall( r.text )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else -1
        num_r = int(ps2[0]) if (len(ps2) >= 1) else -1
        num_d = int(ps3[0]) if (len(ps3) >= 1) else -1
        num_h = int(ps4[0]) if (len(ps4) >= 1) else -1
        num_s = int(ps5[0]) if (len(ps5) >= 1) else -1
        
        return (num_t, num_r, num_d, num_h, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_jena.dat"
    num_latest = [-1, -1, -1, -1, -1]
    
    n1 = getJenaNumbers_OpenData()
    if n1 != False:
        num_latest = n1
        
    n2 = getJenaNumbers_Website()
    if n2 != False:
        # take the maximum value for total cases, recovered, and deceased
        for i in range(0, 3):
            if ( n2[i] > num_latest[i] ):
                num_latest[i] = n2[i]
        
        # for the rest prefer the OpenData table
        for i in range(3, 5):
            if ( num_latest[i] == -1 ):
                num_latest[i] = n2[i]
    
    if num_latest[0] > -1:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i %-8i %-8i %-8i %-8i\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4]))
        f.close()
