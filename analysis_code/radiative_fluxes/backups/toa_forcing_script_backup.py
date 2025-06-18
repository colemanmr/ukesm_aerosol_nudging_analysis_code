#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:52:31 2020

@author: nn819853
"""

import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import diagnostics.file_locations_module as file_loc
import numpy as np
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt


def main(cont_filename, pert_filename, sky_type):
    """
    Script for calculating and visualising forcing between control and 
    perturbed simulation pair. Needs tweaking of savefig names for determining
    flux diffs.
    """
    
    #!! Better have same number of years - edit code to handle diff years better!##
    control_filepath = file_loc.diag_dir + 'net_flux/' + cont_filename 
    perturbed_filepath = file_loc.diag_dir + 'net_flux/' + pert_filename 
    
    # Read species name from input .pp file
    species = pert_filename[15:17]
    
    # Reading nudging type from input file (using perturbed arbitrarily)
    index1 = pert_filename.find('nudging')
    index2 = pert_filename.find('.pp')
    nudging_type = pert_filename[index1 + 8: index2]
    
    # Extract suite IDs from input files
    cont_suite = cont_filename[0:5]
    pert_suite = pert_filename[0:5]
    
    control_area_sw, control_area_lw, control_area_net, \
    control_time_sw, control_time_lw, control_time_net, \
    control_area_time_sw, control_area_time_lw, control_area_time_net = \
    flux_mod.toa_flux(control_filepath, sky_type = sky_type,\
                      spinup_years = 0)
    
    perturbed_area_sw, perturbed_area_lw, perturbed_area_net, \
    perturbed_time_sw, perturbed_time_lw, perturbed_time_net, \
    perturbed_area_time_sw, perturbed_area_time_lw, perturbed_area_time_net = \
    flux_mod.toa_flux(perturbed_filepath, sky_type = sky_type,\
                      spinup_years = 0)
    
    plot_dir = file_loc.plot_dir + 'net_fluxes/'
    
    # Calculate annual area meaned forcings for forcing time series plots
    area_mean_net_forcing = flux_mod.cube_diff(control_area_net,\
                                               perturbed_area_net)
    area_mean_sw_forcing = flux_mod.cube_diff(control_area_sw,\
                                               perturbed_area_sw)
    area_mean_lw_forcing = flux_mod.cube_diff(control_area_lw,\
                                               perturbed_area_lw)
    
    # Calculate time meaned forcing for forcing maps
    time_mean_net_forcing = flux_mod.cube_diff(control_time_net[0],\
                                               perturbed_time_net[0])
    time_mean_sw_forcing = flux_mod.cube_diff(control_time_sw[0],\
                                               perturbed_time_sw[0])
    time_mean_lw_forcing = flux_mod.cube_diff(control_time_lw[0],\
                                               perturbed_time_lw[0])
    
    area_time_net_forcing = flux_mod.time_mean_cube(area_mean_net_forcing)
    area_time_sw_forcing = flux_mod.time_mean_cube(area_mean_sw_forcing)
    area_time_lw_forcing = flux_mod.time_mean_cube(area_mean_lw_forcing)
    
    
    net_forcing_string = [str(np.round(area_time_net_forcing[0].data, 2)),\
                          str(np.round(area_time_net_forcing[2].data, 2))]
    print('Overall forcing is ' + net_forcing_string[0] \
          + ' \u00B1 ' + net_forcing_string[1])
    sw_forcing_string = [str(np.round(area_time_sw_forcing[0].data, 2)),\
                          str(np.round(area_time_sw_forcing[2].data, 2))]
    print('Overall sw forcing is ' + sw_forcing_string[0] \
          + ' \u00B1 ' + sw_forcing_string[1])
    lw_forcing_string = [str(np.round(area_time_lw_forcing[0].data, 2)),\
                          str(np.round(area_time_lw_forcing[2].data, 2))]
    print('Overall lw forcing is ' + lw_forcing_string[0] \
          + ' \u00B1 ' + lw_forcing_string[1])
    
    # Calculate overall area and time mean forcing
    #area_time_net_forcing = flux_mod.cube_diff(control_area_time_net[0],\
    #                                           perturbed_area_time_net[0],\
    #                                           control_area_time_net[2],\
    #                                           perturbed_area_time_net[2])
    #area_time_sw_forcing = flux_mod.cube_diff(control_area_time_sw[0],\
    #                                           perturbed_area_time_sw[0],\
    #                                           control_area_time_sw[2],\
    #                                           perturbed_area_time_sw[2])
    #area_time_lw_forcing = flux_mod.cube_diff(control_area_time_lw[0],\
    #                                           perturbed_area_time_lw[0],\
    #                                           control_area_time_lw[2],\
    #                                           perturbed_area_time_lw[2])

    # Determine model years from time dimension, which is hours since 1970
    time_points = area_mean_net_forcing.coord('time').points
    model_years = time_points/(360*24) + 1970
    
#    # Determine number of years in simulation (not just averaged for overall)
#    length_1 = len(control_area_net.data)
#    length_2 = len(perturbed_area_net.data)
#    no_years = min((length_1, length_2))
#    
#    # Make array of year number
#    years = np.linspace(1, no_years, no_years)
    
    #!! need to set plot titles and labels based on command line input !!#
    plt.figure()
    #plt.title(u'uvt nudged control - perturbed SU forcing G=1/6 hr$^{-1}$', \
    #     fontsize = 'medium')
    plt.plot(model_years, area_mean_net_forcing.data, color = 'black', linestyle = '-', label = 'net_all')  
    plt.plot(model_years, area_mean_sw_forcing.data, color = 'mediumblue', linestyle = '-', label = 'sw_all')
    plt.plot(model_years, area_mean_lw_forcing.data, color = 'r', linestyle = '-', label = 'lw_all')
    plt.ylabel(u'Radiative forcing / W m$^{-2}$', fontsize = 'medium')
    plt.xlabel('Model Year', fontsize = 'medium')
    #plt.ylim(-2.8,0.7)
    plt.legend(ncol = 3, fontsize = 'small')
    plt.tight_layout()
    plt.savefig(plot_dir + cont_suite + '-' + pert_suite + '_' + species + '_'\
                + nudging_type + '_toa_forcing_' + sky_type + '_annual_means_time_series', \
                dpi = 400)
    plt.show()       


    # plot map of multiannual mean forcing
    plt.figure()
    mesh = iplt.pcolormesh(time_mean_net_forcing, cmap = 'bwr', vmin = -27, vmax = 27)
    plt.colorbar(mesh, shrink = 0.9, label = u' W m$^{-2}$', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    #plt.title('Free control - perturbed SU mean TOA net forcing', fontsize = 'medium')
    plt.tight_layout()
    plt.savefig(plot_dir + cont_suite + '-' + pert_suite + '_' + species + '_'\
                + nudging_type + '_net_toa_forcing_' + sky_type + '_map.png', \
                dpi = 400)
    plt.show()
    
    # plot map of multiannual mean forcing
    plt.figure()
    mesh = iplt.pcolormesh(time_mean_sw_forcing, cmap = 'bwr', vmin = -27, vmax = 27)
    plt.colorbar(mesh, shrink = 0.9, label = u' W m$^{-2}$', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    #plt.title('Free control - perturbed SU mean TOA sw forcing', fontsize = 'medium')
    plt.tight_layout()
    plt.savefig(plot_dir + cont_suite + '-' + pert_suite + '_' + species + '_'\
                + nudging_type + '_sw_toa_forcing_' + sky_type + '_map.png', \
                dpi = 400)    
    plt.show()
    
    # plot map of multiannual mean forcing
    plt.figure()
    mesh = iplt.pcolormesh(time_mean_lw_forcing, cmap = 'bwr', vmin = -27, vmax = 27)
    plt.colorbar(mesh, shrink = 0.9, label = u' W m$^{-2}$', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    #plt.title('Free control - perturbed SU mean TOA lw forcing', fontsize = 'medium')
    plt.tight_layout()
    plt.savefig(plot_dir + cont_suite + '-' + pert_suite + '_' + species + '_'\
                + nudging_type + '_lw_toa_forcing_' + sky_type + '_map.png', \
                dpi = 400)    
    plt.show()

if __name__ == '__main__':
    main('br793_net_flux_control_nudging_free.pp',\
         'bv046_net_flux_su_nudging_free.pp',\
         'clearclean')
