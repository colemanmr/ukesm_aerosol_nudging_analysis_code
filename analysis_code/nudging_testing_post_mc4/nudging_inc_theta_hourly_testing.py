#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:11:36 2021

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

# import nc_time_axis 

# import datetime
# from iris.time import PartialDateTime
# import cftime


diag_loc = file_loc.diag_dir + 'nudging_testing_post_mc4/theta_inc_diags/'

# filename = diag_loc + 'month_mean_nudge_inc_theta_cb108.pp'


# other inc
filename1 = diag_loc + 'hourly_other_inc_theta_cb108_2014_01_01-02.pp'
filename2 = diag_loc + 'hourly_other_inc_theta_cb108_day_selections.pp'

cube1 = iris.load_cube(filename1)
cube2 = iris.load_cube(filename2)

cubes = iris.cube.CubeList([cube1, cube2])
cubes_merged = cubes.concatenate()

# area_mean_cube = flux_mod.area_mean_cube(cubes_merged[0])


# Nudge inc
filename3 =  diag_loc + 'hourly_nudge_inc_theta_cb108_day_selections.pp'

cube3 = iris.load_cube(filename3)



# Plotting
hours = np.linspace(1, 47, num=47)


# Other inc plotting
plt.figure()
plt.plot(hours, cubes_merged[0][0:47,9,113,0].data, linestyle = '-', color = 'b', label = 'Jan 2014')
plt.plot(hours, cubes_merged[0][48:95,9,113,0].data, linestyle = '--', color = 'g', label = 'Jan 2015')
plt.plot(hours, cubes_merged[0][96:143,9,113,0].data, linestyle = '-.', color = 'm', label = 'Jan 2016')
plt.plot(hours, cubes_merged[0][144:191,9,113,0].data, linestyle = ':', color = 'black', label = 'Jul 2017')
plt.ylabel('theta other inc / K')
plt.xlabel('hours since 1st month 0000Z')
plt.xticks([0,12,24,36,48])
plt.title('Other inc theta G=1/6, BL nudged, control')
plt.legend()
plt.show()


# nudge inc plotting
plt.figure()
plt.plot(hours, cube3[0:47,9,113,0].data, linestyle = '-', color = 'b', label = 'Jan 2014')
plt.plot(hours, cube3[48:95,9,113,0].data, linestyle = '--', color = 'g', label = 'Jan 2015')
plt.plot(hours, cube3[96:143,9,113,0].data, linestyle = '-.', color = 'm', label = 'Jan 2016')
plt.plot(hours, cube3[144:191,9,113,0].data, linestyle = ':', color = 'black', label = 'Jul 2017')
plt.ylabel('theta nudge inc / K')
plt.xlabel('hours since 1st month 0000Z')
plt.xticks([0,12,24,36,48])
plt.title('Nudge inc theta G=1/6, BL nudged, control')
plt.legend()
plt.show()


# plt.figure()
# iplt.pcolormesh(cube[0, 0, 105:115, 0:10])
# axes = plt.gca()
# axes.coastlines()
# plt.show
