"""
Plotting Utilities Module

This module provides utility functions for creating and manipulating Plotly subplots and traces.

Functions:
    - create_subplots: Create a subplot grid.
    - plot_psd: Plot Power Spectral Density (PSD) on a subplot.
    - find_trace_index: Find the index of a trace in a Plotly figure.
    - unplot_psd_by_name: Remove a PSD trace from a Plotly figure by its name.

"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from . import plot_globals

def create_subplots(n_rows,n_cols):
    """
    Create a subplot grid.

    Args:
        n_rows (int): Number of rows in the grid.
        n_cols (int): Number of columns in the grid.

    Returns:
        plotly.subplots.Subplot: Plotly subplot grid.
    """
    fig = make_subplots(rows=n_rows, cols=n_cols)
    return fig

def plot_psd(psd,freqs,row_,col_,fig_,name_,db_limit=None,freqs_limit=None,figsize_=(550,60)):
    """
    Plot Power Spectral Density (PSD) on a subplot.

    Args:
        psd (array-like): Power spectral density values.
        freqs (array-like): Frequency values corresponding to the PSD.
        row_ (int): Row index of the subplot.
        col_ (int): Column index of the subplot.
        fig_ (plotly.subplots.Subplot): Plotly subplot to plot on.
        name_ (str): Name of the trace.
        db_limit (tuple, optional): Limits for the y-axis (in dB). Default is None.
        freqs_limit (tuple, optional): Limits for the x-axis (in Hz). Default is None.

    Returns:
        None
    """


    if int(name_[-1])%2==0:
        fig_.add_trace(
            go.Scatter(
                x=freqs,y=psd,
                name=name_,
                line={'color': plot_globals.sensors_colors[name_][0]}
                ),
            row=row_,col=col_,
            )
    else:
        fig_.add_trace(
            go.Scatter(
                x=freqs,y=psd,
                name=name_,
                line={'color': plot_globals.sensors_colors[name_][0], 'dash': 'dash'}
                ),
            row=row_,col=col_,
            )
    fig_.update_xaxes(range=[freqs_limit[0], freqs_limit[1]])  # Set the range for the x-axis
    if db_limit is not None:
        fig_.update_yaxes(range=[db_limit[0], db_limit[1]])
    fig_.update_layout(width=figsize_[0])

def find_trace_index(fig_, name_):
    """
    Find the index of the trace with the specified name.

    Args:
        fig_ (plotly.subplots.Subplot): Plotly subplot containing traces.
        name_ (str): Name of the trace to find.

    Returns:
        int or None: Index of the trace if found, else None.
    """
    for i, trace in enumerate(fig_.data):
        if trace.name == name_:
            return i
    return None

def unplot_psd_by_name(name_, fig_):
    """
    Remove a PSD trace from a Plotly figure by its name.

    Args:
        name_ (str): Name of the trace to remove.
        fig_ (plotly.subplots.Subplot): Plotly subplot containing the trace.

    Returns:
        None
    """
    trace_index = find_trace_index(fig_, name_)
    if trace_index is not None:
        fig_.delete_trace(trace_index)
        fig_.update_layout(height=fig_.layout.height, width=fig_.layout.width)
