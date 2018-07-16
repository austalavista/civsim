import numpy as np
import config
import time

def demographics():
    nation_data = config.nation_data
    province_data = config.province_data
    owner_mask = config.owner_mask

    #Pop_auto
    nation_data[:,5] = np.dot(province_data[:,2] * (1-province_data[:,0]),owner_mask) #currently outputting all zeros without proper data

def agriculture():
    nation_data = config.nation_data
    province_data = config.province_data
    owner_mask = config.owner_mask

    #Agri_national
    nation_data[:,2] = np.dot(province_data[:,3] * province_data[:,2] * (1-province_data[:,0]) , owner_mask) * nation_data[:,3] + nation_data[:,4]

    #Agri_retained
    province_data[:,4] = province_data[:,3] * province_data[:,2] * province_data[:,0] * np.dot(owner_mask, nation_data[:,3])

    #Agri_state NOTE: Agri_public = Agri_national - Agri_state
    nation_data[:,6] = nation_data[:,2] * (1-nation_data[:,3])

    #Agri_distributed
    province_data[:,5] = np.dot(owner_mask, (nation_data[:,2] - nation_data[:,6]) / nation_data[:,5]) * province_data[:,2] * (1 - province_data[:,0])

def population():
    nation_data = config.nation_data
    province_data = config.province_data
    owner_mask = config.owner_mask
    universal_data = config.universal_data

    #pop_food
    province_data[:,7] = universal_data[0] * ((province_data[:,5] + province_data[:,4]) / province_data[:,2] - 1)

