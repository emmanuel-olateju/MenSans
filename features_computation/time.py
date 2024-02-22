"""
Hjorth Parameters Computation Module

This module contains functions for computing Hjorth parameters 
from EEG (electroencephalography) data.

Functions:
    - hjorth_parameters_computation: Computes Hjorth parameters for a given EEG data segment.
    - hjorth_2D: Computes Hjorth parameters for each channel of EEG data.

Dependencies:
    - numpy
    - pandas

"""

from typing import *
import numpy as np
import pandas as pd

def hjorth_parameters_computation(data:Union[np.ndarray,List], segment_size:int=10)->dict:
    """
    Compute Hjorth parameters for a given EEG data segment.

    Args:
        data (Union[np.ndarray, List]): EEG data segment.
        segment_size (int, optional): Segment size for computing Hjorth parameters. Default is 10.

    Returns:
        dict: Dictionary containing Hjorth parameters:
            - 'mean_activity': Mean activity
            - 'mean_mobility': Mean mobility
            - 'mean_complexity': Mean complexity
            - 'std_activity': Standard deviation of activity
            - 'std_mobility': Standard deviation of mobility
            - 'std_complexity': Standard deviation of complexity

    Example:
        >>> import numpy as np
        >>> from custom_module import hjorth_parameters_computation
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> hjorth_params = hjorth_parameters_computation(eeg_data)
    """
    num_segments = len(data)//segment_size
    activities = []
    mobilities = []
    complexities = []
    for i in range(num_segments): 
        start = i*segment_size
        end = start+segment_size
        segment = data[start:end]
        activity = np.var(segment)
        activities.append(activity)
        mobility = np.var(np.diff(segment))
        mobilities.append(mobility)
        complexity = np.var(np.diff(np.diff(segment)))
        complexities.append(complexity)
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

def hjorth_2D(
        data:Union[np.ndarray,List[list]],
        segment_size:int,ch_names:Union[List,np.ndarray]=None
        )->pd.DataFrame:
    """
    Compute Hjorth parameters for each channel of EEG data.

    Args:
        data (Union[np.ndarray, List[list]]): EEG data matrix.
        segment_size (int): Segment size for computing Hjorth parameters.
        ch_names (Union[List, np.ndarray], optional): List of channel names. Default is None.

    Returns:
        pd.DataFrame: DataFrame containing Hjorth parameters for each channel.

    Raises:
        AssertionError: If the input data dimension is not 2 or if the length of channel
          names doesn't match the number of rows in data.

    Example:
        >>> import numpy as np
        >>> from custom_module import hjorth_2D
        >>> eeg_data = np.random.randn(1000, 16)  # EEG data with 16 channels
        >>> hjorth_params_df = hjorth_2D(eeg_data, 10)
    """
    if isinstance(data,list):
        data = np.array(data)
    assert data.ndim==2
    if ch_names!=None:
        assert data.shape[0]==len(ch_names)

    hjorth_parameters = []

    for c in range(len(data)):
        hjorth_parameters.append(hjorth_parameters_computation(data[c,:],segment_size))
    if ch_names!=None:
        hjorth_parameters = pd.DataFrame(hjorth_parameters,index=ch_names)
    else:
        hjorth_parameters = pd.DataFrame(hjorth_parameters)
    return hjorth_parameters
