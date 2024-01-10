import mne

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

def filter(raw,lpf=None,hpf=None):
  raw.filter(hpf,lpf)
  return raw