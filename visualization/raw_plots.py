import copy
from typing import List, Tuple, Union
import mne
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import numpy as np
import seaborn as sns
import features_computation.frequency as frequency_features
from . import plot_globals as viz_globals

def suppress_extr_plot(func):
    def wrapper(*args, **kwargs):
        plt.close('all')
        return func(*args,**kwargs)
        # plt.close('all')
    return wrapper

@suppress_extr_plot
def plot_psd_topmap(raw,wargs):
    return raw.plot_psd_topomap(**wargs)

@suppress_extr_plot
def plot_psds(data:List[np.ndarray],fmin_:int,fmax_:int,
              figsize_=None,recording_names:List[str]=None,
              db_limit:Union[Tuple[float],List[float]]=(-50.0,50.0))->plt.figure:

    figures = []
    for row,data_ in enumerate(data):
        if figsize_ is not None:
            fig_, ax_ = plt.subplots(1,1,figsize=figsize_)
        else:
            fig_, ax_ = plt.subplots(1,1,figsize=(8,5))
        spectrum_, freqs_ = frequency_features.compute_psd(
            data_,
            125
        )
        for channel,ch_name in enumerate(globals.channel_names):
            if int(ch_name[-1])%2==0:
                ax_.plot(freqs_[(freqs_>fmin_) & (freqs_<fmax_)],spectrum_[channel][(freqs_>fmin_) & 
                                                                               (freqs_<fmax_)],
                         label=ch_name,color=globals.sensors_colors[ch_name][0])
            else:
                ax_.plot(freqs_[(freqs_>fmin_) & (freqs_<fmax_)],spectrum_[channel][(freqs_>fmin_) & 
                                                                               (freqs_<fmax_)],
                         label=ch_name,color=globals.sensors_colors[ch_name][0],linestyle='--')
            ax_.spines['top'].set_visible(False)
            ax_.spines['right'].set_visible(False)
            ax_.spines['bottom'].set_visible(False)
            ax_.spines['left'].set_visible(False)
            ax_.set_ylim(ymin=db_limit[0], ymax=db_limit[1])  # Adjust according to your data
            ax_.legend()

            record_name = recording_names[row][:-3]
            if len(record_name)>15:
                fig_.suptitle(record_name[:15]+'\n'+record_name[15:])
            else:
                fig_.suptitle(record_name)
        figures.append(fig_)

    return figures

@suppress_extr_plot
def head_plots(data:Union[List[np.ndarray],np.ndarray],pos:Union[list,np.ndarray],
               no_rows:int,no_columns:int,colorbar_orientation:str='vertical',
               axis:int=1,figsize_:Tuple[int,int]=None,
               recording_names:List[str]=None,band_names:List[str]=None)->plt.figure:

    assert data.ndim in (2,3)
    assert len(band_names)==no_columns
    assert len(recording_names)==no_rows

    figures = []
    data_ = copy.deepcopy(data)

    min_val = np.min(data_)
    max_val = np.max(data_)
    norm = Normalize(vmin=min_val, vmax=max_val)
    new_cmap = LinearSegmentedColormap.from_list('white_to_red', viz_globals.white_to_red_color, N=256)

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

    for row in range(no_rows):
        if figsize_ is not None:
            fig_, ax_ = plt.subplots(1,no_columns,figsize=figsize_)
        else:
            fig_, ax_ = plt.subplots(1,no_columns,figsize=(no_columns*2,2))
        for column in range(no_columns):
            index_ = (row*no_columns)+column
            if data_.ndim==2:
                pt_ = mne.viz.plot_topomap(
                    data_[index_,:],pos,
                    axes=ax_.flatten()[column],show=False,
                    cmap=new_cmap,cnorm=norm
                    )
            elif data_.ndim==3:
                pt_ = mne.viz.plot_topomap(
                    data_[row,column,:],pos,
                    axes=ax_.flatten()[column],show=False,
                    cmap=new_cmap,cnorm=norm
                    )
            plt.colorbar(
                pt_[0],
                orientation = colorbar_orientation,
                use_gridspec=True,
                label=r'$uV^2 /Hz (dB)$'
                )
            if band_names is not None:
                ax_.flatten()[column].set_title(band_names[column])
        record_name = recording_names[row][:-3]
        if len(record_name)>15:
            fig_.suptitle(record_name[:15]+'\n'+record_name[15:])
        else:
            fig_.suptitle(record_name)
        fig_.tight_layout()
        figures.append(fig_)

    return figures

@suppress_extr_plot
def covariance_plot(
    data:np.ndarray,ch_names:List[str],
    axes:matplotlib.axes=None,method:str='cov',
    record_name:str=None,
    vmin:float=None,vmax:float=None):

    assert len(ch_names) == data.shape[0]

    new_cmap = 'RdBu'

    if method=='cov':
        cov_corr = np.cov(data)
    elif method=='corr':
        cov_corr = np.corrcoef(data)
        vmin = -1
        vmax = 1
        # new_cmap = 'RdBu'

    if axes is None:
        fig = plt.figure()
        sns.heatmap(cov_corr,cmap=new_cmap,vmin=vmin,vmax=vmax)
        plt.xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        plt.yticks(list(range(data.shape[0])),ch_names,fontsize=7)
        return fig
    else:
        sns.heatmap(cov_corr,cmap=new_cmap,ax=axes,vmin=vmin,vmax=vmax)
        axes.set_xticks(list(range(data.shape[0])),ch_names,fontsize=7)
        axes.set_yticks(list(range(data.shape[0])),ch_names,fontsize=7)
        if record_name is not None:
            record_name = record_name[:-3]
            if len(record_name)>15:
                axes.set_title(record_name[:15]+'\n'+record_name[15:])
            else:
                axes.set_title(record_name)
        return

@suppress_extr_plot
def covariance_plots(
    data:List[np.array],ch_names:List[str],
    no_rows:int,method:str='cov',
    recording_names:List[str]=None)->plt.figure:

    assert no_rows==len(recording_names)
    figures = []

    min_val = np.min(np.array([np.cov(data_) for data_ in data]))
    max_val = np.max(np.array([np.cov(data_) for data_ in data]))

    for row in range(no_rows):
        fig, ax_ = plt.subplots(1,1,figsize=(10,4))
        if recording_names is None:
            covariance_plot(data[row],ch_names,axes=ax_,method=method,vmin=min_val,vmax=max_val)
        else:
            covariance_plot(
                data[row],ch_names,axes=ax_,
                method=method,record_name=recording_names[row],
                vmin=min_val,vmax=max_val
                )
        figures.append(fig)
    return figures

@suppress_extr_plot
def hjorth_plot(hjorth_values,recording_names=None):

    all_values = []

    for values in hjorth_values:
        all_values += values.values.flatten().tolist()

    new_cmap = LinearSegmentedColormap.from_list('white_to_red', viz_globals.white_to_red_color, N=256)

    if isinstance(hjorth_values,list):

        no_rows = len(hjorth_values)

        figures = []
        for row in range(no_rows):
            fig, ax_ = plt.subplots(1,2,figsize=(14,6))
            hjorth_ = hjorth_values[row]
            sns.heatmap(
                hjorth_[['mean_activity','mean_mobility','mean_complexity']].T,
                ax=ax_[0],cmap=new_cmap
                )
            sns.heatmap(
                hjorth_[['std_activity','std_mobility','std_complexity']].T,
                ax=ax_[1],cmap=new_cmap
                )
            if recording_names is not None:
                fig.suptitle(recording_names[row])
            fig.tight_layout()
            figures.append(fig)
    else:
        fig, ax_ = plt.subplots(1,2,figsize=(14,6))
        hjorth_ = hjorth_values[0]
        sns.heatmap(hjorth_.iloc[:][0:3].T,ax=ax_[0],cmap=new_cmap)
        sns.heatmap(hjorth_.iloc[:][3:].T,ax=ax_[1],cmap=new_cmap)
        fig.suptitle(recording_names[0])
        fig.tight_layout()
        figures.append(fig)
    return figures
