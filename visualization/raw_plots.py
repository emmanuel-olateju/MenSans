import mne
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import numpy as np
import copy
import seaborn as sns
from typing import *
import pandas as pd

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
def plot_psds(raws:list,no_rows:int,no_columns:int,fmin_:int,fmax_:int,dB_=True,figsize_=None,recording_names:List[str]=None,dBlimit:Union[Tuple[float],List[float]]=(-50.0,50.0)):

    assert no_columns==1
    assert len(raws)==(no_rows)
    figures = list()
    
    
    if no_rows>1:
        for r in range(no_rows):
            if figsize_!=None:
                fig_, ax_ = plt.subplots(1,1,figsize=figsize_)
            else:
                fig_, ax_ = plt.subplots(1,1,figsize=(8,2))
            for c in range(no_columns):   
                pt = raws[r].plot_psd(fmin_,fmax_,dB_,ax=ax_)
                if recording_names!=None:
                    ax_.set_title(recording_names[r],fontsize=10)
                    ax_.set_ylim(dBlimit[0],dBlimit[1])
            figures.append(pt)
    else:
        if figsize_!=None:
            fig_, ax_ = plt.subplots(1,1,figsize=figsize_)
        else:
            fig_, ax_ = plt.subplots(1,1,figsize=(8,2))
        pt = raws[0].plot_psd(fmin_,fmax_,dB_,ax=ax_)
        if recording_names!=None:
            ax_.set_title(recording_names[0],fontsize=10)
            ax_.set_ylim(dBlimit[0],dBlimit[1])
        figures.append(pt)
    return figures
        

@suppress_extr_plot
def head_plot(data,pos,colorbar_orientation='vertical',axes_=None,recording_name:str=None):

    min_val = np.min(data)
    max_val = np.max(data)
    norm = Normalize(vmin=min_val, vmax=max_val)
    global colors
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', colors, N=256)

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
def head_plots(data,pos,no_rows,no_columns,colorbar_orientation='vertical',axis=1,figsize_=None,recording_names=None,band_names=None):

    assert data.ndim==2 or data.ndim==3
    assert len(band_names)==no_columns
    assert len(recording_names)==no_rows

    figures = list()
    data_ = copy.deepcopy(data)

    min_val = np.min(data_)
    max_val = np.max(data_)
    norm = Normalize(vmin=min_val, vmax=max_val)
    global colors
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', colors, N=256)

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

    # if figsize_!=None:
    #     fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=figsize_)
    # else:
    #     fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=(no_columns*2,no_rows*2))

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
def covariance_plot(data,ch_names,axes=None,method='cov',record_name=None,vmin=None,vmax=None):

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