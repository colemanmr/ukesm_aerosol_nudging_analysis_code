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


# load free cont and pert 34 year theta data
free_cont_file = diag_dir + 'time_mean_theta_br793.pp'
free_cont = iris.load(free_cont_file)
free_cont_time_mean = free_cont[1]

free_pert_file = diag_dir + 'time_mean_theta_bv046.pp'
free_pert = iris.load(free_pert_file)
free_pert_time_mean = free_pert[1]


# Calculate free adjustment bias and area RMS
free_adjustment = free_cont_time_mean - free_pert_time_mean

free_adjustment_copy = copy.deepcopy(free_adjustment)

level_mean_free_adjustment = flux_mod.area_mean_cube(free_adjustment)

level_mean_free_adjustment_rms = flux_mod.area_rms_cube(free_adjustment_copy)



# # Calculate adjustment and cont error for G=1/6 uvt nudged
nudged_cont_file = diag_dir + 'time_mean_theta_cb108.pp'
nudged_cont = iris.load(nudged_cont_file)
nudged_cont_time_mean = nudged_cont[1]

nudged_pert_file = diag_dir + 'time_mean_theta_cb109.pp'
nudged_pert = iris.load(nudged_pert_file)
nudged_pert_time_mean = nudged_pert[1]

nudged_adjustment = nudged_cont_time_mean - nudged_pert_time_mean
level_mean_nudged_adjustment = flux_mod.area_mean_cube(nudged_adjustment)

# nudged_cont_error = free_cont_time_mean - nudged_cont_time_mean
# level_mean_nudged_cont_error = flux_mod.area_mean_cube(nudged_cont_error)


########## Select nudged suites for monthly means ############

# nudged_cont_file_monthly_spun = diag_dir + 'theta_month_mean_by937_2015-2023.pp'
# nudged_cont_monthly_spun = iris.load_cube(nudged_cont_file_monthly_spun)
# # nudged_9years_cont_time_mean = nudged_9years_cont[1]
# nudged_cont_file_monthly_2014 = diag_dir + 'theta_month_mean_by937_2014.pp'
# nudged_cont_monthly_2014 = iris.load_cube(nudged_cont_file_monthly_2014)
# nudged_cont_monthly_list = iris.cube.CubeList([nudged_cont_monthly_spun, nudged_cont_monthly_2014])
# nudged_cont_monthly = nudged_cont_monthly_list.concatenate()

# nudged_pert_file_monthly_spun = diag_dir + 'theta_month_mean_by965_2015-2023.pp'
# nudged_pert_monthly_spun = iris.load_cube(nudged_pert_file_monthly_spun)
# # nudged_9years_pert_time_mean = nudged_9years_pert[1]
# nudged_pert_file_monthly_2014 = diag_dir + 'theta_month_mean_by965_2014.pp'
# nudged_pert_monthly_2014 = iris.load_cube(nudged_pert_file_monthly_2014)
# nudged_pert_monthly_list = iris.cube.CubeList([nudged_pert_monthly_spun, nudged_pert_monthly_2014])
# nudged_pert_monthly = nudged_pert_monthly_list.concatenate()

# nudged_adjustment_monthly = nudged_cont_monthly[0] - nudged_pert_monthly[0]
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


nudged_cont_file_monthly = diag_dir + 'theta_month_mean_cb108_2014-2018.pp'
nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)

nudged_pert_file_monthly = diag_dir + 'theta_month_mean_cb109_2014-2018.pp'
nudged_pert_monthly = iris.load_cube(nudged_pert_file_monthly)

nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly
level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


# set plot directory
# plot_directory = file_loc.plot_dir + 'nudging_testing_new/'
new_plot_dir = '/storage/silver/scenario/nn819853/plots/nudging_testing_post_mc4/'


# plot level mean adjustments
#!! not full height! !!#
month = 5
index_month = month - 1

plt.figure()
iplt.plot(level_mean_free_adjustment[0:63], \
          level_mean_free_adjustment[0:63].coord('level_height'),
          label = 'free',
          color = 'black')
iplt.plot(level_mean_nudged_adjustment[0:63],
          level_mean_nudged_adjustment[0:63].coord('level_height'),
          label = 'uvt G = 1/6 BL',
          color = 'red')
iplt.plot(level_mean_nudged_adjustment_monthly[index_month,0:63],
          level_mean_nudged_adjustment_monthly[index_month,0:63].coord('level_height'),
          label = 'uvt G = 1/6 BL month',
          color = 'g')
# for i in range(n_suites):
#     iplt.plot(adjustment_list[i][0:63], \
#               adjustment_list[i][0:63].coord('level_height'),
#               label = labels[i],
#               color = colours[i],
#               linestyle = linestyles[i])
plt.vlines(0, 0, 28000, linestyle = '--', color = 'darkgrey')
plt.legend(loc = 'lower right', ncol = 2, fontsize = 'small')
plt.xlim(-0.4, 1.4)
plt.ylabel('Altitude / m')
plt.xlabel('Potential temperature adjustment / K ')
plt.title(r'SU perturbed $\theta$ adjustment profile, month ' + str(month))
# plt.savefig(new_plot_dir + 'level_mean_theta_su_adjustments_free_and_cb108-cb109_with_month_mean_' + str(month), dpi=300)
plt.show()


# plot time series
model_levels = np.array([1,9,20,40,55])
# model_level = 1
index_levels = model_levels - 1

save_target = new_plot_dir + 'monthly_level_mean_theta_adjustment_time_series_cb108-cb109'

level_labels = ['level 1', 'level 9', 'level 20', 'level 40', 'level 55']

plt.figure()
for i in range(len(index_levels)):
    level_mean_nudged_adjustment_monthly_array = level_mean_nudged_adjustment_monthly[:,index_levels[i]].data
    time_series = np.linspace(1, 60, num=60)
    plt.plot(time_series, level_mean_nudged_adjustment_monthly_array, label = level_labels[i])
plt.legend(loc = 'upper right', ncol = 3)
plt.xlabel('Month')
plt.ylabel(r'$\theta$ adjustment / K ')
plt.xlim(-5,125)
plt.ylim(-0.13,0.00)
plt.title(r'Monthly level mean $\theta$ adjustment, ' + r'uv$\theta$ G=1/6 BL')
# plt.savefig(save_target, dpi = 300)
plt.show()


