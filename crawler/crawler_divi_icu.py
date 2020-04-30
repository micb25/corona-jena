#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, os, requests, datetime


def get_divi_statistics(URL):
    headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

    pattern_date = re.compile(r"Stand: ([0-9:\.\s\/]*)<")

    pattern_th_beds_occ  = re.compile(r"<text id=\"Text_67\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_th_beds_free = re.compile(r"<text id=\"Text_84\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_th_c19_cases = re.compile(r"<text id=\"Text_16\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_th_c19_vent  = re.compile(r"<text id=\"Text_33\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    
    pattern_ger_beds_occ  = re.compile(r"<text id=\"Text_51\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_ger_beds_free = re.compile(r"<text id=\"Text_68\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_ger_c19_cases = re.compile(r"<text x=\"488.33\" y=\"269.19\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    pattern_ger_c19_vent  = re.compile(r"<text id=\"Text_17\"[^>]*?>[\n\s]*?([\.\d]*)[\n\s]*?</text>")
    
    result_array = []
    
    try:    
        r = requests.get(URL, headers=headers, allow_redirects=True, timeout=5.0)
        
        if r.status_code != 200:
            return False
        
        svgdata = r.text
        
        # get timestamp
        pd = pattern_date.findall(svgdata)
        if len(pd) < 1:
            return False
        
        dt = datetime.datetime.strptime(pd[0], "%d.%m.%Y / %H:%M")
        timestamp = int(dt.strftime("%s"))
        result_array.append(timestamp)
        
        # get data for TH
        ps_th1 = pattern_th_beds_occ.findall(svgdata)
        ps_th2 = pattern_th_beds_free.findall(svgdata)
        ps_th3 = pattern_th_c19_cases.findall(svgdata)
        ps_th4 = pattern_th_c19_vent.findall(svgdata)
        
        if ( len(ps_th1) < 1 ) or ( len(ps_th2) < 1 ) or ( len(ps_th3) < 1) or ( len(ps_th4) < 1 ):
            return False
        
        num_th1 = int(ps_th1[0].replace(".", ""))
        num_th2 = int(ps_th2[0].replace(".", ""))
        num_th0 = num_th1 + num_th2
        num_th3 = int(ps_th3[0].replace(".", ""))
        num_th4 = int(ps_th4[0].replace(".", ""))
        
        result_array.append([num_th0, num_th1, num_th2, num_th3, num_th4])
        
        # get data for Germany
        ps_ger1 = pattern_ger_beds_occ.findall(svgdata)
        ps_ger2 = pattern_ger_beds_free.findall(svgdata)
        ps_ger3 = pattern_ger_c19_cases.findall(svgdata)
        ps_ger4 = pattern_ger_c19_vent.findall(svgdata)
        
        if ( len(ps_ger1) < 1 ) or ( len(ps_ger2) < 1 ) or ( len(ps_ger3) < 1) or ( len(ps_ger4) < 1 ):
            return False
        
        num_ger1 = int(ps_ger1[0].replace(".", ""))
        num_ger2 = int(ps_ger2[0].replace(".", ""))
        num_ger0 = num_ger1 + num_ger2
        num_ger3 = int(ps_ger3[0].replace(".", ""))
        num_ger4 = int(ps_ger4[0].replace(".", ""))
        
        result_array.append([num_ger0, num_ger1, num_ger2, num_ger3, num_ger4])
    
        return result_array
    except:
        return False
    

if __name__ == "__main__":

    # source
    URL = "https://diviexchange.z6.web.core.windows.net/laendertabelle1.svg"
    
    # data folder
    DATAFOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../data/divi_db_th/"
    DATAFILE1  = DATAFOLDER + "divi_data_th.csv"
    DATAFILE2  = DATAFOLDER + "divi_data_germany.csv"
    
    num_latest = get_divi_statistics(URL)
    
    if (num_latest != False):
        
        # get old values for TH
        with open(DATAFILE1, 'r') as df:
            raw_data = df.read().splitlines()
        last_values = raw_data[-1].split(",")[1:5]
        
        # check for changes for TH
        value_changed = False
        for i in enumerate(last_values):
            if ( int(i[1]) != num_latest[1][i[0]] ):
                if ( num_latest[1][i[0]] != -1 ):
                    value_changed = True
        
        if value_changed:
            # write new csv data
            f = open(DATAFILE1, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (num_latest[0], num_latest[1][0], num_latest[1][1], num_latest[1][2], num_latest[1][3], num_latest[1][4], URL))
            f.close()
            
        # get old values for Germany
        with open(DATAFILE2, 'r') as df:
            raw_data = df.read().splitlines()
        last_values = raw_data[-1].split(",")[1:5]
        
        # check for changes for TH
        value_changed = False
        for i in enumerate(last_values):
            if ( int(i[1]) != num_latest[2][i[0]] ):
                if ( num_latest[2][i[0]] != -1 ):
                    value_changed = True
                    
        if value_changed:
            # write new csv data
            f = open(DATAFILE2, 'a')
            f.write("%i,%i,%i,%i,%i,%i,%s\n" % (num_latest[0], num_latest[2][0], num_latest[2][1], num_latest[2][2], num_latest[2][3], num_latest[2][4], URL))
            f.close()
