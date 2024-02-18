from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_subplots(n_rows,n_cols):
    fig = make_subplots(rows=n_rows, cols=n_cols)
    return fig

def plot_psd(psd,freqs,row_,col_,fig_,name_):
    # assert len(psd)==len(freqs)
    # print(psd.shape,freqs.shape)
    fig_.add_trace(go.Scatter(x=freqs,y=psd,name=name_),row=row_,col=col_)

def find_trace_index(fig_, name_):
    """Find the index of the trace with the specified name."""
    for i, trace in enumerate(fig_.data):
        if trace.name == name_:
            return i
    return None

def unplot_psd_by_name(name_, fig_):
    """Unplot a PSD from the figure with the specified name."""
    trace_index = find_trace_index(fig_, name_)
    if trace_index is not None:
        fig_.delete_trace(trace_index)
        fig_.update_layout(height=fig_.layout.height, width=fig_.layout.width)