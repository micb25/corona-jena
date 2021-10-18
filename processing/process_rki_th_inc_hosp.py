#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def processIncHospData():

    CSV_INC  = "../data/rki_th_by_date/incidence_by_day_and_age.csv"
    CSV_HOSP = "../data/RKI_TH_Hospitalisierung.csv"

    dfi = pd.read_csv(CSV_INC)
    dfi.drop('inc_ALL', axis=1, inplace=True)
    dfi.drop(dfi[ dfi.gender != "A" ].index, axis=0, inplace=True)
    dfi.drop('gender', axis=1, inplace=True)

    dfi['timestamp'] = dfi['timestamp'].apply(lambda x: (x//86400)*86400)

    cols = list(dfi.columns)
    cols.remove('timestamp')

    for c in cols:
        col_name = c.replace('inc_', '').replace('A', '')
        dfi[col_name] = dfi[c].rolling(window=7).mean()
        dfi[col_name] = dfi[col_name].fillna(0)
        dfi.drop(c, axis=1, inplace=True)

    dfh = pd.read_csv(CSV_HOSP)
    dfh.drop(dfh[ dfh.Altersgruppe == "00+" ].index, axis=0, inplace=True)
    dfh.drop(['7T_Hospitalisierung_Faelle', 'Hospitalisierung_Faelle', 'Hospitalisierung_Summe'], axis=1, inplace=True)
    dfh['Timestamp'] = dfh['Timestamp'].apply(lambda x: (x//86400)*86400)

    dfh['7T_Inzidenz'] = -1.0
    for i, r in dfh.iterrows():
        ts = r['Timestamp']
        ag = r['Altersgruppe']

        dfi_sub = dfi[ dfi.timestamp == ts ]
        if ( len(dfi_sub) > 0 ):
            dfh.at[i, '7T_Inzidenz'] = dfi_sub.iloc[-1][ag]

    dfh.to_csv('../data/RKI_TH_Inc_Hosp_Correlation.csv', float_format='%.2f', sep=",", decimal=".", encoding='utf-8', index=False)

    return



if __name__ == "__main__":

    processIncHospData()
