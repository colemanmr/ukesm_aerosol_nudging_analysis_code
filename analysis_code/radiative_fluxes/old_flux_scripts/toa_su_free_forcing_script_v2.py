#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:39:19 2020

@author: nn819853
"""

import iris 
import iris.plot as iplt
import iris.quickplot as qplt
import iris.coord_categorisation
import matplotlib.pyplot as plt
import numpy as np
import datetime

def main():
    
    def control():
        """
        """
        
        # set directory and filename of diagnostics - should be for one year
        filepath = '/storage/silver/scenario/nn819853/diags/net_flux/cont_free_ap5.pp'
        
        # read diagnostics into cubes
        diag_names = ['toa_incoming_shortwave_flux', \
                      'toa_outgoing_longwave_flux', \
                      'toa_outgoing_shortwave_flux']
        sw_down, lw_up, sw_up = iris.load(filepath, diag_names)
        
        # make a normal list of cubes - don't think is same as cubelist
        cubes = [sw_down, lw_up, sw_up]
        
        # initialise list for annual averaged toa cubes
        toa_time_meaned_cubes = []
        
        # set variables for extracting only whole years
        tdelta_1yr = datetime.timedelta(hours = 24*360)
        spans_1yr = lambda t: (t.bound[1] - t.bound[0]) == tdelta_1yr
        spans_1yr_constraint = iris.Constraint(time = spans_1yr)
        
        # determine multi-annual averages for each cube and filter incomplete years
        for i in np.arange(len(cubes)):
            iris.coord_categorisation.add_year(cubes[i], 'time', name='year')
            annual_mean = cubes[i].aggregated_by('year',iris.analysis.MEAN)
            
            full_year_annual_mean = annual_mean.extract(spans_1yr_constraint)
    
            toa_time_meaned_cubes.append(full_year_annual_mean)
            
        # unpack toa time meaned cubes
        sw_down_toa, lw_up_toa, sw_up_toa = toa_time_meaned_cubes
        
        # determine number of years
        no_years = int((sw_down_toa.coord('time').bounds[-1,1] - \
        sw_down_toa.coord('time').bounds[0,0])/8640)
        
        # create cubes of zeros for lw subtraction to avoid units changing
        zeros = lw_up_toa.copy(data=None)
        
        for h in np.arange(0,no_years,1):
            for i in np.arange(0,144,1):
                    for j in np.arange(0,192,1):
                        zeros.data[h,i,j] = 0.0
        
        # determine net flux cubes
        net_sw_down = sw_down_toa - sw_up_toa
        net_lw_down = zeros - lw_up_toa
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
        
        # initialise list for holding net down spatial mean fluxes
        area_mean_float = np.zeros(no_years)
        net_sw_down_area_mean_float = np.zeros(no_years)
        net_lw_down_area_mean_float = np.zeros(no_years)
        
        # retrieve area mean fluxes from the scalar cubes
        for year in np.arange(no_years):
            area_mean_float[year] = np.round(area_mean[year].data, 2)
            net_sw_down_area_mean_float[year] = np.round(net_sw_down_area_mean[year].data, 2)
            net_lw_down_area_mean_float[year] = np.round(net_lw_down_area_mean[year].data, 2)
        
        return net_sw_down, net_lw_down, net_down, net_sw_down_area_mean_float, net_lw_down_area_mean_float, area_mean_float
        
            
    def su_free():
        """
        """
        
        # set directory and filename of diagnostics - should be for one year
        filepath = '/storage/silver/scenario/nn819853/diags/net_flux/su_free_ap5.pp'
        
        # read diagnostics into cubes
        diag_names = ['toa_incoming_shortwave_flux', \
                      'toa_outgoing_longwave_flux', \
                      'toa_outgoing_shortwave_flux']
        sw_down, lw_up, sw_up = iris.load(filepath, diag_names)

        # make a normal list of cubes - don't think is same as cubelist
        cubes = [sw_down, lw_up, sw_up]
        
        # initialise list for annual averaged toa cubes
        toa_time_meaned_cubes = []
        
        # set variables for extracting only whole years
        tdelta_1yr = datetime.timedelta(hours = 24*360)
        spans_1yr = lambda t: (t.bound[1] - t.bound[0]) == tdelta_1yr
        spans_1yr_constraint = iris.Constraint(time = spans_1yr)
        
        # determine multi-annual averages for each cube and filter incomplete years
        for i in np.arange(len(cubes)):
            iris.coord_categorisation.add_year(cubes[i], 'time', name='year')
            annual_mean = cubes[i].aggregated_by('year',iris.analysis.MEAN)
            
            full_year_annual_mean = annual_mean.extract(spans_1yr_constraint)
    
            toa_time_meaned_cubes.append(full_year_annual_mean)
            
        # unpack toa time meaned cubes
        sw_down_toa, lw_up_toa, sw_up_toa = toa_time_meaned_cubes
        
        # determine number of years
        no_years = int((sw_down_toa.coord('time').bounds[-1,1] - \
        sw_down_toa.coord('time').bounds[0,0])/8640)
        
        # create cubes of zeros for lw subtraction to avoid units changing
        zeros = lw_up_toa.copy(data=None)
        
        for h in np.arange(0,no_years,1):
            for i in np.arange(0,144,1):
                    for j in np.arange(0,192,1):
                        zeros.data[h,i,j] = 0.0
        
        # determine net flux cubes
        net_sw_down = sw_down_toa - sw_up_toa
        net_lw_down = zeros - lw_up_toa
        net_down = net_sw_down + net_lw_down
        # maybe should assign names to the new cubes?
        # also for some reason the *-1 turns lw units in kg.s^-3 which is equivalent to W.m^-2
        
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
        
        # initialise list for holding net down spatial mean fluxes
        area_mean_float = np.zeros(no_years)
        net_sw_down_area_mean_float = np.zeros(no_years)
        net_lw_down_area_mean_float = np.zeros(no_years)
        
        # retrieve area mean fluxes from the scalar cubes
        for year in np.arange(no_years):
            area_mean_float[year] = np.round(area_mean[year].data, 2)
            net_sw_down_area_mean_float[year] = np.round(net_sw_down_area_mean[year].data, 2)
            net_lw_down_area_mean_float[year] = np.round(net_lw_down_area_mean[year].data, 2)
        
        return net_sw_down, net_lw_down, net_down, net_sw_down_area_mean_float, net_lw_down_area_mean_float, area_mean_float  
    

    # unpack su and control sw, lw, and net flux annual averaged cubes
    cont_sw, cont_lw, cont_net, cont_sw_mean, cont_lw_mean, cont_net_mean = control()
    su_sw, su_lw, su_net, su_sw_mean, su_lw_mean, su_net_mean = su_free() 
    
    # determine number of years in su simulation as shorter so far
    no_years = int((su_net.coord('time').bounds[-1,1] - \
    su_net.coord('time').bounds[0,0])/8640)
    
    # cut control simulation to same number of years as su perturbation
    cont_sw_cut = cont_sw[0:no_years]
    cont_lw_cut = cont_lw[0:no_years]
    cont_net_cut = cont_net[0:no_years]
    
    # calculate annual forcing cubes
    sw_forcing = cont_sw_cut - su_sw
    lw_forcing = cont_lw_cut - su_lw
    net_forcing = cont_net_cut - su_net
    
    # control simulation area means to same number of years as su perturbation
    cont_sw_mean_cut = cont_sw_mean[0:no_years]
    cont_lw_mean_cut = cont_lw_mean[0:no_years]
    cont_net_mean_cut = cont_net_mean[0:no_years]
    
    # Determine the area weighted mean forcings from area weighted mean fluxes
    area_mean_net_forcing = cont_net_mean_cut - su_net_mean
    area_mean_sw_forcing = cont_sw_mean_cut - su_sw_mean
    area_mean_lw_forcing = cont_lw_mean_cut - su_lw_mean
        
    print(area_mean_net_forcing)
    print(area_mean_sw_forcing)
    print(area_mean_lw_forcing)
    
    # create an array of the years
    years = np.linspace(1,no_years,num = no_years)
    
    # set plot directory
    plot_directory = '/storage/silver/scenario/nn819853/plots/'
    
    font = {'size' : 14}
    plt.rc('font', **font)
    
    # plot the area mean net forcing against year
    plt.figure()
    plt.plot(years, area_mean_net_forcing)
    plt.title(u'PI SU free running TOA forcing')
    plt.xlabel('Model year')
    plt.ylabel(u'radiative flux / Wm$^{-2}$')
    plt.savefig(plot_directory + 'so2_free_toa_total_forcing_time_series', \
                dpi=220)
    plt.show()
    
    fig, axarr = plt.subplots(3, sharex = True)
    axarr[0].set_title(u'PI SU TOA forcings / Wm$^{-2}$')
    axarr[0].plot(years, area_mean_net_forcing)
    axarr[1].plot(years, area_mean_sw_forcing)
    axarr[2].plot(years, area_mean_lw_forcing)
    axarr[0].set_ylabel('Total')
    axarr[1].set_ylabel('SW')
    axarr[2].set_ylabel('LW')
#    axarr[0].set_ylim(0.8,1.3)
#    axarr[1].set_ylim(240.5,241.0)
#    axarr[2].set_ylim(-240.0,-239.5)
    plt.savefig(plot_directory + 'so2_free_toa_forcing_time_series', \
                dpi = 220)
    plt.show()   
    
    # plot the area mean net fluxes for both simulations against year
    plt.figure()
    plt.plot(years, cont_net_mean_cut)
    plt.plot(years, su_net_mean)
    plt.title(u'Control vs Su free TOA net flux')
    plt.xlabel('Model year')
    plt.ylabel(u'radiative flux / Wm$^{-2}$')
    plt.savefig(plot_directory + 'so2_control_free_toa_mean_net_flux_time_series', \
                dpi=220)
    plt.show()
    
    fig, axarr = plt.subplots(3, sharex = True)
    axarr[0].set_title(u'Free control vs SU downwards TOA fluxes / Wm$^{-2}$', \
         fontsize = 'medium')
    axarr[0].plot(years, cont_net_mean_cut)
    axarr[1].plot(years, cont_sw_mean_cut)
    axarr[2].plot(years, cont_lw_mean_cut, label = 'control')
    axarr[0].plot(years, su_net_mean)
    axarr[1].plot(years, su_sw_mean)
    axarr[2].plot(years, su_lw_mean, label = 'SU pert.')
    axarr[0].set_ylabel('Total', fontsize = 'medium')
    axarr[1].set_ylabel('SW', fontsize = 'medium')
    axarr[2].set_ylabel('LW', fontsize = 'medium')
    axarr[0].set_ylim(0,3)
    axarr[1].set_ylim(240,243)
    axarr[2].set_ylim(-242,-239)
    axarr[2].set_xlabel('Model Year', fontsize = 'medium')
    axarr[2].legend(ncol = 2, fontsize = 'small')
    plt.tight_layout()
    plt.savefig(plot_directory + 'so2_control_free_toa_mean_net_fluxes_time_series', \
                dpi = 400)
    plt.show()      
    
    # determine multiannual averages of forcing cubes
    mean_net_forcing = net_forcing.collapsed('time', iris.analysis.MEAN)
    mean_sw_forcing = sw_forcing.collapsed('time', iris.analysis.MEAN)
    mean_lw_forcing = lw_forcing.collapsed('time', iris.analysis.MEAN)
    
    # plot maps of multiannual mean forcings
    plt.figure()
    qplt.pcolormesh(mean_net_forcing, cmap = 'bwr', vmin = -27, vmax = 27)
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Free control - perturbed SU mean TOA forcing', fontsize = 'medium')
#    plt.tight_layout()
    plt.savefig(plot_directory + 'su_free_mean_toa_forcing_map.png', \
                dpi = 400)
    plt.show()
    
    plt.figure()
    qplt.pcolormesh(mean_sw_forcing, cmap = 'bwr', vmin = -27, vmax = 27)
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Free control - perturbed SU mean TOA SW forcing')
    plt.savefig(plot_directory + 'su_free_mean_toa_shortwave_forcing_map.png', \
                dpi = 220)
    plt.show()

    plt.figure()
    qplt.pcolormesh(mean_lw_forcing, cmap = 'bwr', vmin = -5, vmax = 5)
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Sulphate Longwave all-sky forcing', fontsize= 'medium')
    plt.savefig(plot_directory + 'su_free_mean_toa_longwave_forcing_map.png', \
                dpi = 400)
    plt.show()

    plt.figure()
    mesh = iplt.pcolormesh(mean_net_forcing, cmap = 'bwr', vmin = -26, vmax = 26)
    plt.colorbar(mesh, shrink = 0.9, label = u' W m$^{-2}$', orientation = 'horizontal')
    current_map = plt.gca()
    current_map.coastlines(linewidth = 1)
    plt.title('Free control - perturbed SU mean TOA forcing', fontsize = 'medium')
#    plt.tight_layout()
    plt.savefig(plot_directory + 'su_free_mean_toa_forcing_map_NEW.png', \
                dpi = 400)
    plt.show()
    
if __name__ == '__main__':
    main()
    