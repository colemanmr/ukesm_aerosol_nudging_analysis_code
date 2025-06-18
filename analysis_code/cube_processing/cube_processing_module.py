#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 10:38:23 2020

@author: nn819853
"""

import iris
import numpy as np
import iris.coord_categorisation
import toa_fluxes_script

def annual_averages(cubes):
    """
    """
    
    averaged_cubes = []
    
    for i in np.arange(len(cubes)):
        iris.coord_categorisation.add_year(cubes[i], 'time', name='year')
        annual_mean = cubes[i].aggregated_by('year',iris.analysis.MEAN)
        averaged_cubes.append(annual_mean) 
        
    return averaged_cubes