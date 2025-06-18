#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:23:33 2021

@author: nn819853
"""

"""
Script to calculate mean bias of theta on levels and plot as vertical profile
for control error and adjustment for time slice experiments
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

# set directory name 
diag_folder = 'nudging_testing_new/uv_wind/'
diag_dir = file_loc.diag_dir + diag_folder

# load free cont uv data
free_cont_file_4years = diag_dir + 'time_mean_uv_br793_2015-2018.nc'
free_cont_4years_u_wind = iris.load_cube(free_cont_file_4years, 'mean_u_wind')
free_cont_4years_v_wind = iris.load_cube(free_cont_file_4years, 'mean_v_wind')

# convert level units
free_cont_4years_u_wind.coord('level_height').convert_units('km')
free_cont_4years_v_wind.coord('level_height').convert_units('km')

free_cont_time_mean_4years = [free_cont_4years_u_wind, free_cont_4years_v_wind]

# load free cont and pert 34 year uv data
free_cont_file = diag_dir + 'time_mean_uv_br793.nc'
free_cont_u = iris.load_cube(free_cont_file, 'mean_u_wind')
free_cont_v = iris.load_cube(free_cont_file, 'mean_v_wind')

free_pert_file = diag_dir + 'time_mean_uv_bv046.nc'
free_pert_u = iris.load_cube(free_pert_file, 'mean_u_wind')
free_pert_v = iris.load_cube(free_pert_file, 'mean_v_wind')

# convert level units
free_cont_u.coord('level_height').convert_units('km')
free_pert_u.coord('level_height').convert_units('km')
free_cont_v.coord('level_height').convert_units('km')
free_pert_v.coord('level_height').convert_units('km')

# Calculate free adjustment bias and area RMS
free_adjustment_u = free_cont_u - free_pert_u
free_adjustment_v = free_cont_v - free_pert_v

free_adjustment_copy_u = copy.deepcopy(free_adjustment_u)
free_adjustment_copy_v = copy.deepcopy(free_adjustment_v)

level_mean_free_adjustment_u = flux_mod.area_mean_cube(free_adjustment_u)
level_mean_free_adjustment_v = flux_mod.area_mean_cube(free_adjustment_v)

level_mean_free_adjustment_rms_u = flux_mod.area_rms_cube(free_adjustment_copy_u)
level_mean_free_adjustment_rms_v = flux_mod.area_rms_cube(free_adjustment_copy_v)




# set nudged suite names
nudged_cont_names = [\
                     # 'bz529',
                     #  'bz236',
                      # 'by937',
                      # 'bz237',
                      # 'bz528',
                      'cb108',
                      # 'cb110',
                      #  'ca683',
                      #  'ca682',
                       # 'bz531',
                       # 'ca681',
                       # 'ca680',
                       'cb349',
                       # 'cb351',
                       #  'cj765',
                     ]

nudged_pert_names = [\
                     # 'bz527',
                     #  'bz234',
                      # 'by965',
                      # 'bz235',
                      # 'bz526',
                      'cb109',
                      # 'cb111',
                      #  'ca687',
                      #  'ca686',
                       # 'bz530',
                       # 'ca685',
                       # 'ca684',
                       'cb350',
                       # 'cb352',
                       #  'cj766',
                     ]

n_suites = len(nudged_cont_names)

# set empty lists to contain control errors and adjustments
u_adjustment_list = []
u_cont_error_list = []

v_adjustment_list = []
v_cont_error_list = []

adjustments = [u_adjustment_list, v_adjustment_list]
cont_errors = [u_cont_error_list, v_cont_error_list]

u_adjustment_rms_list = []
u_cont_error_rms_list = []

v_adjustment_rms_list = []
v_cont_error_rms_list = []

adjustments_rms = [u_adjustment_rms_list, v_adjustment_rms_list]
cont_errors_rms = [u_cont_error_rms_list, v_cont_error_rms_list]

# set labels for looping ov u and v separately
winds = ['mean_u_wind', 'mean_v_wind']

for j in range(2):
    
    # load and calculate cont error and adjustment on each nudging setup
    for i in range(n_suites):
        nudged_cont_file = diag_dir + 'time_mean_uv_'+nudged_cont_names[i]+'.nc'
        nudged_pert_file = diag_dir + 'time_mean_uv_'+nudged_pert_names[i]+'.nc' 
        
        nudged_cont_time_mean = iris.load_cube(nudged_cont_file, winds[j])
        nudged_pert_time_mean = iris.load_cube(nudged_pert_file, winds[j])
        
        # convert height to Km
        nudged_cont_time_mean.coord('level_height').convert_units('km')
        nudged_pert_time_mean.coord('level_height').convert_units('km')
        
        cont_error = free_cont_time_mean_4years[j] - nudged_cont_time_mean
        adjustment = nudged_cont_time_mean - nudged_pert_time_mean
        
        cont_error_copy = copy.deepcopy(cont_error)
        adjustment_copy = copy.deepcopy(adjustment)
        
        level_mean_cont_error = flux_mod.area_mean_cube(cont_error)
        level_mean_adjustment = flux_mod.area_mean_cube(adjustment)
        
        adjustments[j].append(level_mean_adjustment)
        cont_errors[j].append(level_mean_cont_error)
        
        level_mean_cont_error_rms = flux_mod.area_rms_cube(cont_error_copy)
        level_mean_adjustment_rms = flux_mod.area_rms_cube(adjustment_copy)
        
        adjustments_rms[j].append(level_mean_adjustment_rms)
        cont_errors_rms[j].append(level_mean_cont_error_rms)    
    

labels = [\
          # r'uv$\theta$, G=1/24',
          # r'uv$\theta$, G=1/12',
          # r'uv$\theta$, G=1/6',
          # r'uv$\theta$, G=1/3',
          # r'uv$\theta$, G=1/1',
          r'uv$\theta$-nudged',    #r'uv$\theta$, BL no-ramp',
          # r'uv$\theta$, BL ramp',
          # 'uv, G=1/24',
          # 'uv, G=1/12',
          # 'uv, G=1/6',
          # 'uv, G=1/3',
          # 'uv, G=1/1',
          'uv-nudged',    #'uv, BL no-ramp',
          # 'uv, BL ramp',
          #  r'uv$\theta$, nudge lev1'
          ]

colours = [\
           # 'brown',
           #  'firebrick',
            # 'red',
            # 'tomato',
            # 'lightcoral',
            'r',   #'peru',
            # 'darkorange',
            # 'midnightblue',
            # 'mediumblue',
            # 'royalblue',
            # 'cornflowerblue',
            # 'lightsteelblue',
            'b',   #'indigo',
            # 'darkviolet',
            # 'green'
            ]

linestyles = [\
              # (0,(1,1)),
              # (0,(1,3)),
              # '-' ,
              # (0,(5,1)),
              # (0,(5,3)),
              ':',    #(0,(5,2,1,2)),
              # (0,(5,1,1,1)),
              # (0,(1,1)),
              # (0,(1,3)),
              # '-' ,
              # (0,(5,1)),
              # (0,(5,3)),
              '--',    #(0,(5,2,1,2)),
              # (0,(5,1,1,1)),
              #  '-'
              ]

# set plot directory
plot_directory = file_loc.plot_dir + 'nudging_testing_new/'


########## Bias plots ##########

### U adjustments ###

#!! not full height! !!#
plt.figure()
for i in range(n_suites):
    iplt.plot(u_adjustment_list[i][0:63], \
              u_adjustment_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
iplt.plot(level_mean_free_adjustment_u[0:63],
          level_mean_free_adjustment_u[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
# plt.xlim(-0.01, 0.015)
plt.ylabel('Altitude / km')
plt.xlabel('U wind speed adjustment / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_u_wind_su_adjustments_profile_best_case', dpi=300)
plt.show()

### U cont error ###
plt.figure()
for i in range(n_suites):
    iplt.plot(u_cont_error_list[i][0:63], \
              u_cont_error_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
plt.xlim(-0.11, 0.03)
plt.ylabel('Altitude / km')
plt.xlabel('U wind speed control error / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_u_wind_cont_errors_profile_best_case', dpi=300)
plt.show()

### V adjustments ###
plt.figure()
for i in range(n_suites):
    iplt.plot(v_adjustment_list[i][0:63], \
              v_adjustment_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
iplt.plot(level_mean_free_adjustment_v[0:63],
          level_mean_free_adjustment_v[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
# plt.xlim(-0.01, 0.015)
plt.ylabel('Altitude / km')
plt.xlabel('V wind speed adjustment / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_v_wind_su_adjustments_profile_best_case', dpi=300)
plt.show()

### V cont error ###
plt.figure()
for i in range(n_suites):
    iplt.plot(v_cont_error_list[i][0:63], \
              v_cont_error_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
plt.xlim(-0.11, 0.03)
plt.ylabel('Altitude / km')
plt.xlabel('V wind speed control error / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_v_wind_cont_errors_profile_best_case', dpi=300)
plt.show()


########### RMS ############


### U adjustments ###
#!! not full height! !!#
plt.figure()
for i in range(n_suites):
    iplt.plot(u_adjustment_rms_list[i][0:63], \
              u_adjustment_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
iplt.plot(level_mean_free_adjustment_rms_u[0:63],
          level_mean_free_adjustment_rms_u[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
plt.xlim(-0.05, 0.8)
plt.ylabel('Altitude / km')
plt.xlabel('U wind speed adjustment rms / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_u_wind_su_adjustments_rms_profile_best_case', dpi=300)
plt.show()

### U cont error ###
plt.figure()
for i in range(n_suites):
    iplt.plot(u_cont_error_rms_list[i][0:63], \
              u_cont_error_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
plt.xlim(-0.02, 0.35)
plt.ylabel('Altitude / km')
plt.xlabel('U wind speed control error rms / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_u_wind_cont_errors_rms_profile_best_case', dpi=300)
plt.show()

### V adjustments ###
plt.figure()
for i in range(n_suites):
    iplt.plot(v_adjustment_rms_list[i][0:63], \
              v_adjustment_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
iplt.plot(level_mean_free_adjustment_rms_v[0:63],
          level_mean_free_adjustment_rms_v[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
plt.xlim(-0.02, 0.4)
plt.ylabel('Altitude / km')
plt.xlabel('V wind speed adjustment rms / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_v_wind_su_adjustments_rms_profile_best_case', dpi=300)
plt.show()

### V cont error ###
plt.figure()
for i in range(n_suites):
    iplt.plot(v_cont_error_rms_list[i][0:63], \
              v_cont_error_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i] 
              )
plt.xlim(-0.01, 0.1)
plt.ylabel('Altitude / km')
plt.xlabel('V wind speed control error rms / m s$^{-1}$')
# plt.legend()
plt.savefig(plot_directory + 'level_mean_v_wind_cont_errors_rms_profile_best_case', dpi=300)
plt.show()
