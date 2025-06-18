#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 11:03:16 2020

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


###### Edit here ######

#!! maybe make suite 1 and 2 species options so doesn;t have to be control !!#
#!! also set sky for each suite so can difference sky types !!#
#!! ditto for nudging type !!#
cont_suite = 'br793'
pert_suite = 'ce067'
nudging_type = 'free'
sky_type = 'dre'
species = 'bc'

# set base  name for plot titles
title = 'Free BC ' + sky_type + ' sky'
# title = 'Nudged uv (G=1/6, bl=1, r=1) SU ' + sky_type + ' sky'
# title = r'Nudged uv$\theta$ (G=1/6, bl=1, r=1) SU ' + sky_type + ' sky' 

#######################

##! maybe keep this script non-command line input for flexible plot changing !##
input_file = 'calc_forcing_'+cont_suite+'_control_nudging_'+nudging_type+\
    '_flux_'+sky_type+'_sky_minus_'+pert_suite+'_'+species+\
        '_nudging_'+nudging_type+'_flux_'+sky_type+'_sky_1yr_spinup.nc'
filename = file_loc.diag_dir + 'net_flux/' + input_file

names = [
        'annual_area_meaned_total_sw_down_forcing',
        'annual_area_meaned_total_lw_down_forcing',
        'annual_area_meaned_total_net_down_forcing',
        'multiannual_mean_total_sw_down_forcing',
        'multiannual_mean_total_lw_down_forcing',
        'multiannual_mean_total_net_down_forcing',
        'multiannual_area_mean_total_sw_down_forcing',
        'multiannual_area_mean_total_lw_down_forcing',
        'multiannual_area_mean_total_net_down_forcing',
        'multiannual_area_mean_total_sw_down_forcing_2SE',
        'multiannual_area_mean_total_lw_down_forcing_2SE',
        'multiannual_area_mean_total_net_down_forcing_2SE'
        ]

area_sw_forcing, area_lw_forcing, area_net_forcing,\
time_sw_forcing, time_lw_forcing, time_net_forcing,\
area_time_sw_forcing, area_time_lw_forcing, area_time_net_forcing,\
area_time_double_se_sw_forcing, area_time_double_se_lw_forcing, area_time_double_se_net_forcing\
 = iris.load(filename, names)
 
net_forcing_string = [str(np.round(area_time_net_forcing.data, 2)),\
                      str(np.round(area_time_double_se_net_forcing.data, 2))]
print('Overall forcing is ' + net_forcing_string[0] \
      + ' \u00B1 ' + net_forcing_string[1])
sw_forcing_string = [str(np.round(area_time_sw_forcing.data, 2)),\
                      str(np.round(area_time_double_se_sw_forcing.data, 2))]
print('Overall sw forcing is ' + sw_forcing_string[0] \
      + ' \u00B1 ' + sw_forcing_string[1])
lw_forcing_string = [str(np.round(area_time_lw_forcing.data, 2)),\
                      str(np.round(area_time_double_se_lw_forcing.data, 2))]
print('Overall lw forcing is ' + lw_forcing_string[0] \
      + ' \u00B1 ' + lw_forcing_string[1])

# Determine model years from time dimension, which is hours since 1970
time_points = area_net_forcing.coord('time').points
model_years = time_points/(360*24) + 1970
model_year_labels = np.array(model_years - 0.5, dtype='int') 

# Set plot font size
font = {'size' : 12}
plt.rc('font', **font)

# Set target for saving files
plot_dir = file_loc.plot_dir + 'net_fluxes/'
name = input_file[13:-3]
target = plot_dir + name

# #!!! need to make clear where spin up begins! !!!#
# # Plot time series of annual mean forcings
# plt.figure()
# plt.title(title + ' annual mean forcing', fontsize = 'medium')
# plt.plot(model_years, area_net_forcing.data, color = 'black', linestyle = '-', label = 'net')  
# plt.plot(model_years, area_sw_forcing.data, color = 'mediumblue', linestyle = '-', label = 'sw')
# plt.plot(model_years, area_lw_forcing.data, color = 'r', linestyle = '-', label = 'lw')
# plt.ylabel(u'Radiative forcing / W m$^{-2}$', fontsize = 'medium')
# plt.xlabel('Model Year', fontsize = 'medium')
# plt.ylim(-3,1.5)
# plt.xticks(ticks=model_years, labels = model_year_labels)
# plt.legend(ncol = 3)
# plt.savefig(target + '_annual_means_time_series', dpi = 400)
# plt.show()       

#!! change color scheme to better for color blindness!!! !!#
# plot maps of multiannual mean forcings
plt.figure()
mesh = iplt.pcolormesh(time_net_forcing, cmap = 'seismic', vmin = -15, vmax = 15)
plt.colorbar(mesh, fraction = 0.075, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.title(title + ' net forcing', fontsize = 'medium')
plt.text(-170, -110, 'Mean = ' + net_forcing_string[0] + ' \u00B1 ' + net_forcing_string[1] + u' W m$^{-2}$')
plt.savefig(target + '_multiannual_mean_map_net_15_to_15_scale', dpi = 300)
plt.show()

plt.figure()
mesh = iplt.pcolormesh(time_sw_forcing, cmap = 'seismic', vmin = -15, vmax = 15)
plt.colorbar(mesh, fraction = 0.075, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.title(title + ' sw forcing', fontsize = 'medium')
plt.text(-170, -110, 'Mean = ' + sw_forcing_string[0] + ' \u00B1 ' + sw_forcing_string[1] + u' W m$^{-2}$')
plt.savefig(target + '_multiannual_mean_map_sw_15_to_15_scale', dpi = 300)
plt.show()

plt.figure()
mesh = iplt.pcolormesh(time_lw_forcing, cmap = 'seismic', vmin = -15, vmax = 15)
plt.colorbar(mesh, fraction = 0.075, label = u' W m$^{-2}$', orientation = 'horizontal')
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.title(title + ' lw forcing', fontsize = 'medium')
plt.text(-170, -110, 'Mean = ' + lw_forcing_string[0] + ' \u00B1 ' + lw_forcing_string[1] + u' W m$^{-2}$')
plt.savefig(target + '_multiannual_mean_map_lw_15_to_15_scale', dpi = 300)
plt.show()
