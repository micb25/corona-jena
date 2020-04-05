#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os

DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_thuringia.csv"

def strToTimestamp(datetimestr):    
    s = datetimestr.replace("Uhr", "").strip()
    
    # fix for dates, since 25.03.
    if re.search(",", s) is None:
        s += ", 10"
            
    months = {"Januar": "1", "Februar": "2", "März": "3", "April": "4", "Mai": "5", "Juni": "6", "Juli": "7", "August": "8", "September": "9", "Oktober": "10", "November": "11", "Dezember": "12" }    
    for key in months.keys():
        s = s.replace(key, months[key])
            
    try:    
        struct_time = time.strptime(s, "%d. %m %Y, %H")
        return int(time.mktime(struct_time))
    except:
        return False

def getNumbers():
    url          = "https://www.landesregierung-thueringen.de/corona-bulletin"
    headers      = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }

    date_pattern = re.compile(r"\<strong\>.*?\s\(Stand: (.*?)\)\<\/strong\>.*?\<table.*?\<\/table\>.*?<table.*?\<tbody\>(.*?)\<\/tbody\>")
    num_pattern  = re.compile(r"\<tr\>\<th scope=\"row\">([A-Za-z\s\-äöüÄÖÜ]{1,})\<\/th\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\><\/tr\>") # 
    
    # new layout, since 21.03.2020
    num_pattern2 = re.compile(r"\<tr\>\<th scope=\"row\">([A-Za-z\s\-äöüÄÖÜ]{1,})\<\/th\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\>\<td\>([\-0-9]{1,})\<\/td\><\/tr\>") # 
    
    res = ""
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        pd = date_pattern.findall( r.text.replace("\n", "").replace("\r", "").replace("<p>", "").replace("</p>", "") )
        pd.reverse()
        
        for p in pd:
            dt = strToTimestamp(p[0])
            if dt is not False:
                
                # old layout
                ps = num_pattern.findall( p[1].replace("&nbsp;", "0") )             
                for d in ps:
                    
                    # fix for data since 26.03.2020:
                    # number of recovered people is not included any more
                    
                    if ( dt < 1585180800 ):
                        res = res + "%i,%s,%i,%i,%i,%i,%i,%i\n" % (dt, d[0], int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]), int(d[6]))
                    else:
                        res = res + "%i,%s,%i,%i,%i,%i,%i,%i\n" % (dt, d[0], int(d[3]), int(d[2]), int(d[4]), int(d[5]), int(d[6]), 0)                    
                
                # fix for data since 21.03.2020
                if ( len(ps) == 0 ):
                    ps = num_pattern2.findall( p[1].replace("&nbsp;", "0") )
                    for d in ps:
                        # fix for data since 27.03.
                        if ( dt < 1585299600 ):
                            res = res + "%i,%s,%i,%i,%i,%i,%i,%i\n" % (dt, d[0], int(d[3]), int(d[2]), int(d[4]), int(d[5]), int(d[6]), int(d[7]))
                        else:
                            res = res + "%i,%s,%i,%i,%i,%i,%i,%i\n" % (dt, d[0], int(d[3]), int(d[2]), int(d[5]), int(d[6]), int(d[7]), 0)
                            
        return res
    except:
        return False
    
if __name__ == "__main__":

    n = getNumbers()
    
    if n != False:
        f = open(DATAFILE, 'a')
        f.write(n) 
        f.close()
