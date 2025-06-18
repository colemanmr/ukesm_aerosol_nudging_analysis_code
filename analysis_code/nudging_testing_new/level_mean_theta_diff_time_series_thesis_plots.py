#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:23:33 2021

@author: nn819853
"""

"""
Script to calculate mean bias of theta on levels and surface T and plot 
as time series for a single cont-pert pair of suites
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


# # load free cont and pert 34 year theta data
# free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
# free_cont = iris.load(free_cont_file)
# free_cont_time_mean = free_cont[1]

# free_pert_file = diag_dir + 'time_mean_theta_bv046.pp'
# free_pert = iris.load(free_pert_file)
# free_pert_time_mean = free_pert[1]


# # Calculate free adjustment
# free_adjustment = free_cont_time_mean - free_pert_time_mean
# level_mean_free_adjustment = flux_mod.area_mean_cube(free_adjustment)


# initialise lists for per and cont simulations and lists of suite names
cont_suite_names = ['cb108', 'ch277', 'ch425', 'ch999']
pert_suite_names = ['cb109', 'ch278', 'ch424', 'ci000']

conts_theta = []
perts_theta = []

# loop over suite names loading monthly mean theta data
for suite in cont_suite_names:
    if suite == 'cb108':
            cont_theta = iris.load_cube(diag_dir + 'theta_month_mean_' \
                           + suite + '_2014-2018.pp')
    else:
            cont_theta = iris.load_cube(diag_dir + 'theta_month_mean_' \
                                        + suite + '_2014.pp')
            
    conts_theta.append(cont_theta)
    
    
for suite in pert_suite_names:
    if suite == 'cb109':
            pert_theta = iris.load_cube(diag_dir + 'theta_month_mean_' \
                           + suite + '_2014-2018.pp')
    else:
            pert_theta = iris.load_cube(diag_dir + 'theta_month_mean_' \
                                        + suite + '_2014.pp')
            
    perts_theta.append(pert_theta)
    
    
# initialise list for holding monthly level mean theta adjustments
mon_lev_mean_theta_adj = []

# calculate adjustments and level mean for each suite's monthly mean
for i in range(len(cont_suite_names)):
    monthly_theta_adjustment = conts_theta[i]  - perts_theta[i]
    
    level_mean_theta_adjustment = \
        flux_mod.area_mean_cube(monthly_theta_adjustment)
        
    mon_lev_mean_theta_adj.append(level_mean_theta_adjustment)   
    



# # free
# nudged_cont_file_monthly = diag_dir + 'theta_month_mean_br793_2014-2023.pp'
# nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)

# nudged_pert_file_monthly = diag_dir + 'theta_month_mean_bv046_2014-2023.pp'
# nudged_pert_monthly = iris.load_cube(nudged_pert_file_monthly)

# nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)



####################################################################


########## Select suite for surface T monthly means ############

# surf_t_diag_dir = file_loc.diag_dir + 'other_adjustments/surf_t/'

# # G =1/6 uvt
# nudged_cont_file_monthly_spun_surf_t = surf_t_diag_dir + 'month_mean_surf_t_by937.pp'
# nudged_cont_monthly_spun_surf_t = iris.load(nudged_cont_file_monthly_spun_surf_t)
# nudged_cont_file_monthly_2014_surf_t = surf_t_diag_dir + 'month_mean_surf_t_by937_2014.pp'
# nudged_cont_monthly_2014_surf_t = iris.load(nudged_cont_file_monthly_2014_surf_t)
# nudged_cont_monthly_list_surf_t = iris.cube.CubeList([nudged_cont_monthly_spun_surf_t[0], nudged_cont_monthly_2014_surf_t[0]])
# nudged_cont_monthly_surf_t = nudged_cont_monthly_list_surf_t.concatenate()

# nudged_pert_file_monthly_spun_surf_t = surf_t_diag_dir + 'month_mean_surf_t_by965.pp'
# nudged_pert_monthly_spun_surf_t = iris.load(nudged_pert_file_monthly_spun_surf_t)
# nudged_pert_file_monthly_2014_surf_t = surf_t_diag_dir + 'month_mean_surf_t_by965_2014.pp'
# nudged_pert_monthly_2014_surf_t = iris.load(nudged_pert_file_monthly_2014_surf_t)
# nudged_pert_monthly_list_surf_t = iris.cube.CubeList([nudged_pert_monthly_spun_surf_t[0], nudged_pert_monthly_2014_surf_t[0]])
# nudged_pert_monthly_surf_t = nudged_pert_monthly_list_surf_t.concatenate()

# nudged_adjustment_monthly_surf_t = nudged_cont_monthly_surf_t[0] - nudged_pert_monthly_surf_t[0]
# area_mean_nudged_adjustment_monthly_surf_t = flux_mod.area_mean_cube(nudged_adjustment_monthly_surf_t)


## G =1/6 uvt BL
# nudged_cont_file_monthly_spun_surf_t = surf_t_diag_dir + 'month_mean_surf_t_cb108.pp'
# nudged_cont_monthly_spun_surf_t = iris.load_cube(nudged_cont_file_monthly_spun_surf_t)
# nudged_cont_file_monthly_2014_surf_t = surf_t_diag_dir + 'month_mean_surf_t_cb108_2014.pp'
# nudged_cont_monthly_2014_surf_t = iris.load(nudged_cont_file_monthly_2014_surf_t)
# nudged_cont_monthly_list_surf_t = iris.cube.CubeList([nudged_cont_monthly_spun_surf_t, nudged_cont_monthly_2014_surf_t[0]])
# nudged_cont_monthly_surf_t = nudged_cont_monthly_list_surf_t.concatenate()

# nudged_pert_file_monthly_spun_surf_t = surf_t_diag_dir + 'month_mean_surf_t_cb109.pp'
# nudged_pert_monthly_spun_surf_t = iris.load_cube(nudged_pert_file_monthly_spun_surf_t)
# nudged_pert_file_monthly_2014_surf_t = surf_t_diag_dir + 'month_mean_surf_t_cb109_2014.pp'
# nudged_pert_monthly_2014_surf_t = iris.load(nudged_pert_file_monthly_2014_surf_t)
# nudged_pert_monthly_list_surf_t = iris.cube.CubeList([nudged_pert_monthly_spun_surf_t, nudged_pert_monthly_2014_surf_t[0]])
# nudged_pert_monthly_surf_t = nudged_pert_monthly_list_surf_t.concatenate()

# nudged_adjustment_monthly_surf_t = nudged_cont_monthly_surf_t[0] - nudged_pert_monthly_surf_t[0]
# area_mean_nudged_adjustment_monthly_surf_t = flux_mod.area_mean_cube(nudged_adjustment_monthly_surf_t)


# area_mean_nudged_adjustment_monthly_surf_t_array = area_mean_nudged_adjustment_monthly_surf_t.data

####################################################################


# set plot directory
new_plot_dir = '/storage/silver/scenario/nn819853/plots/nudging_testing_post_mc4/'


from okabe_ito_colours_mod import colours
plt.tight_layout()
plt.rcParams.update({'font.size': 10})


# set levels to plot over
model_levels = np.array([1,11,26,55])
index_levels = model_levels - 1

# set linestyles and colours for simulations and levels
linestyles = [(0,(1,3,1,3)),(0,(4,5,4,5)),(0,(5,4,1,4)),'-']
# colours = ['midnightblue', 'teal', 'seagreen', 'khaki']
colours = [colours[0], colours[1], colours[2], colours[3]]

# set x axis points as calendar not working with 360 days(?)
months = np.linspace(0.5,12.5,num=12)
cb108_months = np.linspace(0.5,60.5,num=60)

save_target = new_plot_dir + \
    'month_lev_mean_theta_adjust_time_series_varying_time_res'

level_labels = ['level 1', 'level 11', 'level 26', 'level 55']
nudge_experiment_labels = ['G=1/6, res=6hr', 'G=1/6, res=3hr',\
                           'G=1/6, res=1hr', 'G=1/3, res=3hr']

plt.figure()
for i in range(len(cont_suite_names)):
    if cont_suite_names[i] == 'cb108':
        for j in range(len(index_levels)):
            plt.plot(cb108_months,\
                     mon_lev_mean_theta_adj[i][:,index_levels[j]].data,\
                     label = level_labels[j],\
                     # label = nudge_experiment_labels[i],\
                     color = colours[i],\
                     linestyle = linestyles[j]
                     # linestyle = '',
                     # marker = 'x'
                     ) 
    else:
        for j in range(len(index_levels)):
            plt.plot(months,\
                     mon_lev_mean_theta_adj[i][:,index_levels[j]].data,\
                     # label = level_labels[j],\
                     # label = nudge_experiment_labels[i],\
                     color = colours[i],\
                     linestyle = linestyles[j]
                     # linestyle = '',
                     # marker = 'x'
                     )
plt.legend()
plt.xlabel('Months')
plt.ylabel('Potential temperature adjustment / K ')
plt.xlim(0,13)
# plt.ylim(-0.21, 0.14)
# plt.ylim(-4.5,3.5)
# plt.xticks([0,12,24,36,48,60])
# plt.title(r'Monthly level mean $\theta$ adjustment, ' + r'uv$\theta$ G=1/6 BL, 3hr input')
# plt.title(r'Monthly level mean $\theta$ adjustment, ' + 'free SU')
# plt.title(r'Monthly level mean $\theta$ adjustment G = 1/6, BL, 3hr input')
plt.savefig(save_target, dpi = 300, bbox_inches='tight')
plt.show()



# # plot level mean adjustments with monthly and total time means
# #!! not full height! !!#
# month = 5
# index_month = month - 1

# plt.figure()
# iplt.plot(level_mean_free_adjustment[0:63], \
#           level_mean_free_adjustment[0:63].coord('level_height'),
#           label = 'free',
#           color = 'black')
# iplt.plot(level_mean_nudged_adjustment[0:63],
#           level_mean_nudged_adjustment[0:63].coord('level_height'),
#           label = 'uvt G = 1/6 BL',
#           color = 'red')
# iplt.plot(level_mean_nudged_adjustment_monthly[index_month,0:63],
#           level_mean_nudged_adjustment_monthly[index_month,0:63].coord('level_height'),
#           label = 'uvt G = 1/6 BL month',
#           color = 'g')
# # for i in range(n_suites):
# #     iplt.plot(adjustment_list[i][0:63], \
# #               adjustment_list[i][0:63].coord('level_height'),
# #               label = labels[i],
# #               color = colours[i],
# #               linestyle = linestyles[i])
# plt.vlines(0, 0, 28000, linestyle = '--', color = 'darkgrey')
# plt.legend(loc = 'lower right', ncol = 2, fontsize = 'small')
# plt.xlim(-0.4, 1.4)
# plt.ylabel('Altitude / m')
# plt.xlabel('Potential temperature adjustment / K ')
# plt.title(r'SU perturbed $\theta$ adjustment profile, month ' + str(month))
# # plt.savefig(new_plot_dir + 'level_mean_theta_su_adjustments_free_and_cb108-cb109_with_month_mean_' + str(month), dpi=300)
# plt.show()