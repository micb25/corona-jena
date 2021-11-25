#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os, sys, datetime


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


def parseTHData(text):

    num_pattern_T1 = re.compile(r"<div class=\"[^\"]{1,}\">\s{0,}Neuinfektionen\s{0,}<\/div>\s{0,}<div class=\"[^\"]{1,}\">\s{0,}([0-9\.]{1,})(?:\s{1,}gesamt)?\s{0,}<\/div>")
    num_pattern_R1 = re.compile(r"<div class=\"[^\"]{1,}\">\s{0,}([0-9\.]{1,})\s{0,}<\/div>\s{0,}<div class=\"[^\"]{1,}\">Genesene<\/div>")
    num_pattern_D1 = re.compile(r"<div class=\"[^\"]{1,}\">Verstorbene<\/div>\s{0,}<div class=\"[^\"]{1,}\">(?:[^<]{1,})?\s{0,}([0-9\.]{4,})(?:\s{1,}gesamt)?\s{0,}<\/div>")
            
    try:
        ps1  = num_pattern_T1.findall( text )
        ps2  = num_pattern_R1.findall( text )
        ps3  = num_pattern_D1.findall( text )
                                        
        num_t  = int(ps1[0])  if (len(ps1) >= 1) else -1
        num_r  = int(ps2[0])  if (len(ps2) >= 1) else -1
        num_d  = int(ps3[0])  if (len(ps3) >= 1) else -1
        
        return [num_t, num_r, num_d, -1, -1, -1]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_th_sums.csv"
    URL = 'https://www.tmasgff.de/covid-19/fallzahlen'
    
    # RE pattern for TMASGFF data
    th_data_pattern = re.compile(r"<main id=\"main\">.*</main>")
    th_date_pattern = re.compile(r"Stand: ([0-9]{1,2}).([0-9]{1,2}).([0-9]{2,4})")
        
    # do the request
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    r = requests.get(URL, headers=headers, allow_redirects=True, timeout=5.0)
    s = r.text.replace("\t", " ").replace("\n", " ")

    # parse data
    rawdata = th_data_pattern.findall( s )
    if ( len(rawdata) > 0 ):
        
        entry = rawdata[0]
        
        # read date
        date_day = date_month = date_year = 0
        rawdate = th_date_pattern.findall( rawdata[0] )
        if len(rawdate) < 1 or len(rawdate[0]) < 2:
            sys.exit(0)
            
        date_day = int(rawdate[0][0])
        date_month = int(rawdate[0][1])
        if len(rawdate[0]) <= 3:
            date_year = int(rawdate[0][2])
        if date_year == 0:
            date_year = datetime.datetime.now().year
        elif date_year < 2020:
            date_year += 2000
        
        timestamp = int(datetime.datetime(year=date_year, month=date_month, day=date_day, hour=10).strftime("%s"))
                
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        timestamp_last = int(raw_data[-1].split(",")[0])
        
        # get latest values
        data = parseTHData(entry.replace(".", ""))
                                
        new_record = {}
        new_record[0] = timestamp
        
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
            