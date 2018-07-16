import numpy as np
import config
import timeit

def population():
    config.province_data[:,2] += config.province_data[:,2] * (0.2 + config.universal_data[1] * config.provine_data[:,1]) #0.2 is k_growth temporarily

def agriculture():
    nation_data = config.nation_data
    province_data = config.province_data
    owner_mask = config.owner_mask

    #Agri_national
    nation_data[:,2] = np.dot(province_data[:,3] * province_data[:,2] * (1-province_data[:,0]) , owner_mask) * nation_data[:,3] + nation_data[:,4] #need to add Agri_imported