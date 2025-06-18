#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:37:27 2023

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import character_shortcuts as char


diag_dir = '/storage/silver/scenario/nn819853/diags/cloud_diags/'
plot_dir = '/storage/silver/scenario/nn819853/plots/clouds/'

cont_file = diag_dir + 'cloud_frac_br793_apm.pp'
pert_file = diag_dir + 'cloud_frac_ce067_apm.pp'

cont_cube = iris.load_cube(cont_file)
pert_cube = iris.load_cube(pert_file)


# remove first year (2014)
cont_cube = cont_cube[14:]
pert_cube = pert_cube[12:]

multi_ann_mean_cont = cont_cube.collapsed('time', iris.analysis.MEAN)
multi_ann_mean_pert = pert_cube.collapsed('time', iris.analysis.MEAN)


diff = (multi_ann_mean_cont - multi_ann_mean_pert)*100/multi_ann_mean_cont


low_cloud_diff = diff[2:15].collapsed('model_level_number', iris.analysis.MEAN)
mid_cloud_diff = diff[15:27].collapsed('model_level_number', iris.analysis.MEAN)
high_cloud_diff = diff[27:45].collapsed('model_level_number', iris.analysis.MEAN)


cubes_list = [low_cloud_diff, mid_cloud_diff, high_cloud_diff]

for i in range(3):

    plt.figure()
    mesh = qplt.pcolormesh(cubes_list[i], vmin = -20, vmax=20)
    # plt.colorbar(vmin)
    plt.show()



# low_cloud_cont = multi_ann_mean_cont[2:15].collapsed('model_level_number', iris.analysis.MEAN)
# mid_cloud_cont = multi_ann_mean_cont[15:27].collapsed('model_level_number', iris.analysis.MEAN)
# high_cloud_cont = multi_ann_mean_cont[27:45].collapsed('model_level_number', iris.analysis.MEAN)

# cubes_list = [low_cloud_cont, mid_cloud_cont, high_cloud_cont]

# for i in range(3):

#     plt.figure()
#     qplt.pcolormesh(cubes_list[i])
#     plt.show()



