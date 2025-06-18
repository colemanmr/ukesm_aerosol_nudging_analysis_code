#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:16:49 2023

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')


import numpy as np
import matplotlib.pyplot as plt
import diagnostics.file_locations_module as file_loc
import character_shortcuts as char
import iris


diag_dir =  file_loc.diag_dir + 'net_flux/'

filename = diag_dir + 'calc_forcing_cb108_control_nudging_uvt_flux_all_' +\
    'sky_minus_ce303_bc_nudging_uvt_flux_all_sky_1yr_spinup.nc'
    
cubes = iris.load(filename)

print(cubes)

net = cubes[6]
sw = cubes[3]
lw = cubes[5]


filename2 = diag_dir + 'calc_forcing_cb108_control_nudging_uvt_flux_all_' +\
    'sky_minus_cb109_su_nudging_uvt_flux_all_sky_1yr_spinup.nc'
    

cubes2 = iris.load(filename2)

print(cubes2)

net2 = cubes2[6]
sw2 = cubes2[3]
lw2 = cubes2[5]
