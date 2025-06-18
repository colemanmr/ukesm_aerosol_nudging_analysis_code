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


### Note to future me:
###I decided to do this step by just replacing string for each of the 
###three free running simulations as it takes so long I hope I don't
###have to do it again! But leaving this code for transparency of how
###the data was processed :)

# set directory name 
diag_folder = 'aerosols/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'aerosols/'


cont_file_1 = iris.load(diag_dir + 'aer_burden_mmr_bc_br793_2015-2032')
cont_file_2 = iris.load(diag_dir + 'aer_burden_mmr_bc_br793_2033-2048')

cont_nuc_cubelist = iris.cube.CubeList([cont_file_1[0], cont_file_2[0]])
cont_nuc = cont_nuc_cubelist.concatenate('time')[0]

cont_ait_cubelist = iris.cube.CubeList([cont_file_1[1], cont_file_2[1]])
cont_ait = cont_ait_cubelist.concatenate('time')[0]

cont_acc_cubelist = iris.cube.CubeList([cont_file_1[2], cont_file_2[2]])
cont_acc = cont_acc_cubelist.concatenate('time')[0]

cont_coa_cubelist = iris.cube.CubeList([cont_file_1[3], cont_file_2[3]])
cont_coa = cont_coa_cubelist.concatenate('time')[0]


time_mean_cont_nuc,_,_ = flux_mod.time_mean_cube(cont_nuc)
time_mean_cont_ait,_,_ = flux_mod.time_mean_cube(cont_ait)
time_mean_cont_acc,_,_ = flux_mod.time_mean_cube(cont_acc)
time_mean_cont_coa,_,_ = flux_mod.time_mean_cube(cont_coa)


cont_cubelist = iris.cube.CubeList([time_mean_cont_nuc,\
                                    time_mean_cont_ait,\
                                    time_mean_cont_acc,\
                                    time_mean_cont_coa])

iris.save(cont_cubelist, diag_dir + 'aer_burden_mmr_bc_br793_time_mean.pp')




