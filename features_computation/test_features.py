"""
Custom Module

This module contains functions for processing EEG (electroencephalography) data, 
including spectral analysis,time-domain analysis, and computation of 
Hjorth parameters.

Functions:
    - band_power: Computes the power within a specified frequency band.
    - bands_power: Computes the power within multiple frequency bands.
    - compute_psd: Computes the power spectral density (PSD).
    - hjorth_parameters_computation: Computes Hjorth parameters for EEG data.
    - hjorth_2D: Computes Hjorth parameters for 2D EEG data.

Tests:
    - test_band_power_method: Test different method and averaging type combinations 
    for 'band_power' function.
    - test_bands_power: Test different method and averaging type combinations 
    for 'bands_power' function.
    - test_compute_psd: Test the 'compute_psd' function.
    - test_hjorth_method: Test the 'hjorth_parameters_computation' function.
    - test_hjorth_2D: Test the 'hjorth_2D' function.

Fixtures:
    - hjorth_segment_size: Fixture providing the segment size for computing Hjorth parameters.

Dependencies:
    - pytest
    - numpy
    - pandas
    - frequency (from .frequency)
    - time (from .time)

"""

import pytest
import numpy as np
import pandas as pd
from .frequency import band_power, bands_power, compute_psd
from .time import hjorth_parameters_computation, hjorth_2D

@pytest.mark.parametrize(
        "method_, avg_type_", 
        [("welch","mean"),("welch","median"),("medfilt","mean"),("medfilt","median")]
        )
def test_band_power_method(eeg_data,sampling_frequency,bands,method_,avg_type_):
    """
    Test the 'band_power' function with different method and averaging type combinations.

    Args:
        eeg_data: The EEG data for testing.
        sampling_frequency: The sampling frequency of the EEG data.
        bands: The frequency bands of interest.
        method_ (str): The method used for spectral estimation.
        avg_type_ (str): The type of averaging to apply.

    Returns:
        None

    Raises:
        AssertionError: If the returned spectrum is complex or has an unexpected dimension.

    Example:
        >>> import numpy as np
        >>> from custom_module import test_band_power_method
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> fs = 1000  # Sampling frequency
        >>> bands = [(8, 12)]  # Frequency band of interest
        >>> test_band_power_method(eeg_data, fs, bands, "welch", "mean")
    """
    spectrum = band_power(eeg_data,sampling_frequency,bands[1],method_,avg_type_)
    assert np.iscomplexobj(spectrum) is False
    assert spectrum.ndim == 1

@pytest.mark.parametrize(
        "method_, avg_type_", 
        [("welch","mean"),("welch","median"),("medfilt","mean"),("medfilt","median")]
        )
def test_bands_power(eeg_data,sampling_frequency,bands,method_,avg_type_):
    """
    Test the 'bands_power' function with different method and averaging type combinations.

    Args:
        eeg_data: The EEG data for testing.
        sampling_frequency: The sampling frequency of the EEG data.
        bands: The frequency bands of interest.
        method_ (str): The method used for spectral estimation.
        avg_type_ (str): The type of averaging to apply.

    Returns:
        None

    Raises:
        AssertionError: If the returned bands_power array is complex, has an unexpected dimension,
        or doesn't have the expected shape.

    Example:
        >>> import numpy as np
        >>> from custom_module import test_bands_power
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> fs = 1000  # Sampling frequency
        >>> bands = [(8, 12), (13, 30)]  # Frequency bands of interest
        >>> test_bands_power(eeg_data, fs, bands, "welch", "mean")
    """
    bands_power_ = bands_power(eeg_data,sampling_frequency,bands,method_,avg_type_)
    assert np.iscomplexobj(bands_power_) is False
    assert bands_power_.ndim<=2 & bands_power_.ndim!=0
    assert bands_power_.shape[-1]==len(bands)
    if bands_power_.ndim==2:
        assert bands_power_.shape[0]==eeg_data.shape[0]

def test_compute_psd(eeg_data,sampling_frequency):
    """
    Test the 'compute_psd' function.

    Args:
        eeg_data: The EEG data for testing.
        sampling_frequency: The sampling frequency of the EEG data.

    Returns:
        None

    Raises:
        AssertionError: If the returned spectrum array doesn't have the expected dimension
        or if the shape of the spectrum and frequency arrays doesn't match.

    Example:
        >>> import numpy as np
        >>> from custom_module import test_compute_psd
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> fs = 1000  # Sampling frequency
        >>> test_compute_psd(eeg_data, fs)
    """
    spectrum, freqs = compute_psd(eeg_data,sampling_frequency)
    assert spectrum.ndim==eeg_data.ndim
    assert spectrum.shape[-1]==freqs.shape[0]

@pytest.fixture
def hjorth_segment_size():
    return 10

def test_hjorth_method(eeg_data,hjorth_segment_size):
    """
    Test the 'hjorth_parameters_computation' function.

    Args:
        eeg_data: The EEG data for testing.
        hjorth_segment_size: The segment size for computing Hjorth parameters.

    Returns:
        None

    Raises:
        AssertionError: If the returned hjorth_results object is not a dictionary,
        if it doesn't have the expected length, or if any of its values are NaN or infinity.

    Example:
        >>> import numpy as np
        >>> from custom_module import test_hjorth_method
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> seg_size = 100  # Segment size for Hjorth parameters
        >>> test_hjorth_method(eeg_data, seg_size)
    """
    hjorth_results = hjorth_parameters_computation(eeg_data,hjorth_segment_size)
    assert isinstance(hjorth_results,dict)
    assert len(hjorth_results) == 6
    for hjorth_result in hjorth_results:
        assert np.isnan(hjorth_result) == 0
        assert np.isinf(hjorth_result) == 0

def test_hjorth_2D(eeg_data,hjorth_segment_size,openBCI_16channels):
    """
    Test the 'hjorth_parameters_computation' function.

    Args:
        eeg_data: The EEG data for testing.
        hjorth_segment_size: The segment size for computing Hjorth parameters.

    Returns:
        None

    Raises:
        AssertionError: If the returned hjorth_results object is not a dictionary,
        if it doesn't have the expected length, or if any of its values are NaN or infinity.

    Example:
        >>> import numpy as np
        >>> from custom_module import test_hjorth_method
        >>> eeg_data = np.random.randn(1000)  # EEG data
        >>> seg_size = 100  # Segment size for Hjorth parameters
        >>> test_hjorth_method(eeg_data, seg_size)
    """
    assert len(openBCI_16channels) == eeg_data.shape[0]
    hjorth_df = hjorth_2D(eeg_data,hjorth_segment_size,openBCI_16channels)
    assert isinstance(hjorth_df,pd.DataFrame)
    # assert hjorth_df.isin([np.nan, np.inf, -np.inf]).sum().sum() == 0
