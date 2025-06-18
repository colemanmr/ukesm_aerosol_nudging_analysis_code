#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:25:23 2020

@author: nn819853
"""

import numpy as np
import matplotlib.pyplot as plt
import diagnostics.file_locations_module as file_loc

plot_dir = file_loc.plot_dir + 'net_fluxes/'

# Data from su forcing: free = br793 - bv046; uvt_nudged = by937 - by965

########## net    sw     lw

nudged = [
        -1.82, -2.10, 0.28   # all sky
          , -0.82, -1.02, 0.2   # clear sky
#           -1.20, -1.44, 0.25   # clean sky
#          , 0.10, -0.05, 0.14   # clearclean sky
          ]

nudged_error = [
        0.02, 0.03, 0.01   # all sky
        ,0.02, 0.02, 0.01   # clear sky
#        0.02, 0.02, 0.01   # clean sky
#        ,0.01, 0.00, 0.01   # clearclean sky
        ]

free = [
        -1.45, -1.81, 0.37   # all sky
        ,-0.88, -1.03, 0.15   # clear sky
#        -0.82, -1.15, 0.33   # clean sky
#        ,0.03 , -0.07, 0.1   # clearclean sky
        ]

free_error = [
        0.06, 0.06, 0.05   # all sky
        ,0.05, 0.04, 0.04   # clear sky
#        0.06, 0.05, 0.05   # clean sky
#        ,0.04, 0.03, 0.04   # clearclean sky
        ]

nudged_G12 =[
        -1.72,-2.03,0.31
        ,-0.81,-1.01,0.20
#        -1.1,-1.37,0.27
#        ,0.1,-0.04,0.14
        ]

nudged_G12_error =[
        0.04,0.05,0.02
        ,0.03,0.04,0.02
#        0.02,0.03,0.01
#        ,0.01,0.00,0.01
        ]

nudged_G3 =[
        -1.70,-1.93,0.24
        ,-0.84,-1.01,0.17
#        -1.07,-1.27,0.20
#        ,0.08,-0.04,0.12
        ]

nudged_G3_error =[
        0.03,0.03,0.01
        ,0.02,0.03,0.01
#        0.02,0.02,0.01
#        ,0.0,0.0,0.01
        ]

labels = ['Net', 'SW', 'LW'
          ,'Net', 'SW', 'LW'
#          ,'Net', 'SW', 'LW'
#          ,'Net', 'SW', 'LW'
          ]

font = {'size' : 12}
plt.rc('font', **font)

label_points = np.arange(len(labels))
width = 0.2

fix, ax = plt.subplots()
ax.bar(label_points - 3*width/2, free, width, yerr = free_error, color = 'darkred', label = 'free, n = 30')
ax.bar(label_points - width/2, nudged_G12, width, yerr = nudged_G12_error, color = 'blue', label = 'nudged, G=1/12, n = 5')
ax.bar(label_points + width/2, nudged, width, yerr = nudged_error, color = 'tomato', label = 'nudged G=1/6, n = 10')
ax.bar(label_points + 3*width/2, nudged_G3, width, yerr = nudged_G3_error, color = 'green', label = 'nudged, G=1/3, n = 5')
ax.set_xticks(label_points)
ax.set_xticklabels(labels)
ax.set_ylim(-2.5, 0.8)
plt.legend(loc=[0.52,0.05])
ax.text(0.5,0.5,'All sky')
ax.text(3.3,0.5,'Clear Sky')
ax.axvline(x = 2.5, ymin= 0, ymax = 1, color = 'darkgrey', linestyle = '-')
ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')
ax.set_ylabel(u'ERF / W m$^{-2}$')
plt.tight_layout()
plt.savefig(plot_dir + 'su_forcing_comparison_free_uvt_nudged_bar_chart_Gvarying_all_clear.png', dpi = 400)
plt.show()