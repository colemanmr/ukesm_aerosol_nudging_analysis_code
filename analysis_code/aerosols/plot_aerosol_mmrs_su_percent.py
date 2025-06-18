#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:32:39 2023

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
import copy
import character_shortcuts as char
import iris.quickplot as qplt


# set directory name 
diag_folder = 'aerosols/'
diag_dir = file_loc.diag_dir + diag_folder
plot_dir = file_loc.plot_dir + 'aerosols/'


### Load in time mean mode separated mass aerosol per mass of air data
# create list to contain a CubeList of four cubes (modes) from each suite
cubelists = []

# list of suite names: free, uv-nudged, uvt-nudged
suite_names = [\
                'br793',
                'bv046',
                'ce067',
                'cb349',
                'cb350',
                'ce304',
                'cb108',
                'cb109',
                'ce303',
               ]

# calculate number of suites
no_suites = len(suite_names)

# load cubes into cubelists
for i in range(no_suites):
    cubes = iris.load(diag_dir + 'aer_burden_mmr_su_' \
                      + suite_names[i] + '_time_mean.pp')
        
    cubelists.append(cubes)
    

### For each suite calculate total burden 
# create lists to hold
tot_burdens = []

# calculate  for each suite
for i in range(no_suites):
    cubes = cubelists[i]
    print(cubes)
    
    tot_burden = cubes[0] + cubes[1] + cubes[2] + cubes[3]
    # tot_burden = cubes[1]
    # tot_burden = cubes[1] + cubes[2] + cubes[3]
    # tot_burden = cubes[2] + cubes[3]
    
    tot_burdens.append(tot_burden)
    

### Caclulate adjustment 
# create list 
tot_adjs = []
percent_adjs = []

# calc number of nudging types of experiments
no_nudging_types = int(no_suites/3)

# Calculate adjustments in burden
for i in range(no_nudging_types):
    cont = tot_burdens[i*3]
    su_pert = tot_burdens[i*3+1]
    bc_pert = tot_burdens[i*3+2]
    
    tot_adj_su = cont - su_pert
    tot_adj_bc = cont - bc_pert
    
    tot_adjs.append([tot_adj_su, tot_adj_bc])
    
    # calculate percent adjustment as fraction of free control burden
    percent_adj_su = tot_adj_su * 100 / tot_burdens[0]
    percent_adj_bc = tot_adj_bc * 100 / tot_burdens[0]
    
    percent_adjs.append([percent_adj_su, percent_adj_bc])    
    

### Plotting
# set contour intervals
# adj_intervals = np.linspace(start = - 0.6* 1e-9, stop = 0.3e-9, num = 19)
cont_intervals = np.linspace(start = 0, stop = 2e-8, num = 9)
# neg_percent_intervals_bc_runs = np.linspace(start = -0.22, stop = 0, num = 23)*100
percent_intervals = np.linspace(start = -1.0, stop = 1.0, num = 21)*100

# percent_intervals_manual_bc = (-200, -100, -20, -15, -12.5, -10, -8, -6, -4, -2, 0,
#                                2, 4, 6, 8, 10, 12.5, 15, 20, 100, 200)


# from matplotlib.colors import LinearSegmentedColormap

# # Define custom colormap similar to seismic
# colors = [(0.0, "blue"), (0.3, "lightblue"), (0.45, "white"), (0.55, "white"),
#           (0.7, "lightcoral"), (1.0, "red")]
# cmap_name = 'custom_seismic'
# custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors)


# loop over however many nudging types there are
for i in range (no_nudging_types):
    
    # separate SU and BC adjustment
    tot_adj_pair = tot_adjs[i]
    tot_adj_su = tot_adj_pair[0]
    tot_adj_bc = tot_adj_pair[1]
    
    # # take MIN or MAX over lower trop levels    
    # tot_adj_su_max = tot_adj_su[3:16].collapsed('model_level_number', \
    #                                             iris.analysis.MIN)
    # tot_adj_bc_max = tot_adj_bc[3:16].collapsed('model_level_number', \
    #                                             iris.analysis.MIN)
    
    percent_adj_pair = percent_adjs[i]
    percent_adj_su = percent_adj_pair[0]
    percent_adj_bc = percent_adj_pair[1]
    
    # take control for each nudging type
    cont = tot_burdens[i*3]
    cont_max = cont[3:16].collapsed('model_level_number', \
                                                iris.analysis.MAX)
    
    
    # Plot SU perturbed pair adjustment
    plt.figure()
    mesh = iplt.contourf(percent_adj_su[11],\
                         # .collapsed('model_level_number', \
                         #                        iris.analysis.MAX), \
                    levels = percent_intervals_manual_bc, \
                  cmap = 'seismic')
    plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment / %', \
                  orientation = 'horizontal')    
    plt.title('all mode SU burden 1km % adjustment ' + \
              suite_names[i*3] + '-' + suite_names[i*3+1])
    figure = plt.gca()
    figure.coastlines(linewidth = 1)
    # plt.savefig(plot_dir + 'aer_burden_lev11_percent_adjustment_su_all_modes_' +\
    #     suite_names[i*3] + '-' + suite_names[i*3+1] + '_negative_scale')
    plt.show()
    
    
    # plot BC perturbed pair adjustment
    plt.figure()
    mesh = iplt.contourf(percent_adj_bc[11],\
                         # .collapsed('model_level_number', \
                         #                        iris.analysis.MIN), \
                    levels = percent_intervals_manual_bc,\
                  cmap = 'seismic')
    plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment / %', \
                  orientation = 'horizontal')
    plt.title('all mode SU burden 1km % adjustment ' + \
              suite_names[i*3] + '-' + suite_names[i*3+2])
    figure = plt.gca()
    figure.coastlines(linewidth = 1)
    # plt.savefig(plot_dir + 'aer_burden_lev11_percent_adjustment_su_all_modes_' +\
    #     suite_names[i*3] + '-' + suite_names[i*3+2] + '_negative_scale')
    plt.show()
    
    
#     # Plot control burdens
#     plt.figure()
#     qplt.contourf(cont_max, \
#                     levels = cont_intervals,\
#                   cmap = 'magma')
#     plt.title('all mode SU burden max in control ' + \
#               suite_names[i*3])
#     figure = plt.gca()
#     figure.coastlines(linewidth = 1)
#     plt.savefig(plot_dir + 'aer_burden_max_cont_su_all_modes_' +\
#         suite_names[i*3])
#     plt.show()    
    

# # More plotting - diff of diffs
# free_minus_uv_adj_su = percent_adjs[0][0] - percent_adjs[1][0]
# uv_minus_uvt_adj_su = percent_adjs[1][0] - percent_adjs[2][0]
# free_minus_uv_adj_bc = percent_adjs[0][1] - percent_adjs[1][1]
# uv_minus_uvt_adj_bc = percent_adjs[1][1] - percent_adjs[2][1]

# # set intervals
# diffofdiff_intervals = np.linspace(start = -24, stop = 24, num = 13)


# # free minus uv-nudged percentage SU burden adjustment
# plt.figure()
# mesh = iplt.contourf(free_minus_uv_adj_su[11],\
#                      # .collapsed('model_level_number', \
#                      #                        iris.analysis.MAX), \
#                 levels = diffofdiff_intervals, \
#               cmap = 'seismic')
# plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment difference / %', \
#               orientation = 'horizontal')    
# plt.title('all mode SU burden free minus uv-nudged % adjustment')
# figure = plt.gca()
# figure.coastlines(linewidth = 1)
# plt.savefig(plot_dir + 'aer_burden_lev11_percent_free-uv_adjust_su_all_modes_' +\
#     suite_names[0] + '-' + suite_names[1] + '_minus_' +\
#         suite_names[3] + '-' + suite_names[4])
# plt.show()


# # uv-nudged minus uvt-nudged percentage SU burden adjustment
# plt.figure()
# mesh = iplt.contourf(uv_minus_uvt_adj_su[11],\
#                      # .collapsed('model_level_number', \
#                      #                        iris.analysis.MAX), \
#                 levels = diffofdiff_intervals, \
#               cmap = 'seismic')
# plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment difference / %', \
#               orientation = 'horizontal')    
# plt.title('all mode SU burden uv- minus uvt-nudged % adjustment')
# figure = plt.gca()
# figure.coastlines(linewidth = 1)
# plt.savefig(plot_dir + 'aer_burden_lev11_percent_uv-uvt_adjust_su_all_modes_' +\
#     suite_names[3] + '-' + suite_names[4] + '_minus_' +\
#         suite_names[6] + '-' + suite_names[7])
# plt.show()


# # free minus uv-nudged percentage SU burden adjustment BC perturbed experiment
# plt.figure()
# mesh = iplt.contourf(free_minus_uv_adj_bc[11],\
#                      # .collapsed('model_level_number', \
#                      #                        iris.analysis.MAX), \
#                 levels = diffofdiff_intervals, \
#               cmap = 'seismic')
# plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment difference / %', \
#               orientation = 'horizontal')    
# plt.title('all mode SU burden free minus uv-nudged (BC pert) % adjustment')
# figure = plt.gca()
# figure.coastlines(linewidth = 1)
# plt.savefig(plot_dir + 'aer_burden_lev11_percent_free-uv_adjust_su_all_modes_' +\
#     suite_names[0] + '-' + suite_names[2] + '_minus_' +\
#         suite_names[3] + '-' + suite_names[5])
# plt.show()


# # uv-nudged minus uvt-nudged percentage SU burden adjustment BC perturbed experimnt
# plt.figure()
# mesh = iplt.contourf(uv_minus_uvt_adj_bc[11],\
#                      # .collapsed('model_level_number', \
#                      #                        iris.analysis.MAX), \
#                 levels = diffofdiff_intervals, \
#               cmap = 'seismic')
# plt.colorbar(mesh,  fraction = 0.070, label = 'SU mmr adjustment difference / %', \
#               orientation = 'horizontal')    
# plt.title('all mode SU burden uv- minus uvt-nudged (BC pert) % adjustment')
# figure = plt.gca()
# figure.coastlines(linewidth = 1)
# plt.savefig(plot_dir + 'aer_burden_lev11_percent_uv-uvt_adjust_su_all_modes_' +\
#     suite_names[3] + '-' + suite_names[5] + '_minus_' +\
#         suite_names[6] + '-' + suite_names[8])
# plt.show()