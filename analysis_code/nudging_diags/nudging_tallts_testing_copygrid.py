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

filename = 'bw842_ts_3hours_and_6hourly_nudge_diags_copygrid_ap7.pp'

nudge_analysis, after_nudge, nudge_inc, other_inc, prog_diag \
= iris.load(nudge_dir + filename)

nudge_analysis = nudge_analysis[7:]
after_nudge = after_nudge[7:]
nudge_inc = nudge_inc[7:]
other_inc = other_inc[7:]
prog_diag = prog_diag[7:]

############Reading in free control and Mohit script processed data###########

# Read in theta input for first day 
filename_input = 'br793_theta.pp'
raw_input = iris.load_cube(nudge_dir + filename_input, 'air_potential_temperature')

# Read in Mohit script processed u,v,theta input for time step 0, 18, 36, 54 and select theta
filename_processed = [nudge_dir + 'GLUM_201401010000.nc', \
                      nudge_dir + 'GLUM_201401010600.nc', \
                      nudge_dir + 'GLUM_201401011200.nc', \
                      nudge_dir + 'GLUM_201401011800.nc']
processed_input = iris.load(filename_processed, 'Potential temperature')

# Concatenate cube list into one cube (should work with merge, but for some
# reason each cube in cube list has a 1 length time dimension, rather than
# just scalar coordinate for time)
processed_input = processed_input.concatenate_cube()


##########Plotting############

# 0 - DO NOT USE (0hr for input but is 2hr40min for diags) 1 - 6hr; 2 - 12hr; 3 - 18hr
timestep = 1

fig, ax1 = plt.subplots()
iplt.plot(nudge_inc[timestep,:,72,96], color = 'b', marker = 'x', linewidth = 0.5, label = 'nudge_inc')
iplt.plot(other_inc[timestep,:,72,96], color = 'r', marker = 'x', linewidth = 0.5, label = 'other_inc')
#ax1.set_ylim(-0.5, 0.5)

ax2 = ax1.twinx()
#
iplt.plot(after_nudge[timestep,:,72,96], color = 'g', marker = 'x', linewidth = 0.5, label = 'after_nudge')
iplt.plot(nudge_analysis[timestep,:,72,96], color = 'm', marker = 'x', linewidth = 0.5, label = 'nudge_analysis')
#ax2.set_ylim(320, 390)

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = 'x', linewidth = 0.5, label = 'nudge_analysis_adjusted')
#iplt.plot(raw_input[timestep,:,72,96], color = 'y', marker = 'x', linewidth = 0.5, label = 'raw_input')
#iplt.plot(processed_input[0,:,72,96], color = 'c', marker = 'x', linewidth = 0.5, label = 'processed_input')

#ax2.set_xlim(0, 20000)

ax1.legend(loc = 6, fontsize = 'medium')
ax2.legend(loc = 2, fontsize = 'medium')

plt.title('Test nudging diagnostics - theta')
ax1.set_ylabel('increments of theta / K')
ax2.set_ylabel('theta / K')
ax1.set_xlabel('height / m')

fig.tight_layout()

ax1.set_ylim(-80, 60)
ax2.set_ylim(-300, 6999)

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/fixed_bw842_time_step_' + str(timestep * 18) + '_nudging_diag_profile_analysis_copygrid',\
            dpi = 300)
plt.show()
    

###############Difference######################

# Assign varaibles for specific time step
ts_after_nudge = after_nudge[timestep,:,72,96]
ts_raw_input = raw_input[timestep,:,72,96]
ts_anal = nudge_analysis[timestep,:,72,96]
ts_processed_input = processed_input[timestep,:,72,96]

# Change units to all the same to allow subtraction
ts_anal.units = 'K'
ts_after_nudge.units = 'K'

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
#plt.plot(heights, anal_processed_diff, linewidth = 1, label='analysis - processed input')
#plt.plot(heights, raw_processed_diff, linewidth = 1, label='raw_input - processed input')
#iplt.plot(nudge_diff, label='nudged - analysis')
#iplt.plot(nudge_diff_raw, label='nudged - input')
plt.title('nudging diagnostic differences')
plt.ylabel('theta / K')
plt.xlabel('height / m')
plt.ylim(-9.5, 27.5)
plt.legend()
plt.tight_layout()
plt.savefig(plot_directory + '/fixed_bw842_time_step_' + str(timestep * 18) + '_nudging_diag_profile_differences_copygrid',\
            dpi = 300)
plt.show()
