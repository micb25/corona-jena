#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re, os


def saveSMNumbers():
    url = "https://www.lra-sm.de/?p=22632"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    DATADIR = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_sm/"
    
    try:
        # download the website to get the URL of the document
        src = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
        
        # find the URL of the document
        pattern_pdf = re.compile(r"<a\ href=\"https\:\/\/www.lra-sm.de/(.*(?:Lage|Stand|TLB|Bulletin).*\.pdf)\"\>")        
        pdfsrc = pattern_pdf.findall(src)
        
        if ( len(pdfsrc) < 1 ):
            return False
            
        # get the document
        pdf_url = "https://www.lra-sm.de/" + pdfsrc[0]
            
        filename_pattern = re.compile(r"\/([^\/]*\.pdf)$")
        filename = filename_pattern.findall(pdf_url)
        
        if (len(filename) < 1):
            return False
        
        # check if document exists and is not empty
        pdf_local = DATADIR + filename[0]
        try:
            fs = os.path.getsize(pdf_local)
        except:
            fs = 0
        
        if ( fs > 0 ):
            return False
        
        # do the request
        pdf_data = requests.get(pdf_url, headers=headers, allow_redirects=True, timeout=5.0)
        
        if pdf_data.status_code != 200:
            return False
        
        # save the document        
        with open(pdf_local, 'wb') as f:
            f.write(pdf_data.content)
                
        return True
        
    except:
        return False


if __name__ == "__main__":
    
    saveSMNumbers()
    
    