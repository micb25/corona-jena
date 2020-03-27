#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/cases_jena.dat"

def getNumber():
    url = 'https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv'

    try:
        lines = requests.get(url).text.splitlines()
        data  = lines[-1].split(',')
        return (int(data[1]), int(data[2]), int(data[3]))
    
    except:
        return False  
    
if __name__ == "__main__":
    n = getNumber()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write("%-16i %-8i %-8i %-8i\n" % (int(time.time()), n[0], n[1], n[2]))
        f.close()
