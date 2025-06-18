#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 10:08:30 2021

@author: nn819853
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import iris.analysis
import character_shortcuts as char

diag_dir = file_loc.diag_dir + 'nudging_testing_new/'
plot_dir = file_loc.plot_dir + ''

analysis_file = diag_dir + 'nudge_anal_uv_mon_pt_by937.pp'

after_nudge_files = [diag_dir + 'after_nudge_uv_mon_pt_by937.pp',
                     diag_dir + 'after_nudge_uv_mon_pt_by965.pp',
                     diag_dir + 'after_nudge_uv_mon_pt_bz234.pp',
                     diag_dir + 'after_nudge_uv_mon_pt_bz235.pp',
                     diag_dir + 'after_nudge_uv_mon_pt_bz236.pp',
                     diag_dir + 'after_nudge_uv_mon_pt_bz237.pp',
                     ]

labels = ['G=1/6 cont',
          'G=1/6 su',
          'G=1/12 su',
          'G=1/3 su',
          'G=1/12 cont',
          'G=1/3 cont',
          ]

anal = iris.load_cube(analysis_file, 'm01s39i006')
after_nudge = iris.load(after_nudge_files, 'm01s39i007')

#months = len(after_nudge[])

for i in range(1):
    plt.figure()
    iplt.plot(anal[i,:,68,105], label = 'analysis',\
#              coords = ['m01s39i006', 'level_height']
          )
    for j in range(len(labels)):
        iplt.plot(after_nudge[j][i,:,68,105], label = labels[j],\
    #              coords = ['m01s39i006', 'level_height']
                  )
        plt.ylabel('Zonal wind / m s-1')
        plt.xlabel('Level Height / m')
        plt.legend()
        
    
