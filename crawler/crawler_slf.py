#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def saveSLFNumbers():
    url = 'http://www.kreis-slf.de/landratsamt/' # no https available
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    DATADIR = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_slf/"
    
    try:
        # download the website to get the URL of the picture
        src = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
        
        # find the URL of the picture
        pattern_img = re.compile(r"csc-textpic-last\"\>\<img\ssrc=\"(.*?)\"")        
        imgsrc = pattern_img.findall(src)
        
        if ( len(imgsrc) < 1 ):
            return False
            
        # get the picture
        pic_url = "http://www.kreis-slf.de/" + imgsrc[0]
            
        filename_pattern = re.compile(r"\/([a-zA-Z0-9\-_]*\.jpg)$")
        filename = filename_pattern.findall(pic_url)
        
        if (len(filename) < 1):
            return False
        
        # check if picture exists and is not empty
        pic_local = DATADIR + filename[0]
        try:
            fs = os.path.getsize(pic_local)
        except:
            fs = 0
        
        if ( fs > 0 ):
            return False
        
        # do the request
        pic_data = requests.get(pic_url, headers=headers, allow_redirects=True, timeout=5.0)
        
        if pic_data.status_code != 200:
            return False

        # save the picture        
        with open(pic_local, 'wb') as f:
            f.write(pic_data.content)
        
        return True
        
    except:
        return False


if __name__ == "__main__":
    
    saveSLFNumbers()
    
    