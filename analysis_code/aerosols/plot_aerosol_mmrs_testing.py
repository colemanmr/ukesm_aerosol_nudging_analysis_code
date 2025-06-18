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


# set directory name 
diag_folder = 'aerosols/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'aerosols/'


# load cube
cont = iris.load(diag_dir + 'aer_burden_mmr_su_cb108')
pert = iris.load(diag_dir + 'aer_burden_mmr_su_cb109')


time_mean_cont,_,_ = flux_mod.time_mean_cube(cont[1])
time_mean_pert,_,_ = flux_mod.time_mean_cube(pert[1])


diff = time_mean_cont - time_mean_pert


plt.figure()
iplt.pcolormesh(time_mean_cont[11])
plt.show()

plt.figure()
iplt.pcolormesh(time_mean_pert[11])
plt.show()

plt.figure()
qplt.pcolormesh(diff[11], cmap = 'seismic', vmin = -0.3e-9, vmax = 0.3e-9)
figure = plt.gca()
figure.coastlines(linewidth = 1)
plt.show()