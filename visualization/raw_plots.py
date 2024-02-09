import mne
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import numpy as np
import copy
import seaborn as sns

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
def plot_psds(raws:list,no_rows:int,no_columns:int,fmin_:int,fmax_:int,dB_=True,figsize_=None):

    assert len(raws)==(no_rows*no_columns)
    
    if figsize_!=None:
        fig_, ax_ = plt.subplots(no_rows,no_columns,figsize=figsize_)
    else:
        fig_, ax_ = plt.subplots(no_rows,no_columns)
    
    for r in range(no_rows):
        for c in range(no_columns):
            b = (r*no_columns)+c
            pt = raws[b].plot_psd(fmin_,fmax_,dB_,ax=ax_.flatten()[b])
    
    fig_.tight_layout()

    return fig_
        

@suppress_extr_plot
def head_plot(data,pos,colorbar_orientation='vertical',axes_=None):

    min_val = np.min(data)
    max_val = np.max(data)
    norm = Normalize(vmin=min_val, vmax=max_val)
    colors = [new_cmap(norm(value)) for value in data.flatten()]

    if axes_==None:
        pt = mne.viz.plot_topomap(data,pos,show=False,cmap=new_cmap,cnorm=norm)
    else:
        pt = mne.viz.plot_topomap(data,pos,axes=axes_,show=False,cmap=new_cmap,cnorm=norm)
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
def covarince_plot(data,ch_names):

    assert len(ch_names) == data.shap[0]
    covariance = np.cov(data,axis=1)
    fig = plt.figure()
    sns.heatmap(covariance,cmap="YlGnBu")
    plt.xticks(list(range(data.shape[0])),ch_names,fontsize=7)
    plt.yticks(list(range(data.shape[0])),ch_names,fontsize=7)

    return fig