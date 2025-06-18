#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:30:29 2020

@author: nn819853
"""

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    clear_area_mean_net_forcing = [-0.54, -0.75, -1.03, -1.04, -0.95, -0.8, \
                                   -1., -0.85, -1.05, -0.94, -0.89, -0.85, \
                                   -0.75, -0.98, -0.86, -0.85, -1.06, -0.85, \
                                   -0.58, -0.85, -0.9,  -0.86, -0.72, -0.85, \
                                   -0.89, -0.93, -0.76, -0.93]
    clear_area_mean_sw_forcing = [-0.68, -0.89, -1.21, -1.05, -1.03, -0.94, \
                                  -1.12, -0.95, -0.99, -1.21, -1.13, -0.93, \
                                  -1.07, -1.16, -0.94, -1.02, -1.05, -1.05, \
                                  -0.84, -1.01, -1.14, -1.06, -1.06, -1.08, \
                                  -0.99, -1.04, -1.1, -1.13]
    clear_area_mean_lw_forcing = [0.15, 0.13, 0.17, 0.01, 0.08, 0.14, 0.13, \
                                  0.09, -0.06, 0.27, 0.24, 0.08, 0.32, 0.17, \
                                  0.08,  0.17, -0.01, 0.21, 0.26, 0.17, 0.25, \
                                  0.2, 0.33, 0.24, 0.1, 0.11, 0.34, 0.2]
    
    area_mean_net_forcing = [-1.18, -1.28, -1.36, -1.58, -1.29, -1.27, -1.54, \
                             -1.5, -1.57, -1.83, -1.31, -1.52, -1.37, -1.16, \
                             -1.31, -1.35, -1.58, -1.47, -1.17, -1.4, -1.19, \
                             -1.45, -1.43, -1.39, -1.55, -1.23, -1.46, -1.55]
    area_mean_sw_forcing = [-1.65, -1.67, -1.73, -1.87, -1.65, -1.52, -1.87, \
                            -1.7, -1.79, -2.2, -1.84, -1.75, -1.82, -1.61, \
                            -1.65, -1.86, -1.72, -1.9, -1.78, -1.75, -1.71, \
                            -1.92, -2. , -1.77, -1.97, -1.64, -2.06, -1.71 ]
    area_mean_lw_forcing = [0.47, 0.39, 0.37, 0.29, 0.36, 0.25, 0.33, 0.22, \
                            0.22, 0.37, 0.52, 0.23, 0.44, 0.45, 0.34, 0.52, \
                            0.14, 0.44, 0.61, 0.35, 0.52, 0.47, 0.57, 0.39, \
                            0.42, 0.41, 0.59, 0.16]
    
    mean_erf_all_sky = np.average(area_mean_net_forcing)
    mean_erf_sw_all_sky = np.average(area_mean_sw_forcing)
    mean_erf_lw_all_sky = np.average(area_mean_lw_forcing)
    print(mean_erf_all_sky)
    print(mean_erf_sw_all_sky)
    print(mean_erf_lw_all_sky)
    
    stdev_erf_all_sky = np.std(area_mean_net_forcing)
    stdev_erf_sw_all_sky = np.std(area_mean_sw_forcing)
    stdev_erf_lw_all_sky = np.std(area_mean_lw_forcing)
    
    num_years = len(area_mean_net_forcing)
    se_erf_all_sky = stdev_erf_all_sky/np.sqrt(num_years)
    se_erf_sw_all_sky = stdev_erf_sw_all_sky/np.sqrt(num_years)
    se_erf_lw_all_sky = stdev_erf_lw_all_sky/np.sqrt(num_years)
    
    print(se_erf_all_sky)
    print(se_erf_sw_all_sky)
    print(se_erf_lw_all_sky)
    
    clear_mean_erf_all_sky = np.average(clear_area_mean_net_forcing)
    clear_mean_erf_sw_all_sky = np.average(clear_area_mean_sw_forcing)
    clear_mean_erf_lw_all_sky = np.average(clear_area_mean_lw_forcing)
    print(clear_mean_erf_all_sky)
    print(clear_mean_erf_sw_all_sky)
    print(clear_mean_erf_lw_all_sky)
    
    clear_stdev_erf_all_sky = np.std(clear_area_mean_net_forcing)
    clear_stdev_erf_sw_all_sky = np.std(clear_area_mean_sw_forcing)
    clear_stdev_erf_lw_all_sky = np.std(clear_area_mean_lw_forcing)
    
    num_years = len(area_mean_net_forcing)
    clear_se_erf_all_sky = clear_stdev_erf_all_sky/np.sqrt(num_years)
    clear_se_erf_sw_all_sky = clear_stdev_erf_sw_all_sky/np.sqrt(num_years)
    clear_se_erf_lw_all_sky = clear_stdev_erf_lw_all_sky/np.sqrt(num_years)
    
    print(clear_se_erf_all_sky)
    print(clear_se_erf_sw_all_sky)
    print(clear_se_erf_lw_all_sky)
    
    print('All sky ERF = ', np.round(mean_erf_all_sky, 2), '+/-', \
          np.round(2*se_erf_all_sky, 2))
    
    print('Clear sky ERF = ', np.round(clear_mean_erf_all_sky, 2), '+/-', \
      np.round(2*clear_se_erf_all_sky, 2))
    
    plot_directory = '/storage/silver/scenario/nn819853/plots/'
    
    font = {'size' : 12}
    plt.rc('font', **font)
    
    years = np.linspace(1, num_years, num = num_years)
    print(years)
    
#    fig, axarr = plt.subplots(3, sharex = True)
#    axarr[0].set_title(u'Free control - perturbed SU radiative forcing / Wm$^{-2}$', \
#         fontsize = 'medium')
#    axarr[0].plot(years, area_mean_net_forcing)
#    axarr[1].plot(years, area_mean_sw_forcing)
#    axarr[2].plot(years, area_mean_lw_forcing, label = 'all-sky')
#    axarr[0].plot(years, clear_area_mean_net_forcing)
#    axarr[1].plot(years, clear_area_mean_sw_forcing)
#    axarr[2].plot(years, clear_area_mean_lw_forcing, label = 'clear-sky')
#    axarr[0].set_ylabel('Total', fontsize = 'medium')
#    axarr[1].set_ylabel('SW', fontsize = 'medium')
#    axarr[2].set_ylabel('LW', fontsize = 'medium')
#    axarr[0].set_ylim(-2, 0)
#    axarr[1].set_ylim(240,243)
#    axarr[2].set_ylim(-242,-239)
#    axarr[2].set_xlabel('Model Year', fontsize = 'medium')
#    axarr[2].legend(ncol = 2, fontsize = 'small')
#    plt.tight_layout()
#    plt.savefig(plot_directory + 'free_su_forcing_clear_vs_all_sky', \
#                dpi = 400)
#    plt.show()          

    plt.figure()
    plt.title(u'Free control - perturbed SU radiative forcing', \
         fontsize = 'medium')
    plt.plot(years, area_mean_net_forcing, color = 'black', linestyle = '-', label = 'net_all')
    plt.plot(years, clear_area_mean_net_forcing,color = 'black', linestyle = '--', label = 'net_clear')    
    plt.plot(years, area_mean_sw_forcing, color = 'mediumblue', linestyle = '-', label = 'sw_all')
    plt.plot(years, clear_area_mean_sw_forcing, color = 'mediumblue', linestyle = '--', label = 'sw_clear')
    plt.plot(years, area_mean_lw_forcing, color = 'r', linestyle = '-', label = 'lw_all')
    plt.plot(years, clear_area_mean_lw_forcing, color = 'r', linestyle = '--', label = 'lw_clear')
    plt.ylabel(u'Radiative forcing / W m$^{-2}$', fontsize = 'medium')
    plt.ylim(-2.8,0.7)
    plt.xlabel('Model Year', fontsize = 'medium')
    plt.legend(ncol = 3, fontsize = 'small')
#    plt.tight_layout()
    plt.savefig(plot_directory + 'free_su_forcing_clear_vs_all_sky', \
                dpi = 400)
    plt.show()             
    
    
if __name__ == '__main__':
    main()