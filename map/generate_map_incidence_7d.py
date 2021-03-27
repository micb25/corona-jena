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
    
    DATAFILE = SCRIPTPATH + "/../data/cases_rki_7day_incidence.csv"
    TEMPLATE = SCRIPTPATH + "/TH.svg.template"
    SVGFILE  = SCRIPTPATH + "/map_th.svg"
    JPGFILE  = SCRIPTPATH + "/../map_th_incidence_week.jpg"
    PNGFILET = SCRIPTPATH + "/../map_th_incidence_week.tmp.png"
    
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
    
    try:
        
        # read data file
        with open(DATAFILE, "r") as df:
            rawdata = df.read().splitlines()
            
        columns = rawdata[0].split(",")[2:]
        last_line = rawdata[-1].split(",")
        timestamp = int(last_line.pop(0))
        
        # convert to float
        for i, entry in enumerate(last_line):
            last_line[i] = float(entry)
        
        # 7-day incidence for TH
        inc_th = last_line.pop(0)
        
        # get maximum value
        max_value = max(last_line)
                
        # count total cases and assign cases
        area_data = {}
        
        for k, r in replace_array.items():
            key = r[4:]
            col_idx = columns.index(key[:-1])
            area_data[k] = last_line[col_idx]
        
        # read SVG template
        with open(TEMPLATE, "r") as df:
            svgdata = df.read()
            
        for k, r in replace_array.items():
            # fix color for case corrections
            if ( int(area_data[k]) < 0 ):
                area_data[k] = -1
                
            area_color = value_to_color(area_data[k], max_value)
            svgdata = svgdata.replace(r, area_color)

        # change labels
        svgdata = svgdata.replace("%TITLE%", "7-Tages-Inzidenz")
        svgdata = svgdata.replace("%MIN_VAL%", "+0.0 Fälle/100.000 EW")
        svgdata = svgdata.replace("%MID_VAL%", "%+.1f Fälle/100.000 EW" % (int(max_value/2)))
        svgdata = svgdata.replace("%MAX_VAL%", "%+.1f Fälle/100.000 EW" % (max_value))               
        svgdata = svgdata.replace("%LABEL_SUM%", "+%.1f Fälle/100.000 EW" % (inc_th))
            
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
