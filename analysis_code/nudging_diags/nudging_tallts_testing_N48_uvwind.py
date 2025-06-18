#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:47:53 2020

@author: nn819853
"""

import numpy as np
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import iris.coord_categorisation

nudge_dir = '/storage/silver/scenario/nn819853/diags/nudging_diags/'

filename = 'by762_6hourly_nudge_diags_uv_ap7.pp'

nudge_analysis_u, after_nudge_u, nudge_inc_u, other_inc_u, \
nudge_analysis_v, after_nudge_v, nudge_inc_v, other_inc_v,  \
prog_diag_u, prog_diag_v \
= iris.load(nudge_dir + filename)

nudge_analysis = nudge_analysis_v
after_nudge = after_nudge_v
nudge_inc = nudge_inc_v
other_inc = other_inc_v
prog_diag = prog_diag_v

############Reading in free control and Mohit script processed data###########

# Read in theta input for first day 
filename_input = 'br793_uv_ap7.pp'
raw_input = iris.load_cube(nudge_dir + filename_input, 'y_wind')
raw_input = raw_input[1:]

# Read in Mohit script processed u,v,theta input for time step 0, 18, 36, 54 and select theta
filename_processed = [nudge_dir + 'GLUM_201401010000.nc', \
                      nudge_dir + 'GLUM_201401010600.nc', \
                      nudge_dir + 'GLUM_201401011200.nc', \
                      nudge_dir + 'GLUM_201401011800.nc']
processed_input = iris.load(filename_processed, 'Northerly component of wind  v')

# Concatenate cube list into one cube (should work with merge, but for some
# reason each cube in cube list has a 1 length time dimension, rather than
# just scalar coordinate for time)
processed_input = processed_input.concatenate_cube()


##########Plotting############

# 0 - 6hr; 1 - 12hr; 2 - 18hr
timestep = 0

fig, ax1 = plt.subplots()
iplt.plot(nudge_inc[timestep,:,0,0], color = 'b', marker = 'x', linewidth = 0.5, label = 'nudge_inc')
iplt.plot(other_inc[timestep,:,0,0], color = 'r', marker = 'x', linewidth = 0.5, label = 'other_inc')
#ax1.set_ylim(-0.5, 0.5)

ax2 = ax1.twinx()
#
iplt.plot(after_nudge[timestep,:,0,0], color = 'g', marker = 'x', linewidth = 0.5, label = 'after_nudge')
iplt.plot(nudge_analysis[timestep,:,0,0], color = 'm', marker = 'x', linewidth = 0.5, label = 'nudge_analysis')
#ax2.set_ylim(320, 390)

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = 'x', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[timestep,:,0,0], color = 'y', marker = 'x', linewidth = 0.5, label = 'raw_input')
#iplt.plot(processed_input[0,:,72,96], color = 'c', marker = 'x', linewidth = 0.5, label = 'processed_input')

#ax2.set_xlim(0, 20000)

ax1.legend(loc = 6, fontsize = 'medium')
ax2.legend(loc = 2, fontsize = 'medium')

plt.title('Test nudging diagnostics - v-wind')
ax1.set_ylabel('increments of v / m s-1')
ax2.set_ylabel('v / m s-1')
ax1.set_xlabel('height / m')

fig.tight_layout()

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/fixed_by762_vwind_N48_time_step_' + str((timestep + 1) * 18) + '_nudging_diag_profile_analysis_lat0lon0',\
            dpi = 300)
plt.show()
    

###############Difference######################

# Assign varaibles for specific time step
ts_after_nudge = after_nudge_u[timestep,:,0,0]
ts_raw_input = raw_input[timestep,:,0,0]
ts_anal = nudge_analysis_u[timestep,:,0,0]
ts_processed_input = processed_input[timestep,:,0,0]

# Change units to all the same to allow subtraction
ts_anal.units = 'm s-1'
ts_after_nudge.units = 'm s-1'

# Extract data from processed input and anal for subtraction as diff coords
ts_anal_data = ts_anal.data
ts_processed_input_data = ts_processed_input.data
ts_raw_input_data = ts_raw_input.data

#Extract model levels for plottign data anal_processed_diff
heights = ts_after_nudge.coord('level_height').points

# Calculate differences in variables
#nudge_diff_raw = ts_after_nudge - ts_raw_input
#nudge_diff = ts_after_nudge - ts_anal
anal_raw_diff = ts_anal - ts_raw_input
anal_processed_diff = ts_anal_data - ts_processed_input_data
raw_processed_diff = ts_raw_input_data - ts_processed_input_data

plt.figure()
iplt.plot(anal_raw_diff, linewidth = 2, label='analysis - raw input')
#plt.plot(heights, anal_processed_diff, linewidth = 2, label='analysis - processed input')
#plt.plot(heights, raw_processed_diff, linewidth = 1, label='raw_input - processed input')
#iplt.plot(nudge_diff, label='nudged - analysis')
#iplt.plot(nudge_diff_raw, label='nudged - input')
plt.title('nudging diagnostic differences')
plt.ylabel('v / m s-1')
plt.xlabel('height / m')
plt.legend()
plt.tight_layout()
plt.savefig(plot_directory + '/fixed_by762_vwind_N48_time_step_' + str((timestep + 1) * 18) + '_nudging_diag_profile_differences_lat0lon0',\
            dpi = 300)
plt.show()
