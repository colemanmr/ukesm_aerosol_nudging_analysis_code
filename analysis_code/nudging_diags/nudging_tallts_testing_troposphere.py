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

filename = 't_nudging_diags_ap7.pp'

nudge_analysis, after_nudge, nudge_inc, other_inc, prog_diag_1, prog_diag_2 \
= iris.load(nudge_dir + filename)

#############For shifting one model elvel up#########################

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

###########Plotting############

fig, ax1 = plt.subplots()
iplt.plot(nudge_inc[0,:,72,96], color = 'b', marker = 'x', linewidth = 0.5, label = 'nudge_inc')

ax1.set_ylim(-0.3, 5)

ax2 = ax1.twinx()
iplt.plot(other_inc[0,:,72,96], color = 'r', marker = 'x', linewidth = 1, label = 'other_inc')
iplt.plot(after_nudge[0,:,72,96], color = 'g', marker = 'x', linewidth = 0.5, label = 'after_nudge')
iplt.plot(nudge_analysis[0,:,72,96], color = 'm', marker = 'x', linewidth = 0.5, label = 'nudge_analysis')
ax2.set_ylim(320, 390)

ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = 'x', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[0,:,72,96], color = 'y', marker = 'x', linewidth = 0.5, label = 'raw_input')
iplt.plot(processed_input[0,:,72,96], color = 'c', marker = 'x', linewidth = 0.5, label = 'processed_input')

ax2.set_xlim(0, 20000)

ax1.legend(loc = 6, fontsize = 'medium')
ax2.legend(loc = 2, fontsize = 'medium')

plt.title('Test nudging diagnostics - theta')
ax1.set_ylabel('increments of theta / K')
ax2.set_ylabel('theta / K')
ax1.set_xlabel('height')

fig.tight_layout()

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/bw842_time_step_1_nudging_diag_profile_analysis_1_lev_up_troposphere',\
            dpi = 300)
plt.show()
    
