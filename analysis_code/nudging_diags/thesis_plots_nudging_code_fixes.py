#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:22:21 2024

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import numpy as np
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import iris.coord_categorisation

from okabe_ito_colours_mod import colours


# set diag directory
nudge_dir = '/storage/silver/scenario/nn819853/diags/nudging_diags/'


# load nudgign STASH diagnostics from nudged suite
filename = 't_nudging_diags_ap7.pp'

nudge_analysis, after_nudge, nudge_inc, other_inc, prog_diag_1, prog_diag_2 \
= iris.load(nudge_dir + filename)


# Read in raw theta input for first day from control sim
filename_input = 'br793_theta.pp'
raw_input = iris.load_cube(nudge_dir + filename_input, 'air_potential_temperature')


# Read in Mohit script processed u,v,theta input for time step 0, 18, 36, 54 and select theta
filename_processed = [nudge_dir + 'GLUM_201401010000.nc', \
                      nudge_dir + 'GLUM_201401010600.nc', \
                      nudge_dir + 'GLUM_201401011200.nc', \
                      nudge_dir + 'GLUM_201401011800.nc']
processed_input = iris.load(filename_processed, 'Potential temperature')

processed_input = processed_input.concatenate_cube()


# get model levels coords for one variable (same for all)
heights = nudge_inc.coord('level_height') / 1000


##########Plotting - pre index error fix plot ############

# The outputs from nudged suite are timestep, but inputs are 6 hourly
# 0 - 20 min; 1 - 40 min, 3 - 1 hr etc
timestep = 17

# 0 - 20min; 1 - 6hr; 2 - 12hr; 3 - 18hr
processed_raw_timestep = 1


fig, ax1 = plt.subplots()
iplt.plot(nudge_inc[timestep,:,72,96], heights, color = colours[0], marker = '', linewidth = 1, label = 'nudge increment')
iplt.plot(other_inc[timestep,:,72,96], heights, color = colours[1], marker = '', linewidth = 1, label = 'other increment')

ax2 = ax1.twiny()

# iplt.plot(after_nudge[timestep,:,72,96], heights, color = 'g', marker = '', linewidth = 1, label = 'after_nudge')
iplt.plot(nudge_analysis[timestep,:,72,96], heights, color = colours[2], marker = '', linewidth = 1, label = 'input-read')

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = '', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[processed_raw_timestep,:,72,96], heights, color = colours[3], marker = '', linewidth = 1, label = 'input-raw')
#iplt.plot(processed_input[processed_raw_timestep,:,72,96], heights, color = 'c', marker = '', linewidth = 0.5, label = 'processed_input')

ax1.set_xlim(-20,20)
ax2.set_xlim(-100,7000)

fig.legend(loc = [0.67,0.165], fontsize = 'medium')
# ax1.legend(loc = 2, fontsize = 'medium')
# ax2.legend(loc = 2, fontsize = 'medium')

# plt.title('Test nudging diagnostics - theta')
ax1.set_xlabel('Potential temperature increment / K')
ax2.set_xlabel('Potential temperature / K')
ax1.set_ylabel('height / km')

fig.tight_layout()

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/bw842_time_step_18_nudging_diag_profile',\
            dpi = 300)
plt.show()


### Fixed index error ########################################################

filename = 't_nudging_diags_ap7_redo.pp'

nudge_analysis_redo, after_nudge_redo, nudge_inc_redo, other_inc_redo, \
= iris.load(nudge_dir + filename)


# all the inputs are 6 hourly here
timestep_redo = 1



### plotting ################################################################


fig, ax1 = plt.subplots()
iplt.plot(nudge_inc_redo[timestep_redo,:,72,96], heights, color = colours[0], marker = '', linewidth = 1, label = 'nudge increment')
iplt.plot(other_inc_redo[timestep_redo,:,72,96], heights, color = colours[1], marker = '', linewidth = 1, label = 'other increment')

ax2 = ax1.twiny()

# iplt.plot(after_nudge[timestep_redo,:,72,96], heights, color = 'g', marker = '', linewidth = 1, label = 'after_nudge')
iplt.plot(nudge_analysis_redo[timestep_redo,:,72,96], heights, color = colours[2], marker = '', linewidth = 1, label = 'input-read')

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = '', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[timestep_redo,:,72,96], heights, color = colours[3], marker = '', linewidth = 1, label = 'input-raw')
#iplt.plot(processed_input[timestep_redo,:,72,96], heights, color = 'c', marker = '', linewidth = 0.5, label = 'processed_input')

ax1.set_xlim(-20,20)
ax2.set_xlim(-100,7000)

# fig.legend(loc = [0.67,0.165], fontsize = 'medium')
# ax2.legend(loc = 2, fontsize = 'medium')

# plt.title('Test nudging diagnostics - theta')
ax1.set_xlabel('Potential temperature increment / K')
ax2.set_xlabel('Potential temperature / K')
ax1.set_ylabel('height / km')

fig.tight_layout()

plot_directory = '/storage/silver/scenario/nn819853/plots/nudging_diags'
plt.savefig(plot_directory + '/bw842_time_step_18_nudging_diag_profile_index_error_fixed',\
            dpi = 300)
plt.show()



### Final inedx error thesis plot ############################################

import cartopy.crs as ccrs    
plt.tight_layout()
plt.rcParams.update({'font.size': 10})


fig = plt.figure()

ax1 = plt.subplot(121)
iplt.plot(nudge_inc[timestep,:,72,96], heights, color = colours[0], marker = '', linewidth = 1, label = 'nudge inc.')
iplt.plot(other_inc[timestep,:,72,96], heights, color = colours[1], marker = '', linewidth = 1, label = 'other inc.')

ax2 = ax1.twiny()

# iplt.plot(after_nudge[timestep,:,72,96], heights, color = 'g', marker = '', linewidth = 1, label = 'after_nudge')
iplt.plot(nudge_analysis[timestep,:,72,96], heights, color = colours[2], marker = '', linewidth = 1, label = 'input-read')

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = '', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[processed_raw_timestep,:,72,96], heights, color = colours[3], marker = '', linewidth = 1, label = 'input-raw')
#iplt.plot(processed_input[processed_raw_timestep,:,72,96], heights, color = 'c', marker = '', linewidth = 0.5, label = 'processed_input')

ax1.set_xlim(-21,21)
ax2.set_xlim(-200,7000)

ax3 = plt.subplot(122, sharey = ax1)
iplt.plot(nudge_inc_redo[timestep_redo,:,72,96], heights, color = colours[0], marker = '', linewidth = 1)
iplt.plot(other_inc_redo[timestep_redo,:,72,96], heights, color = colours[1], marker = '', linewidth = 1)

plt.tick_params('y', labelleft=False)

ax4 = ax3.twiny()

# iplt.plot(after_nudge[timestep_redo,:,72,96], heights, color = 'g', marker = '', linewidth = 1, label = 'after_nudge')
iplt.plot(nudge_analysis_redo[timestep_redo,:,72,96], heights, color = colours[2], marker = '', linewidth = 1)

#ax2.plot(alt_adjust, anal_adjust, color = 'black', marker = '', linewidth = 0.5, label = 'nudge_analysis_adjusted')
iplt.plot(raw_input[timestep_redo,:,72,96], heights, color = colours[3], marker = '', linewidth = 1)
#iplt.plot(processed_input[processed_raw_timestep,:,72,96], heights, color = 'c', marker = '', linewidth = 0.5, label = 'processed_input')

plt.tick_params('y', labelleft=False)

ax3.set_xlim(-21,21)
ax4.set_xlim(-200,7000)

fig.legend(loc = [0.79,0.12])

# fig.legend(loc = [0.67,0.165], fontsize = 'medium')
# ax1.legend(loc = 2, fontsize = 'medium')
# ax2.legend(loc = 2, fontsize = 'medium')

# plt.title('Test nudging diagnostics - theta')
ax1.set_xlabel('Potential temperature increment / K')
ax2.set_xlabel('Potential temperature / K')
ax3.set_xlabel('Potential temperature increment / K')
ax4.set_xlabel('Potential temperature / K')
ax1.set_ylabel('height / km')

plt.subplots_adjust(bottom=0,
                    left=0,
                    right=1, 
                    top=1, 
                    wspace=0.05, 
                    hspace=0.25)

ax1.text(-17,-1,'(a) Before fix')
ax3.text(-17,-1,'(b) After fix')

plt.savefig(plot_directory + '/bw842_time_step_18_nudging_diag_profile_index_error_before_after',\
            dpi = 300, bbox_inches='tight')
    
    
    
### Load copygrid fix data ############################################

copygrid_filename = 'bw842_ts_3hours_and_6hourly_nudge_diags_copygrid_ap7.pp'

nudge_analysis_copygrid, after_nudge_copygrid, nudge_inc_copygrid, other_inc_copygrid, prog_diag_copygrid \
= iris.load(nudge_dir + copygrid_filename)


# load only from 7th time index as the frst 7 times were timestep output
# then was 6 hourly for last three times :) 
# i.e. 0 is 2hr40min for these diags but is 0hr for the raw input and 1 - 6hr; 2 - 12hr; 3 - 18hr
nudge_analysis_copygrid = nudge_analysis_copygrid[7:]
after_nudge_copygrid = after_nudge_copygrid[7:]
nudge_inc_copygrid = nudge_inc_copygrid[7:]
other_inc_copygrid = other_inc_copygrid[7:]
prog_diag_copygrid = prog_diag_copygrid[7:]



### Difference analysis - raw input, for both fixes ##########################

nudge_analysis_redo.units = 'K'
nudge_analysis_copygrid.units = 'K'

input_diff_index_err_fix = nudge_analysis_redo[1,:,72,96] - raw_input[1,:,72,96]
input_diff_copygrid = nudge_analysis_copygrid[1,:,72,96] - raw_input[1,:,72,96]


plt.figure()
iplt.plot(input_diff_index_err_fix, heights, color = colours[0], 
          linestyle = '--', label = 'Grid interpolated')
iplt.plot(input_diff_copygrid, heights, color = colours[0],
          linestyle = '-', label = 'Grid copied')
plt.xlabel('Potential temperature difference / K')
plt.ylabel('Height / km')
# plt.xlim(-30, 30)
plt.legend()
plt.savefig(plot_directory + '/bw842_time_step_18_analysis_minus_raw_before_after_copygrid',
            dpi = 300)
plt.show()


