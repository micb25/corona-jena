#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, time, requests, re, os


def strToTimestamp(datetimestr):    
    s = datetimestr.replace("Uhr", "").strip()
    
    # fix for dates, since 25.03.
    if re.search(",", s) is None:
        s += ", 10"
            
    months = {"Januar": "1", "Februar": "2", "März": "3", "April": "4", "Mai": "5", "Juni": "6", "Juli": "7", "August": "8", "September": "9", "Oktober": "10", "November": "11", "Dezember": "12" }    
    for key in months.keys():
        s = s.replace(key, months[key])
            
    complex_date_pattern = re.compile(r"([0-9]{1,2})\.\s?([0-9]{1,2})\s?\.?\s?([0-9]{2,4}),?\s?([0-9]{0,2})")

    s = s.replace(".09.21,", ".21,") # hot-fix for "Stand: 05.10.09.21, 0:00 Uhr"
        
    try:    
        pd = complex_date_pattern.findall(s)
        
        timestamp = 0
        if ( len(pd) < 0 ) or ( len(pd[0]) < 3 ):
            return False
        
        date_day   = int(pd[0][0])
        date_month = int(pd[0][1])
        date_year  = int(pd[0][2])
        
        # fix short year notation
        if date_year < 2020:
            date_year += 2000
        
        if len(pd[0]) >= 4:
            date_hour = int(pd[0][3])
        else:
            date_hour = 10
        
        timestamp = int(datetime.datetime(year=date_year, month=date_month, day=date_day, hour=date_hour).strftime("%s"))
        return timestamp
    except:
        return False


def getTHStatistics(url, latest_case_numbers):
    # general patterns
    date_pattern     = re.compile(r"Stand: (.*?)</")
    district_pattern = re.compile(r"(<div class=\"accordion__item\".*?</div></div></div></div></div>)")
    
    # district patterns
    dp_name    = re.compile(r">([a-zäöüÄÖÜßA-Z\s\-]*?)</h3>")
    dp_new_inf = re.compile(r"<li>Neuinfektionen letzte 24h\s?:?\s?([\+\-0-9]{1,})")
    dp_sum_inf = re.compile(r"<li>Infizierte insgesamt\s?:?\s?([\+\-0-9]{1,})")
    dp_hosp    = re.compile(r"Patienten stationär\s?(?:insgesamt)?:?\s([\+\-0-9]{1,})")
    dp_severe  = re.compile(r"schwerer?\s(?:Verläufe|Verlauf)\s?:?\s([\+\-0-9]{1,})")
    dp_dec     = re.compile(r"<li>Verstorbene?\s?:?\s?([\+\-0-9]{1,})")
    
    data_timestamp = 0
    
    try:
        # result buffer
        res = ""
        
        # perform HTML request
        headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        
        # filter some stuff
        raw_text = r.text.replace("\n", "").replace("\r", "").replace("<p>", "").replace("</p>", "").replace("*", "")
        
        # get the timestamp and try to recognize missing updated date labels
        pd = date_pattern.findall( raw_text )
        for date_entry in pd:
            current_timestamp = strToTimestamp(date_entry)
            if current_timestamp > data_timestamp:
                data_timestamp = current_timestamp
                
        # return if date could not be read
        if data_timestamp == 0:
            return False
                
        # get all district data
        pv = district_pattern.findall(raw_text)
        for entry in pv:
            
            entry_str = entry.replace(".", "")
            
            dName = dp_name.findall(entry_str)
            dNew  = dp_new_inf.findall(entry_str)
            dSum  = dp_sum_inf.findall(entry_str)
            dHosp = dp_hosp.findall(entry_str)
            dSev  = dp_severe.findall(entry_str)
            dDec  = dp_dec.findall(entry_str)
            
            d = []
            d.append(dName[0] if len(dName) > 0 else "")
            
            # try to verify/fix per day
            if len(dNew) > 0:
                if (len(dSum) > 0) and (len(dName) > 0):
                    
                    # calculate delta in case numbers
                    delta_cases = int(dSum[0]) - latest_case_numbers[dName[0]]
                    
                    # check if "new cases" entry has not been correctly updated
                    if delta_cases < int(dNew[0]):
                        d.append(delta_cases)
                    else:
                        d.append(int(dNew[0]) if len(dNew) > 0 else -1)
                else:
                    d.append(int(dNew[0]))        
            else:
                if (len(dSum) > 0) and (len(dName) > 0):
                    # calculate delta in case numbers
                    delta_cases = int(dSum[0]) - latest_case_numbers[dName[0]]
                    d.append(delta_cases)
                else:
                    d.append(0)
                
            d.append(int(dSum[0]) if len(dSum) > 0 else -1)
            d.append(int(dHosp[0]) if len(dHosp) > 0 else -1)
            d.append(int(dSev[0]) if len(dSev) > 0 else -1)
            d.append(int(dDec[0]) if len(dDec) > 0 else -1)
                        
            res = res + "%i,%s,%i,%i,%i,%i,%i,%i\n" % (data_timestamp, d[0], d[1], d[2], d[3], d[4], d[5], 0)
        
        return [data_timestamp, res]
    except:
        return False
    
if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_thuringia.csv"
    
    URL = "https://www.tmasgff.de/covid-19/fallzahlen"
    
    # get latest values
    with open(DATAFILE, 'r') as df:
        raw_data = df.read().splitlines()
    current_date = int(raw_data[-1].split(",")[0])
    
    # try to detect mistakes in "new cases since 24h"
    latest_values = {}
    for line in raw_data[1:]:
        entries = line.split(",")
        if int(entries[0]) == current_date:
            latest_values[entries[1]] = int(entries[3])
    
    n = getTHStatistics(URL, latest_values)

    if n != False:
        # write new data
        if ( n[0] > current_date ):
            f = open(DATAFILE, 'a')
            f.write(n[1]) 
            f.close()
