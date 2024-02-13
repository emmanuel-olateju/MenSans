import numpy as np
import pandas as pd
from typing import *



def hjorth_parameters_computation(data:Union[np.ndarray,List], segment_size:int=10)->dict:

    num_segments = len(data)//segment_size
    activities = list()
    mobilities = list()
    complexities = list()

    for i in range(num_segments):
        
        start = i*segment_size
        end = start+segment_size

        segment = data[start:end]

        activity = np.var(segment)
        activities.append(activity)

        mobility = np.var(np.diff(segment))
        mobilities.append(segment)

        complexity = np.var(np.diff(np.diff(segment)))
        complexities.append(segment)
    
    avg_activity = np.mean(activities)
    avg_mobility= np.mean(mobilities)
    avg_complexity = np.mean(complexities)
    std_activity = np.std(activities)
    std_mobility= np.std(mobilities)
    std_complexity = np.std(complexities)

    hjorth_parameters = {
        'mean_activity': avg_activity,
        'mean_mobility': avg_mobility,
        'mean_complexity': avg_complexity,
        'std_activity': std_activity,
        'std_mobility': std_mobility,
        'std_complexity': std_complexity
    }
    
    return hjorth_parameters

def hjorth_2D(data:Union[np.ndarray,List[list]],segment_size:int,ch_names:Union[List,np.ndarray]=None)->pd.DataFrame:

    if isinstance(data,list):
        data = np.array(data)
    assert data.ndim==2
    if ch_names!=None:
        assert data.shape[0]==len(ch_names)

    hjorth_parameters = list()

    for c in range(len(data)):
        hjorth_parameters.append(hjorth_parameters_computation(data[c,:],segment_size))
    
    if ch_names!=None:
        hjorth_parameters = pd.DataFrame(hjorth_parameters,index=ch_names)
    else:
        hjorth_parameters = pd.DataFrame(hjorth_parameters)

    return hjorth_parameters