#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 11:01:09 2020

@author: nn819853
"""

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt

#!! add comments !!#
#!! make function with command line input !!#

filename = file_loc.diag_dir + 'net_flux/by965_net_flux_su_nudging_uvt.pp'

area_sw, area_lw, area_net, time_sw, time_lw, time_net, area_time_sw, area_time_lw, area_time_net = \
flux_mod.toa_flux(filename, sky_type = 'all')

plot_dir = file_loc.plot_dir + 'net_fluxes'

no_years = len(area_sw.data)
years_labels = np.linspace(1, no_years, num = no_years)

# plot the area mean net flux against year
plt.figure()
plt.plot(years_labels, area_net.data)
plt.title('')
plt.xlabel('Model year')
plt.ylabel(u'radiative flux / W m$^{-2}$')
#plt.savefig(plot_dir + 'cont_free_net_toa_flux_time_series', dpi=220)
plt.show()

# plot the area mean fluxes against year
fig, axarr = plt.subplots(3, sharex = True)
axarr[0].set_title(u'TOA downwards fluxes / W m$^{-2}$')
axarr[0].plot(years_labels, area_net.data)
axarr[1].plot(years_labels, area_sw.data)
axarr[2].plot(years_labels, area_lw.data)
axarr[0].set_ylabel('Net')
axarr[1].set_ylabel('Net SW')
axarr[2].set_ylabel('Net LW')
#    axarr[0].set_ylim(0.8,1.3)
#    axarr[1].set_ylim(240.5,241.0)
#    axarr[2].set_ylim(-240.0,-239.5)
#plt.savefig(plot_dir + 'cont_free_net_toa_fluxes_time_series', dpi = 220)
plt.show()

plt.figure()
mesh = iplt.pcolormesh(time_net[0])
plt.colorbar(mesh, shrink = 0.65, label = u' W m$^{-2}$')
plt.title('Net downwards radiative flux')
#plt.savefig(plot_dir + 'net_flux_toa_map.png', dpi = 220)
plt.show()