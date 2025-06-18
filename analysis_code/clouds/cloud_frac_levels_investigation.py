#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:04:32 2023

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


######### CHANGE HERE #########
# Set suites 
cont_suite = 'br793'
pert_suite = 'ce067'

# set base  name for plot titles
title = 'Free BC'
# title = 'Nudged uv (G=1/6, bl=1, r=1) BC'
# title = r'Nudged uv$\theta$ (G=1/6, bl=1, r=1) BC' 


# Set plot and diagnostic directories and save fig and title targets
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

save_plot_target = plot_dir + 'cloud_adjustment_levels_' + cont_suite + '-' + pert_suite + '_map_'


# Load control and perturbed files
# cont_file = 'cloud_frac_' + cont_suite + '_apm.pp'
# pert_file = 'cloud_frac_' + pert_suite + '_apm.pp'
cont_file = 'cloud_frac_00266_br793_apm_2015_2018.pp'
pert_file = 'cloud_frac_00266_ce067_apm_2015_2018.pp'


cont_cube = iris.load_cube(diag_dir + cont_file)
pert_cube = iris.load_cube(diag_dir + pert_file)


###############################
# Area mean over Africa

cont_area_mean = flux_mod.area_mean_cube(cont_cube[:,:,60:100,0:40])
pert_area_mean = flux_mod.area_mean_cube(pert_cube[:,:,60:100,0:40])


plt.figure()
plt.plot(cont_area_mean[:,2].data, label = 'cont_lvl_2')
plt.plot(cont_area_mean[:,5].data, label = 'cont_lvl_5')
plt.plot(pert_area_mean[:,2].data, label = 'pert_lvl_2')
plt.plot(pert_area_mean[:,5].data, label = 'pert_lvl_5')
plt.legend()
plt.show()


###############################
# Single points in north and central Africa

north_lat = 95
north_lon = 0

cent_lat = 85
cent_lon = 10


plt.figure()
plt.plot(cont_cube[:,45,north_lat,north_lon].data, label = 'cont_north')
plt.plot(cont_cube[:,45,cent_lat,cent_lon].data, label = 'cont_cent')
plt.plot(pert_cube[:,45,north_lat,north_lon].data, label = 'pert_north')
plt.plot(pert_cube[:,45,cent_lat,cent_lon].data, label = 'pert_cent')
plt.legend()
plt.show()