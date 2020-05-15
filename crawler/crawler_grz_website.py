#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def saveGRZWebsite():
    url = "https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/?tx_ttnews%5Btt_news%5D=224&cHash=74595518f951c32f22d04b7591d643fe"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    DATADIR = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_grz/"
    
    if True:
        # download the website
        src = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
                
        # find the important stuff
        pattern_text = re.compile(r"(<div class=\"news-single-item\">[\s\S\r\n]*?<\/div>[\s\r\n]*?<\/div>)")        
        pattern_date = re.compile(r"<div class=\"news-single-rightbox\">[\s\r\n]*?([\S][\S\s]*?)[\s\r\n]*?<\/div>")
        text = pattern_text.findall(src)
        
        if ( len(text) < 1 ):
            return False
            
        date = pattern_date.findall(src)
        if ( len(date) < 1 ):
            return False
                
        # use the date as filename
        date = datetime.datetime.strptime(date[0], "%d.%m.%Y %H:%M")
        filename = DATADIR + date.strftime("cases_grz_%Y_%m_%d_%H%M.txt")
        
        # check if file exists and is not empty
        try:
            fs = os.path.getsize(filename)
        except:
            fs = 0
        
        if ( fs > 0 ):
            return False
        
        # save text
        with open(filename, 'w') as f:
            f.write(text[0])
            
        return True
            
    #except:
    #    return False


if __name__ == "__main__":
    
    saveGRZWebsite()
    
    