#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv, pandas as pd


if __name__ == "__main__":
    
    SCRIPTPATH  = os.path.dirname(os.path.realpath(__file__))
    SOURCEPATH  = SCRIPTPATH + '/../data/'
    SOURCEFILE  = SOURCEPATH + 'cases_rki_db_th.csv'
    OUTPUTFILE  = SOURCEPATH + 'rki_th_by_date/cases_by_day_and_age.csv'
    OUTPUTFILE2 = SOURCEPATH + 'rki_th_by_date/new_cases_by_day_and_age.csv'
    OUTPUTFILE3 = SOURCEPATH + 'rki_th_by_date/incidence_by_day_and_age.csv'
        
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
                # use either 'Meldedatum' or 'Erkrankungsbeginn'
                # timestamp = min(row[row_index_meldedatum], row[row_index_refdatum])            
                
                # use 'Meldedatum'
                timestamp = row[row_index_meldedatum]
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
    
    inc_data_a = []
    inc_data_f = []
    inc_data_m = []    
    
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
            
            if current_timestamp > sorted_cases_th[0][0]:
                inc_data_a.append( [current_timestamp, 'A', arr_a[0]-data_a[-1][2], arr_a[1]-data_a[-1][3], arr_a[2]-data_a[-1][4], arr_a[3]-data_a[-1][5], arr_a[4]-data_a[-1][6], arr_a[5]-data_a[-1][7] ] )
                inc_data_f.append( [current_timestamp, 'F', arr_f[0]-data_f[-1][2], arr_f[1]-data_f[-1][3], arr_f[2]-data_f[-1][4], arr_f[3]-data_f[-1][5], arr_f[4]-data_f[-1][6], arr_f[5]-data_f[-1][7] ] )
                inc_data_m.append( [current_timestamp, 'M', arr_m[0]-data_m[-1][2], arr_m[1]-data_m[-1][3], arr_m[2]-data_m[-1][4], arr_m[3]-data_m[-1][5], arr_m[4]-data_m[-1][6], arr_m[5]-data_m[-1][7] ] )
            
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
    
    csv_header = "timestamp,gender,A00-A04,A05-A14,A15-A34,A35-A59,A60-A79,A80+,ALL\n"
    csv_data = csv_header
    for i, r in enumerate(inc_data_a):
        csv_data += "{},{},{},{},{},{},{},{},{}\n".format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], sum(r[2:8]))
        f = inc_data_f[i]
        csv_data += "{},{},{},{},{},{},{},{},{}\n".format(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], sum(f[2:8]))
        m = inc_data_m[i]
        csv_data += "{},{},{},{},{},{},{},{},{}\n".format(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], sum(m[2:8]))
        
    with open(OUTPUTFILE2, 'w') as csvfile:
        csvfile.write(csv_data)
        csvfile.close()
        
    genders = ['A', 'F', 'M']
    columns = ['A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+', 'ALL']
    pop = {
            'A_ALL': 2133378,
            'F_ALL': 1077382,
            'M_ALL': 1055996,
            
            'A_A00-A04': 90338,
            'F_A00-A04': 44119,
            'M_A00-A04': 46219,
            
            'A_A05-A14': 181978,
            'F_A05-A14': 88419,
            'M_A05-A14': 93559,
            
            'A_A15-A34': 397268,
            'F_A15-A34': 187832,
            'M_A15-A34': 209436,
            
            'A_A35-A59': 733338,
            'F_A35-A59': 353489,
            'M_A35-A59': 379849,
            
            'A_A60-A79': 560974,
            'F_A60-A79': 296464,
            'M_A60-A79': 264510,
            
            'A_A80+': 169482,
            'F_A80+': 107059,
            'M_A80+': 62423
    }
        
    df = pd.read_csv(OUTPUTFILE2, sep=',', decimal='.', encoding='utf-8')
    df['timestamp'] = df.apply(lambda r: int(r['timestamp']/86400)*86400, axis=1)
    
    for c in columns:
        df['inc_{}'.format(c)] = 0
    
    df_a = df.loc[df.gender == 'A']
    df_f = df.loc[df.gender == 'F']
    df_m = df.loc[df.gender == 'M']
    
    for c in columns:
    
        ser_a  = df_a[c].rolling(min_periods=1, window=7).sum().div( pop['{}_{}'.format('A', c)] / 100000 )
        for i in ser_a.index.tolist():
            df.loc[i, 'inc_{}'.format(c)] = ser_a[i]
            
        ser_f  = df_f[c].rolling(min_periods=1, window=7).sum().div( pop['{}_{}'.format('F', c)] / 100000 )
        for i in ser_f.index.tolist():
            df.loc[i, 'inc_{}'.format(c)] = ser_f[i]
            
        ser_m  = df_m[c].rolling(min_periods=1, window=7).sum().div( pop['{}_{}'.format('M', c)] / 100000 )
        for i in ser_m.index.tolist():
            df.loc[i, 'inc_{}'.format(c)] = ser_m[i]
        
    df.drop(columns, inplace=True, axis=1)
    df.to_csv(OUTPUTFILE3, sep=',', decimal='.', encoding='utf-8', float_format='%.2f', index=False)
    