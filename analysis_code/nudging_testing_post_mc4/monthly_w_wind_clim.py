#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 11:21:16 2021

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris.analysis
import character_shortcuts as char


data_dir = file_loc.diag_dir + 'nudging_testing_post_mc4/w_wind/'
plot_dir = file_loc.plot_dir + 'nudging_testing_post_mc4/w_wind/'

# Change these to change free suites used
free_cont = 'br793'

# load free w-wind time means
free_cont_w_wind_time_mean_cubes = iris.load(data_dir + 'time_mean_w_'+free_cont+'.pp')
free_cont_w_wind_time_mean = free_cont_w_wind_time_mean_cubes[1]

trop_data_dir = file_loc.diag_dir + 'nudging_testing_new/'

# load time, longitude mean tropopause height diags
free_cont_trop = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+free_cont+'.nc')

# convert level height coord to km
free_cont_w_wind_time_mean.coord('level_height').convert_units('kilometre')


# convert trop height cubes to km
free_cont_trop.convert_units('kilometre')


# set figure font size
font = {'size' : 12}
plt.rc('font', **font)


### Levels ###
# Determine adjustment/cont errors on level
levels = [0, 8, 25, 45, 53]

for level in levels:
    actual_level = str(level+1)
    
    # means - !should be weighted!
    #mean_free_adjust_level = np.round(np.mean(free_w_wind_adjust[level].data), 3)
    #mean_cont_error_level = np.round(np.mean(cont_w_wind_error[level].data), 3)
    #mean_nudged_adjust_level = np.round(np.mean(nudged_w_wind_adjust[level].data), 3)
    #mean_nudged_adjust_free_cont_relative_level = np.round(np.mean(nudged_w_wind_adjust_free_cont_relative[level].data), 3)
    
    # plotting levels 
    plt.figure()
    mesh = iplt.pcolormesh(free_cont_w_wind_time_mean[level], cmap = 'seismic',\
                            vmin = -0.008, vmax = 0.008)
    plt.colorbar(mesh, fraction = 0.07, label = u'w-wind / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Free cont w-wind clim, level '+actual_level, size = 'medium')
    #plt.text(-170,-108, 'Mean = ' + str(mean_free_adjust_level) + ' k')
    plt.savefig(plot_dir + free_cont+'_free_cont_w_wind_clim_level_' + str(actual_level),\
                dpi = 400)
    plt.tight_layout()
    plt.show()

    
### Time zonal means ###
free_cont_w_wind_zonal = free_cont_w_wind_time_mean.collapsed('longitude', iris.analysis.MEAN)

# means - !Should be weighted!
#mean_free_adjust_zonal = np.round(np.mean(free_w_wind_adjust_zonal[:65].data), 3)
#mean_cont_error_zonal = np.round(np.mean(cont_w_wind_error_zonal[:65].data), 3)
#mean_nudged_adjust_zonal = np.round(np.mean(nudged_w_wind_adjust_zonal[:65].data), 3)
#mean_nudged_adjust_free_cont_relative_zonal = np.round(np.mean(nudged_w_wind_adjust_free_cont_relative_zonal[:65].data), 3)


# plot zonal
plt.figure()
mesh = iplt.pcolormesh(free_cont_w_wind_zonal[:65], cmap = 'seismic',\
                            vmin = -0.008, vmax = 0.008, coords = ['latitude', 'level_height'])
plt.colorbar(mesh, fraction = 0.07, label = u'w-wind / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
iplt.plot(free_cont_trop, linestyle = '--', linewidth = 2, color = 'black')
#iplt.plot(free_pert_trop, linestyle = ':', linewidth = 2, color = 'black')
plt.ylabel('Altitude / km')
plt.title('Free cont w-wind zonal mean clim', size = 'medium')
#plt.text(-85,2, 'Mean = ' + str(mean_free_adjust_zonal) + ' k')
plt.savefig(plot_dir + free_cont+'_free_cont_w_wind_clim_zonal',\
            dpi = 400)
plt.tight_layout()
plt.show()