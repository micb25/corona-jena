#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, requests, re, os, sys, json, hashlib


def getFilteredJSONdata(url):
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    replace_pattern = re.compile(r"var\ json_[^\s]*? = ({.*})")
        
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        s = r.text.replace("\r", "").replace("\n", "")
        
        rp = replace_pattern.findall(s)
        if ( len(rp) > 0 ):
            return [json.loads(rp[0].encode('utf-8')), rp[0]]
        
    except:
        return [False, False]
    return [False, False]
    

if __name__ == "__main__":
    
    DATAFOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../data/schools/"
    CSVFILE = DATAFOLDER + "TH_schools.csv"
    
    verbose = False
    
    BASEURL = "https://bildung.thueringen.de/fileadmin/otc/Karte/data/"    
    URLs = [ 
            "KitaStufeGRN_3.js",
            "KitaStufeGELB_4.js",
            "KitaStufeROT_5.js",
            "SchuleStufeGRN_6.js",
            "SchuleStufeGELB_7.js",
            "SchuleStufeROT_8.js"
    ]
    
    collected_data = []
    str_data = ""
    
    for url in URLs:
        # get data
        basename = url.replace(".js", "")
        data, str_data_url = getFilteredJSONdata(BASEURL + url)
        
        if data != False:
            # merge data
            data_category = {}
            data_category['name'] = basename
            data_category['data'] = data
            str_data += str_data_url
            
            collected_data.append( data_category )
        else:
            if verbose: print("Error downloading '{}'".format(url))
            sys.exit(0)
            
    num_data = [0] * (len(collected_data) + 2)
    num_data[0] = int( datetime.datetime.now().timestamp() ) # timestamp
    num_data[1] = hashlib.sha1(str_data.encode('utf-8')).hexdigest()  # SHA1 checksum
        
    for i, line in enumerate(collected_data):
        num_data[i+2] = len(line['data']['features'])
        
    # get old values
    with open(CSVFILE, 'r') as df:
        raw_data = df.read().splitlines()
        last_checksum = raw_data[-1].split(",")[1]
    
    # check for changed data
    if num_data[1] != last_checksum:
        
        if verbose:
            print("data changed!")
            
        # write statistics
        with open(CSVFILE, 'a') as f:
            f.write("%i,%s,%i,%i,%i,%i,%i,%i\n" % (num_data[0], num_data[1], num_data[2], num_data[3], num_data[4], num_data[5], num_data[6], num_data[7]))
            f.close()
        
        # write data
        filename = "TH_schools_data_{}.json".format( datetime.datetime.fromtimestamp( num_data[0] ).strftime("%Y-%m-%d_%H-%M") )
        with open(DATAFOLDER + filename, 'w', encoding='utf-8') as f:
            json.dump(collected_data, f, ensure_ascii=False)
    