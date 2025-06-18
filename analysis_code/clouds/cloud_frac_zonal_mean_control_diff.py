#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 14:44:18 2021

@author: nn819853
"""

"""
Script to determine difference in control simulation zonal annual mean 
cloud volume fraction (00266) and plot as cross section
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import matplotlib.pyplot as plt
import character_shortcuts as char


diag_dir = file_loc.diag_dir + 'cloud_diags/'
plot_dir = file_loc.plot_dir + 'clouds/'

### Change suites here ###
suite1 = 'br793'
suite2 = 'cb349'


# load cloud zonal mean control suite cubes
control_1_file = 'cloud_frac_annual_zonal_mean_' + suite1 + '.nc'
control_2_file = 'cloud_frac_annual_zonal_mean_' + suite2 + '.nc'

control_1 = iris.load_cube(diag_dir + control_1_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

control_2 = iris.load_cube(diag_dir + control_2_file,\
          'annual_zonal_mean_cloud_volume_fraction_in_atmosphere_layer')

#zonal_time_mean_control_1 = control_1[:4].collapsed('time', iris.analysis.MEAN)
#zonal_time_mean_control_2 = control_2[:4].collapsed('time', iris.analysis.MEAN)


# difference controls to get control error and time mean
diff = control_1[:4] - control_2[:4]

error, error_stdev, error_double_se =\
flux_mod.time_mean_cube(diff)


# Change units of level height to km
error.coord('level_height').convert_units('km')


# check mean error
mean_error = np.mean(np.abs(error.data))
print('Mean cloud fraction error is: ', mean_error)


# Plotting
font = {'size' : 12}
plt.rc('font', **font)

target = plot_dir + 'cloud_frac_zonal_time_mean_control_diff_' + suite1 + '_minus_' + suite2

plt.figure()
mesh = iplt.pcolormesh(error[0:63],
                       coords = ['latitude', 'level_height'],
                       cmap = 'seismic',
                       vmin = -0.02,
                       vmax = 0.02)
plt.colorbar(mesh,
             fraction = 0.070,
             label = 'Cloud volume fraction difference',
             orientation = 'horizontal',
              ticks = [-0.02,-0.01,0,0.01,0.02]
             )
plt.ylabel('Altitude / km')
plt.xlabel('Latitude')
# plt.title('Cloud control error: nudging uv' + char.theta() + ' G=1/6 minus free',\
#           fontsize = 'medium')
plt.savefig(target, dpi = 300)
plt.show()
