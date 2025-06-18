#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 15:49:24 2020

@author: nn819853
"""

import iris
import numpy as np
import datetime
import iris.coord_categorisation


#def flux_annual_mean(sw_down, sw_up, lw_up):
#    """
#    Determines annual mean cubes of fluxes trimming incomplete years
#    :param iris.cube sw_down: cube of downwards sw flux
#    :param iris.cube sw_up: cube of upwards sw flux
#    :param iris.cube lw_up: cube of upwards lw flux
#    :returns: cubes of annual mean total downwards net, lw and sw flux
#    """
#    
#    # make a normal list of cubes - don't think is same as cubelist
#    cubes = [sw_down, sw_up, lw_up]
#    
#    # initialise list for annual averaged toa cubes
#    annual_meaned_cubes = []
#    
#    # set variables for extracting only whole years
#    tdelta_1yr = datetime.timedelta(hours = 24*360)
#    spans_1yr = lambda t: (t.bound[1] - t.bound[0]) == tdelta_1yr
#    spans_1yr_constraint = iris.Constraint(time = spans_1yr)


def annual_mean(cube):
    """
    Determines annual means of cube, trimming incomplete years
    :param iris.cube cube: cube to annually average
    :returns: annually meaned cube
    """
    
    # set variables for extracting only whole years
    tdelta_1yr = datetime.timedelta(hours = 24*360)
    spans_1yr = lambda t: (t.bound[1] - t.bound[0]) == tdelta_1yr
    spans_1yr_constraint = iris.Constraint(time = spans_1yr)
    
    #!! maybe add exception for if units of time coord are not hours? !!#
    
    # determine multi-annual averages for cube and filter incomplete years
    iris.coord_categorisation.add_year(cube, 'time', name='year')
    annual_mean = cube.aggregated_by('year',iris.analysis.MEAN)
    trimmed_annual_mean = annual_mean.extract(spans_1yr_constraint)
    
    return trimmed_annual_mean


def total_down_fluxes(sw_down, sw_up, lw_up):
    """
    Determines total downwards fluxes for net, sw, lw
    :param iris.cube sw_down: cube of downwards sw flux
    :param iris.cube sw_up: cube of upwards sw flux
    :param iris.cube lw_up: cube of upwards lw flux
    :returns: cubes of total downwards sw, lw and net fluxes
    """
    
    #!! add exception to check cubes have right diagnostics !!#
    
    # determine net flux cubes
    net_sw_down = sw_down - sw_up
    net_lw_down = lw_up*(-1)
    net_down = net_sw_down + net_lw_down
    
    return net_sw_down, net_lw_down, net_down

#!! maybe remove as too simple - can eb done in one line in calling script !!#
def time_mean_cube(cube):
    """
    Determines time mean of a cube
    :param iris.cube cube: cube with time dimension
    :returns: time averaged cube
    """
    
    # Mean over time
    time_mean_cube = cube.collapsed('time', iris.analysis.MEAN)
    
    # Stdev over time
    time_stdev_cube = cube.collapsed('time', iris.analysis.STD_DEV)
    
    # calculate 2*SE
    n = len(cube.coord('time').points)
    time_double_SE_cube = 2*time_stdev_cube/(np.sqrt(n))
    #!! not sure if should be n or n-1? !!#
    
    return time_mean_cube, time_stdev_cube, time_double_SE_cube
    

def area_mean_cube(cube):
    """
    Determines area weighted mean of cube using lat and lon coordinates
    :param iris.cube cube: cube with lat and lon dimensions
    :returns: area weighted mean cube
    """
    
    # determine area weightings for spatial averaging
    cube.coord('latitude').guess_bounds()
    cube.coord('longitude').guess_bounds()
    grid_area = iris.analysis.cartography.area_weights(cube)
    
    # Determine area weighted mean 
    area_mean_cube = cube.collapsed(['latitude','longitude'], \
                                    iris.analysis.MEAN, \
                                    weights = grid_area) 
    
    # Determine area-weighted stdev
#    area_stdev_cube = cube.collapsed(['latitude','longitude'], \
#                                    iris.analysis.STD_DEV, ddof = 2, \
#                                    weights = grid_area)
    #!! not certain needs ddof = 2!!#
    #!! analysis.STD_DEV does not seem to allow weighting (by area anyway) !!#
    
    # calculate 2*SE
#    n = len(cube.coord('time').points)
#    area_double_SE_cube = 2*area_stdev_cube/(np.sqrt(n))
    #!! not sure if should be n or n-1? !!#
    
    return area_mean_cube #, area_stdev_cube, area_double_SE_cube


def area_mean_cube_nans(cube):
    """
    Returns area weighted mean of cube, excluding nans, with lat and lon coords
    :param iris.cube cube: cube with lat and lon dimensions, containing nans
    :returns: area weighted mean cube
    """
    
    # Return boolean array of nans locations
    cube_nans = np.isnan(cube.data)
    
    # Make masked version of cube, with nans masked
    nans_masked_cube = iris.util.mask_cube(cube, cube_nans)
    
    # Calculate area mean
    area_mean_cube_nans = area_mean_cube(nans_masked_cube)
    
    return area_mean_cube_nans


def area_rms_cube(cube):
    """
    Determines area weighted rms of cube using lat and lon coordinates
    :param iris.cube cube: cube with lat and lon dimensions
    :returns: area weighted rms cube
    """
    
    # determine area weightings for spatial averaging
    cube.coord('latitude').guess_bounds()
    cube.coord('longitude').guess_bounds()
    grid_area = iris.analysis.cartography.area_weights(cube)
    
    # Determine area weighted mean 
    area_rms_cube = cube.collapsed(['latitude','longitude'], \
                                    iris.analysis.RMS, \
                                    weights = grid_area)
        
    return area_rms_cube

#!! add some code to trim longer cube to same length? with warning? !!#
#!! add code to read name, units etc from either cube, as seems to lose !###
def cube_diff(cube1, cube2, error_cube1 = 0, error_cube2 = 0):
    """
    """
    
    diff_cube = cube1 - cube2
    if error_cube1 and error_cube2 != 0:
        error_diff_cube = error_cube1 + error_cube2
        return diff_cube, error_diff_cube
        
    else:
        error_diff_cube = 0
        return diff_cube
    

def toa_flux(pp_file, sky_type, spinup_years = 0, end_year = 35):
    """
    """
    
    # load diags based on sky type 
    if sky_type == 'all':
        diag_names = ['toa_incoming_shortwave_flux', \
                      'toa_outgoing_shortwave_flux', \
                      'toa_outgoing_longwave_flux']
    elif sky_type == 'clear':
        diag_names = ['toa_incoming_shortwave_flux', \
                      'toa_outgoing_shortwave_flux_assuming_clear_sky', \
                      'toa_outgoing_longwave_flux_assuming_clear_sky']
    elif sky_type == 'clean':
        diag_names = ['toa_incoming_shortwave_flux', \
                      'm01s01i517', \
                      'm01s02i517']
    elif sky_type == 'clearclean':
        diag_names = ['toa_incoming_shortwave_flux', \
                      'm01s01i519', \
                      'm01s02i519']
        
    sw_d, sw_u, lw_u = iris.load(pp_file, diag_names)
    
    # since these diags don't include a unit for some reason
    if sky_type == 'clean' or sky_type == 'clearclean':
        sw_u.units = 'W m-2'
        lw_u.units = 'W m-2'
        
    #!!! Should check if calculating down total fluxes before annual meaning changes results (ignore tick on line!)!!!#
    cubes = [sw_d, sw_u, lw_u]
    annual_means = []
    
    for cube in cubes:
        annual_means.append(annual_mean(cube))
        
    yr_mean_sw_down, yr_mean_sw_up, yr_mean_lw_up = annual_means
    
    total_sw_down, total_lw_down, net_down = total_down_fluxes(yr_mean_sw_down, \
                                                               yr_mean_sw_up, \
                                                               yr_mean_lw_up)
    # Determine area means for time series plots using all years
    yr_area_means_total_sw_down = area_mean_cube(total_sw_down)
    yr_area_means_total_lw_down = area_mean_cube(total_lw_down)
    yr_area_means_net_down = area_mean_cube(net_down)
    
    # Extract just years after spin up and before set end of total down 3D cubes
    total_sw_down_spun = total_sw_down[spinup_years:end_year]
    total_lw_down_spun = total_lw_down[spinup_years:end_year]
    net_down_spun = net_down[spinup_years:end_year]
    
    # Determine multiannual mean 2D cubes using just years after spinup
    multi_yr_mean_total_sw_down = time_mean_cube(total_sw_down_spun)
    multi_yr_mean_total_lw_down = time_mean_cube(total_lw_down_spun)
    multi_yr_mean_net_down = time_mean_cube(net_down_spun)
    
    # Extract from area mean 1D cube just years after spinup and before set end
    yr_area_means_total_sw_down_spun = yr_area_means_total_sw_down[spinup_years:end_year]
    yr_area_means_total_lw_down_spun = yr_area_means_total_lw_down[spinup_years:end_year] 
    yr_area_means_net_down_spun = yr_area_means_net_down[spinup_years:end_year]
    
    # Determine multiannual 0D area mean cubes using just years after spinup and before set end
    multi_yr_area_mean_total_sw_down = time_mean_cube(yr_area_means_total_sw_down_spun)
    multi_yr_area_mean_total_lw_down = time_mean_cube(yr_area_means_total_lw_down_spun)
    multi_yr_area_mean_net_down = time_mean_cube(yr_area_means_net_down_spun)
        
    return yr_area_means_total_sw_down, yr_area_means_total_lw_down, yr_area_means_net_down, \
multi_yr_mean_total_sw_down, multi_yr_mean_total_lw_down, multi_yr_mean_net_down, \
multi_yr_area_mean_total_sw_down, multi_yr_area_mean_total_lw_down, multi_yr_area_mean_net_down



