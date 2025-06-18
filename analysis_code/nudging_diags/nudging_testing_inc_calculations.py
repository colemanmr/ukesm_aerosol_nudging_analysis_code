#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 13:46:39 2020

@author: nn819853
"""

import iris 
import numpy as np
import iris.plot as iplt
import matplotlib.pyplot as plt

###################################

# read in timestep tallts nudging diags
nudge_dir = '/storage/silver/scenario/nn819853/diags/nudging_diags/'

filename = 'bw842_ts_nudge_diags_ap7.pp'

nudge_anal, after_nudge, nudge_inc, other_inc, prog_diag\
= iris.load(nudge_dir + filename)

prog_diag.units = 'unknown'

# set timestep for all diags for plotting
timestep = 2

# set varaibles to hold specific ts for each nudging diag
ts_nudge_anal = nudge_anal[timestep,13:81,72,96]
ts_previous_nudge_anal = nudge_anal[timestep-1,13:81,72,96]
ts_after_nudge = after_nudge[timestep,13:81,72,96]
ts_previous_after_nudge = after_nudge[timestep-1,13:81,72,96]
ts_nudge_inc = nudge_inc[timestep,13:81,72,96]
ts_other_inc = other_inc[timestep,13:81,72,96]
ts_prog_diag = prog_diag[timestep,13:81,72,96]
ts_previous_prog_diag = prog_diag[timestep-1,13:81,72,96]

# calculate nudge inc based on anal - after_nudge current timestep
diff1 = (1/18) * (ts_nudge_anal - ts_after_nudge)

# calculate nudge inc based on anal - after_nudge previous timestep
diff2 = (1/18) * (ts_nudge_anal - ts_previous_after_nudge)

# calculate nudge inc based on anal - section zero diag current timestep
diff3 = (1/18) * (ts_nudge_anal - ts_prog_diag)

# calculate nudge inc based on anal - section zero diag previous timestep
diff4 = (1/18) * (ts_nudge_anal - ts_previous_prog_diag)

# calculate nudge inc based on anal - section zero diag previous timestep
diff5 = (1/18) * (ts_previous_nudge_anal - ts_prog_diag)

# calculate nudge inc based on anal - section zero diag previous timestep
diff6 = (1/18) * (ts_previous_nudge_anal - ts_after_nudge)

plt.figure()
iplt.plot(ts_nudge_inc, color = 'b', marker = 'x', linewidth = 0.5, label = 'nudge_inc')
#iplt.plot(diff1, color = 'm', marker = 'x', linewidth = 0.5, label = 'diff_current_after_nudge')
#iplt.plot(diff2, color = 'c', marker = 'x', linewidth = 0.5, label = 'diff_previous_after_nudge')
#iplt.plot(diff3, color = 'k', marker = 'x', linewidth = 0.5, label = 'diff_current_prog_diag')
#iplt.plot(diff4, color = 'y', marker = 'x', linewidth = 0.5, label = 'diff_previous_prog_diag')
#iplt.plot(diff5, color = 'g', marker = 'x', linewidth = 0.5, label = 'diff_previous_anal_current_prog_diag')
iplt.plot(diff6, color = 'r', marker = 'x', linewidth = 0.5, label = 'diff_previous_anal_current_after_nudge')
plt.show()

#print(ts_nudge_inc.data)
#print(np.round(diff1.data, 3))
#print(np.round(diff3.data, 4))