#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:34:07 2021

@author: nn819853
"""

"""
Script to determine difference in cloud fraction (00266) adjustment between 
two different pairs of cont-pert simulations, including error estimation, 
and plotting cross section
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import matplotlib.pyplot as plt

diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

cont_suite = 'cb108'
pert_suite = 'cb109'

cont_file = 'cloud_frac_annual_zonal_mean_' + cont_suite + '.nc'
pert_file = 'cloud_frac_annual_zonal_mean_' + pert_suite + '.nc'

cont_cube = iris.load_cube(diag_dir + cont_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

pert_cube = iris.load_cube(diag_dir + pert_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

diff = cont_cube - pert_cube

adjustment, adjustment_stdev, adjustment_double_se =\
flux_mod.time_mean_cube(diff)


cont_suite2 = 'cb349'
pert_suite2 = 'cb350'

cont_file2 = 'cloud_frac_annual_zonal_mean_' + cont_suite2 + '.nc'
pert_file2 = 'cloud_frac_annual_zonal_mean_' + pert_suite2 + '.nc'

cont_cube2 = iris.load_cube(diag_dir + cont_file2,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

pert_cube2 = iris.load_cube(diag_dir + pert_file2,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

diff2 = cont_cube2 - pert_cube2

adjustment2, adjustment_stdev2, adjustment_double_se2 =\
flux_mod.time_mean_cube(diff2)


adjustment_diff = adjustment - adjustment2

########## Temp extraction of values from cube ###########
lat = adjustment_diff.coord('latitude').points
heights = adjustment_diff.coord('level_height').points
cloud_adjustment_diff = adjustment_diff.data

#need to figure out why iplt or qplt pcolormesh are plotting with model level number
##########################################################

# Plotting
font = {'size' : 12}
plt.rc('font', **font)

target = plot_dir + 'cloud_frac_zonal_time_mean_delta_adjustment' + cont_suite + '_minus_' + pert_suite

plt.figure()
#mesh = qplt.pcolormesh(adjustment[:65], cmap='seismic', vmin=-0.02, vmax=0.02)
mesh = plt.pcolormesh(lat, heights, cloud_adjustment_diff, cmap='seismic', vmin=-0.02, vmax=0.02)
plt.colorbar(mesh, shrink = 0.9, label = 'Cloud volume fraction adjustment difference', \
             orientation = 'horizontal')
plt.ylabel('Altitude / m')
plt.xlabel('Latitude')
plt.ylim(0,28000)
plt.title('SU nudging uvt G=1/6 BL ramp=1 - SU nudging uv G=1/6 BL ramp=1', \
          fontsize = 'medium')
plt.tight_layout()
plt.savefig(target, dpi = 400)
plt.show()
