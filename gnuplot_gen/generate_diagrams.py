#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    TEMPLATE = SCRIPTPATH + "/plotT1_Template.gnuplot"
    GNUPFILE = SCRIPTPATH + "/plotT1.gnuplot"
    
    province_array = [
        ("Altenburger Land", "ABG", "im Altenburger Land"),
        ("Eichsfeld", "EIC", "im Eichsfeld"),
        ("Eisenach", "EA", "in Eisenach"),
        ("Gera", "G", "in Gera"),
        ("Gotha", "GTH", "im Landkreis Gotha"),
        ("Greiz", "GRZ", "im Landkreis Greiz"),
        ("Hildburghausen", "HBN", "im Landkreis Hildburghausen"),
        ("Ilm-Kreis", "IK", "im Ilm-Kreis"),
        ("Jena", "J", "in Jena"),
        ("Kyffhäuserkreis", "KYF", "im Kyffhäuserkreis"),
        ("Nordhausen", "NDH", "in Nordhausen"),
        ("Saale-Holzland-Kreis", "SHK", "im Saale-Holzland-Kreis"),
        ("Saale-Orla-Kreis", "SOK", "im Saale-Orla-Kreis"),
        ("Saalfeld-Rudolstadt", "SLF", "im Landkreis Saalfeld-Rudolstadt"),
        ("Schmalkalden-Meiningen", "SM", "in Schmalkalden-Meiningen"),
        ("Sömmerda", "SOM", "im Landkreis Sömmerda"),
        ("Sonneberg", "SON", "im Landkreis Sonneberg"),
        ("Suhl", "SHL", "in Suhl"),
        ("Unstrut-Hainich-Kreis", "UH", "im Unstrut-Hainich-Kreis"),
        ("Wartburgkreis", "WAK", "im Wartburgkreis"),
        ("Weimarer Land", "AP", "im Weimarer Land")
    ]
    
    # skip the following:
    
    # ("Erfurt", "EF", "in Erfurt"),
    # ("Weimar", "WE", "in Weimar"),
    
    replace_array = [
        "%NAME%",
        "%FILENAME%",
        "%NAMEYLABEL%",
    ]
    
    if True:
        
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
        
    #except:
    #    print("Error occured!")
