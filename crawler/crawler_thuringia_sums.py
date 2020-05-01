#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os


def strToTimestamp(datetimestr):    
    s = datetimestr.replace("Uhr", "").strip()
    
    # fix dates without hours
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


def parseTHBulletinTable(text):

    num_pattern_T1 = re.compile(r"<tr><td>(?:<strong>)?Gesamtzahl der Infizierten:\s?(?:<\/strong>)?</td><td>(?:<strong>)?([0-9]{1,})(?:<\/strong>)?</td></tr>")
    num_pattern_R1 = re.compile(r"<tr><td>(?:<strong>)?.*?(?:Gesamtzahl\ der\ Genesenen|Anzahl\ Genesene).*?(?:<\/strong>)?</td><td>(?:<strong>)?([0-9]{1,})(?:<\/strong>)?</td></tr>")
    num_pattern_R2 = re.compile(r"von\ ([0-9]{1,})\ Genesenen")
    num_pattern_D1 = re.compile(r"[vV]erstorbene.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?<\/td>")
    num_pattern_HI = re.compile(r"Patienten\ stationär\ \/\ Gesamt.*?</td><td.*?>(?:<strong>|<p>)?([\+\-0-9]{1,})(?:<\/strong>|<\/p>)?<\/td>")
    num_pattern_HC = re.compile(r"Patienten\ stationär\ \/\ aufgrund.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?<\/td>")
    num_pattern_S1 = re.compile(r"[sS]chwere Verläufe.*?</td><td.*?>(?:<strong>)?([\+\-0-9]{1,})(?:<\/strong>)?<\/td>")
            
    try:
        ps1  = num_pattern_T1.findall( text )
        ps2A = num_pattern_R1.findall( text )
        ps2B = num_pattern_R2.findall( text )
        ps3  = num_pattern_D1.findall( text )
        ps4  = num_pattern_HI.findall( text )
        ps5  = num_pattern_HC.findall( text )
        ps6  = num_pattern_S1.findall( text )
                                        
        num_t  = int(ps1[0])  if (len(ps1) >= 1) else -1
        num_r  = int(ps2A[0]) if (len(ps2A) >= 1) else ( int(ps2B[0]) if (len(ps2B) >= 1) else -1 )
        num_d  = int(ps3[0])  if (len(ps3) >= 1) else -1
        num_hi = int(ps4[0])  if (len(ps4) >= 1) else -1
        num_hc = int(ps5[0])  if (len(ps5) >= 1) else -1
        num_s  = int(ps6[0])  if (len(ps6) >= 1) else -1
        
        return (num_t, num_r, num_d, num_hi, num_hc, num_s)
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_th_sums.csv"
    URL = 'https://corona.thueringen.de/covid-19-bulletin/'
    
    # RE pattern for bulletin
    bulletin_pattern = re.compile(r"<h[23].*?>.*?\(Stand:?\s(.*?)\).*?<\/h[23]>(.*?<table.*?>.*?)<\/table>")
        
    # do the request
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    r = requests.get(URL, headers=headers, allow_redirects=True, timeout=5.0)
    s = r.text.replace("\t", "")
    
    # parse data
    bulletin_rawdata = bulletin_pattern.findall( s )
    
    if ( len(bulletin_rawdata) > 0 ):
        
        entry = bulletin_rawdata[0]
        
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        timestamp_last = int(raw_data[-1].split(",")[0])
        
        # get latest values
        data = parseTHBulletinTable(entry[1].replace(".", ""))
                        
        new_record = {}
        new_record[0] = int(strToTimestamp(entry[0]))
        
        # 28.04.2020: fix for incorrect date
        if ( data[0] == 2145 ):
            new_record[0] = int(strToTimestamp("28. April 2020"))
            
        # 01.05.2020: fix for incorrect date
        if ( data[0] == 2323 ):
            new_record[0] = int(strToTimestamp("01. Mai 2020"))
        
        for i in range(len(data)):
            new_record[i+1] = data[i]
        new_record[len(new_record)] = URL
        
        if ( new_record[0] > timestamp_last ):
            
            # generate csv line
            data_str = ""
            for i in range(len(new_record)):
                data_str += ("" if i == 0 else "," ) + (new_record[i] if isinstance(new_record[i], str) else str(new_record[i]))
            
            # write new data
            f = open(DATAFILE, 'a')            
            f.write("%s\n" % (data_str))
            f.close()
            