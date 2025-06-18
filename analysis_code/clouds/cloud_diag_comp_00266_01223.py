#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:24:19 2023

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import character_shortcuts as char



# Set plot and diagnostic directories and save fig and title targets
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'


# File names
bulk_file = diag_dir + 'cloud_frac_00266_br793_apm_2015.pp'
weight_file = diag_dir + 'cloud_frac_01223_br793_apm_2015.pp'


# load cubes
bulk = iris.load_cube(bulk_file)
weight = iris.load_cube(weight_file)


# # check zeros and plot - where equals 1 is a zero in cloud diag
# diags = [bulk, weight]
# time = 0
# level = 10

# for i in range(2):
    
#     zeros = np.where(diags[i].data == 0)
#     binary = np.zeros_like(diags[i].data)
#     binary[zeros] = 1
    
#     plt.figure()
#     mesh = plt.pcolormesh(binary[time,level,:,:], cmap = 'viridis')
#     plt.colorbar(mesh)
#     plt.show()
    
    
    
### Repeat for annual means ###
bulk_ann_mean,_,_ = flux_mod.time_mean_cube(bulk)
weight_ann_mean,_,_ = flux_mod.time_mean_cube(weight)

# # check zeros and plot - where equals 1 is a zero in cloud diag
# diags = [bulk_ann_mean, weight_ann_mean]
# level = 8

# for i in range(2):
    
#     zeros = np.where(diags[i].data == 0)
#     binary = np.zeros_like(diags[i].data)
#     binary[zeros] = 1
    
#     plt.figure()
#     mesh = plt.pcolormesh(binary[level,:,:], cmap = 'viridis')
#     plt.colorbar(mesh)
#     plt.show()
    
    
    
### Repeat for vertical annual mean ###
bulk_ann_lvl_mean = bulk_ann_mean[2:15].collapsed('model_level_number', \
                                            iris.analysis.MEAN)
weight_ann_lvl_mean = weight_ann_mean[2:15].collapsed('model_level_number', \
                                            iris.analysis.MEAN)
    
# # check zeros and plot - where equals 1 is a zero in cloud diag
# diags = [bulk_ann_lvl_mean, weight_ann_lvl_mean]

# for i in range(2):
    
#     zeros = np.where(diags[i].data == 0)
#     binary = np.zeros_like(diags[i].data)
#     binary[zeros] = 1
    
#     plt.figure()
#     mesh = plt.pcolormesh(binary[:,:], cmap = 'viridis')
#     plt.colorbar(mesh)
#     # current_map = plt.gca()
#     # current_map.coastlines(linewidth = 1)
#     plt.show()



### plotting diags ###
diags = [bulk_ann_lvl_mean, weight_ann_lvl_mean]

for i in range(2):

    plt.figure()
    mesh = iplt.pcolormesh(diags[i], cmap='viridis', vmin = 0, vmax = 0.7)
    plt.colorbar(mesh)
    plt.show()



