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
    
    DATAFILE = SCRIPTPATH + "/../data/rki_th_by_date/cases_by_day_and_region.csv"
    TEMPLATE = SCRIPTPATH + "/TH.svg.template"
    SVGFILE  = SCRIPTPATH + "/map_th.svg"
    JPGFILE  = SCRIPTPATH + "/../map_th.jpg"
    PNGFILET = SCRIPTPATH + "/../map_th.tmp.png"
    
    # list of placeholders for the colors in the SVG template
    replace_array  = {
        "ABG": "%FC_ABG%",
        "EIC": "%FC_EIC%",
        "EA": "%FC_EA%",
        "EF": "%FC_EF%",
        "G": "%FC_G%",
        "GTH": "%FC_GTH%",
        "GRZ": "%FC_GRZ%",
        "HBN": "%FC_HBN%",
        "IK": "%FC_IK%",
        "J": "%FC_J%",
        "KYF": "%FC_KYF%",
        "NDH": "%FC_NDH%",
        "SHK": "%FC_SHK%",
        "SOK": "%FC_SOK%",
        "SLF": "%FC_SLF%",
        "SM": "%FC_SM%",
        "SOM": "%FC_SOM%",
        "SON": "%FC_SON%",
        "SHL": "%FC_SHL%",
        "UH": "%FC_UH%",
        "WAK": "%FC_WAK%",
        "WE": "%FC_WE%",
        "AP": "%FC_AP%"
    }
    
    try:
        # read RKI data file
        with open(DATAFILE, "r") as df:
            rawdata = df.read().splitlines()[-24:]
            
        th_data = []
        for line in rawdata:
            line_data = line.split(",")
            for i, e in enumerate(line_data):
                if i != 1:
                    line_data[i] = int(e)
                    
            th_data.append( line_data )
        
        # get latest timestamp
        timestamp = int(th_data[0][0])
        
        cases_tmp = [th_data[i][1:3] for i in range(0, len(th_data))]
        area_data = {}
        max_cases = 0
        sum_cases = 0
        for key, c in cases_tmp:
            if key != 'TH':
                area_data[key] = c
                max_cases = max(c, max_cases)
                sum_cases += c
                        
        # read SVG template
        with open(TEMPLATE, "r") as df:
            svgdata = df.read()
            
        for k, r in replace_array.items():
            area_color = value_to_color(area_data[k], max_cases)
            svgdata = svgdata.replace(r, area_color)

        # change labels
        svgdata = svgdata.replace("%TITLE%", "Fallzahlen nach Landkreis/Stadt")
        svgdata = svgdata.replace("%MIN_VAL%", "0 Fälle")
        svgdata = svgdata.replace("%MID_VAL%", "%i Fälle" % (int(max_cases/2)))
        svgdata = svgdata.replace("%MAX_VAL%", "%i Fälle" % (max_cases))
        svgdata = svgdata.replace("%LABEL_SUM%", "%i Fälle insgesamt" % (sum_cases))
        now = datetime.fromtimestamp(timestamp)
        svgdata = svgdata.replace("%DATE%", now.strftime("letzte Aktualisierung: %d.%m.%Y"))
            
        # write SVG file
        with open(SVGFILE, "w") as svg:
            svg.write(svgdata)
            svg.close()
        
        # create png
        os.system( "convert -resize 800x628 -background '#f2f2f2' -alpha remove -alpha off {} {}".format(SVGFILE, PNGFILET) )
        os.system( "convert {} gradient.png -gravity northwest -geometry +552+95 -composite -quality 80 {}".format(PNGFILET, JPGFILE) )
        os.system( "rm -f {}".format(PNGFILET) )
        
    except:
        print("Error occured!")
