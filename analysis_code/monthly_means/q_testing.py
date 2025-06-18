#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 09:36:47 2020

@author: nn819853
"""

import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot

filename = '/storage/silver/scenario/nn819853/diags/mon_mn_diags/cont_free_apm_q_theta.pp'

cube = iris.load_cube(filename, 'specific_humidity')
print(cube)

time_zonal_mean = cube.collapsed(['time', 'longitude'], iris.analysis.MEAN)

plt.figure()
qplt.pcolormesh(time_zonal_mean)
plt.show()