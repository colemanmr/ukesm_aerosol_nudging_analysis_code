# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import Documents.python_code.diagnostics.radiative_fluxes.fluxes_module as flux_mod
import Documents.python_code.diagnostics.file_locations_module as file_loc

file_dir = file_loc.diag_dir + 'net_flux/'
file1 = file_dir + 'bv046_net_flux_su_nudging_free_calc_fluxes_all_sky_1yr_spinup.nc'
file2 = file_dir + 'bv046_test_all.nc'

cube1 = iris.load(file1)
cube2 = iris.load(file2)

annual_area_mean_net_1 = cube1[1]
annual_area_mean_net_2 = cube2[1]
annual_area_mean_net_diff = annual_area_mean_net_1 - annual_area_mean_net_2
print('annual area mean net diff = ', annual_area_mean_net_diff.data)


time_mean_net_1 = cube1[3]
time_mean_net_2 = cube2[3]
time_mean_net_diff = time_mean_net_1 - time_mean_net_2
print('time mean net diff = ', time_mean_net_diff.data)

print('max time mean error = ', np.max(time_mean_net_diff.data))
print('min time mean error = ', np.min(time_mean_net_diff.data))

plt.figure()
qplt.pcolormesh(time_mean_net_1)
plt.plot()

plt.figure()
qplt.pcolormesh(time_mean_net_2)
plt.plot()

plt.figure()
qplt.pcolormesh(time_mean_net_diff)
plt.plot()

