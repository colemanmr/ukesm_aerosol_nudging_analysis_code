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
diag_folder = 'nudging_testing_new/theta/'
diag_dir = file_loc.diag_dir + diag_folder


# load free cont 4 year only theta data
free_cont_file_4years = diag_dir + 'time_mean_theta_br793_2015-2018.pp'
free_cont_4years = iris.load(free_cont_file_4years)
free_cont_time_mean_4years = free_cont_4years[1]

# convert level units
free_cont_time_mean_4years.coord('level_height').convert_units('km')


# load free cont and pert 34 year theta data
free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
free_cont = iris.load(free_cont_file)
free_cont_time_mean = free_cont[1]

free_pert_file = diag_dir + 'time_mean_theta_bv046.pp'
free_pert = iris.load(free_pert_file)
free_pert_time_mean = free_pert[1]

# convert level units
free_cont_time_mean.coord('level_height').convert_units('km')
free_pert_time_mean.coord('level_height').convert_units('km')


# Calculate free adjustment bias and area RMS
free_adjustment = free_cont_time_mean - free_pert_time_mean

free_adjustment_copy = copy.deepcopy(free_adjustment)

level_mean_free_adjustment = flux_mod.area_mean_cube(free_adjustment)

level_mean_free_adjustment_rms = flux_mod.area_rms_cube(free_adjustment_copy)


# # Calculate adjustment and cont error for 9 years G=1/6 uvt nudged
# free_9years_cont_file = diag_dir + 'time_mean_theta_br793_2015-2023.pp'
# free_9years_cont = iris.load(free_9years_cont_file)
# free_9years_cont_time_mean = free_9years_cont[1]

# nudged_9years_cont_file = diag_dir + 'time_mean_theta_by937_2015-2023.pp'
# nudged_9years_cont = iris.load(nudged_9years_cont_file)
# nudged_9years_cont_time_mean = nudged_9years_cont[1]

# nudged_9years_pert_file = diag_dir + 'time_mean_theta_by965_2015-2023.pp'
# nudged_9years_pert = iris.load(nudged_9years_pert_file)
# nudged_9years_pert_time_mean = nudged_9years_pert[1]

# nudged_9years_adjustment = nudged_9years_cont_time_mean - nudged_9years_pert_time_mean
# level_mean_nudged_9years_adjustment = flux_mod.area_mean_cube(nudged_9years_adjustment)

# nudged_9years_cont_error = free_9years_cont_time_mean - nudged_9years_cont_time_mean
# level_mean_nudged_9years_cont_error = flux_mod.area_mean_cube(nudged_9years_cont_error)


# set nudged suite names
nudged_cont_names = [\
                      'bz529',
                       'bz236',
                        'by937',
                       'bz237',
                       'bz528',
                      'cb108',
                       'cb110',
                        'ca683',
                        'ca682',
                        'bz531',
                        'ca681',
                        'ca680',
                       'cb349',
                        'cb351',
                         'cj765',
                     ]

nudged_pert_names = [\
                      'bz527',
                      'bz234',
                       'by965',
                      'bz235',
                      'bz526',
                      'cb109',
                       'cb111',
                        'ca687',
                        'ca686',
                        'bz530',
                        'ca685',
                        'ca684',
                       'cb350',
                        'cb352',
                         'cj766',
                     ]

n_suites = len(nudged_cont_names)

# set empty lists to contain control errors and adjustments
adjustment_list = []
cont_error_list = []

adjustment_rms_list = []
cont_error_rms_list = []

# load and calculate cont error and adjustment on each nudging setup
for i in range(n_suites):
    nudged_cont_file = diag_dir + 'time_mean_theta_'+nudged_cont_names[i]+'.pp'
    nudged_pert_file = diag_dir + 'time_mean_theta_'+nudged_pert_names[i]+'.pp' 
    
    nudged_cont = iris.load(nudged_cont_file)
    nudged_cont_time_mean = nudged_cont[1]
    
    nudged_pert = iris.load(nudged_pert_file)
    nudged_pert_time_mean = nudged_pert[1]
    
    # convert height to km
    nudged_cont_time_mean.coord('level_height').convert_units('km')
    nudged_pert_time_mean.coord('level_height').convert_units('km')
    
    cont_error = free_cont_time_mean_4years - nudged_cont_time_mean
    adjustment = nudged_cont_time_mean - nudged_pert_time_mean
    
    cont_error_copy = copy.deepcopy(cont_error)
    adjustment_copy = copy.deepcopy(adjustment)
    
    level_mean_cont_error = flux_mod.area_mean_cube(cont_error)
    level_mean_adjustment = flux_mod.area_mean_cube(adjustment)
    
    adjustment_list.append(level_mean_adjustment)
    cont_error_list.append(level_mean_cont_error)
    
    level_mean_cont_error_rms = flux_mod.area_rms_cube(cont_error_copy)
    level_mean_adjustment_rms = flux_mod.area_rms_cube(adjustment_copy)
    
    adjustment_rms_list.append(level_mean_adjustment_rms)
    cont_error_rms_list.append(level_mean_cont_error_rms)    
    

# set plotting features 

labels = [\
           r'uv$\theta$, G=1/24',
          r'uv$\theta$, G=1/12',
           r'uv$\theta$, G=1/6',
          r'uv$\theta$, G=1/3',
          r'uv$\theta$, G=1/1',
          r'uv$\theta$, BL no-ramp',
           r'uv$\theta$, BL ramp',
           'uv, G=1/24',
           'uv, G=1/12',
            'uv, G=1/6',
           'uv, G=1/3',
           'uv, G=1/1',
          'uv, BL no-ramp',
           'uv, BL ramp',
            r'uv$\theta$, nudge lev1'
          ]

colours = [\
            'brown',
            'firebrick',
            'red',
            'tomato',
            'lightcoral',
            'peru',
            'darkorange',
            'midnightblue',
            'mediumblue',
            'royalblue',
            'cornflowerblue',
            'lightsteelblue',
            'indigo',
            'darkviolet',
            'green'
            ]

linestyles = [\
               (0,(1,1)),
               (0,(1,3)),
               '-' ,
               (0,(5,1)),
               (0,(5,3)),
              (0,(5,2,1,2)),
               (0,(5,1,1,1)),
               (0,(1,1)),
               (0,(1,3)),
               '-' ,
               (0,(5,1)),
               (0,(5,3)),
              (0,(5,2,1,2)),
               (0,(5,1,1,1)),
                '-'
              ]

# set plot directory
plot_directory = file_loc.plot_dir + 'nudging_testing_new/'
plt.tight_layout()
plt.rcParams.update({'font.size': 10})


# plot level mean adjustments
#!! not full height! !!#
plt.figure(figsize=(10,5))
iplt.plot(level_mean_free_adjustment[0:63], \
          level_mean_free_adjustment[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
# iplt.plot(level_mean_nudged_9years_adjustment[0:63],
#           level_mean_nudged_9years_adjustment[0:63].coord('level_height'),
#           label = 'uvt G = 1/6, 9years',
#           color = 'g')
for i in range(n_suites):
    iplt.plot(adjustment_list[i][0:63], \
              adjustment_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 'small', \
#            labelspacing = 0.2, columnspacing = 0.5, borderaxespad = 0.2,\
#                handleheight = 1.6)
plt.xlim(-0.4, 0.8)
plt.ylabel('Altitude / km')
plt.xlabel(r'$\theta$ adjustment / K ')
plt.savefig(plot_directory + 'level_mean_theta_su_adjustments_profile_nudge_lev1',
             dpi = 300, bbox_inches='tight')
plt.show()

# plot level mean control errors
plt.figure(figsize=(10,5))
for i in range(n_suites):
    iplt.plot(cont_error_list[i][0:63], \
              cont_error_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
# iplt.plot(level_mean_nudged_9years_cont_error[0:63],
#           level_mean_nudged_9years_cont_error[0:63].coord('level_height'),
#           label = 'uvt G = 1/6, 9years',
#           color = 'g')
plt.vlines(0, 0, 28, linestyle = '--', color = 'darkgrey')
# plt.legend(loc = 'center left', ncol = 1, fontsize = 'small', \
#            labelspacing = 0.1, columnspacing = 0.5, borderaxespad = 0.2,\
#                handleheight = 1.3)
plt.xlim(-1.7, 2.3)
plt.ylabel('Altitude / km')
plt.xlabel(r'$\theta$ control error / K ')
plt.savefig(plot_directory + 'level_mean_theta_cont_errors_profile_nudge_lev1', 
            dpi = 300, bbox_inches='tight')
plt.show()

# plot level mean adjustment rms
plt.figure()
iplt.plot(level_mean_free_adjustment_rms[0:63], \
          level_mean_free_adjustment_rms[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
for i in range(n_suites):
    iplt.plot(adjustment_rms_list[i][0:63], \
              adjustment_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
plt.legend(loc = 'lower right', ncol = 1, fontsize = 'small')
plt.xlim(-0.1, 1.4)
plt.ylabel('Altitude / km')
plt.xlabel('Potential temperature RMS-adjustment / K ')
# plt.savefig(plot_directory + 'level_mean_theta_su_adjustments_rms_profile_nudge_lev1', dpi=300)
plt.show()

# plot level mean control error rms
plt.figure()
for i in range(n_suites):
    iplt.plot(cont_error_rms_list[i][0:63], \
              cont_error_rms_list[i][0:63].coord('level_height'),
              label = labels[i],
              color = colours[i],
              linestyle = linestyles[i])
plt.legend(loc = 'lower right', ncol = 1, fontsize = 'small')
plt.xlim(-0.1, 2.5)
plt.ylabel('Altitude / km')
plt.xlabel('Potential temperature RMS-control error / K ')
# plt.savefig(plot_directory + 'level_mean_theta_cont_errors_rms_profile_nudge_lev1', dpi=300)
plt.show()

