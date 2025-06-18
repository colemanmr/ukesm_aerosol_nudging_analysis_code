#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:22:39 2020

@author: nn819853
"""

import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt

nudge_dir = '/storage/silver/scenario/nn819853/diags/nudging_diags/'
file = 'theta_g_restart_file_u-bw797.nc'

# Only needed because surface altitude seems to have been added to .nc file -
# hopefully if save as .pp this won't happen, so coudl use load_cube instead
cubes = iris.load(nudge_dir + file)
cube = cubes[0]

# Extract just data over levels for single lat/lon
# use coords over sea
alt_profile = cube[:,30,0]

# Since iris plots altitude on x axis, extract altitudes coords and data
altitudes = alt_profile.coord('altitude').points
altitudes_km = altitudes/1000
g_6hr_param = alt_profile.data * 3

# Make profiles for varying G
g_24hr_param = g_6hr_param/4
g_12hr_param = g_6hr_param/2
g_3hr_param = g_6hr_param*2
g_1hr_param = g_6hr_param*6

# Make profiles for varying levels
g_6hr_bl1_r1 = np.zeros(85)
g_6hr_bl1_r1[:] = g_6hr_param[:]
g_6hr_bl1_r1[1:15] = g_6hr_param[15]

g_6hr_bl1_r4 = np.zeros(85)
g_6hr_bl1_r4[:] = g_6hr_param[:]
g_6hr_bl1_r4[5:15] = g_6hr_param[15]
g_6hr_bl1_r4[1:5] = g_6hr_param[10:14]


# plot with pyplot
plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags/'

plt.figure()
#plt.plot(g_24hr_param, altitudes_km, marker = '+', color = 'brown', label = 'G=1/24')
#plt.plot(g_12hr_param, altitudes_km, marker = 'x', color = 'firebrick', label = 'G=1/12')
#plt.plot(g_6hr_param, altitudes_km, marker = 'o', color = 'red', label = 'G=1/6')
#plt.plot(g_3hr_param, altitudes_km, marker = 'D', color = 'tomato', label = 'G=1/3')
#plt.plot(g_1hr_param, altitudes_km, marker = 'h', color = 'lightcoral', label = 'G=1/1')
#plt.plot(g_6hr_bl1_r1, altitudes_km, marker = 'v', color = 'peru', label = 'G=1/6, bl=1, ramp=1')
#plt.plot(g_6hr_bl1_r4, altitudes_km, marker = '^', color = 'darkorange', label = 'G=1/6, bl=1, ramp=4')

plt.plot(g_24hr_param, altitudes_km, linestyle = (0,(1,1)), linewidth = 2, color = 'brown', label = 'G=1/24')
plt.plot(g_12hr_param, altitudes_km, linestyle = (0,(1,3)), linewidth = 2, color = 'firebrick', label = 'G=1/12')
plt.plot(g_6hr_param, altitudes_km, linestyle = '-' , linewidth = 2, color = 'red', label = 'G=1/6')
plt.plot(g_3hr_param, altitudes_km, linestyle = (0,(5,1)), linewidth = 2, color = 'tomato', label = 'G=1/3')
plt.plot(g_1hr_param, altitudes_km, linestyle = (0,(5,3)), linewidth = 2, color = 'lightcoral', label = 'G=1/1')
plt.plot(g_6hr_bl1_r1, altitudes_km, linestyle = (0,(5,2,1,2)), linewidth = 2, color = 'peru', label = 'G=1/6, bl=1, ramp=1')
plt.plot(g_6hr_bl1_r4, altitudes_km, linestyle = (0,(5,1,1,1)), linewidth = 2, color = 'darkorange', label = 'G=1/6, bl=1, ramp=4')

#plt.title('Theta relaxation parameter vertical profile')
plt.ylabel('Altitude / km')
plt.xlabel(u'G / hr$^{-1}$')
plt.ylim(-5,95)
# plt.ylim(-0.2, 2)
#plt.legend(ncol = 3, fontsize = 'x-small', handlelength = 3.2)
plt.savefig(plot_directory + 'g_param_profile_varying_g_zoom_in.png', dpi = 400)
plt.tight_layout()
plt.show()