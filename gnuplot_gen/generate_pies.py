#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    
    SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))
    
    TEMPLATE_A = SCRIPTPATH + "/plot0_pie_mini_Template.gnuplot"
    GNUPFILE_A = SCRIPTPATH + "/plot0_pie_mini.gnuplot"
        
    regions = [ 
            "ABG", "EIC", "EA", "EF", "G", "GTH", "GRZ", "HBN", "IK", "J", "KYF", "NDH", 
            "SHK", "SOK", "SLF", "SM", "SOM", "SON", "SHL", "UH", "WAK", "WE", "AP", "TH"
    ]
    
    try:
        # read gnuplot template
        with open(TEMPLATE_A, "r") as df:
            datafile_a = df.read()
        
        # iterate regions
        for entry in regions:
            gnuplot_source_a = datafile_a.replace("%NAME%", entry)

            # write gnuplot file
            with open(GNUPFILE_A, "w") as gpf:
                gpf.write(gnuplot_source_a)
                gpf.close()
                
            # run gnuplot
            os.system("gnuplot {} >/dev/null 2>&1".format(GNUPFILE_A))
        
        # clean-up
        os.system( "rm -f {}".format(GNUPFILE_A) )
        
    except:
        print("Error occured!")
