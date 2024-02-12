import pytest
import random
import numpy as np
np.random.seed(45)

from typing import *

fs = 125
chs = 16
t = 600
all_bands = [(1.0,4.0),(4.0,8.0),(8.0,12.0),(12.0,16.0),(16.0,20.0),]

@pytest.fixture
def sampling_frequency():
    assert isinstance(fs,int)
    return fs

@pytest.fixture
def no_channels():
    assert isinstance(chs,int)
    return chs

@pytest.fixture
def recording_duration():
    assert isinstance(t,int)
    return t

@pytest.fixture
def eeg_data(no_channels, recording_duration, sampling_frequency):
    ts = int(round(recording_duration/sampling_frequency))
    ts_ = np.linspace(0,recording_duration,ts)
    data = np.empty((no_channels,ts))
    for ch in range(no_channels):
        data[ch,:] = random.randint(1,10)*np.sin(ts_) + random.randint(1,10)*np.cos(ts_)
    return data
    

@pytest.fixture
def bands():
    assert isinstance(all_bands,list)
    return all_bands

@pytest.fixture
def openBCI_16channels():
    return ['Fp1','Fp2','F3','F4','F7','F8','C3','C4','T3','T4','P3','P4','T5','T6','O1','O2']