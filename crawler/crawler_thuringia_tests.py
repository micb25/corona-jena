#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, requests, re, os, sys, datetime


def week_to_date_min_max_with_1d_offset(mw, year=2020):
    dto_min = datetime.datetime.strptime("{}-{}-{}".format(year, mw-1, 2), '%Y-%W-%w')
    datestr_min = dto_min.strftime("%d.%m.%Y")
    dto_max = datetime.datetime.strptime("{}-{}-{}".format(year, mw, 1), '%Y-%W-%w')
    datestr_max = dto_max.strftime("%d.%m.%Y")
    return [datestr_min, datestr_max]


def parseTestData(text):

    th_date_pattern = re.compile(r"Stand\s([0-9]{1,2}).([0-9]{1,2}).([0-9]{2,4})")
    th_tests_pattern = re.compile(r"([0-9]{1,})\sProben\suntersucht")
    th_capacity_pattern = re.compile(r"Probenkapazität\s.*?([0-9]{1,})\sProben")
            
    try:
        ps1  = th_date_pattern.findall( text )
        ps2  = th_tests_pattern.findall( text.replace(".", "") )
        ps3  = th_capacity_pattern.findall( text.replace(".", "") )
        
        if len(ps1) < 1 or len(ps1[0]) < 2:
            return False
        
        num_c   = -1
        num_t   = int(ps2[0])  if (len(ps2) >= 1) else -1
        num_cap = 7 * int(ps3[0])  if (len(ps3) >= 1) else -1
        num_r   = -1
        
        # get number of cases in this week
        date_day = int(ps1[0][0])
        date_month = int(ps1[0][1])
        date_year = 0
        if len(ps1[0]) < 3:
            date_year = int(ps1[0][2])
        if date_year == 0:
            date_year = 2020
        elif date_year < 2020:
            date_year += 2000
        
        dt = datetime.datetime(year=date_year, month=date_month, day=date_day, hour=10)
        timestamp = int(dt.strftime("%s"))
        week_num = int(datetime.datetime(year=date_year, month=date_month, day=date_day, hour=10).strftime("%V")) - 1
        
        dates = week_to_date_min_max_with_1d_offset(mw=week_num, year=date_year)
        if len(dates) == 2:
            fileA = os.path.dirname(os.path.realpath(__file__)) + "/../data/rki_th_by_date/cases_by_region_" + dates[0] + ".csv"
            fileB = os.path.dirname(os.path.realpath(__file__)) + "/../data/rki_th_by_date/cases_by_region_" + dates[1] + ".csv"
            
            with open(fileA, 'r') as df:
                raw_data = df.read().splitlines()
                cases_A = int(raw_data[-1].split(",")[2])
                
            with open(fileB, 'r') as df:
                raw_data = df.read().splitlines()
                cases_B = int(raw_data[-1].split(",")[2])
                
            num_c = cases_B - cases_A
            num_r = 100.0 * num_c / num_t if num_t > 0 else 0.0
        
        return [timestamp, week_num, num_cap, num_t, num_c, num_r]
    
    except:
        return False  


if __name__ == "__main__":
    
    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/tests_th.csv"
    URL = 'https://www.tmasgff.de/covid-19/testverfahren-und-laborkapazitaeten'
    
    # do the request
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    r = requests.get(URL, headers=headers, allow_redirects=True, timeout=5.0)
    s = r.text.replace("\t", "")
    
    data = parseTestData(s)
    
    if data != False:
        
        # get old values
        with open(DATAFILE, 'r') as df:
            raw_data = df.read().splitlines()
        current_values = raw_data[-1].split(",")[1:6]
        
        if data[1] > int(current_values[0]):
            # generate csv line
            data_str = "{},{},{},{},{},{:.3f},{}".format(data[0], data[1], data[2], data[3], data[4], data[5], URL)
        
            # write new data
            f = open(DATAFILE, 'a')
            f.write("%s\n" % (data_str))
            f.close()
            