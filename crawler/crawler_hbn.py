#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os
from num2words import num2words

number_dict = {}
number_dict["kein"] = 0
number_dict["keine"] = 0
number_dict["keiner"] = 0
number_dict["eine"] = 1
number_dict["einer"] = 1

for i in range(1, 501):
    number_dict[ num2words(i, lang='de') ] = i
    
def germanWordToInt(w):   
    if re.match("^[0-9]{1,}$", w) is not None:
        return int(w)
    else:  
        for n in number_dict:
            if ( w.lower() == n ):
                return number_dict[n]
        return False
    
    
def getHBNSubPage(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    try:
        r = requests.get('https://www.landkreis-hildburghausen.de' + url.replace("&amp;", "&"), headers=headers, allow_redirects=True, timeout=5.0)
        return r.text
    except:
        return False
    

def getHBNNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    pattern_Subpage = re.compile(r"<small class=\"date\">([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4,4})</small>\s*?<h4 class=\"liste-titel\"><a href=\"(.*?)\">.*?Aktuelle\sFallzahlen.*?</a></h4>")
    pattern_date = re.compile(r"([0-9]{1,})\.([0-9]{1,}).([0-9]{2,4}),\s?([0-9]{1,})[\.:]([0-9]{1,})")    
    
    num_pattern_T = re.compile(r"\s([^\s]*)\s(?:positiv\sgetestete\sPersonen|Personen\spositiv)")
    num_pattern_R = re.compile(r"([^\.\s]*)\sPersonen[^\.]*?(?:genesen|überstanden)")
    num_pattern_D = re.compile(r"\s([^\s]*)\s(?:Todesfall|Todesfälle|Verstorbene|Tote)")
    
    replace_array = ["<p>", "</p>", "<em>", "</em>", "<strong>", "</strong>", "\n", "\t", "\r" ]
    
    html_replace_dict = {
                "&nbsp;": " ",
                "&auml;": "ä",
                "&ouml;": "ö",
                "&uuml;": "ü",
                "&Auml;": "Ä",
                "&Ouml;": "Ö",
                "&Uuml;": "Ü",
                "&szlig;": "ß"
            }
    
    deceased_cnt = 0
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
                
        pmsub = pattern_Subpage.findall( r.text )
        pmsub.reverse()        
        
        for pm in pmsub:
            pm_content = getHBNSubPage(pm[1])
            
            for entry in replace_array:
                pm_content = pm_content.replace(entry, "")
                
            for entry in html_replace_dict:
                pm_content = pm_content.replace(entry, html_replace_dict[entry])
                
            pd = pattern_date.findall( pm_content )
            
            if ( len(pd) < 1 ):
                continue
                            
            timestamp = int(datetime.datetime(int(pd[0][2]), int(pd[0][1]), int(pd[0][0]), int(pd[0][3]) if int(pd[0][3]) < 24 else 23, int(pd[0][4]) ).strftime("%s"))
            
            ps1 = num_pattern_T.findall( pm_content )
            if ( len(ps1) < 0 ):
                continue
            
            num_t = germanWordToInt(ps1[0])
            if num_t is False:
                continue
            
            ps2 = num_pattern_R.findall( pm_content )
            
            num_r = germanWordToInt(ps2[0]) if len(ps2) >= 1 else -1
            if num_r is False:
                num_r = -1
                
            ps3 = num_pattern_D.findall( pm_content )
            num_d = germanWordToInt(ps3[0]) if len(ps3) >= 1 else -1
            if num_d is False:            
                num_d = -1
                
            if ( num_d == -1 ):
                num_d = deceased_cnt
            else:
                deceased_cnt = num_d
            
        num_h = -1
        num_s = -1
               
        return [timestamp, num_t, num_r, num_d, num_h, num_s]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_hbn.csv"
    URL = 'https://www.landkreis-hildburghausen.de/Aktuelles-Covid-19/Aktuelles-zu-Covid-19-im-Landkreis/Aktuelle-Meldungen-aus-dem-Landkreis'
    
    num_latest = getHBNNumbers(URL)
    
    if (num_latest != False) and (num_latest[1] > -1):
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        last_values = raw_data[-1].split(",")[1:6]
        
        # check for changes
        value_changed = False
        for i in enumerate(last_values):
            if ( int(i[1]) != num_latest[i[0]+1] ):
                if ( ( num_latest[i[0]+1] != -1 ) and ( i[0] != 2 ) ):
                    value_changed = True
                
        # deceased number is not always included in new reports
        if value_changed:
            num_latest[3] = max(num_latest[3], int(last_values[2]))
            
        if value_changed:
            # write new csv data
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], num_latest[5], URL))
            f.close()
