#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, requests, csv, urllib.parse


def rki_db_query(offset = 0, chunk_size = 8000):
    
    # RKI databases: 
    # - Coronafälle_in_den_Bundesländern
    # - Covid19_RKI_Sums
    #       AnzahlFall, AnzahlTodesfall, SummeFall	, SummeTodesfall, ObjectId, Datenstand, Meldedatum	,
    #       Bundesland, IdBundesland, Landkreis, IdLandkreis, AnzahlGenesen	, SummeGenesen
    # - Deutschland_Bundesländergrenzen_2018
    # - Inzidenzen
    # - RKI_COVID19:
    #       IdBundesland, Bundesland, Landkreis, Altersgruppe, Geschlecht, AnzahlFall, AnzahlTodesfall, ObjectId, Meldedatum, IdLandkreis,
    #       Datenstand, NeuerFall, NeuerTodesfall, Refdatum, NeuGenesen, AnzahlGenesen
    # - RKI_Landkreisdaten  
    
    url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?'
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }

    qry_params = urllib.parse.urlencode(
    {
            "where": "IdBundesland=16", # Thuringia only
            "outFields": "Meldedatum,Landkreis,SummeFall,SummeGenesen,SummeTodesfall,AnzahlFall,AnzahlGenesen,AnzahlTodesfall",
            "returnGeometry": "false",
            "orderByFields": "Landkreis asc",
            "resultOffset": offset,
            "resultRecordCount": chunk_size,
            "f": "json"
        }
    )
    
    url += qry_params
    
    try:    
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        
        if r.status_code != 200:
            return False
        
        return r.json()
        
    except:
        return False
    

if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_th_rki_sums.csv"
    
    data = rki_db_query()
    
    if data == False:
        sys.exit()

    header = data["fields"]
    header = [h["name"] for h in header]
    
    # remove 'ObjectId' field
    header.remove("ObjectId")
    
    index_date = 0
    for h in enumerate(header):
        if ( h[1] == 'Meldedatum' ):
            index_date = h[0]
        
    try:
        
        f = csv.writer(open(DATAFILE, "w+"))
        f.writerow(header)
        
        offset = 0
        chunk_size = 2000
        while(True):
            
            data = rki_db_query(offset=offset, chunk_size=chunk_size)
            
            cases = data["features"]
            
            if not cases:
                break
            
            for c in cases:
                row = [c["attributes"][h] for h in header]
                row[index_date] = int(row[index_date] / 1000.0)
                f.writerow(row)
            
            offset += chunk_size
        
    except:
        sys.exit()
    
