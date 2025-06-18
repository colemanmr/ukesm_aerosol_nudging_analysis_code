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
free_pert = 'ce067'

# load free w-wind time means
free_cont_w_wind_time_mean = iris.load(data_dir + 'time_mean_w_'+free_cont+'.pp')
free_cont_w_wind_time_mean_4years = iris.load(data_dir + 'time_mean_w_'+free_cont+'_2015-2018.pp')
free_pert_w_wind_time_mean = iris.load(data_dir + 'time_mean_w_'+free_pert+'.pp')


# Change these to change the nudged suites used
nudged_cont = 'cb108'
nudged_pert = 'ce303'
nudging_type = 'uv' + char.theta() + ' (G=1/6, bl=1, r=1)'
# nudging_type = 'uv (G=1/6, bl=1, r=1)'

# Set species (for figure titles and filenames only)
species = 'BC'


# load nudged w-wind time means - change as appropriate
nudged_cont_w_wind_time_mean = iris.load(data_dir + 'time_mean_w_'+nudged_cont+'.pp')
nudged_pert_w_wind_time_mean = iris.load(data_dir + 'time_mean_w_'+nudged_pert+'.pp')


trop_data_dir = file_loc.diag_dir + 'nudging_testing_new/'

# load time, longitude mean tropopause height diags
free_cont_trop = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+free_cont+'.nc')
free_cont_trop_4years = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+free_cont+'_2015-2018.nc')
# free_pert_trop = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+free_pert+'.nc')
nudged_cont_trop = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+nudged_cont+'.nc')
# nudged_pert_trop = iris.load_cube(trop_data_dir + 'trop_height/time_lon_mn_trop_height_'+nudged_pert+'.nc')


# compute adjustments and cont error diff
free_w_wind_adjust = free_cont_w_wind_time_mean[1] - free_pert_w_wind_time_mean[1]
cont_w_wind_error = free_cont_w_wind_time_mean_4years[1] - nudged_cont_w_wind_time_mean[1]
nudged_w_wind_adjust = nudged_cont_w_wind_time_mean[1] - nudged_pert_w_wind_time_mean[1]
nudged_w_wind_adjust_free_cont_relative = free_cont_w_wind_time_mean_4years[1] -  nudged_pert_w_wind_time_mean[1]


# convert level height coord to km
cubes = [free_w_wind_adjust, cont_w_wind_error, nudged_w_wind_adjust,\
nudged_w_wind_adjust_free_cont_relative]
 
for cube in cubes:
    cube.coord('level_height').convert_units('kilometre')


# convert trop height cubes to km
trop_cubes = [
    free_cont_trop, 
    free_cont_trop_4years, 
    # free_pert_trop, 
    nudged_cont_trop, 
    # nudged_pert_trop
    ]

for cube in trop_cubes:
    cube.convert_units('kilometre')


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
    # # free pair - comment out after first run #
    # plt.figure()
    # mesh = iplt.pcolormesh(free_w_wind_adjust[level], cmap = 'seismic',\
    #                         vmin = -0.0015, vmax = 0.0015)
    # plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
    # current_map = plt.gca()
    # current_map.coastlines(linewidth = 1)
    # plt.title(species+' Free w-wind adjustment, level '+actual_level, size = 'medium')
    # #plt.text(-170,-108, 'Mean = ' + str(mean_free_adjust_level) + ' k')
    # plt.savefig(plot_dir + free_cont+'-'+free_pert+'_free_'+species+'_w_wind_adjustment_level_' + str(actual_level),\
    #             dpi = 400)
    # plt.tight_layout()
    # plt.show()
    # # free pair - comment out after first run #
    
    plt.figure()
    mesh = iplt.pcolormesh(cont_w_wind_error[level], cmap = 'seismic',\
                            vmin = -0.0015, vmax = 0.0015)
    plt.colorbar(mesh, fraction = 0.07, label = u'w-wind control error / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Nudged '+nudging_type+' control w-wind error, level '+actual_level, size = 'medium')
    #plt.text(-170,-108, 'Mean = ' + str(mean_cont_error_level) + ' k')
    plt.savefig(plot_dir + free_cont+'-'+nudged_cont+'_w_wind_cont_error_level_' + str(actual_level),\
                dpi = 400)
    plt.tight_layout()
    plt.show()
    
    plt.figure()
    mesh = iplt.pcolormesh(nudged_w_wind_adjust[level], cmap = 'seismic',\
                            vmin = -0.0015, vmax = 0.0015)
    plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title(species+' Nudged '+nudging_type+' w-wind adjustment, level '+actual_level, size = 'medium')
    #plt.text(-170,-108, 'Mean = ' + str(mean_nudged_adjust_level) + ' k')
    plt.savefig(plot_dir + nudged_cont+'-'+nudged_pert+'_nudged_'+species+'_w_wind_adjustment_level_' + str(actual_level),\
                dpi = 400)
    plt.tight_layout()
    plt.show()
    
    plt.figure()
    mesh = iplt.pcolormesh(nudged_w_wind_adjust_free_cont_relative[level], cmap = 'seismic',\
                            vmin = -0.0015, vmax = 0.0015)
    plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title(species+' Nudged '+nudging_type+' w-wind adjustment, free control, level '+actual_level, size = 'small')
    #plt.text(-170,-108, 'Mean = ' + str(mean_nudged_adjust_free_cont_relative_level) + ' k')
    plt.savefig(plot_dir + free_cont+'-'+nudged_pert+'_nudged_'+species+'_w_wind_adjustment_free_cont_level_' + str(actual_level),\
            dpi = 400)
    plt.tight_layout()
    plt.show()


### Time zonal means ###

# determine adjustments/cont error
free_w_wind_adjust_zonal = free_w_wind_adjust.collapsed('longitude', iris.analysis.MEAN)
cont_w_wind_error_zonal = cont_w_wind_error.collapsed('longitude', iris.analysis.MEAN)
nudged_w_wind_adjust_zonal = nudged_w_wind_adjust.collapsed('longitude', iris.analysis.MEAN)
nudged_w_wind_adjust_free_cont_relative_zonal = nudged_w_wind_adjust_free_cont_relative.collapsed('longitude', iris.analysis.MEAN)

# means - !Should be weighted!
#mean_free_adjust_zonal = np.round(np.mean(free_w_wind_adjust_zonal[:65].data), 3)
#mean_cont_error_zonal = np.round(np.mean(cont_w_wind_error_zonal[:65].data), 3)
#mean_nudged_adjust_zonal = np.round(np.mean(nudged_w_wind_adjust_zonal[:65].data), 3)
#mean_nudged_adjust_free_cont_relative_zonal = np.round(np.mean(nudged_w_wind_adjust_free_cont_relative_zonal[:65].data), 3)



# plot zonal
# # free pair - comment out after first run #
# plt.figure()
# mesh = iplt.pcolormesh(free_w_wind_adjust_zonal[:65], cmap = 'seismic',\
#                             vmin = -0.0015, vmax = 0.0015, coords = ['latitude', 'level_height'])
# plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
# iplt.plot(free_cont_trop, linestyle = '--', linewidth = 2, color = 'black')
# #iplt.plot(free_pert_trop, linestyle = ':', linewidth = 2, color = 'black')
# plt.ylabel('Altitude / km')
# plt.title(species+' Free w-wind zonal mean adjustment', size = 'medium')
# #plt.text(-85,2, 'Mean = ' + str(mean_free_adjust_zonal) + ' k')
# plt.savefig(plot_dir + free_cont+'-'+free_pert+'_free_'+species+'_w_wind_adjustment_zonal',\
#             dpi = 400)
# plt.tight_layout()
# plt.show()
# # free pair - comment out after first run #

plt.figure()
mesh = iplt.pcolormesh(cont_w_wind_error_zonal[:65], cmap = 'seismic',\
                            vmin = -0.0015, vmax = 0.0015, coords = ['latitude', 'level_height'])
plt.colorbar(mesh, fraction = 0.07, label = u'w-wind control error / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
iplt.plot(free_cont_trop, linestyle = '--', linewidth = 2, color = 'black')
#iplt.plot(nudged_cont_trop, linestyle = ':', linewidth = 2, color = 'black')
plt.ylabel('Altitude / km')
plt.title('Nudged '+nudging_type+' w-wind zonal mean control error', size = 'medium')
#plt.text(-85,2, 'Mean = ' + str(mean_cont_error_zonal) + ' k')
plt.savefig(plot_dir + free_cont+'-'+nudged_cont+'_w_wind_cont_error_zonal',\
            dpi = 400)
plt.tight_layout()
plt.show()

plt.figure()
mesh = iplt.pcolormesh(nudged_w_wind_adjust_zonal[:65], cmap = 'seismic',\
                           vmin = -0.0015, vmax = 0.0015, coords = ['latitude', 'level_height'])
plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
iplt.plot(nudged_cont_trop, linestyle = '--', linewidth = 2, color = 'black')
#iplt.plot(nudged_pert_trop, linestyle = ':', linewidth = 2, color = 'black')
plt.ylabel('Altitude / km')
plt.title(species+' Nudged '+nudging_type+' w-wind zonal mean adjustment', size = 'medium')
#plt.text(-85,2, 'Mean = ' + str(mean_nudged_adjust_zonal) + ' k')
plt.savefig(plot_dir + nudged_cont+'-'+nudged_pert+'_nudged_'+species+'_w_wind_adjustment_zonal',\
            dpi = 400)
plt.tight_layout()
plt.show()

plt.figure()
mesh = iplt.pcolormesh(nudged_w_wind_adjust_free_cont_relative_zonal[:65], cmap = 'seismic',\
                            vmin = -0.0015, vmax = 0.0015, coords = ['latitude', 'level_height'])
plt.colorbar(mesh, fraction = 0.07, label = u'w-wind adjustment / m s$^{-1}$', orientation = 'horizontal', extend = 'both')
iplt.plot(free_cont_trop_4years, linestyle = '--', linewidth = 2, color = 'black')
#iplt.plot(nudged_pert_trop, linestyle = ':', linewidth = 2, color = 'black')
plt.ylabel('Altitude / km')
plt.title(species+' Nudged '+nudging_type+' w-wind zonal mean adjustment, free control', size = 'small')
#plt.text(-85,2, 'Mean = ' + str(mean_nudged_adjust_free_cont_relative_zonal) + ' k')
plt.savefig(plot_dir + free_cont+'-'+nudged_pert+'_nudged_'+species+'_w_wind_adjustment_free_cont_zonal',\
            dpi = 400)
plt.tight_layout()
plt.show()
