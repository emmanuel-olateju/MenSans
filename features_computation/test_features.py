from .frequency import *
from .time import *
import pytest

@pytest.fixture
def hjorth_segment_size():
    return 10

@pytest.mark.parametrize("method_, avg_type_", [("welch","mean"),("welch","median"),("medfilt","mean"),("medfilt","median")])
def test_band_power_method(eeg_data,sampling_frequency,bands,method_,avg_type_):
    spectrum = band_power(eeg_data,sampling_frequency,bands[1],method_,avg_type_)
    assert np.iscomplexobj(spectrum) == False
    assert spectrum.ndim == 1

def test_hjorth_method(eeg_data,hjorth_segment_size):
    hjorth_results = hjorth_parameters_computation(eeg_data,hjorth_segment_size)
    assert isinstance(hjorth_results,dict)
    assert len(hjorth_results) == 6
    for k in hjorth_results.keys():
        assert np.isnan(hjorth_results[k]) == 0
        assert np.isinf(hjorth_results[k]) == 0

def test_hjorth_2D(eeg_data,hjorth_segment_size,openBCI_16channels):
    assert len(openBCI_16channels) == eeg_data.shape[0]
    hjorth_df = hjorth_2D(eeg_data,hjorth_segment_size,openBCI_16channels)
    assert isinstance(hjorth_df,pd.DataFrame)
    # assert hjorth_df.isin([np.nan, np.inf, -np.inf]).sum().sum() == 0