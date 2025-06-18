#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:39:19 2020

@author: nn819853
"""

import iris 
import iris.quickplot as qplt
import iris.coord_categorisation
import matplotlib.pyplot as plt
import numpy as np
import datetime

def main():
    """
    """
    
    # set directory and filename of diagnostics - should be for one year
    filepath = '/storage/silver/scenario/nn819853/diags/clear_and_clean_net/free_control_ap5.pp'
    
    # read diagnostics into cubes
    diag_names = ['toa_incoming_shortwave_flux', \
                  'toa_outgoing_longwave_flux_assuming_clear_sky', \
                  'toa_outgoing_shortwave_flux_assuming_clear_sky']
    sw_down, lw_up, sw_up = iris.load(filepath, diag_names)
    
    # make a normal list of cubes - don't think is same as cubelist
    cubes = [sw_down, lw_up, sw_up]
    
    # initialise list for annual averaged toa cubes
    toa_time_meaned_cubes = []
    
    # set variables for extracting only whole years
    tdelta_1yr = datetime.timedelta(hours = 24*360)
    spans_1yr = lambda t: (t.bound[1] - t.bound[0]) == tdelta_1yr
    spans_1yr_constraint = iris.Constraint(time = spans_1yr)
    
    # determine multi-annual averages for each cube and select top model level
    for i in np.arange(len(cubes)):
        iris.coord_categorisation.add_year(cubes[i], 'time', name='year')
        annual_mean = cubes[i].aggregated_by('year',iris.analysis.MEAN)
        
        full_year_annual_mean = annual_mean.extract(spans_1yr_constraint)
        
        toa_time_meaned_cubes.append(full_year_annual_mean)
        
    # unpack toa time meaned cubes
    sw_down_toa, lw_up_toa, sw_up_toa = toa_time_meaned_cubes
    
    # determine net flux cubes
    net_sw_down = sw_down_toa - sw_up_toa
    net_lw_down = lw_up_toa*(-1)
    net_down = net_sw_down + net_lw_down
    # maybe should assign names to the new cubes?
    
    # determine area weightings for spatial averaging
    net_down.coord('latitude').guess_bounds()
    net_down.coord('longitude').guess_bounds()
    grid_area = iris.analysis.cartography.area_weights(net_down)
    
    # Determine area weighted means for Net down, Net SW down, and OLR
    area_mean = net_down.collapsed(['latitude','longitude'], \
                                                iris.analysis.MEAN, \
                                                weights = grid_area) 
    net_sw_down_area_mean = net_sw_down.collapsed(['latitude','longitude'], \
                                                iris.analysis.MEAN, \
                                                weights = grid_area)
    net_lw_down_area_mean = net_lw_down.collapsed(['latitude','longitude'], \
                                                iris.analysis.MEAN, \
                                                weights = grid_area)
    
    # determine number of years
    no_years = int((net_down.coord('time').bounds[-1,1] - \
    net_down.coord('time').bounds[0,0])/8640)
    
    # initialise list for holding net down spatial mean fluxes
    area_mean_float = np.zeros(no_years)
    net_sw_down_area_mean_float = np.zeros(no_years)
    net_lw_down_area_mean_float = np.zeros(no_years)
    
    # retrieve area mean fluxes from the scalar cubes
    for year in np.arange(no_years):
        area_mean_float[year] = np.round(area_mean[year].data, 2)
        net_sw_down_area_mean_float[year] = np.round(net_sw_down_area_mean[year].data, 2)
        net_lw_down_area_mean_float[year] = np.round(net_lw_down_area_mean[year].data, 2)

    # create an array of the years
    years = np.linspace(1,no_years,num = no_years)
    
    # set plot directory
    plot_directory = '/storage/silver/scenario/nn819853/plots/'
    
    # plot the mean net flux against year
    plt.figure()
    plt.plot(years, area_mean_float)
    plt.title('Free control net TOA radiative flux')
    plt.xlabel('Model year')
    plt.ylabel(u'radiative flux / Wm$^{-2}$')
    plt.savefig(plot_directory + 'Free_control_net_toa_clear_flux_time_series', \
                dpi=220)
    plt.show()
    
    fig, axarr = plt.subplots(3, sharex = True)
    axarr[0].set_title(u'TOA clear sky downwards fluxes / Wm$^{-2}$')
    axarr[0].plot(years, area_mean_float)
    axarr[1].plot(years, net_sw_down_area_mean_float)
    axarr[2].plot(years, net_lw_down_area_mean_float)
    axarr[0].set_ylabel('Net')
    axarr[1].set_ylabel('Net SW')
    axarr[2].set_ylabel('Net LW')
#    axarr[0].set_ylim(0.9,1.3)
#    axarr[1].set_ylim(240.5,240.9)
#    axarr[2].set_ylim(-239.9,-239.5)
    plt.savefig(plot_directory + 'PD_control_net_toa_clear_fluxes_time_series', \
                dpi = 220)
    plt.show()
    
    
    # PLot maps of net TOA flux for each year
#    for year in np.arange(no_years):
#        plt.figure()
#        qplt.pcolormesh(net_down[year])
#        plt.title('Net downwards radiative flux at TOA | Mean = ' + \
#                  str(area_mean_float[year]) + u' Wm$^{-2}$ | Year ' + \
#                  str(year + 1))
#        plt.savefig(plot_directory + 'net_flux_clear_sky_toa' + str(year+1) + '.png', \
#                    dpi = 220)
#        plt.show()
     
     # plot map of difference between last year and first year net TOA fluxes
#    diff = net_down[-1]-net_down[0]
#    plt.figure()
#    qplt.pcolormesh(diff)
#    plt.title('Net downwards clear sky radiative flux year 11 - year 1')
#    plt.savefig(plot_directory + 'net_flux_clear_sky_toa_11-1.png', dpi = 220)
#    plt.show()
  
if __name__ == '__main__':
    main()

            