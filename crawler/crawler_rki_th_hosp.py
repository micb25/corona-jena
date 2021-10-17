#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def getRKIHospitalizationData():

    URL = 'https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Hospitalisierungen_in_Deutschland/master/Aktuell_Deutschland_COVID-19-Hospitalisierungen.csv'
    
    # read dataframe
    df = pd.read_csv(URL)

    # prepare dataframe
    df.drop(df[ df.Bundesland != 'Thüringen'  ].index  , axis=0, inplace=True)
    df.drop(['Bundesland_Id', 'Bundesland'], axis=1, inplace=True)
    df.fillna(-1, inplace=True)
    df['7T_Hospitalisierung_Faelle'] = df['7T_Hospitalisierung_Faelle'].astype(int)
    df['Timestamp'] = df['Datum'].apply(lambda r: pd.Timestamp(r) )
    df['Timestamp'] = df['Timestamp'].astype(int) / 10**9
    df['Timestamp'] = df['Timestamp'].astype(int)
    df.drop('Datum', axis=1, inplace=True)
    df['Altersgruppe'] = df['Altersgruppe'].astype('category')

    # zero-fill
    ags = list(df['Altersgruppe'].unique())
    min_date = df['Timestamp'].min()
    for i in range(1, 10):
        for ag in ags:
            zero_row = { 'Timestamp': min_date - i * 86400, 'Altersgruppe': ag, '7T_Hospitalisierung_Faelle': 0, '7T_Hospitalisierung_Inzidenz': 0.00 }
            df = df.append(zero_row, ignore_index=True)

    # sort rows
    df.sort_values(by=['Timestamp', 'Altersgruppe'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # sort columns
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    # calculate cases by day
    df['Hospitalisierung_Faelle'] = df['Timestamp'].apply(lambda r: 0 if (r <= min_date) else -1 )
    df['Hospitalisierung_Summe'] = 0
    for ag in ags:
        df_sub = df[ df.Altersgruppe == ag ]
        sum_cases = 0
        for i, r in df_sub.iterrows():
            if ( r['Timestamp'] >= min_date ):
                prev_row = df_sub.iloc[df_sub.index.get_loc(i)-1]
                prev_week = df_sub.iloc[df_sub.index.get_loc(i)-7]
                hosp_cases = r['7T_Hospitalisierung_Faelle'] - prev_row['7T_Hospitalisierung_Faelle'] + prev_week['Hospitalisierung_Faelle']
                sum_cases += hosp_cases
                df_sub.at[i, 'Hospitalisierung_Faelle'] = hosp_cases
                df.at[i, 'Hospitalisierung_Faelle'] = hosp_cases
                df.at[i, 'Hospitalisierung_Summe'] = sum_cases

    # drop zero-fill
    df.drop(df[ df.Timestamp < min_date ].index  , axis=0, inplace=True)

    # export data
    df.to_csv('../data/RKI_TH_Hospitalisierung.csv', float_format='%.2f', sep=",", decimal=".", encoding='utf-8', index=False)


if __name__ == "__main__":

    getRKIHospitalizationData()

