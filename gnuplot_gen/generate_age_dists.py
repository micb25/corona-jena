#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    TEMPLATE_A = SCRIPTPATH + "/plot5A_Template.gnuplot"
    GNUPFILE_A = SCRIPTPATH + "/plot5A.gnuplot"
    
    TEMPLATE_B = SCRIPTPATH + "/plot5B_Template.gnuplot"
    GNUPFILE_B = SCRIPTPATH + "/plot5B.gnuplot"
    
    province_array = [
        ("LK Altenburger Land", "ABG", "im Altenburger Land"),
        ("LK Eichsfeld", "EIC", "im Eichsfeld"),
        ("SK Eisenach", "EA", "in Eisenach"),
        ("SK Erfurt", "EF", "in Erfurt"),
        ("SK Gera", "G", "in Gera"),
        ("LK Gotha", "GTH", "im Landkreis Gotha"),
        ("LK Greiz", "GRZ", "im Landkreis Greiz"),
        ("LK Hildburghausen", "HBN", "im LK Hildburghausen"),
        ("LK Ilm-Kreis", "IK", "im Ilm-Kreis"),
        ("SK Jena", "J", "in Jena"),
        ("LK Kyffhäuserkreis", "KYF", "im Kyffhäuserkreis"),
        ("LK Nordhausen", "NDH", "in Nordhausen"),
        ("LK Saale-Holzland-Kreis", "SHK", "im Saale-Holzland-Kreis"),
        ("LK Saale-Orla-Kreis", "SOK", "im Saale-Orla-Kreis"),
        ("LK Saalfeld-Rudolstadt", "SLF", "im LK Saalfeld-Rudolstadt"),
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
        
        # read gnuplot templates
        with open(TEMPLATE_A, "r") as df:
            datafile_a = df.read()
        
        with open(TEMPLATE_B, "r") as df:
            datafile_b = df.read()
        
        # iterate all entries
        for entry in province_array:
            gnuplot_source_a = datafile_a
            gnuplot_source_b = datafile_b
            for re in enumerate(replace_array):
                gnuplot_source_a = gnuplot_source_a.replace(re[1], entry[re[0]])
                gnuplot_source_b = gnuplot_source_b.replace(re[1], entry[re[0]])

            # write gnuplot files
            with open(GNUPFILE_A, "w") as gpf:
                gpf.write(gnuplot_source_a)
                gpf.close()
                
            with open(GNUPFILE_B, "w") as gpf:
                gpf.write(gnuplot_source_b)
                gpf.close()
                
            # run gnuplot
            os.system("gnuplot {} > /dev/null".format(GNUPFILE_A))
            os.system("gnuplot {} > /dev/null".format(GNUPFILE_B))
        
        # clean-up
        os.system( "rm -f {} {}".format(GNUPFILE_A, GNUPFILE_B) )
        
    except:
        print("Error occured!")
