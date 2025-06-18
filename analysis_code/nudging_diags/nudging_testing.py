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

########################################################
#filename = 't_nudging_diags_ap7.pp'
    
########################################################

#g_param = iris.load_cube(nudge_dir + filename_g_param)
#
#plt.figure()
#qplt.plot(g_param[1,:,72,96])
#plt.show()
#
#plt.figure()
#qplt.pcolormesh(g_param[1,30,:,:])
#plt.show()

#####################################################
        
input_filename = 'br793_uvt_out_ap7.pp'
output_filename = 'uvt_6hourly_mar2014_ap7.pp'

#first_month_cons = iris.Constraint(forecast_period = lambda cell: cell <= 721)
#level_lat_lon_cons = iris.Constraint(model_level_number = [20, 15, 10], \
#                                    latitude = 72, longitude = 96)
#
#input_t = iris.load(nudge_dir + input_filename,\
#                         'air_potential_temperature' & first_month_cons & level_lat_lon_cons)
#output_t = iris.load(nudge_dir + output_filename,\
#                          'air_potential_temperature' & level_lat_lon_cons)

input_t = iris.load_cube(nudge_dir + input_filename, 'air_potential_temperature')
output_t = iris.load_cube(nudge_dir + output_filename, 'air_potential_temperature')

level_range = [15,30,50]

for level in level_range:
    test_input = input_t[240:359,level,130,180]
    test_output = output_t[0:119,level,130,180]
    diff = test_output - test_input
    print(diff.data)
    
    mean_diff = np.mean(np.absolute(diff.data))
    print('Mean difference at ', level, 'is: ', mean_diff)
