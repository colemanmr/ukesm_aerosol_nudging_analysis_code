#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:44:15 2021

@author: nn819853
"""

"""
Script to determine cloud fraction (00266) adjustment between control and
perturbed suites, including error estimation, and plotting cross section
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


# Assign diag and plot directories
diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

###CHange here###
# Set suite pairs (second pair adjustment is subtracted from first)
cont_suite = 'cb349'
pert_suite = 'ce304'

cont_suite2 = 'cb108'
pert_suite2 = 'ce303'


# load control land perturbed cubes
cont_file = 'cloud_frac_annual_zonal_mean_' + cont_suite + '.nc'
pert_file = 'cloud_frac_annual_zonal_mean_' + pert_suite + '.nc'

cont_cube = iris.load_cube(diag_dir + cont_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')
pert_cube = iris.load_cube(diag_dir + pert_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')
    
    
# Dfiference first pair of sims and time mean
diff, diff_stdev, diff_double_se = flux_mod.time_mean_cube(cont_cube - pert_cube)


# load control land perturbed cubes
cont_file2 = 'cloud_frac_annual_zonal_mean_' + cont_suite2 + '.nc'
pert_file2 = 'cloud_frac_annual_zonal_mean_' + pert_suite2 + '.nc'

cont_cube2 = iris.load_cube(diag_dir + cont_file2,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')
pert_cube2 = iris.load_cube(diag_dir + pert_file2,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

    
# Dfiference second pair of sims and time mean
diff2, diff_stdev2, diff_double_se2 = flux_mod.time_mean_cube(cont_cube2 - pert_cube2)


# Determine delta adjustment
adjustment = diff - diff2


# Change units of level height to km
adjustment.coord('level_height').convert_units('km')


# Adjust plotting variables
font = {'size' : 12}
plt.rc('font', **font)


#Set target for plot saving
target = plot_dir + 'cloud_frac_zonal_time_mean_delta_adjustment_'\
    + cont_suite + '_minus_' + pert_suite + '_delta_'\
        + cont_suite2 + '_minus_' + pert_suite2


# Plot zonal mean cross section
plt.figure()
mesh = iplt.pcolormesh(adjustment[0:63],
                       coords = ['latitude', 'level_height'],
                       cmap = 'seismic',
                       vmin = -0.02,
                       vmax = 0.02)
plt.colorbar(mesh,
             fraction = 0.070,
             label = 'Cloud volume fraction adjustment',
             orientation = 'horizontal',
             ticks = [-0.02,-0.01,0,0.01,0.02])
plt.ylabel('Altitude / km')
plt.xlabel('Latitude')
plt.savefig(target, dpi = 300)
plt.show()








