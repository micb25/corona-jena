#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, requests, pandas as pd
from datetime import datetime

class RKI_GitHub:

    BASEURL = "https://media.githubusercontent.com/media/robert-koch-institut/SARS-CoV-2_Infektionen_in_Deutschland/master/Archiv/"
    CSVFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_rki_db_th.csv"
    COLS = "Meldedatum,Datenstand,Landkreis,AnzahlFall,AnzahlTodesfall,NeuerFall,NeuerTodesfall,Geschlecht,Altersgruppe,Refdatum,AnzahlGenesen,NeuGenesen".split(",")

    AGS = {
        16051: "SK Erfurt",
        16052: "SK Gera",
        16053: "SK Jena",
        16054: "SK Suhl",
        16055: "SK Weimar",
        16056: "SK Eisenach",
        16061: "LK Eichsfeld",
        16062: "LK Nordhausen",
        16063: "LK Wartburgkreis",
        16064: "LK Unstrut-Hainich-Kreis",
        16065: "LK Kyffhäuserkreis",
        16066: "LK Schmalkalden-Meiningen",
        16067: "LK Gotha",
        16068: "LK Sömmerda",
        16069: "LK Hildburghausen",
        16070: "LK Ilm-Kreis",
        16071: "LK Weimarer Land",
        16072: "LK Sonneberg",
        16073: "LK Saalfeld-Rudolstadt",
        16074: "LK Saale-Holzland-Kreis",
        16075: "LK Saale-Orla-Kreis",
        16076: "LK Greiz",
        16077: "LK Altenburger Land"
    }

    def get_csv_url(self, isodate=""):
        return "{}{}_Deutschland_SarsCov2_Infektionen.csv".format(RKI_GitHub.BASEURL, isodate if isodate != "" else self.isodate)

    def is_day_available(self, isodate=""):
        URL = self.get_csv_url(isodate)
        r = requests.head(URL)
        return r.status_code == 200

    def was_data_scraped(self, isodate=""):
        try:
            isodatestr = isodate if (isodate != "") else datetime.now().strftime("%Y-%m-%d")
            with open(self.CSVFILE, "r") as csvfile:
                csv_header = csvfile.readline()
                csv_line = csvfile.readline()
                cols = csv_header.split(",")
                fields = csv_line.split(",") 
                last_date = fields[ cols.index('Datenstand') ].replace("\"", "")
                last_date = last_date[6:10] + "-" + last_date[3:5] + "-" + last_date[0:2] 
                return last_date == isodatestr
        except:
            return False

    def scrape(self, isodate="", force=False):
        if not self.is_day_available(isodate):
            return False
        if (force == False) and (self.was_data_scraped(isodate)):
            return False
        
        # download
        os.system( "curl {} --output {} > /dev/null".format(self.get_csv_url(isodate), RKI_GitHub.CSVFILE) )

        # filter TH using awk
        os.system( "cat {0} | awk -F, '{1}' > {0}.tmp && mv {0}.tmp {0}".format(RKI_GitHub.CSVFILE, "{if ($1>=16000) print $0}") )

        return self.prepare_data()

    def prepare_data(self):

        try:
            df = pd.read_csv(RKI_GitHub.CSVFILE)
            cols = list(df.columns)
        except:
            return False

        if 'Datenstand' in cols:
            return True

        # transform 'IdLandkreis' to 'Landkreis'
        df['Landkreis'] = ""
        df['Landkreis'] = df['IdLandkreis'].apply(lambda r: RKI_GitHub.AGS[r])
        df.drop('IdLandkreis', axis=1, inplace=True)

        # add date
        df['Datenstand'] = self.RKI_datestr

        # convert 'Meldedatum' and 'RefDatum' to timestamps
        df['Meldedatum'] = df['Meldedatum'].apply(lambda r: int(datetime.strptime(r, "%Y-%m-%d").timestamp()) )
        df['Refdatum'] = df['Refdatum'].apply(lambda r: int(datetime.strptime(r, "%Y-%m-%d").timestamp()) )

        # reorder columns
        df = df[ RKI.COLS ]

        # sort by Meldedatum
        df.sort_values(['Meldedatum'])

        # export CSV
        df.to_csv(RKI_GitHub.CSVFILE, index=False)

        return True

    def __init__(self, isodate=""):
        self.isodate = isodate if  (isodate != "") else datetime.now().strftime("%Y-%m-%d")
        self.RKI_datestr = "{}.{}.{}, 00:00 Uhr".format(self.isodate[8:10], self.isodate[5:7], self.isodate[0:4])


if __name__ == "__main__":

    DATAFILE = os.path.dirname(os.path.realpath(__file__)) + "/../data/cases_rki_db_th.csv"

    RKI = RKI_GitHub()
    RKI.scrape()
