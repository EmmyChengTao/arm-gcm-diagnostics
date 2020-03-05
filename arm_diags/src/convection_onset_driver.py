import cdms2, MV2
import cdtime
import numpy as np
import numpy.ma as ma
import glob
import matplotlib.pyplot as plt
import os
import scipy.io
# Convective onset metrics generated by the Neelin group, UCLA
# Original code: Kathleen Schiro, python version 22 Dec 2016, references privided in detail from convective_onset_statistics_ARM_Diagnostics.py

from convection_onset_statistics import convection_onset_statistics

def convection_onset(parameter):
    """Calculate """
    variables = parameter.variables
    #seasons = parameter.season
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
   
    test_model = parameter.test_data_set 
    #ref_models = parameter.ref_models
    
    #Read in observation data
    precip_threshold = 0.5
    #print('Read in observation data')
    for index, site in enumerate(sites):
        #print('site',site)
        #print('index',index)
        if site == 'twpc1':     #twpc1
            cwv_max = 85
            cwv_min = 28
            bin_width = 1.5
            sitename = 'Manus Island'
        if site == 'twpc2':     #twpc2
            cwv_max = 70
            cwv_min = 28
            bin_width = 2.0
            sitename = 'Nauru'
        if site == 'twpc3':     #twpc3
            cwv_max = 85
            cwv_min = 28
            bin_width = 2.0
            sitename = 'Darwin'
        if site == 'sgp':     #sgp
            cwv_max = 75
            cwv_min = 20
            bin_width = 2.0
            sitename = 'SGP'
    
        for va in variables:
            #print(glob.glob(os.path.join(obs_path,'ARMdiag_'+va+'_1hr_*_'+site+'.nc')))
            filename = glob.glob(os.path.join(obs_path,'ARMdiag_'+va+'_1hr_*_'+site+'.nc'))[0]
            
            #print(filename)
            f_in=cdms2.open(filename)
            var=f_in(va)
            #print('var_shape',va,var.shape)
            if va == 'pr':
                precip = var
                precip[precip<-900] = np.nan
                #print('Max PRECIP:',max(precip))
            if va == 'prw':
                prw = var
                prw[prw<-900] = np.nan
                #print('Max PRW:',max(prw))
            f_in.close()
        convection_onset_statistics(precip_threshold,cwv_max,cwv_min,bin_width,prw, precip,'ARM',output_path,sites,sitename)

        pr_prw_mod = []
        for va in variables:
            filename = glob.glob(os.path.join(test_path, '*'+va+'_cfSites_'+test_model+'*'+site+'.nc'))
            if len(filename) == 0:
               raise RuntimeError('No sub daily data for test model were found.')
            f_in=cdms2.open(filename[0])
            pr=f_in(va)#,time=('1979-01-01','1979-12-31')) #Read in the variable
            if va == 'pr':
                pr = pr *3600.           #'kg m-2 s-1' to 'mm/hr'
            pr_prw_mod.append(pr)
    convection_onset_statistics(precip_threshold,cwv_max,cwv_min,bin_width,pr_prw_mod[1],pr_prw_mod[0],test_model,output_path,sites,sitename)
 
