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

    # sort rows
    df.sort_values(by=['Timestamp', 'Altersgruppe'], inplace=True)

    # sort columns
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    # calculate average cases by day 
    df['Hospitalisierung_Faelle'] = df['7T_Hospitalisierung_Faelle'] / 7

    # export data
    df.to_csv('../data/RKI_TH_Hospitalisierung.csv', float_format='%.2f', sep=",", decimal=".", encoding='utf-8', index=False)


if __name__ == "__main__":

    getRKIHospitalizationData()

