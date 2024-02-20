import mne
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import numpy as np
import copy
import seaborn as sns
from typing import *
import pandas as pd
from . import globals
import features_computation.frequency as frequency_features

colors = [(1, 1, 1), (1, 0, 0)]  # White to red


def suppress_extr_plot(func):
    def wrapper(*args, **kwargs):
        plt.close('all')
        # fig = plt.figure()
        return func(*args,**kwargs)
        plt.close('all')
    return wrapper

@suppress_extr_plot
def plot_psd(raw,wargs):
    return raw.plot_psd(**wargs)

@suppress_extr_plot
def plot(raw,wargs):
    return raw.plot(**wargs)

@suppress_extr_plot
def plot_psd_topmap(raw,wargs):
    return raw.plot_psd_topomap(**wargs)

@suppress_extr_plot
def plot_psds(data:List[np.ndarray],fmin_:int,fmax_:int,dB_=True,figsize_=None,recording_names:List[str]=None,dBlimit:Union[Tuple[float],List[float]]=(-50.0,50.0)):

    figures = list()
    
    for r in range(len(data)):
        if figsize_!=None:
            fig_, ax_ = plt.subplots(1,1,figsize=figsize_)
        else:
            fig_, ax_ = plt.subplots(1,1,figsize=(8,5))
        spectrum_, freqs_ = frequency_features.compute_psd(
            data[r],
            125
        )
        for ch,ch_name in enumerate(globals.channel_names):
            if int(ch_name[-1])%2==0:
                ax_.plot(freqs_[(freqs_>fmin_) & (freqs_<fmax_)],spectrum_[ch][(freqs_>fmin_) & (freqs_<fmax_)],label=ch_name,color=globals.sensors_colors[ch_name][0])
            else:
                ax_.plot(freqs_[(freqs_>fmin_) & (freqs_<fmax_)],spectrum_[ch][(freqs_>fmin_) & (freqs_<fmax_)],label=ch_name,color=globals.sensors_colors[ch_name][0],linestyle='--')
            ax_.spines['top'].set_visible(False)
            ax_.spines['right'].set_visible(False)
            ax_.spines['bottom'].set_visible(False)
            ax_.spines['left'].set_visible(False)
            ax_.set_ylim(ymin=dBlimit[0], ymax=dBlimit[1])  # Adjust according to your data
            ax_.legend()
            fig_.suptitle(recording_names[r])
        figures.append(fig_)

    return figures
        

@suppress_extr_plot
def head_plot(data:Union[list,np.ndarray],pos:Union[list,np.ndarray],colorbar_orientation:str='vertical',axes_:matplotlib.axes=None,recording_name:str=None)-> None:

    min_val = np.min(data)
    max_val = np.max(data)
    norm = Normalize(vmin=min_val, vmax=max_val)
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', globals.white_to_red_color, N=256)

    if axes_==None:
        pt = mne.viz.plot_topomap(data,pos,show=False,cmap=new_cmap,cnorm=norm)
        if recording_name!=None:
            plt.title(recording_name)
    else:
        pt = mne.viz.plot_topomap(data,pos,axes=axes_,show=False,cmap=new_cmap,cnorm=norm)
        if recording_name!=None:
            axes_.set_title(recording_name)
        
    plt.colorbar(pt[0],orientation = colorbar_orientation,use_gridspec=True,label=r'$uV^2 /Hz (dB)$')

@suppress_extr_plot
def head_plots(data:Union[List[np.ndarray],np.ndarray],pos:Union[list,np.ndarray],no_rows:int,no_columns:int,colorbar_orientation:str='vertical',axis:int=1,figsize_:Tuple[int,int]=None,recording_names:List[str]=None,band_names:List[str]=None)->plt.figure:

    assert data.ndim==2 or data.ndim==3
    assert len(band_names)==no_columns
    assert len(recording_names)==no_rows

    figures = list()
    data_ = copy.deepcopy(data)

    min_val = np.min(data_)
    max_val = np.max(data_)
    norm = Normalize(vmin=min_val, vmax=max_val)
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', globals.white_to_red_color, N=256)

    if data_.ndim==2:
        if axis==1: 
            data_ = np.moveaxis(data_,range(data_.ndim),[1,0])
        assert data_.shape[0]==(no_rows*no_columns)
    elif data_.ndim==3:
        if axis==1:
            data_ = np.moveaxis(data_,range(data_.ndim),[1,0,2])
        elif axis==2:
            data_ = np.moveaxis(data_,range(data_.ndim),[2,0,1])
        print(data_.shape)
        assert data_.shape[0]==no_rows and data_.shape[1]==no_columns

    for r in range(no_rows):
        if figsize_!=None:
            fig_, ax_ = plt.subplots(1,no_columns,figsize=figsize_)
        else:
            fig_, ax_ = plt.subplots(1,no_columns,figsize=(no_columns*2,2))
        for c in range(no_columns):
            b = (r*no_columns)+c
            if data_.ndim==2:
                pt = mne.viz.plot_topomap(data_[b,:],pos,axes=ax_.flatten()[c],show=False,cmap=new_cmap,cnorm=norm)
            elif data_.ndim==3:
                pt = mne.viz.plot_topomap(data_[r,c,:],pos,axes=ax_.flatten()[c],show=False,cmap=new_cmap,cnorm=norm)
            plt.colorbar(pt[0],orientation = colorbar_orientation,use_gridspec=True,label=r'$uV^2 /Hz (dB)$')
            if band_names!=None:
                ax_.flatten()[c].set_title('({})'.format(band_names[c]))
            # if c==0 and recording_names!=None:
            #     ax_.flatten()[b].set_title(recording_names[r])
        fig_.suptitle(recording_names[r])
        fig_.tight_layout()
        figures.append(fig_)

    return figures

@suppress_extr_plot
def covariance_plot(data:np.ndarray,ch_names:List[str],axes:matplotlib.axes=None,method:str='cov',record_name:str=None,vmin:float=None,vmax:float=None):

    assert len(ch_names) == data.shape[0]

    # r2b_colors = [(1, 0, 0), (0, 0, 1)]  # Red To Blue
    # new_cmap = LinearSegmentedColormap.from_list('red_to_blue', r2b_colors, N=256)
    new_cmap = 'RdBu'

    if method=='cov':
        cov_corr = np.cov(data)
        # global colors
        # new_cmap = LinearSegmentedColormap.from_list('white_to_red', colors, N=256)
    elif method=='corr':
        cov_corr = np.corrcoef(data)
        vmin = -1
        vmax = 1
        # new_cmap = 'RdBu'

    if axes==None:
        fig = plt.figure()
        plot = sns.heatmap(cov_corr,cmap=new_cmap,vmin=vmin,vmax=vmax)
        plt.xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        plt.yticks(list(range(data.shape[0])),ch_names,fontsize=7)
    else:
        sns.heatmap(cov_corr,cmap=new_cmap,ax=axes,vmin=vmin,vmax=vmax)
        axes.set_xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        axes.set_yticks(list(range(data.shape[0])),ch_names,fontsize=7)
        if record_name!=None:
            axes.set_title(record_name)

    if axes==None:
        return fig
    else:
        return
    
@suppress_extr_plot
def covariance_plots(data:List[np.array],ch_names:List[str],no_rows:int,no_cols:int=1,method:str='cov',recording_names:List[str]=None)->plt.figure:

    assert no_rows==len(recording_names)
    figures = list()

    min_val = np.min(np.array([np.cov(data_) for data_ in data]))
    max_val = np.max(np.array([np.cov(data_) for data_ in data]))

    for r in range(no_rows):
        fig, ax = plt.subplots(1,1,figsize=(10,4))
        if recording_names==None:
            covariance_plot(data[r],ch_names,axes=ax,method=method,vmin=min_val,vmax=max_val)
        else:
            covariance_plot(data[r],ch_names,axes=ax,method=method,record_name=recording_names[r],vmin=min_val,vmax=max_val)
        figures.append(fig)
    return figures

@suppress_extr_plot
def hjorth_plot(hjorth_values,recording_names=None):

    all_values = list()

    for values in hjorth_values:
        all_values += values.values.flatten().tolist()

    min_val = min(all_values)
    max_val = max(all_values)
    norm = Normalize(vmin=min_val, vmax=max_val)
    global colors
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', colors, N=256)

    if isinstance(hjorth_values,list):

        no_rows = len(hjorth_values)

        figures = list()
        
        for r in range(no_rows):
            fig, ax_ = plt.subplots(1,2,figsize=(14,6))
            h = hjorth_values[r]
            sns.heatmap(h[['mean_activity','mean_mobility','mean_complexity']].T,ax=ax_[0],cmap=new_cmap)
            sns.heatmap(h[['std_activity','std_mobility','std_complexity']].T,ax=ax_[1],cmap=new_cmap)
            if recording_names!=None:
                fig.suptitle(recording_names[r])
            fig.tight_layout()
            figures.append(fig)
    else:
        fig, ax_ = plt.subplots(1,2,figsize=(14,6))
        h = hjorth_values[0]
        sns.heatmap(h.iloc[:][0:3].T,ax=ax_[0],cmap=new_cmap)
        sns.heatmap(h.iloc[:][3:].T,ax=ax_[1],cmap=new_cmap)
        fig.suptitle(recording_names[0])
        fig.tight_layout()
        figures.append(fig)
        
    return figures