"""
Plot Globals Module

This module contains global variables and dictionaries used for plotting EEG sensor data.

Attributes:
    - sensors_colors (dict): Dictionary mapping EEG channel names to tuples containing color 
    and line style.
    - channel_names (list): List of EEG channel names.
    - white_to_red_color (list): List of tuples representing colors ranging from white to red.
    - openBCIcoordsArray (numpy.ndarray): Array containing the coordinates of EEG channels 
    in the OpenBCI 16-channel layout.
    - openBCIcoords (dict): Dictionary containing the coordinates of EEG channels in the 
    OpenBCI 16-channel layout.

"""

import numpy as np

# Dictionary mapping EEG channel names to colors and line styles
sensors_colors = {
    'Fp1': ('deepskyblue', '--'),
    'Fp2': ('deepskyblue', ''),
    'C3': ('darkorange', '--'),
    'C4': ('darkorange', ''),
    'T5': ('limegreen', '--'),
    'T6': ('limegreen', ''),
    'O1': ('hotpink', '--'),
    'O2': ('hotpink', ''),
    'F7': ('goldenrod', '--'),
    'F8': ('goldenrod', ''),
    'F3': ('mediumpurple', '--'),
    'F4': ('mediumpurple', ''),
    'T3': ('teal', '--'),
    'T4': ('teal', ''),
    'P3': ('crimson', '--'),
    'P4': ('crimson', ''),
}

# List of EEG channel names
channel_names = [
    'Fp1', 'Fp2', 'C3', 'C4',
    'T5', 'T6', 'O1', 'O2',
    'F7', 'F8', 'F3', 'F4',
    'T3', 'T4', 'P3', 'P4'
]

# White to red color gradient
white_to_red_color = [(1, 1, 1), (1, 0, 0)]

# OpenBCI 16-channel layout coordinates
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

# OpenBCI 16-channel layout channel coordinates
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
