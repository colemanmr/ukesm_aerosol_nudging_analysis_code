#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:59:25 2023

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import copy
import character_shortcuts as char


diag_dir = file_loc.diag_dir + 'cloud_diags/'
basename = 'cloud_re_and_weighting_'
file_ext = '.pp'

cont = 'cb108'
pert = 'ce303'

cont_cubes = iris.load(diag_dir + basename + cont + file_ext)
pert_cubes = iris.load(diag_dir + basename + pert + file_ext)


# cont_weighted_re = cont_cubes[1]/cont_cubes[0]
# pert_weighted_re = pert_cubes[1]/pert_cubes[0]

# time_mean_cont_re,_,_ = flux_mod.time_mean_cube(cont_weighted_re)
# time_mean_pert_re,_,_ = flux_mod.time_mean_cube(pert_weighted_re)


time_mean_cont_re_weighted,_,_ = flux_mod.time_mean_cube(cont_cubes[1])
time_mean_cont_weight,_,_ = flux_mod.time_mean_cube(cont_cubes[0])

time_mean_pert_re_weighted,_,_ = flux_mod.time_mean_cube(pert_cubes[1])
time_mean_pert_weight,_,_ = flux_mod.time_mean_cube(pert_cubes[0])

time_mean_cont_re = time_mean_cont_re_weighted / time_mean_cont_weight
time_mean_pert_re = time_mean_pert_re_weighted / time_mean_pert_weight


re_diff = time_mean_cont_re - time_mean_pert_re

# re_diff_plot = re_diff[5:15].collapsed('model_level_number', iris.analysis.MEAN)
re_diff_plot = re_diff[14]


plt.figure()
qplt.pcolormesh(re_diff_plot, cmap = 'seismic', vmin = -0.5e-6, vmax = 0.5e-6)
figure = plt.gca()
figure.coastlines(linewidth = 1)
plt.show()



