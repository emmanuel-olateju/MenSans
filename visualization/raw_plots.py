import mne
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import numpy as np
import copy
import seaborn as sns
from typing import *

colors = [(1, 1, 1), (1, 0, 0)]  # White to red
new_cmap = LinearSegmentedColormap.from_list('white_to_red', colors, N=256)


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
def plot_psds(raws:list,no_rows:int,no_columns:int,fmin_:int,fmax_:int,dB_=True,figsize_=None,recording_names:List[str]=None,dBlimit:int=50):

    assert len(raws)==(no_rows*no_columns)
    
    if figsize_!=None:
        fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=figsize_)
    else:
        fig_, ax_ = plt.subplots(no_rows,no_columns)
    
    for r in range(no_rows):
        for c in range(no_columns):
            b = (r*no_columns)+c
            pt = raws[b].plot_psd(fmin_,fmax_,dB_,ax=ax_.flatten()[b])
            if recording_names!=None:
                ax_.flatten()[b].set_title(recording_names[b])
                ax_.flatten()[b].set_ylim((-1)*dBlimit,dBlimit)
    
    fig_.tight_layout()

    return fig_
        

@suppress_extr_plot
def head_plot(data,pos,colorbar_orientation='vertical',axes_=None,recording_name:str=None):

    min_val = np.min(data)
    max_val = np.max(data)
    norm = Normalize(vmin=min_val, vmax=max_val)
    colors = [new_cmap(norm(value)) for value in data.flatten()]

    if axes_==None:
        pt = mne.viz.plot_topomap(data,pos,show=False,cmap=new_cmap,cnorm=norm)
        if recording_name!=None:
            plt.title(recording_name)
    else:
        pt = mne.viz.plot_topomap(data,pos,axes=axes_,show=False,cmap=new_cmap,cnorm=norm)
        if recording_name!=None:
            axes_.set_title(recording_name)
        
    plt.colorbar(pt[0],orientation = colorbar_orientation,use_gridspec=True,label=r'$uV^2 /Hz (dB)$')
    
    return

@suppress_extr_plot
def head_plots(data,pos,no_rows,no_columns,colorbar_orientation='vertical',axis=1,figsize_=None):

    assert data.ndim==2 or data.ndim==3

    data_ = copy.deepcopy(data)

    min_val = np.min(data_)
    max_val = np.max(data_)
    norm = Normalize(vmin=min_val, vmax=max_val)
    colors = [new_cmap(norm(value)) for value in data_.flatten()]

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

    if figsize_!=None:
        fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=figsize_)
    else:
        fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=(no_columns*2,no_rows*2))

    for r in range(no_rows):
        for c in range(no_columns):
            b = (r*no_columns)+c
            if data_.ndim==2:
                pt = mne.viz.plot_topomap(data_[b,:],pos,axes=ax_.flatten()[b],show=False,cmap=new_cmap,cnorm=norm)
            elif data_.ndim==3:
                pt = mne.viz.plot_topomap(data_[r,c,:],pos,axes=ax_.flatten()[b],show=False,cmap=new_cmap,cnorm=norm)
            plt.colorbar(pt[0],orientation = colorbar_orientation,use_gridspec=True,label=r'$uV^2 /Hz (dB)$')
    
    fig_.tight_layout()

    return fig_

@suppress_extr_plot
def covariance_plot(data,ch_names,axes=None,method='cov'):

    assert len(ch_names) == data.shape[0]

    if method=='cov':
        cov_corr = np.cov(data)
        global new_cmap
    elif method=='corr':
        cov_corr = np.corrcoef(data)
        new_cmap = 'RdBu'

    if axes==None:
        fig = plt.figure()
        plot = sns.heatmap(cov_corr,cmap=new_cmap)
        plt.xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        plt.yticks(list(range(data.shape[0])),ch_names,fontsize=7)
    else:
        sns.heatmap(cov_corr,cmap=new_cmap,ax=axes)
        axes.set_xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        axes.set_yticks(list(range(data.shape[0])),ch_names,fontsize=7)

    if axes==None:
        return fig
    else:
        return
    
@suppress_extr_plot
def covariance_plots(data:List[np.array],ch_names:List[str],no_rows:int,no_cols:int,method:str='cov')->plt.figure:

    fig, ax = plt.subplots(no_rows,no_cols,figsize=(no_cols*10,no_rows*4))

    for r in range(no_rows):
        for c in range(no_cols):
            b = (r*no_cols)+c
            covariance_plot(data[b],ch_names,axes=ax.flatten()[b],method=method)
    
    return fig