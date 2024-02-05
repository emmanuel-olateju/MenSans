import mne 
import matplotlib.pyplot as plt
import numpy as np

class Montage:
    def __init__(self,chs,coord):
        self.ch_names = chs
        self.coordinates = coord
        self.ch_pos = dict(zip(self.ch_names,self.coordinates))
        self.montage = mne.channels.make_dig_montage(self.ch_pos)
    
    def plot(self,arguments):
        plt.close()
        fig = plt.figure()
        self.montage.plot(**arguments)
        plt.close()

openBCIcoordsArray = np.array([
    [-0.025, 0.09, 0.0],
    [0.025, 0.09, 0.0],
    [-0.045, 0, 0.0],
    [0.045, 0, 0.0],
    [-0.08, -0.05, 0.0],
    [0.08, -0.05, 0.0],
    [-0.025, -0.09, 0.0],
    [0.025, -0.09, 0.0],
    [-0.08, 0.05, 0.0],
    [0.08, 0.05, 0.0],
    [-0.04, 0.045, 0.0],
    [0.04, 0.045, 0.0],
    [-0.095, 0, 0.0],
    [0.095, 0, 0.0],
    [-0.04, -0.045, 0.0],
    [0.04, -0.045, 0.0],
])

openBCIcoords = {
    'Fp1': [-0.025, 0.09, 0.0],
    'Fp2': [0.025, 0.09, 0.0],
    'C3': [-0.045, 0, 0.0],
    'C4': [0.045, 0, 0.0],
    'T5': [-0.08, -0.05, 0.0],
    'T6': [0.08, -0.05, 0.0],
    'O1': [-0.025, -0.09, 0.0],
    'O2': [0.025, -0.09, 0.0],
    'F7': [-0.08, 0.05, 0.0],
    'F8': [0.08, 0.05, 0.0],
    'F3': [-0.04, 0.045, 0.0],
    'F4': [0.04, 0.045, 0.0],
    'T3': [-0.095, 0, 0.0],
    'T4': [0.095, 0, 0.0],
    'P3': [-0.04, -0.045, 0.0],
    'P4': [0.04, -0.045, 0.0],
}
openBCImontage = Montage(list(openBCIcoords.keys()),list(openBCIcoords.values()))