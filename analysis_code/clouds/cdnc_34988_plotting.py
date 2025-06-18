#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:18:59 2023

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
diag_folder = 'cloud_diags/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'clouds/'


cont_cdnc = iris.load_cube(diag_dir + 'cdnc_34968_cb108.pp')
pert_cdnc = iris.load_cube(diag_dir + 'cdnc_34968_ce303.pp')


time_mean_cont,_,_ = flux_mod.time_mean_cube(cont_cdnc[0:48])
time_mean_pert,_,_ = flux_mod.time_mean_cube(pert_cdnc[0:48])


diff = time_mean_cont - time_mean_pert

plt.figure()
mesh = iplt.contourf(diff[11], \
                        # levels = [-5,-4,-3,-2,-1,0,1,2,3,4,5], \
                        # cmap = 'magma',\
                       )
plt.colorbar(mesh, fraction = 0.070, label = r'$\Delta$ CDNC', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.show()


plt.figure()
mesh = qplt.pcolormesh(time_mean_cont[11])
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.show()

plt.figure()
mesh = qplt.pcolormesh(time_mean_pert[11])
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.show()





