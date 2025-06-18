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

filename = 't_nudging_diags_ap7_redo.pp'

nudge_analysis, after_nudge, nudge_inc, other_inc, \
= iris.load(nudge_dir + filename)
#prog_diag_1, prog_diag_2 \

#############For shifting one model level up#########################

# Extract nudge analysis values to ndarray and remove last value
anal = nudge_analysis[0,:,72,96].data
anal_adjust = anal[:-1]

# Extract model level heights to ndarray and remove first value
altitudes = nudge_analysis.coord('level_height').points
alt_adjust = altitudes[1:]

############Reading in free control and Mohit script processed data###########

# Read in theta input for first day 
filename_input = 'br793_theta.pp'
raw_input = iris.load_cube(nudge_dir + filename_input, 'air_potential_temperature')

# Read in Mohit script processed u,v,theta input for time step 0 and select theta
filename_processed = 'GLUM_201401010000.nc'
processed_input = iris.load_cube(nudge_dir + filename_processed, 'Potential temperature')

############# Reading in section zero diags#####################

# Readin  section zero diag for theta (00004)
filename_zero = 'bw842_section_zero_theta_6hr.pp'
output_theta = iris.load_cube(nudge_dir + filename_zero, 'air_potential_temperature')

###########Plotting############

fig, ax1 = plt.subplots()
iplt.plot(nudge_inc[0,:,72,96], color = 'b', marker = 'x', linewidth = 0.5, label = 'nudge_inc')
iplt.plot(other_inc[0,:,72,96], color = 'r', marker = 'x', linewidth = 1, label = 'other_inc')
ax1.set_ylim(-0.5, 0.5)

ax2 = ax1.twinx()
#
iplt.plot(after_nudge[0,:,72,96], color = 'g', marker = 'x', linewidth = 0.5, label = 'after_nudge')
#iplt.plot(nudge_analysis[0,:,72,96], color = 'm', marker = 'x', linewidth = 0.5, label = 'nudge_analysis')
#ax2.set_ylim(320, 390)

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = 'x', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[0,:,72,96], color = 'y', marker = 'x', linewidth = 0.5, label = 'raw_input')
#iplt.plot(processed_input[0,:,72,96], color = 'c', marker = 'x', linewidth = 0.5, label = 'processed_input')

iplt.plot(output_theta[0,:,72,96], color = 'maroon', marker = 'x', linewidth = 0.5, label = 'output_theta_00004')

#ax2.set_xlim(0, 20000)

ax1.legend(loc = 6, fontsize = 'medium')
ax2.legend(loc = 2, fontsize = 'medium')

plt.title('Test nudging diagnostics - theta')
ax1.set_ylabel('increments of theta / K')
ax2.set_ylabel('theta / K')
ax1.set_xlabel('height / m')

fig.tight_layout()

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/fixed_bw842_time_step_1_nudging_diag_profile_analysis_with_00004_diag',\
            dpi = 300)
plt.show()
    

###############Difference######################

ts_after_nudge = after_nudge[1,:,72,96]
ts_raw_input = raw_input[1,:,72,96]
ts_anal = nudge_analysis[1,:,72,96]

ts_anal.units = 'K'
ts_after_nudge.units = 'K'

anal_diff = ts_anal - ts_raw_input
nudge_diff_raw = ts_after_nudge - ts_raw_input
nudge_diff = ts_after_nudge - ts_anal

plt.figure()
iplt.plot(anal_diff, label='analysis - input')
#iplt.plot(nudge_diff, label='nudged - analysis')
#iplt.plot(nudge_diff_raw, label='nudged - input')
plt.ylabel('theta / K')
plt.xlabel('height / m')
plt.legend()
plt.savefig(plot_directory + '/fixed_bw842_time_step_1_nudging_diag_profile_differences_extra',\
            dpi = 300)
plt.show()





