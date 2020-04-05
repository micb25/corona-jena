#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os


def saveJenaNumbers_OpenData():
    url = 'https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:
        
        return requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
    
    except:
        return False


if __name__ == "__main__":
    
    CSVFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_jena_opendata.csv"
    
    content = saveJenaNumbers_OpenData()
        
    if content != False:
        f = open(CSVFILE, 'w')
        f.write(content)
        f.close()
