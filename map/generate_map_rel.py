#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime


def value_to_color(i, imax):
    try:
        # simple blue color gradient
        val = int( 254 - int( 223.0 * float(i) / float(imax) ) )
        return "#{:02x}{:02x}ff".format( val, val )
    except:
        return "#ffffff"


if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    DATAFILE = SCRIPTPATH + "/../data/cases_thuringia.csv"
    TEMPLATE = SCRIPTPATH + "/TH.svg.template"
    SVGFILE  = SCRIPTPATH + "/map_th.svg"
    JPGFILE  = SCRIPTPATH + "/../map_th_rel.jpg"
    PNGFILET = SCRIPTPATH + "/../map_th_rel.tmp.png"
    
    # list of placeholders for the colors in the SVG template
    replace_array  = {
        "Altenburger Land": "%FC_ABG%",
        "Eichsfeld": "%FC_EIC%",
        "Eisenach": "%FC_EA%",
        "Erfurt": "%FC_EF%",
        "Gera": "%FC_G%",
        "Gotha": "%FC_GTH%",
        "Greiz": "%FC_GRZ%",
        "Hildburghausen": "%FC_HBN%",
        "Ilm-Kreis": "%FC_IK%",
        "Jena": "%FC_J%",
        "Kyffhäuserkreis": "%FC_KYF%",
        "Nordhausen": "%FC_NDH%",
        "Saale-Holzland-Kreis": "%FC_SHK%",
        "Saale-Orla-Kreis": "%FC_SOK%",
        "Saalfeld-Rudolstadt": "%FC_SLF%",
        "Schmalkalden-Meiningen": "%FC_SM%",
        "Sömmerda": "%FC_SOM%",
        "Sonneberg": "%FC_SON%",
        "Suhl": "%FC_SHL%",
        "Unstrut-Hainich-Kreis": "%FC_UH%",
        "Wartburgkreis": "%FC_WAK%",
        "Weimar": "%FC_WE%",
        "Weimarer Land": "%FC_AP%"
    }
    
    # number of residents per city/county; values taken from:
    # https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2019%7C%7Cs1
    residents_array  = {
        "Altenburger Land":        89393,
        "Eichsfeld":              100006,
        "Eisenach":                42250,
        "Erfurt":                 213981,
        "Gera":                    93125,
        "Gotha":                  134908,
        "Greiz":                   97398,
        "Hildburghausen":          63197,
        "Ilm-Kreis":              106249,
        "Jena":                   111343,
        "Kyffhäuserkreis":         74212,
        "Nordhausen":              83416,
        "Saale-Holzland-Kreis":    82950,
        "Saale-Orla-Kreis":        80312,
        "Saalfeld-Rudolstadt":    103199,
        "Schmalkalden-Meiningen": 124916,
        "Sömmerda":                69427,
        "Sonneberg":               57717,
        "Suhl":                    36789,
        "Unstrut-Hainich-Kreis":  102232,
        "Wartburgkreis":          118974,
        "Weimar":                  65228,
        "Weimarer Land":           82156
    }
    
    try:
        
        # read data file
        with open(DATAFILE, "r") as df:
            rawdata = df.read().splitlines()

        # get latest timestamp
        timestamp = int(rawdata[-1].split(",")[0])
        
        # count total cases and assign cases
        max_cases = 0
        area_data = {}
        for l in rawdata:
            ds = l.split(",")
            if ( len(ds) == 8 ):
                if ( int(ds[0]) == timestamp ):
                    area_data[ds[1]] = int(ds[3]) / int(residents_array[ds[1]]) * 100000
                    if ( area_data[ds[1]] > max_cases ):
                        max_cases = area_data[ds[1]]

        # read SVG template
        with open(TEMPLATE, "r") as df:
            svgdata = df.read()
            
        for k, r in replace_array.items():
            area_color = value_to_color(area_data[k], max_cases)
            svgdata = svgdata.replace(r, area_color)

        # change labels
        svgdata = svgdata.replace("%TITLE%", "relative Fallzahlen pro 100.000 EW")
        svgdata = svgdata.replace("%MIN_VAL%", "0 Fälle / 100.000 EW")
        svgdata = svgdata.replace("%MID_VAL%", "%.0f Fälle / 100.000 EW" % (float(max_cases/2.0)))
        svgdata = svgdata.replace("%MAX_VAL%", "%i Fälle / 100.000 EW" % (int(max_cases)))
        svgdata = svgdata.replace("%LABEL_SUM%", "")
        now = datetime.fromtimestamp(timestamp)
        svgdata = svgdata.replace("%DATE%", now.strftime("letzte Aktualisierung: %d.%m.%Y"))
            
        # write SVG file
        with open(SVGFILE, "w") as svg:
            svg.write(svgdata)
            svg.close()
        
        # create png
        os.system( "convert -resize 800x628 -background '#f2f2f2' -alpha remove -alpha off {} {}".format(SVGFILE, PNGFILET) )
        os.system( "convert {} gradient.png -gravity northwest -geometry +552+95 -composite -quality 70 {}".format(PNGFILET, JPGFILE) )
        os.system( "rm -f {}".format(PNGFILET) )
        
    except:
        print("Error occured!")
