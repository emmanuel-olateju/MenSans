import Montage
import matplotlib.pyplot as plt


def suppress_extr_plot(func):
    def wrapper(*args, **kwargs):
        plt.close()
        fig = plt.figure()
        return func(*args,**kwargs)
        plt.close(fig)
    return wrapper

@suppress_extr_plot
def plot_psd(raw,wargs):
    raw.plot_psd(**wargs)

@suppress_extr_plot
def plot(raw,wargs):
    raw.plot(**wargs)