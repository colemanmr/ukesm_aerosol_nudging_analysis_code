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


# load free cont and pert 34 year theta data
free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
free_cont = iris.load(free_cont_file)
free_cont_time_mean = free_cont[1]

free_pert_su_file = diag_dir + 'time_mean_theta_bv046.pp'
free_pert_su = iris.load(free_pert_su_file)
free_pert_su_time_mean = free_pert_su[1]

# free_pert_bc_file = diag_dir + 'time_mean_theta_ce067.pp'
# free_pert_bc = iris.load(free_pert_bc_file)
# free_pert_bc_time_mean = free_pert_bc[1]


# Calculate free adjustment
free_su_adjustment = free_cont_time_mean - free_pert_su_time_mean

# free_bc_adjustment = free_cont_time_mean - free_pert_bc_time_mean



# set nudged suite names
nudged_cont_names = [
                        #   'ca683',
                        # 'ca682',
                        # 'bz531',
                        # 'ca681',
                        # 'ca680',
                       'cb349',
                        # 'cb351',
                         # 'cj765',
                         # 'bz529',
                       # 'bz236',
                        # 'by937',
                       # 'bz237',
                      #  'bz528',
                       'cb108',
                      #  'cb110',
                     ]

nudged_pert_names = [                     
                        # 'ca687',
                        # 'ca686',
                        # 'bz530',
                        # 'ca685',
                        # 'ca684',
                       'cb350',
                        # 'cb352',
                         # 'cj766',
                         # 'bz527',
                      # 'bz234',
                       # 'by965',
                      # 'bz235',
                      # 'bz526',
                      'cb109',
                       # 'cb111',
                     ]
    


# # /2 so is same number for uv and uvt nudged sims
# n_suites = int(len(nudged_cont_names)/2) 
n_suites = len(nudged_cont_names)


# set empty lists to contain control errors and adjustments
adjustment_list = []
cont_error_list = []

zonal_adj_list = []
zonal_cont_error_list = []


# add free adjustments to adjustment lists
adjustment_list.append(free_su_adjustment)
zonal_adj_list.append(free_su_adjustment.collapsed('longitude', iris.analysis.MEAN))


# load and calculate cont error and adjustment on each nudging setup
for i in range(n_suites):
    nudged_cont_file = diag_dir + 'time_mean_theta_'+nudged_cont_names[i]+'.pp'
    nudged_pert_file = diag_dir + 'time_mean_theta_'+nudged_pert_names[i]+'.pp' 
    
    nudged_cont = iris.load(nudged_cont_file)
    nudged_cont_time_mean = nudged_cont[1]
    
    nudged_pert = iris.load(nudged_pert_file)
    nudged_pert_time_mean = nudged_pert[1]
    
    cont_error = free_cont_time_mean_4years - nudged_cont_time_mean
    adjustment = nudged_cont_time_mean - nudged_pert_time_mean
    
    adjustment_list.append(adjustment)
    cont_error_list.append(cont_error)
    
    
    zonal_adjust = adjustment.collapsed('longitude', iris.analysis.MEAN)
    zonal_cont_error = cont_error.collapsed('longitude', iris.analysis.MEAN)
    
    zonal_adj_list.append(zonal_adjust)
    zonal_cont_error_list.append(zonal_cont_error)
    
    


for cube in zonal_adj_list:
    cube.coord('level_height').convert_units('kilometre')
    
for cube in zonal_cont_error_list:
    cube.coord('level_height').convert_units('kilometre')
    


### Plotting #################################################################

import cartopy.crs as ccrs    
plt.tight_layout()
plt.rcParams.update({'font.size': 10})


# set plot directory
plot_dir = file_loc.plot_dir + 'nudging_testing_new/'


# levels
levels = [0, 8, 25, 45, 53]


# nudge_conf_text = [
#     'G=1/24, bl=10, r=4',
#     'G=1/6, bl=10, r=4',
#     'G=1/1, bl=10, r=4']
nudge_conf_text = ['free', 'uv-nudged', r'uv$\theta$-nudged']



### T adjustment tesselation ###

fig, axs = plt.subplots(nrows=6, ncols=3,
                        subplot_kw={'projection': ccrs.PlateCarree()},
                        figsize = (6, 7),
                        gridspec_kw={'height_ratios': [1, 1, 1, 1, 1, 1]})

    
plt.subplots_adjust(bottom=0.12,
                    left=0,
                    right=1, 
                    top=1, 
                    wspace=0.05, 
                    hspace=0.05)


for i in range(0,3):
    
    for count, ax  in enumerate(axs[0:5,i]):
        
        level = levels[count]
        actual_level = str(levels[count]+1)

        mesh = iplt.pcolormesh(adjustment_list[i][level], axes = ax,
                        cmap = 'seismic', vmin = -2, vmax = 2)
        
        ax.coastlines(linewidth = 0.15)
        
        if count == 0:
            ax.title.set_text(nudge_conf_text[i])
        else:
            print('')
            
        if i == 0:
            ax.text(-0.1, 0.5, 'Level ' + actual_level, 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, rotation = 'vertical')

    
    
    # zonal mean plot
    ax = fig.add_subplot(6,3,16+i)
        
    mesh = iplt.pcolormesh(zonal_adj_list[i], axes = ax,
                    cmap = 'seismic', vmin = -2, vmax = 2)

    ax.set_ylim(0, 30)
    ax.set_xlabel('Latitude')
    
    if i == 0:
        plt.ylabel('Height / km')
        plt.yticks([0, 10, 20, 30])
        
    else:
        ax.get_yaxis().set_visible(False)
        

cbar_ax = fig.add_axes(rect = [0.1, 0.02, 0.7, 0.025])
fig.colorbar(mesh, cax=cbar_ax, label = r'$\theta$ adjustment / K',
             orientation = 'horizontal')

plt.savefig(plot_dir + 
            'nudging_t_adjustment_levels_zonal_free_uv_uvt_tesselation',
            dpi = 300, bbox_inches='tight')
plt.show()



### T cont error tesselation ###

# nudge_conf_text = [
#     'G=1/24, bl=10, r=4',
#     'G=1/6, bl=10, r=4',
#     'G=1/1, bl=10, r=4']
nudge_conf_text = ['uv-nudged', r'uv$\theta$-nudged']



fig, axs = plt.subplots(nrows=6, ncols=2,
                        subplot_kw={'projection': ccrs.PlateCarree()},
                        figsize = (4, 7),
                        gridspec_kw={'height_ratios': [1, 1, 1, 1, 1, 1]})

    
plt.subplots_adjust(bottom=0.12,
                    left=0,
                    right=1, 
                    top=1, 
                    wspace=0.05, 
                    hspace=0.05)


for i in range(0,2):
    
    for count, ax  in enumerate(axs[0:5,i]):
        
        level = levels[count]
        actual_level = str(levels[count]+1)

        mesh = iplt.pcolormesh(cont_error_list[i][level], axes = ax,
                        cmap = 'seismic', vmin = -2, vmax = 2)
        
        ax.coastlines(linewidth = 0.15)
        
        if count == 0:
            ax.title.set_text(nudge_conf_text[i])
        else:
            print('')
            
        if i == 0:
            ax.text(-0.1, 0.5, 'Level ' + actual_level, 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, rotation = 'vertical')

    
    
    # zonal mean plot
    ax = fig.add_subplot(6,2,11+i)
        
    mesh = iplt.pcolormesh(zonal_cont_error_list[i], axes = ax,
                    cmap = 'seismic', vmin = -2, vmax = 2)

    ax.set_ylim(0, 30)
    ax.set_xlabel('Latitude')
    
    if i == 0:
        plt.ylabel('Height / km')
        plt.yticks([0, 10, 20, 30])
        
    else:
        ax.get_yaxis().set_visible(False)
        

cbar_ax = fig.add_axes(rect = [0.01, 0.02, 0.95, 0.025])
fig.colorbar(mesh, cax=cbar_ax, label = r'$\theta$ control error / K',
             orientation = 'horizontal')

plt.savefig(plot_dir + 
            'nudging_t_cont_error_levels_zonal_free_uv_uvt_tesselation',
            dpi = 300, bbox_inches='tight')
plt.show()
