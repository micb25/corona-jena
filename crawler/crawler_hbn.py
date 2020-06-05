#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os


def germanWordToInt(w):   
    if re.match("^[0-9]{1,}$", w) is not None:
        return int(w)
    else:        
        s = w.lower()        
        number_dict = {
                    "eine": 1, "einer": 1, "ein": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10,
                    "elf": 11, "zwölf": 12, "dreizehn": 13, "vierzehn": 14, "fünfzehn": 15, "sechzehn": 16, "siebzehn": 17, "achtzehn": 18, "neunzehn": 19, "zwanzig": 20,
                    "einundzwanzig": 21, "zweiundzwanzig": 22, "dreiundzwanzig": 23, "vierundzwanzig": 24, "fünfundzwanzig": 25, "sechsundzwanzig": 26, "siebenundzwanzig": 27, "achtundzwanzig": 28, "neunundzwanzig": 29, "dreißig": 30,
                    "einunddreißig": 31, "zweiunddreißig": 32, "dreiunddreißig": 33, "vierunddreißig": 34, "fünfunddreißig": 35, "sechsunddreißig": 36, "siebenunddreißig": 37, "achtunddreißig": 38, "neununddreißig": 39, "vierzig": 40,
                    "einundvierzig": 41, "zweiundvierzig": 42, "dreiundvierzig": 43, "vierundvierzig": 44, "fünfundvierzig": 45, "sechsundvierzig": 46, "siebenundvierzig": 47, "achtundvierzig": 48, "neunundvierzig": 49, "fünfzig": 50,
                    "einundfünfzig": 51, "zweiundfünfzig": 52, "dreiundfünfzig": 53, "vierundfünfzig": 54, "fünfundfünfzig": 55, "sechsundfünfzig": 56, "siebenundfünzig": 57, "achtundfünfzig": 58, "neunundfünzig": 59, "sechzig": 60,
                    "einundsechzig": 61, "zweiundsechzig": 62, "dreiundsechzig": 63, "vierundsechzig": 64, "fünfundsechzig": 65, "sechsundsechzig": 66, "siebenundsechzig": 67, "achtundsechzig": 68, "neunundsechzig": 69, "siebzig": 70
                }        
        for n in number_dict:
            if ( s == n ):
                return number_dict[n]
        return False
    

def getHBNNumbers(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    pattern_PM = re.compile(r"<h2 class=\"toggler-title\">([0-9][^<]*Fallzahlen[^<]*)<\/h2>(.*?)</div>", re.DOTALL)
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
        
        pms = pattern_PM.findall( r.text )
        pms.reverse()
        
        for pm in pms:
            pm_content = pm[1]
            
            for entry in replace_array:
                pm_content = pm_content.replace(entry, "")
                
            for entry in html_replace_dict:
                pm_content = pm_content.replace(entry, html_replace_dict[entry])
                
            pd = pattern_date.findall( pm_content )
            
            if ( len(pd) < 1 ):
                continue
                            
            timestamp = int(datetime.datetime(int(pd[0][2]), int(pd[0][1]), int(pd[0][0]), int(pd[0][3]), int(pd[0][4]) ).strftime("%s"))
            
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
                if ( num_latest[i[0]+1] != -1 ):
                    value_changed = True
        
        if value_changed:
            # write new csv data
            f = open(DATAFILE, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (num_latest[0], num_latest[1], num_latest[2], num_latest[3], num_latest[4], num_latest[5], URL))
            f.close()
