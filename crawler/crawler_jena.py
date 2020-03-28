#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def getJenaNumbers_OpenData():
    url = 'https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:
        lines = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text.splitlines()
        data  = lines[-1].split(',')
        return (int(data[1]), int(data[2]), int(data[3]))
    
    except:
        return False


def getJenaNumbers_Website():
    url = 'https://gesundheit.jena.de/de/coronavirus'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    num_pattern_T = re.compile(r"\s([0-9]{1,})\s?(?:Meldungen|bestätigte\ Fälle)")
    num_pattern_R = re.compile(r"([0-9]{1,})\sPerson.*\sgenesen")
    num_pattern_D = re.compile(r"([0-9]{1,})\sTodesf")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        ps1 = num_pattern_T.findall( r.text )
        ps2 = num_pattern_R.findall( r.text )
        ps3 = num_pattern_D.findall( r.text )
        
        num_t = int(ps1[0]) if (len(ps1) >= 1) else 0
        num_r = int(ps2[0]) if (len(ps2) >= 1) else 0
        num_d = int(ps3[0]) if (len(ps3) >= 1) else 0
        
        return (num_t, num_r, num_d)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_jena.dat"
    num_latest = [0, 0, 0]
    
    n1 = getJenaNumbers_OpenData()
    if n1 != False:
        num_latest = list(n1)
        
    n2 = getJenaNumbers_Website()
    if n2 != False:
        for i in range(0, 3):
            if ( n2[i] > num_latest[i] ):
                num_latest[i] = n2[i]
    
    if num_latest[0] > 0:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i %-8i %-8i\n" % (int(time.time()), num_latest[0], num_latest[1], num_latest[2]))
        f.close()
