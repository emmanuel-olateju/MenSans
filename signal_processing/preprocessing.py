import mne
import sys
from Pipeline.Pipeline import Pipeline

import copy

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

def drop_accelerometer_channels(raw):
  raw.drop_channels(['Accel X','Accel Y','Accel Z'])
  return raw

def rename_channels(raw):
  raw.rename_channels(channels_map)
  return raw

def extract_recording_center(raw,percentage=75):
  t = raw.n_times/raw.info['sfreq']
  percentage = percentage/100
  raw.crop(tmin=(((1-percentage)/2)*t),tmax=((((1-percentage)/2)+percentage)*t))
  return raw

def notch_filter(raw,freqs):
  raw.notch_filter(freqs=freqs)
  return raw

def filter(raw,lpf=None,hpf=None):
  raw.filter(hpf,lpf)
  return raw

class PrepocessingPipeline(Pipeline):
  def __init__(self,name,methods):
    super().__init__(name,methods)
  
  def forward(self, raw: mne.io.Raw) -> mne.io.Raw:
    res = copy.deepcopy(raw)
    for method in self.methods:
      if len(method)==2:
        res = method[0](raw,**method[1])
      elif len(method)==1:
        res = method[0](raw)
    return res