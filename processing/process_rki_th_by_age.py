#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, csv


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    SOURCEPATH = SCRIPTPATH + '/../data/'
    SOURCEFILE = SOURCEPATH + 'cases_rki_db_th.csv'
    OUTPUTFILE = SOURCEPATH + 'rki_th_by_date/cases_by_day_and_age.csv'
        
    row_index_meldedatum = -1
    row_index_refdatum = -1
    row_index_district = -1
    row_index_age_group = -1
    row_index_num_cases = -1
    
    cases_th = []
    timestamp_array = []
    age_groups = []
    
    # RKI DB analysis
    with open(SOURCEFILE, 'r') as csvfile:
        raw_data = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # get header and columns
        header = next(raw_data)
        row_index_meldedatum = header.index('Meldedatum')
        row_index_refdatum   = header.index('Refdatum')
        row_index_gender     = header.index('Geschlecht')
        row_index_age_group  = header.index('Altersgruppe')
        row_index_num_cases  = header.index('AnzahlFall')
        
        # iterate all cases
        for row in raw_data:
            num_cases = int(row[row_index_num_cases])
            for i in range (num_cases):
                timestamp = min(row[row_index_meldedatum], row[row_index_refdatum])            
                age_group = row[row_index_age_group]
                cases_th.append( [timestamp, row[row_index_gender], age_group ] )
            
                if age_group not in age_groups:
                    age_groups.append( age_group )
            
                if timestamp not in timestamp_array:
                    timestamp_array.append( timestamp )
    
    # generate dict of cases by age_group
    cases_per_age_group_a = {}
    cases_per_age_group_f = {}
    cases_per_age_group_m = {}
    for age_group in age_groups:
        cases_per_age_group_a[age_group] = 0
        cases_per_age_group_f[age_group] = 0
        cases_per_age_group_m[age_group] = 0
        
    # sort data by date
    sorted_timestamp_array = sorted(timestamp_array, key=lambda t: t[0])
    sorted_cases_th = sorted(cases_th, key=lambda t: t[0])
    
    data_a = []
    data_f = []
    data_m = []    
    
    current_timestamp = sorted_cases_th[0][0]
    for case in sorted_cases_th:
        if case[0] > current_timestamp:
            arr_a = [ 
                        cases_per_age_group_a['A00-A04'], cases_per_age_group_a['A05-A14'], 
                        cases_per_age_group_a['A15-A34'], cases_per_age_group_a['A35-A59'], 
                        cases_per_age_group_a['A60-A79'], cases_per_age_group_a['A80+'] 
                    ]
            
            arr_f = [ 
                        cases_per_age_group_f['A00-A04'], cases_per_age_group_f['A05-A14'], 
                        cases_per_age_group_f['A15-A34'], cases_per_age_group_f['A35-A59'], 
                        cases_per_age_group_f['A60-A79'], cases_per_age_group_f['A80+'] 
                    ]
            arr_m = [ 
                        cases_per_age_group_m['A00-A04'], cases_per_age_group_m['A05-A14'], 
                        cases_per_age_group_m['A15-A34'], cases_per_age_group_m['A35-A59'], 
                        cases_per_age_group_m['A60-A79'], cases_per_age_group_m['A80+'] 
                    ]
            data_a.append( [current_timestamp, 'A', arr_a[0], arr_a[1], arr_a[2], arr_a[3], arr_a[4], arr_a[5] ] )
            data_f.append( [current_timestamp, 'F', arr_f[0], arr_f[1], arr_f[2], arr_f[3], arr_f[4], arr_f[5] ] )
            data_m.append( [current_timestamp, 'M', arr_m[0], arr_m[1], arr_m[2], arr_m[3], arr_m[4], arr_m[5] ] )
            
        cases_per_age_group_a[case[2]] += 1
        if case[1] == 'W':
            cases_per_age_group_f[case[2]] += 1
        elif case[1] == 'M':
            cases_per_age_group_m[case[2]] += 1   
            
        current_timestamp = case[0]
    
    csv_header = "timestamp,gender,A00-A04,A05-A14,A15-A34,A35-A59,A60-A79,A80+\n"
    csv_data = csv_header
    for i, r in enumerate(data_a):
        csv_data += "{},{},{},{},{},{},{},{}\n".format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        f = data_f[i]
        csv_data += "{},{},{},{},{},{},{},{}\n".format(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7])
        m = data_m[i]
        csv_data += "{},{},{},{},{},{},{},{}\n".format(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7])
    
    
    with open(OUTPUTFILE, 'w') as csvfile:
        csvfile.write(csv_data)
        csvfile.close()
    