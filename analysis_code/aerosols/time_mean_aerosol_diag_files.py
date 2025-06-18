#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:32:39 2023

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import copy
import character_shortcuts as char
import iris.quickplot as qplt


### Note: free sim files dealt with separately as needed to concatenate two
### files for each as well as then time mean, see script:
### 'concatenate_and_time_mean_free_sim_aerosol_diag_files.py'


###also note for BC modes are not the same - there's no nucleation mode
### and is an insoluble mode


# set directory name 
diag_folder = 'aerosols/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'aerosols/'


# suites
suites = [
        'cb349',
        # 'cb350',
        'ce304',
        'cb108',
        # 'cb109',
        'ce303',
        ]

no_suites = len(suites)

# isolate modes and then time average and save cubes
for i in range(no_suites):
        
    aer_modes = iris.load(diag_dir + 'aer_burden_mmr_bc_' + suites[i])
    
    nuc = aer_modes[0]
    ait = aer_modes[1]
    acc = aer_modes[2]
    coa = aer_modes[3]
    
    
    time_mean_nuc,_,_ = flux_mod.time_mean_cube(nuc)
    time_mean_ait,_,_ = flux_mod.time_mean_cube(ait)
    time_mean_acc,_,_ = flux_mod.time_mean_cube(acc)
    time_mean_coa,_,_ = flux_mod.time_mean_cube(coa)
    
    
    cubes = iris.cube.CubeList([time_mean_nuc,\
                                time_mean_ait,\
                                time_mean_acc,\
                                time_mean_coa])
    
    iris.save(cubes, diag_dir + 'aer_burden_mmr_bc_' + suites[i] + \
              '_time_mean.pp')




