#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:20:13 2020

@author: nn819853
"""

import iris
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt

def time_zonal_mean_plots(cont_cube, forced_cube, experiment):
    """
    """
    # average cubes over time
    cont_time_zonal_mean = cont_cube.collapsed(['time', 'longitude'] ,iris.analysis.MEAN)
    forced_time_zonal_mean = forced_cube.collapsed(['time', 'longitude'] ,iris.analysis.MEAN)
    
    # Determine units and variable in cube
    variable = cont_cube.standard_name
    units = str(cont_cube.units)

    # calculate difference (control - forced)
    adjustment_time_zonal_mean = cont_time_zonal_mean - forced_time_zonal_mean
    
    # calculate min and max values for plots and set min = max to have zero centred
    vmax = np.max(adjustment_time_zonal_mean.data)
    vmin = np.min(adjustment_time_zonal_mean.data)
    if vmax > vmin:
        vmin = -1*vmax
    else:
        vmax = -1*vmin
    
    # plot individual and difference cross sections
    plt.figure()
    mesh = iplt.pcolormesh(adjustment_time_zonal_mean, cmap = 'bwr', vmin = vmin, vmax = vmax)
    plt.colorbar(mesh, shrink = 0.9, label = units, orientation = 'horizontal')
    plt.ylabel('Level height / m')
    plt.xlabel('Latitude')
    plt.title('Adjustment in ' + variable + ' ' + experiment)
    plt.savefig('adjustment_'+variable+'_'+experiment+'.png')
    plt.show()
    #add some way of reading the experiment in title and savefig
    
    # plot trop-strat only cubes
    plt.figure()
    trop_mesh = iplt.pcolormesh(adjustment_time_zonal_mean[0:50], cmap = 'bwr', vmin = vmin, vmax = vmax)
    plt.colorbar(trop_mesh, shrink = 0.9, label = units, orientation = 'horizontal')
    plt.ylabel('Level height / m')
    plt.xlabel('Latitude')
    plt.title('Trop adjustment in ' + variable + ' ' + experiment)
    plt.savefig('trop_adjustment_'+variable+'_'+experiment+'.png')
    plt.show() 
    
def main():
    # read in monthly means files    
    diag_names = ['air_potential_temperature', 'specific_humidity']
    
    cont_filename = '/storage/silver/scenario/nn819853/diags/mon_mn_diags/cont_free_apm_q_theta.pp'
    cont_theta, cont_q = iris.load(cont_filename, diag_names)
    
    su_filename = '/storage/silver/scenario/nn819853/diags/mon_mn_diags/su_free_apm_q_theta.pp'
    su_theta, su_q = iris.load(su_filename, diag_names)
    
    # Run time zonal mean plotting function
    time_zonal_mean_plots(cont_theta, su_theta, 'free_su')
    time_zonal_mean_plots(cont_q, su_q, 'free_su')
    
    

if __name__ == '__main__':
        main()
    
    
    
    
