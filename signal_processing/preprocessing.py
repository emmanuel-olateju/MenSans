"""
Preprocessing Pipeline Module

This module provides functions and a class for preprocessing EEG data using MNE.

Functions:
    - drop_accelerometer_channels: Drop accelerometer channels from raw data.
    - rename_channels: Rename channels in raw data based on a predefined mapping.
    - extract_recording_center: Extract a percentage of the recording centered around its duration.
    - notch_filter: Apply a notch filter to raw data.
    - custom_filter: Apply a custom bandpass filter to raw data.

Classes:
    - PreprocessingPipeline: A subclass of Pipeline for executing a sequence of preprocessing steps.

"""

from typing import List, Union
import copy
import mne

from pipeline.pipeline import Pipeline

channels_map = {
  'EEG 1':'Fp1',
  'EEG 2':'Fp2',
  'EEG 3':'C3',
  'EEG 4':'C4',
  'EEG 5':'T5',
  'EEG 6':'T6',
  'EEG 7':'O1',
  'EEG 8':'O2',
  'EEG 9':'F7',
  'EEG 10':'F8',
  'EEG 11':'F3',
  'EEG 12':'F4',
  'EEG 13':'T3',
  'EEG 14':'T4',
  'EEG 15':'P3',
  'EEG 16':'P4'
}

def drop_accelerometer_channels(raw:mne.io.Raw)->mne.io.Raw:
    """
    Drop accelerometer channels from raw data.

    Args:
        raw (mne.io.Raw): The raw data.

    Returns:
        mne.io.Raw: The raw data with accelerometer channels dropped.
    """
    raw.drop_channels(['Accel X','Accel Y','Accel Z'])
    return raw

def rename_channels(raw:mne.io.Raw)->mne.io.Raw:
    """
    Rename channels in raw data based on a predefined mapping.

    Args:
        raw (mne.io.Raw): The raw data.

    Returns:
        mne.io.Raw: The raw data with channels renamed.
    """
    raw.rename_channels(channels_map)
    return raw

def extract_recording_center(raw:mne.io.Raw,percentage:int=75)->mne.io.Raw:
    """
    Extract a percentage of the recording centered around its duration.

    Args:
        raw (mne.io.Raw): The raw data.
        percentage (int): The percentage of the recording to extract. Default is 75.

    Returns:
        mne.io.Raw: The extracted portion of the raw data.
    """
    time_ = raw.n_times/raw.info['sfreq']
    percentage = percentage/100
    raw.crop(tmin=((1-percentage)/2)*time_,tmax=(((1-percentage)/2)+percentage)*time_)
    return raw

def notch_filter(raw:mne.io.Raw,freqs:Union[List[Union[int,float]],int,float])->mne.io.Raw:
    """
    Apply a notch filter to raw data.

    Args:
        raw (mne.io.Raw): The raw data.
        freqs (Union[List[Union[int, float]], int, float]): The frequencies to notch filter.

    Returns:
        mne.io.Raw: The raw data after notch filtering.
    """
    raw.notch_filter(freqs=freqs)
    return raw

def custom_filter(raw:mne.io.Raw,lpf:Union[int,float]=None,hpf:Union[int,float]=None)->mne.io.Raw:
    """
    Apply a custom bandpass filter to raw data.

    Args:
        raw (mne.io.Raw): The raw data.
        lpf (Union[int, float], optional): The low-pass frequency. Default is None.
        hpf (Union[int, float], optional): The high-pass frequency. Default is None.

    Returns:
        mne.io.Raw: The raw data after applying the custom filter.
    """
    raw.filter(hpf,lpf)
    return raw

class PrepocessingPipeline(Pipeline):
    """
    Preprocessing Pipeline Class

    A subclass of Pipeline for executing a sequence of preprocessing steps.

    Attributes:
        name (str): The name of the pipeline.
        methods (list): A list of preprocessing methods to apply.

    Methods:
        __init__(name, methods): Initialize the PreprocessingPipeline object.
        forward(raw): Perform forward pass through the preprocessing pipeline.

    """

    def __init__(self,name:str,methods):
        """
        Initialize the PreprocessingPipeline object.

        Args:
            name (str): The name of the pipeline.
            methods (list): A list of preprocessing methods to apply.

        Returns:
            None
        """
        super().__init__(name,methods)

    def forward(self, raw:mne.io.Raw)->mne.io.Raw:
        """
        Perform forward pass through the preprocessing pipeline.

        Args:
            raw (mne.io.Raw): The raw data.

        Returns:
            mne.io.Raw: The preprocessed raw data.
        """
        res = copy.deepcopy(raw)
        for method in self.methods:
            if len(method)==2:
                res = method[0](raw,**method[1])
            elif len(method)==1:
              res = method[0](raw)
        return res
    