"""
Montage Utilities Module

This module provides a utility class for creating and plotting montages using MNE.

Classes:
    - Montage: A class for creating and plotting montages.
"""
import mne 
import matplotlib.pyplot as plt
from . import plot_globals

class Montage:
    """
    A class for creating and plotting montages using MNE.

    Attributes:
        ch_names (list): List of channel names.
        coordinates (list): List of channel coordinates.
        ch_pos (dict): Dictionary mapping channel names to their coordinates.
        montage (mne.channels.DigMontage): MNE DigMontage object representing the montage.

    Methods:
        - plot: Plot the montage.

    """
    def __init__(self,chs,coord):
        """
        Initialize the Montage object.

        Args:
            chs (list): List of channel names.
            coord (list): List of channel coordinates.

        Returns:
            None
        """
        self.ch_names = chs
        self.coordinates = coord
        self.ch_pos = dict(zip(self.ch_names,self.coordinates))
        self.montage = mne.channels.make_dig_montage(self.ch_pos)
    def plot(self,arguments):
        """
        Plot the montage.

        Args:
            arguments (dict): Additional plotting arguments.

        Returns:
            None
        """
        plt.close()
        plt.figure()
        self.montage.plot(**arguments)
        plt.close()

openBCImontage = Montage(
    list(plot_globals.openBCIcoords.keys()),
    list(plot_globals.openBCIcoords.values())
    )
