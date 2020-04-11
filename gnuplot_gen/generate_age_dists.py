#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    TEMPLATE = SCRIPTPATH + "/plot5A_Template.gnuplot"
    GNUPFILE = SCRIPTPATH + "/plot5A.gnuplot"
    
    province_array = [
        ("LK Altenburger Land", "ABG", "im Altenburger Land"),
        ("LK Eichsfeld", "EIC", "im Eichsfeld"),
        ("SK Eisenach", "EA", "in Eisenach"),
        ("SK Erfurt", "EF", "in Erfurt"),
        ("SK Gera", "G", "in Gera"),
        ("LK Gotha", "GTH", "im Landkreis Gotha"),
        ("LK Greiz", "GRZ", "im Landkreis Greiz"),
        ("LK Hildburghausen", "HBN", "im Landkreis Hildburghausen"),
        ("LK Ilm-Kreis", "IK", "im Ilm-Kreis"),
        ("SK Jena", "J", "in Jena"),
        ("LK Kyffhäuserkreis", "KYF", "im Kyffhäuserkreis"),
        ("LK Nordhausen", "NDH", "in Nordhausen"),
        ("LK Saale-Holzland-Kreis", "SHK", "im Saale-Holzland-Kreis"),
        ("LK Saale-Orla-Kreis", "SOK", "im Saale-Orla-Kreis"),
        ("LK Saalfeld-Rudolstadt", "SLF", "im Landkreis Saalfeld-Rudolstadt"),
        ("LK Schmalkalden-Meiningen", "SM", "in Schmalkalden-Meiningen"),
        ("LK Sömmerda", "SOM", "im Landkreis Sömmerda"),
        ("LK Sonneberg", "SON", "im Landkreis Sonneberg"),
        ("SK Suhl", "SHL", "in Suhl"),
        ("LK Unstrut-Hainich-Kreis", "UH", "im Unstrut-Hainich-Kreis"),
        ("LK Wartburgkreis", "WAK", "im Wartburgkreis"),
        ("SK Weimar", "WE", "in Weimar"),
        ("LK Weimarer Land", "AP", "im Weimarer Land")
    ]
    
    replace_array = [
        "%NAME%",
        "%FILENAME%",
        "%REGION%",
    ]
    
    try:
        
        # read gnuplot template
        with open(TEMPLATE, "r") as df:
            datafile = df.read()
        
        # iterate all entries
        for entry in province_array:
            gnuplot_source = datafile
            for re in enumerate(replace_array):
                gnuplot_source = gnuplot_source.replace(re[1], entry[re[0]])

            # write gnuplot file
            with open(GNUPFILE, "w") as gpf:
                gpf.write(gnuplot_source)
                gpf.close()
                
            # run gnuplot
            os.system("gnuplot {} > /dev/null".format(GNUPFILE))
        
        # clean-up
        os.system( "rm -f {}".format(GNUPFILE) )
        
    except:
        print("Error occured!")
