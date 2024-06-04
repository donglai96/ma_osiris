import matplotlib.colors as colors
import matplotlib.cbook as cbook
from matplotlib import cm
import numpy as np
import copy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

def inter_from_256(x):
    return np.interp(x=x,xp=[0,255],fp=[0,1])

def xinmap():
    cdict = {
        'red':((0.0,inter_from_256(253),inter_from_256(253)),
               (1/8*1,inter_from_256(255),inter_from_256(255)),
               (1/8*2,inter_from_256(220),inter_from_256(220)),
               (1/8*3,inter_from_256(157),inter_from_256(157)),
               (1/8*4,inter_from_256(129),inter_from_256(129)),
               (1/8*5,inter_from_256(100),inter_from_256(100)),
               (1/8*6,inter_from_256(135),inter_from_256(135)),
               (1/8*7,inter_from_256(253),inter_from_256(253)),
               (1.0,inter_from_256(253),inter_from_256(253))),
               
        'green': ((0.0,inter_from_256(252),inter_from_256(252)),
                  (1/8*1,inter_from_256(218),inter_from_256(218)),
                  (1/8*2,inter_from_256(189),inter_from_256(189)),
                  (1/8*3,inter_from_256(183),inter_from_256(183)),
                  (1/8*4,inter_from_256(242),inter_from_256(242)),
                  (1/8*5,inter_from_256(255),inter_from_256(255)),
                  (1/8*6,inter_from_256(255),inter_from_256(255)),
                  (1/8*7,inter_from_256(226),inter_from_256(226)),
                  (1.0,inter_from_256(34),inter_from_256(34))),
        
        'blue':((0.0,inter_from_256(250),inter_from_256(250)),
                (1/8*1,inter_from_256(249),inter_from_256(249)),
                (1/8*2,inter_from_256(255),inter_from_256(255)),
                (1/8*3,inter_from_256(255),inter_from_256(255)),
                (1/8*4,inter_from_256(254),inter_from_256(254)),
                (1/8*5,inter_from_256(158),inter_from_256(158)),
                (1/8*6,inter_from_256(69),inter_from_256(69)),

               (1/8*7,inter_from_256(33),inter_from_256(33)),
               (1.0,inter_from_256(0),inter_from_256(0))),
    }
    xin_cmap = colors.LinearSegmentedColormap('xin_cmap',segmentdata=cdict)
    return xin_cmap


def plot_phasespace(ax, data, xdata, ydata, xlabel, ylabel, title):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plot2d = ax.imshow(np.log(np.abs(data[:,:])), cmap = 'jet', origin = 'lower',
              aspect='auto',
              extent=[xdata[0], xdata[-1], ydata[0], ydata[-1]])
    return plot2d
    