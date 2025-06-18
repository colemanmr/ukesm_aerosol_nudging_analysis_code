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


# # Calculate adjustment for G=1/6 uvt nudged
# nudged_cont_file = diag_dir + 'time_mean_theta_cb108.pp'
# nudged_cont = iris.load(nudged_cont_file)
# nudged_cont_time_mean = nudged_cont[1]

# nudged_pert_file = diag_dir + 'time_mean_theta_cb109.pp'
# nudged_pert = iris.load(nudged_pert_file)
# nudged_pert_time_mean = nudged_pert[1]

# nudged_adjustment = nudged_cont_time_mean - nudged_pert_time_mean
# level_mean_nudged_adjustment = flux_mod.area_mean_cube(nudged_adjustment)


########## Select which nudged suites for theta monthly means ############

# # G=1/6 uvt
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


# # G=1/6 uvt BL
# nudged_cont_file_monthly = diag_dir + 'theta_month_mean_cb108_2014-2018.pp'
# nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)

# nudged_pert_file_monthly = diag_dir + 'theta_month_mean_cb109_2014-2018.pp'
# nudged_pert_monthly = iris.load_cube(nudged_pert_file_monthly)

# nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


# nudged_cont_file_monthly_1 = diag_dir + 'theta_month_mean_cb108_2014-2018.pp'
# nudged_cont_monthly_1 = iris.load_cube(nudged_cont_file_monthly_1)
# # nudged_9years_cont_time_mean = nudged_9years_cont[1]
# nudged_cont_file_monthly_2 = diag_dir + 'theta_month_mean_cb108_2019-2020.pp'
# nudged_cont_monthly_2 = iris.load_cube(nudged_cont_file_monthly_2)
# nudged_cont_monthly_list = iris.cube.CubeList([nudged_cont_monthly_1, nudged_cont_monthly_2])
# nudged_cont_monthly = nudged_cont_monthly_list.concatenate()

# nudged_pert_file_monthly_1 = diag_dir + 'theta_month_mean_cb109_2014-2018.pp'
# nudged_pert_monthly_1 = iris.load_cube(nudged_pert_file_monthly_1)
# # nudged_9years_pert_time_mean = nudged_9years_pert[1]
# nudged_pert_file_monthly_2 = diag_dir + 'theta_month_mean_cb109_2019-2020.pp'
# nudged_pert_monthly_2 = iris.load_cube(nudged_pert_file_monthly_2)
# nudged_pert_monthly_list = iris.cube.CubeList([nudged_pert_monthly_1, nudged_pert_monthly_2])
# nudged_pert_monthly = nudged_pert_monthly_list.concatenate()

# nudged_adjustment_monthly = nudged_cont_monthly[0] - nudged_pert_monthly[0]
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)



# G=1/6 uvt BL 3-hourly input
# nudged_cont_file_monthly = diag_dir + 'theta_month_mean_ch277_2014.pp'
# nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)

# nudged_pert_file_monthly = diag_dir + 'theta_month_mean_ch278_2014_jan-jun.pp'
# nudged_pert_monthly = iris.load_cube(nudged_pert_file_monthly)

# nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly[6]
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


# G=1/3 uvt BL 3-hourly input
nudged_cont_file_monthly = diag_dir + 'theta_month_mean_ch999_2014.pp'
nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)

# nudged_pert_file_monthly = diag_dir + 'theta_month_mean_ch278_2014_jan-jun.pp'
# nudged_pert_monthly = iris.load_cube(nudged_pert_file_monthly)

# nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly[6]
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


# # G=1/6 uvt BL 1-hourly input
# nudged_cont_file_monthly = diag_dir + 'theta_month_mean_ch425_2014.pp'
# nudged_cont_monthly = iris.load_cube(nudged_cont_file_monthly)


# free
free_cont_file_monthly = diag_dir + 'theta_month_mean_br793_2014-2023.pp'
free_cont_monthly = iris.load_cube(free_cont_file_monthly)

# free_pert_file_monthly = diag_dir + 'theta_month_mean_bv046_2014-2023.pp'
# free_pert_monthly = iris.load_cube(free_pert_file_monthly)

# nudged_adjustment_monthly = nudged_cont_monthly - nudged_pert_monthly
# level_mean_nudged_adjustment_monthly = flux_mod.area_mean_cube(nudged_adjustment_monthly)


nudged_cont_error_monthly = free_cont_monthly[:12] - nudged_cont_monthly
level_mean_nudged_cont_error_monthly = flux_mod.area_mean_cube(nudged_cont_error_monthly)

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
# plot_directory = file_loc.plot_dir + 'nudging_testing_new/'
new_plot_dir = '/storage/silver/scenario/nn819853/plots/nudging_testing_post_mc4/'


# plot time series
model_levels = np.array([1,9,20,40,55])
# model_level = 1
index_levels = model_levels - 1

save_target = new_plot_dir + 'monthly_level_mean_theta_cont_error_time_series_br793-ch999_2014'

level_labels = ['level 1', 'level 9', 'level 20', 'level 40', 'level 55']

plt.figure()
for i in range(len(index_levels)):
    level_mean_nudged_cont_error_monthly_array = level_mean_nudged_cont_error_monthly[:,index_levels[i]].data
    time_series = np.linspace(1, 84, num=84)
    plt.plot(time_series[0:12], level_mean_nudged_cont_error_monthly_array, label = level_labels[i])
# plt.plot(time_series[0:60], area_mean_nudged_adjustment_monthly_surf_t_array, color = 'magenta', label = 'surf_t')
plt.legend(loc = 'upper right', ncol = 3)
plt.xlabel('Months')
plt.ylabel('Cont error / K ')
plt.xlim(-5,125)
plt.ylim(-0.21,0.14)
plt.xticks([0,12,24,36,48,60,72,84,96,108,120])
plt.title(r'Monthly level mean $\theta$ cont error, ' + r'uv$\theta$ G = 1/3, BL, 3hr input')
plt.savefig(save_target, dpi = 300)
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