import numpy as np
import neurodsp.spectral as spectral
from typing import *

def band_power(sig:np.array,fs:int,band:List[float],method:str='welch',avg_type:str='mean')->np.array:

    freqs, spectrum = spectral.compute_spectrum(sig,fs,method,avg_type)
    assert (spectrum.ndim!=0) and (spectrum.ndim<=2)
    if spectrum.ndim==2:
        _band_power = np.empty((spectrum.shape[0]))
        for ch in range(spectrum.shape[0]):
            _band_power[ch] = spectrum[ch,((freqs>=band[0]) & (freqs<=band[1]))].mean()
    else:
        _band_power = spectrum[((freqs>=band[0]) & (freqs<=band[1]))].mean()

    return np.log10(_band_power)

def bands_power(sig:np.array,fs:int,bands:List[Tuple[float]],method:str='welch',avg_type:str='mean')->np.array:

    assert sig.ndim!=0 & sig.ndim<=2
    
    if sig.ndim==2:
        _bands_power = np.empty((sig.shape[0],len(bands)))
        for b,band in enumerate(bands):
            _bands_power[:,b] = band_power(sig,fs,band,method,avg_type)
    else:
        _bands_power = np.empty((len(bands)))
        for b,band in enumerate(bands):
            _bands_power[b] = band_power(sig,fs,band,method,avg_type)
    
    return _bands_power