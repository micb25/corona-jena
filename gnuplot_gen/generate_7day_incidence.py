#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    SOURCEFILE = "../data/cases_rki_7day_incidence.csv"
    TEMPLATE_A = SCRIPTPATH + "/plot8_Template.gnuplot"
    GNUPFILE_A = SCRIPTPATH + "/plot8.gnuplot"
    
    province_array = [
        ("LK Altenburger Land", "ABG", "im Altenburger Land", "Altenburger Land"),
        ("LK Eichsfeld", "EIC", "im Eichsfeld", "Eichsfeld"),
        ("SK Eisenach", "EA", "in Eisenach", "Eisenach"),
        ("SK Erfurt", "EF", "in Erfurt", "Erfurt"),
        ("SK Gera", "G", "in Gera", "Gera"),
        ("LK Gotha", "GTH", "im Landkreis Gotha", "Landkreis Gotha"),
        ("LK Greiz", "GRZ", "im Landkreis Greiz", "Landkreis Greiz"),
        ("LK Hildburghausen", "HBN", "im LK Hildburghausen", "Landkreis Hildburghausen"),
        ("LK Ilm-Kreis", "IK", "im Ilm-Kreis", "Ilm-Kreis"),
        ("SK Jena", "J", "in Jena", "Jena"),
        ("LK Kyffhäuserkreis", "KYF", "im Kyffhäuserkreis", "Kyffhäuserkreis"),
        ("LK Nordhausen", "NDH", "im Landkreis Nordhausen", "Landkreis Nordhausen"),
        ("LK Saale-Holzland-Kreis", "SHK", "im Saale-Holzland-Kreis", "Saale-Holzland-Kreis"),
        ("LK Saale-Orla-Kreis", "SOK", "im Saale-Orla-Kreis", "Saale-Orla-Kreis"),
        ("LK Saalfeld-Rudolstadt", "SLF", "im LK Saalfeld-Rudolstadt", "Saalfeld-Rudolstadt"),
        ("LK Schmalkalden-Meiningen", "SM", "in Schmalkalden-Meiningen", "Schmalkalden-Meiningen"),
        ("LK Sömmerda", "SOM", "im Landkreis Sömmerda", "Landkreis Sömmerda"),
        ("LK Sonneberg", "SON", "im Landkreis Sonneberg", "Landkreis Sonneberg"),
        ("SK Suhl", "SHL", "in Suhl", "Suhl"),
        ("LK Unstrut-Hainich-Kreis", "UH", "im Unstrut-Hainich-Kreis", "Unstrut-Hainich-Kreis"),
        ("LK Wartburgkreis", "WAK", "im Wartburgkreis", "Wartburgkreis"),
        ("SK Weimar", "WE", "in Weimar", "Weimar"),
        ("LK Weimarer Land", "AP", "im Weimarer Land", "Weimarer Land"),
        ("Thüringen", "TH", "in Thüringen", "Thüringen")
    ]
    
    replace_array = [
        "%NAME%",
        "%FILENAME%",
        "%REGION%",
        "%SNAME%"
    ]
    
    try:
        
        with open(SOURCEFILE, "r") as df:
            columns = df.read().splitlines()[0].split(",")
            
        # read gnuplot templates
        with open(TEMPLATE_A, "r") as df:
            datafile_a = df.read()
                
        # iterate all entries
        for entry in province_array:
            gnuplot_source_a = datafile_a
            for re in enumerate(replace_array):
                gnuplot_source_a = gnuplot_source_a.replace(re[1], entry[re[0]])
                
            colindex = 1 + columns.index(entry[1])
            gnuplot_source_a = gnuplot_source_a.replace("%COLIDX%", str(colindex))

            # write gnuplot files
            with open(GNUPFILE_A, "w") as gpf:
                gpf.write(gnuplot_source_a)
                gpf.close()
                                
            # run gnuplot
            os.system("gnuplot {} >/dev/null 2>&1".format(GNUPFILE_A))
            
        # clean-up
        os.system( "rm -f {}".format(GNUPFILE_A) )
        
    except:
        print("Error occured!")
