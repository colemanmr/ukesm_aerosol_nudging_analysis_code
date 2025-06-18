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
# create lists for each mode and one for all cubes
#cubelists = []
nuc = []
ait = []
acc = []
coa = []

# list of suite names: free, uv-nudged, uvt-nudged
suite_names = [\
                # 'br793',
                # # 'bv046',
                # 'ce067',
                # 'cb349',
                # # 'cb350',
                # 'ce304',
                'cb108',
                # 'cb109',
                'ce303',
               ]

# calculate number of suites
no_suites = len(suite_names)

# load cubes into cubelists
for i in range(no_suites):
    cubes = iris.load(diag_dir + 'aer_burden_mode_nmbr_ratios_sol_' \
                      + suite_names[i] + '_time_mean.pp')
        
    #cubelists.append(cubes)
    
    nuc.append(cubes[0])
    ait.append(cubes[1])
    acc.append(cubes[2])
    coa.append(cubes[3])
 

### Calculate adjustment in each mode
# create list for each mode
nuc_adj = []
ait_adj = []
acc_adj = []
coa_adj = []

# group mode lists and mode adj lists into two lists for looping
modes = (nuc, ait, acc, coa)
mode_adjs = (nuc_adj, ait_adj, acc_adj, coa_adj)

# count number of modes
no_modes = len(modes)

# calc number of nudging types of sims = 2 as just cont and BC pert for now
no_nudging_types = int(no_suites/2)

# loop over nudging types (in pairs of sims, cont and pert)
for i in range(no_nudging_types):
    
    # loop over modes 
    for j in range(no_modes):
        mode = modes[j]
        print(mode)
        
        cont = mode[i*2]
        bc_pert = mode[i*2+1]        
        adjustment = cont - bc_pert
        
        mode_adjs[j].append(adjustment)

 
### Plotting
# set contour intervals
adj_intervals = np.linspace(start = -0.1* 1e-17, stop = 0.1e-17, num = 9)
cont_intervals = np.linspace(start = 0, stop = 2.5e-17, num = 11)

# list of mode names
mode_names = ['nuc', 'ait', 'acc', 'coa']

# loop over nudging types
for i in range(no_nudging_types):
    
    # loop over modes
    for j in range(no_modes):

        # # Plot adjustment for each nudging type in each mode
        plt.figure()
        qplt.contourf(mode_adjs[j][i][11], \
                        levels = adj_intervals, \
                      cmap = 'seismic')
        plt.title(mode_names[j] + ' mode nmbr conc 1km adjust. ' + \
                  suite_names[i*2] + '-' + suite_names[i*2+1])
        figure = plt.gca()
        figure.coastlines(linewidth = 1)
        # plt.savefig(plot_dir + 'aer_burden_lev11_adjustment_su_all_' +\
            # suite_names[i*2] + '-' + suite_names[i*2+1])
        plt.show()
        
        # Plot control burdens for each nudging type in each mode
        plt.figure()
        qplt.contourf(modes[j][i*2][11], \
                        levels = cont_intervals,\
                      cmap = 'magma')
        plt.title(mode_names[j] + ' mode nmbr conc 1km control ' + \
                  suite_names[i*2])
        figure = plt.gca()
        figure.coastlines(linewidth = 1)
        # plt.savefig(plot_dir + 'aer_burden_lev11_cont_su_all_' +\
            # suite_names[i*2])
        plt.show()    











# # loop over however many nudging types there are
# for i in range (no_nudging_types):
    
#     # separate SU and BC adjustment
#     tot_adj_pair = tot_adjs[i]
#     tot_adj_su = tot_adj_pair[0]
#     tot_adj_bc = tot_adj_pair[1]
    
#     # take MIN or MAX over lower trop levels    
#     tot_adj_su_max = tot_adj_su[3:16].collapsed('model_level_number', \
#                                                 iris.analysis.MAX)
#     tot_adj_bc_max = tot_adj_bc[3:16].collapsed('model_level_number', \
#                                                 iris.analysis.MAX)
    
#     # take control for each nudging type
#     cont = tot_burdens[i*3]
#     cont_max = cont[3:16].collapsed('model_level_number', \
#                                                 iris.analysis.MAX)
    
    

    
#     # plot BC perturbed pair adjustment
#     plt.figure()
#     qplt.contourf(tot_adj_bc[11], \
#                    levels = adj_intervals,\
#                   cmap = 'magma')
#     plt.title('all mode SU burden 1km adjustment ' + \
#               suite_names[i*3] + '-' + suite_names[i*3+2])
#     figure = plt.gca()
#     figure.coastlines(linewidth = 1)
#     plt.savefig(plot_dir + 'aer_burden_lev11_adjustment_su_all_' +\
#         suite_names[i*3] + '-' + suite_names[i*3+2])
#     plt.show()
    
    

    
    
    
    