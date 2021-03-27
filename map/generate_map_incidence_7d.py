#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime


def value_to_color(i):
    if ( i >= 500 ):
        return "#{:02x}{:02x}{:02x}".format( 91, 24, 155 )
    elif ( i >= 200 ):
        return "#{:02x}{:02x}{:02x}".format( 178, 117, 221 )
    elif ( i >= 100 ):
        return "#{:02x}{:02x}{:02x}".format( 172, 19, 22 )
    elif ( i >= 50 ):
        return "#{:02x}{:02x}{:02x}".format( 235, 26, 31 )
    elif ( i >= 35 ):
        return "#{:02x}{:02x}{:02x}".format( 241, 137, 74 )
    elif ( i >= 15 ):
        return "#{:02x}{:02x}{:02x}".format( 254, 255, 177 )
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
                
            area_color = value_to_color(area_data[k])
            svgdata = svgdata.replace(r, area_color)

        # change labels
        svgdata = svgdata.replace("%TITLE%", "7-Tages-Inzidenz")
        svgdata = svgdata.replace("%MIN_VAL%", "")
        svgdata = svgdata.replace("%MID_VAL%", "")
        svgdata = svgdata.replace("%MAX_VAL%", "")
        svgdata = svgdata.replace("%LABEL_SUM%", "+%.0f Fälle/100.000 EW" % (inc_th))
            
        now = datetime.fromtimestamp(timestamp)
        svgdata = svgdata.replace("%DATE%", now.strftime("letzte Aktualisierung: %d.%m.%Y"))
            
        # write SVG file
        with open(SVGFILE, "w") as svg:
            svg.write(svgdata)
            svg.close()
        
        # create png
        os.system( "convert -resize 800x628 -background '#f2f2f2' -alpha remove -alpha off {} {}".format(SVGFILE, PNGFILET) )
        os.system( "convert {} gradient_bg.png -gravity northwest -geometry +552+95 -composite -quality 90 {}".format(PNGFILET, JPGFILE) )
        os.system( "rm -f {}".format(PNGFILET) )
        
    except:
        print("Error occured!")
