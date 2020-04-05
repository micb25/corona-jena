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
    JPGFILE  = SCRIPTPATH + "/../map_th_rel_area.jpg"
    PNGFILET = SCRIPTPATH + "/../map_th_rel_area.tmp.png"
    
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
    
    # area size per city/county; values taken from:
    # https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=GG000101%7C%7C
    area_array  = {
        "Altenburger Land": 569.40,
        "Eichsfeld":  943.07,
        "Eisenach": 104.17,
        "Erfurt":  269.91,
        "Gera": 152.18,
        "Gotha":  936.08,
        "Greiz": 845.98,
        "Hildburghausen": 938.42,
        "Ilm-Kreis":  843.71,
        "Jena": 114.77,
        "Kyffhäuserkreis": 1037.91,
        "Nordhausen": 713.90,
        "Saale-Holzland-Kreis": 815.24,
        "Saale-Orla-Kreis": 1151.30,
        "Saalfeld-Rudolstadt":  1036.03,
        "Schmalkalden-Meiningen": 1210.73,
        "Sömmerda": 806.86,
        "Sonneberg": 433.61,
        "Suhl": 103.03,
        "Unstrut-Hainich-Kreis":  979.69,
        "Wartburgkreis":  1307.44,
        "Weimar": 84.48,
        "Weimarer Land": 804.48
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
                    area_data[ds[1]] = float(ds[3]) / float(area_array[ds[1]]) 
                    if ( area_data[ds[1]] > max_cases ):
                        max_cases = area_data[ds[1]]

        # read SVG template
        with open(TEMPLATE, "r") as df:
            svgdata = df.read()
            
        for k, r in replace_array.items():
            area_color = value_to_color(area_data[k], max_cases)
            svgdata = svgdata.replace(r, area_color)

        # change labels
        svgdata = svgdata.replace("%TITLE%", "relative Fallzahlen pro Quadratkilometer")
        svgdata = svgdata.replace("%MIN_VAL%", "%.1f Fälle / km²" % (0))
        svgdata = svgdata.replace("%MID_VAL%", "%.1f Fälle / km²" % (float(max_cases/2)))
        svgdata = svgdata.replace("%MAX_VAL%", "%.1f Fälle / km²" % (float(max_cases)))
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
