"""
    This module provides functions for calculating spectral power within specified frequency bands
    using different methods like Welch's method or median filtering.

    Functions:
        - band_power: Computes the power within a specified frequency band using Welch's method 
        or median filtering.
        - bands_power: Computes the power within multiple frequency bands using Welch's method 
        or median filtering.
        - compute_psd: Computes the power spectral density (PSD) using Welch's method.

    Dependencies:
        - numpy
        - neurodsp.spectral
        - typing

    Typical usage example:

        import numpy as np
        from custom_module import band_power, bands_power, compute_psd

        # Generate a random signal
        sampling_frequency = 1000  # Sampling frequency
        sig = np.random.randn(1000)  # Random signal
        bands = [(8, 12), (13, 30)]  # Define frequency bands

        # Compute power within specified bands
        bp = band_power(sig, sampling_frequency, [8, 12])
        bps = bands_power(sig, sampling_frequency, bands)
        psd, freqs = compute_psd(sig, sampling_frequency)
"""

from typing import Tuple, List
import numpy as np
from neurodsp import spectral


def band_power(
        sig:np.array,sampling_frequency:int,band:List[float],
        method:str='welch',avg_type:str='mean'
        )->np.array:
    """
    Calculate the power within a specified frequency band.

    Args:
        sig (np.ndarray): The input signal.
        sampling_frequency (int): The sampling frequency of the signal.
        band (List[float]): The frequency band of interest [low_freq, high_freq].
        method (str, optional): The method used for spectral estimation. Default is 'welch'.
        avg_type (str, optional): The type of averaging to apply. Default is 'mean'.

    Returns:
        np.ndarray: The log10 of the power within the specified frequency band.

    Raises:
        ValueError: If an invalid method is specified.

    Notes:
        - Supported methods for spectral estimation are 'welch' and 'medfilt'.

    Example:
        >>> import numpy as np
        >>> from custom_module import band_power
        >>> sampling_frequency = 1000  # Sampling frequency
        >>> sig = np.random.randn(1000)  # Random signal
        >>> band = [8, 12]  # Frequency band of interest
        >>> power = band_power(sig, sampling_frequency, band)
    """

    freqs, spectrum = spectral.compute_spectrum(sig,sampling_frequency,method,avg_type)
    assert (spectrum.ndim!=0) and (spectrum.ndim<=2)
    assert freqs.shape[0] == spectrum.shape[1]
    assert np.isnan(spectrum).sum() == 0

    if method=='welch':
        assert freqs[-1] <= (sampling_frequency/2)
        assert ((freqs>=band[0]) & (freqs<=band[1])).shape[0] >= 1
        if spectrum.ndim==2:
            _band_power = np.empty((spectrum.shape[0]))
            for channel_no in range(spectrum.shape[0]):
                _band_power[channel_no] = (
                    (spectrum[channel_no,((freqs>=band[0]) & (freqs<=band[1]))]).mean()
                    )
        else:
            _band_power = spectrum[((freqs>=band[0]) & (freqs<=band[1]))].mean()
    elif method=='medfilt':
        if spectrum.ndim==2:
            _band_power = np.empty((spectrum.shape[0]))
            for channel_no in range(spectrum.shape[0]):
                _band_power[channel_no] = spectrum[channel_no,:].mean()
        else:
            _band_power = spectrum[:].mean()
    else:
        raise ValueError(f"Inpermissible method, {method} is used")

    return np.log10(_band_power)

def bands_power(
        sig:np.array,sampling_frequency:int,bands:List[Tuple[float]],
        method:str='welch',avg_type:str='mean'
        )->np.array:
    """
    Compute the power within multiple frequency bands using Welch's method or median filtering.

    Args:
        sig (np.ndarray): The input signal.
        sampling_frequency (int): The sampling frequency of the signal.
        bands (List[Tuple[float]]): A list of tuples representing frequency bands of interest.

    Keyword Args:
        method (str, optional): The method used for spectral estimation. Default is 'welch'.
        avg_type (str, optional): The type of averaging to apply. Default is 'mean'.

    Returns:
        np.ndarray: The power within the specified frequency bands.

    Raises:
        AssertionError: If the signal dimension is invalid.

    Example:
        >>> import numpy as np
        >>> from custom_module import bands_power
        >>> fs = 1000  # Sampling frequency
        >>> sig = np.random.randn(1000)  # Random signal
        >>> bands = [(8, 12), (13, 30)]  # Define frequency bands
        >>> powers = bands_power(sig, fs, bands)
    """

    assert sig.ndim!=0 & sig.ndim<=2
    if sig.ndim==2:
        _bands_power = np.empty((sig.shape[0],len(bands)))
        for band_no,band in enumerate(bands):
            _bands_power[:,band_no] = band_power(sig,sampling_frequency,band,method,avg_type)
    else:
        _bands_power = np.empty((len(bands)))
        for band_no,band in enumerate(bands):
            _bands_power[band_no] = band_power(sig,sampling_frequency,band,method,avg_type)
    return _bands_power

def compute_psd(sig_:np.ndarray,sampling_frequency_:int)->Tuple[np.ndarray,int]:
    """
    Compute the Power Spectral Density (PSD) of a signal using Welch's method.

    Args:
        sig_ (np.ndarray): The input signal.
        sampling_frequency_ (int): The sampling frequency of the signal.

    Returns:
        Tuple[np.ndarray, int]: A tuple containing the log10 of the PSD spectrum and 
        the corresponding frequencies.

    Example:
        >>> import numpy as np
        >>> from custom_module import compute_psd
        >>> fs = 1000  # Sampling frequency
        >>> sig = np.random.randn(1000)  # Random signal
        >>> psd, freqs = compute_psd(sig, fs)
    """
    freqs, spectrum = spectral.compute_spectrum(sig_,sampling_frequency_,'welch','mean')
    spectrum = np.log10(spectrum)
    return spectrum, freqs
