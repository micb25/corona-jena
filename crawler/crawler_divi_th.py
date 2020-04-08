#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, requests, datetime


def bed_status_to_int(s):
    str_array = {"NICHT_VERFUEGBAR", "BEGRENZT", "VERFUEGBAR"}    
    for i in enumerate(str_array):
        if ( s == i[1] ):
            return i[0]
    return -1 # None


def divi_db_query(state = "THUERINGEN"):
    URL = "https://www.intensivregister.de/api/public/intensivregister?page=0&bundesland="
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:    
        r = requests.get(URL + state, headers=headers, allow_redirects=True, timeout=5.0)
        
        if r.status_code != 200:
            return False        
        return r.json()
    except:
        return False
    
def divi_records_to_csv(new_data):
    try:
        data_str = ""
        unsorted_data = []
        
        for i in range(0, new_data['rowCount']):
            data_set = new_data['data'][i]
            data_row = {}            
            data_row[0] = int(datetime.datetime.strptime(new_data['data'][i]['meldezeitpunkt'], "%Y-%m-%dT%H:%M:%SZ").timestamp())
            data_row[1] = int(data_set['id'])
            data_row[2] = "\"" + data_set['krankenhausStandort']['bezeichnung'].replace("\"", "'") + "\""
            data_row[3] = int(data_set['faelleCovidAktuell'])            
            data_row[4] = bed_status_to_int(data_set['bettenStatus']['statusLowCare'])
            data_row[5] = bed_status_to_int(data_set['bettenStatus']['statusHighCare'])
            data_row[6] = bed_status_to_int(data_set['bettenStatus']['statusECMO'])
            
            unsorted_data.append(data_row)
            
        sorted_data = sorted(unsorted_data, key=lambda a_entry: a_entry[0]) 
        
        # write csv header to str        
        header = ["timestamp", "id", "name", "faelle", "statusLowCare", "statusHighCare", "statusECMO"]
        for column in header:
            data_str += ("," if column != header[0] else "" ) + column 
        data_str += "\n"     
        
        # write csv data to str
        for row in sorted_data:
            for i in range(len(row)):
                data_str += ("" if i == 0 else "," ) + (row[i] if isinstance(row[i], str) else str(row[i]))
            data_str += "\n"
            
        return data_str
    
    except:
        return False
    

if __name__ == "__main__":

    # data folder
    DATAFOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../data/divi_db_th/"

    # initialization
    now = datetime.datetime.now()
    file_prefix = now.strftime("divi_db_th_%d.%m.%Y_")
    old_data = ""
    last_file = ""
    last_file_index = 0
    
    # check for old files, but always do a full copy at midnight    
    for i in range(1, 25):
        if ( os.path.isfile("%s%s%02i.csv" % (DATAFOLDER, file_prefix, i)) ):
            last_file_index = i
            
    # new filename
    filename = "%s%s%02i.csv" % (DATAFOLDER, file_prefix, last_file_index + 1)
    
    # read old file, if any exists
    if ( last_file_index > 0 ):
        last_file = "%s%s%02i.csv" % (DATAFOLDER, file_prefix, last_file_index)
        with open(last_file, "r") as of:
            old_data = of.read()
            
    # do the request
    new_data = divi_db_query()
        
    if new_data != False:
        
        # convert data to csv
        data_str = divi_records_to_csv(new_data)
                
        # write everything to the new file, but only if content is different
        if (data_str != False) and (old_data != data_str):
            with open(filename, "w") as nf:
                nf.write(data_str)
        