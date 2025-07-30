##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

"""
A collection of functions for plotting with matplotlib. 
"""

#from jax import numpy as np
#import numpy as onp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from contextlib import contextmanager

from . import init

# Definition of colours
data_color = "xkcd:gold"
fit_color  = "xkcd:azure"
sig_color  = "xkcd:coral"
bck_color  = "xkcd:teal"
diff_color = "xkcd:red"

@contextmanager
def plot(name, prefix, figsize = (3.5, 2.7)) : 
  """
  Auxiliary function to simplify matplotlib plotting
  (using "with" statement). Opens the subplot and 
  after yielding saves the figs to .pdf and .png files
  """
  fig, ax = plt.subplots(figsize = figsize )
  fig.subplots_adjust(bottom=0.18, left = 0.18, right = 0.9, top = 0.9)
  yield fig, ax
  if prefix : 
    fig.savefig(prefix + name + ".pdf")
    fig.savefig(prefix + name + ".png")

def set_lhcb_style(grid = True, size = 10, usetex = False) : 
  """
    Set matplotlib plotting style close to "official" LHCb style
    (serif fonts, tick sizes and location, etc.)
  """
  plt.rc('font', family='serif', size=size)
  plt.rc('text', usetex = usetex)
  plt.rcParams['figure.max_open_warning']=40
  plt.rcParams['axes.linewidth']=1.3
  plt.rcParams['axes.grid']=grid
  plt.rcParams['grid.alpha']=0.3
  plt.rcParams["axes.axisbelow"] = False
  plt.rcParams['xtick.major.width']=1
  plt.rcParams['ytick.major.width']=1
  plt.rcParams['xtick.minor.width']=1
  plt.rcParams['ytick.minor.width']=1
  plt.rcParams['xtick.major.size']=6
  plt.rcParams['ytick.major.size']=6
  plt.rcParams['xtick.minor.size']=3
  plt.rcParams['ytick.minor.size']=3
  plt.rcParams['xtick.direction']="in"
  plt.rcParams['ytick.direction']="in"
  plt.rcParams['xtick.minor.visible']=True
  plt.rcParams['ytick.minor.visible']=True
  plt.rcParams['xtick.bottom']=True
  plt.rcParams['xtick.top']=True
  plt.rcParams['ytick.left']=True
  plt.rcParams['ytick.right']=True

def label_title(title, units = None) : 
  label = title
  if units : title += " (" + units + ")"
  return title

def y_label_title(range, bins, units=None):
    binw = (range[1] - range[0]) / bins
    if units == None:
        title = f"Entries/{binw}"
    else:
        title = f"Entries/({binw:g} {units})"
    return title

def plot_hist2d(hist, fig, ax, labels, cmap = "YlOrBr", log = False, symmetric = False, ztitle = None, title = None, units = (None, None)) : 
  """
    Plot 2D histogram in numpy histogram2d format, 
    including colorbox. 
      hist   : histogram to be plotted
      fig    : matplotlib figure object
      ax     : matplotlib axis object
      labels : Axis label titles (2-element list)
      cmap   : matplotlib colormap
      log    : if True, use log z scale
      symmetric : if True, use symmetric z axis limits from -max to +max
      ztitle : x axis title (default is "Entries")
      title : plot title
      units : 2-element list for x axis and y axis units
  """
  counts, xedges, yedges = hist
  aspect = (xedges[-1]-xedges[0])/(yedges[-1]-yedges[0])
  norm = None
  if symmetric : 
    vmax = np.max(np.abs(counts))
    norm = matplotlib.colors.Normalize(vmin=-vmax, vmax = vmax)
  if log : 
    vmax = np.max(counts)
    vmin = np.min(counts)
    if vmin <= 0. : vmin = 0.1
    if vmax <= vmin : vmax = vmin
    norm = matplotlib.colors.LogNorm(vmin = vmin, vmax = vmax)

  arr = counts.T

  X, Y = np.meshgrid(xedges, yedges)
  p = ax.pcolormesh(X, Y, arr, cmap = cmap, norm = norm, linewidth=0, rasterized=True)
  ax.set_xlabel(label_title(labels[0], units[0]), ha='right', x=1.0)
  ax.set_ylabel(label_title(labels[1], units[1]), ha='right', y=1.0)
  if title : ax.set_title(title)
  cb = fig.colorbar(p, pad = 0.01, ax = ax)
  zt = ztitle
  if not ztitle : zt = r"Entries"
  cb.ax.set_ylabel(zt, ha='right', y=1.0)
  if log : 
    cb.ax.set_yscale("log")

def plot_distr2d(arr, xindex, yindex, bins, ranges, fig, ax, labels, cmap = "YlOrBr", 
                 log = False, ztitle = None, title = None, units = (None, None), 
                 weights = None, colorbar = True) : 
  """
    Plot 2D distribution including colorbox.
      hist   : histogram to be plotted
      fig    : matplotlib figure object
      ax     : matplotlib axis object
      labels : Axis label titles (2-element list)
      cmap   : matplotlib colormap
      log    : if True, use log z scale
      ztitle : x axis title (default is "Entries")
      title : plot title
      units : 2-element list for x axis and y axis units
  """
  #print(xarr.shape, yarr.shape, bins)
  #print("hist2d start")
  counts = None
  xedges = None
  yedges = None
  for a,w in zip(arr, weights) : 
    c, xe, ye = np.histogram2d(a[:,xindex], a[:,yindex], bins = bins, range = ranges, weights = w)
    if counts is None : 
      counts = c
      xedges = xe
      yedges = ye
    else : 
      counts += c

  #print("hist2d end")
  norm = None
  if log : 
    vmax = np.max(counts)
    vmin = np.min(counts)
    if vmin <= 0. : vmin = 0.1
    if vmax <= vmin : vmax = vmin
    norm = matplotlib.colors.LogNorm(vmin = vmin, vmax = vmax)

  arr = counts.T

  X, Y = np.meshgrid(xedges, yedges)
  p = ax.pcolormesh(X, Y, arr, cmap = cmap, norm = norm, linewidth=0, rasterized=True)
  ax.set_xlabel(label_title(labels[0], units[0]), ha='right', x=1.0)
  ax.set_ylabel(label_title(labels[1], units[1]), ha='right', y=1.0)
  if title : ax.set_title(title)
  zt = ztitle
  if not ztitle : zt = r"Entries"
  if colorbar : 
    cb = fig.colorbar(p, pad = 0.01, ax = ax)
    cb.ax.set_ylabel(zt, ha='right', y=1.0)
    if log : 
      cb.ax.set_yscale("log")

def plot_distr1d(arr, index, bins, range, ax, label, log = False, units = None, weights = None, title = None, color = None, legend = None) : 
  """
    Plot 1D histogram and its fit result. 
      hist : histogram to be plotted
      func : fitting function in the same format as fitting.fit_hist1d
      pars : list of fitted parameter values (output of fitting.fit_hist2d)
      ax   : matplotlib axis object
      label : x axis label title
      units : Units for x axis
  """
  if isinstance(weights, tuple) : 
    xarr = None
    if log : ax.set_yscale("log")
    for i,ww in enumerate(weights) : 
      #hist, edges = onp.histogram(arr, bins = bins, range = range, weights = w)

      counts = None
      edges = None
      for a,w in zip(arr,ww) : 
        c, e = np.histogram(a[:,index], bins = bins, range = range, weights = w)
        if counts is None : 
          counts = c
          edges = e
        else : 
          counts += c

      if xarr is None : 
        left,right = edges[:-1],edges[1:]
        xarr = np.array([left,right]).T.flatten()
      dataarr = np.array([counts,counts]).T.flatten()
      if color : this_color = color[i]
      else : this_color = f"C{i}"
      if legend : lab = legend[i]
      else : lab = None
      ax.plot(xarr, dataarr, color = this_color, label = lab)
      ax.fill_between( xarr, dataarr, 0., color = this_color, alpha = 0.1)
  else : 
    if color : this_color = color
    else : this_color = data_color
    #hist, edges = onp.histogram(arr, bins = bins, range = range, weights = weights)

    counts = None
    edges = None
    for a,w in zip(arr, weights) : 
      c, e = np.histogram(a[:,index], bins = bins, range = range, weights = w)
      if counts is None : 
        counts = c
        edges = e
      else : 
        counts += c

    left,right = edges[:-1],edges[1:]
    xarr = np.array([left,right]).T.flatten()
    dataarr = np.array([counts,counts]).T.flatten()
    if log : ax.set_yscale("log")
    ax.plot(xarr, dataarr, color = this_color)
    ax.fill_between( xarr, dataarr, 0., color = this_color, alpha = 0.1)
  ax.set_ylim(bottom = 0.)
  ax.set_xlabel(label_title(label, units), ha='right', x=1.0)
  ax.set_ylabel(r"Entries", ha='right', y=1.0)
  if not title : 
    ax.set_title(label + r" distribution")
  else : 
    ax.set_title(title)
  if legend : ax.legend(loc = "best")

  #ax.hist( arr, bins = bins, range = range, color = data_color, histtype = "step", weights = weights )
  #ax.set_ylim(bottom = 0.)
  #ax.set_xlabel(label_title(label, units), ha='right', x=1.0)
  #ax.set_ylabel(r"Entries", ha='right', y=1.0)
  #ax.set_title(label + r" distribution")

def plot_hist1d(hist, ax, label, log = False, units = None, title = None, color = None, legend = None) : 
  """
    Plot 1D histogram and its fit result. 
      hist : histogram to be plotted
      func : fitting function in the same format as fitting.fit_hist1d
      pars : list of fitted parameter values (output of fitting.fit_hist2d)
      ax   : matplotlib axis object
      label : x axis label title
      units : Units for x axis
  """
  if color : this_color = color
  else : this_color = data_color

  counts, edges = hist

  left,right = edges[:-1],edges[1:]
  xarr = np.array([left,right]).T.flatten()
  dataarr = np.array([counts,counts]).T.flatten()
  if log : ax.set_yscale("log")
  ax.plot(xarr, dataarr, color = this_color)
  ax.fill_between( xarr, dataarr, 0., color = this_color, alpha = 0.1)
  ax.set_ylim(bottom = 0.)
  ax.set_xlabel(label_title(label, units), ha='right', x=1.0)
  ax.set_ylabel(r"Entries", ha='right', y=1.0)
  if not title : 
    ax.set_title(label + r" distribution")
  else : 
    ax.set_title(title)
  if legend : ax.legend(loc = "best")


def plot_distr1d_comparison(
    data,
    fit,
    bins,
    range,
    ax,
    label,
    log=False,
    units=None,
    weights=None,
    pull=False,
    cweights=None,
    title=None,
    legend=None,
    color=None,
    data_alpha=1.0,
    legend_ax=None,
    data_weights = None, 
):
    """
    Plot 1D histogram and its fit result.
      hist : histogram to be plotted
      func : fitting function in the same format as fitting.fit_hist1d
      pars : list of fitted parameter values (output of fitting.fit_hist2d)
      ax   : matplotlib axis object
      label : x axis label title
      units : Units for x axis
    """
    if legend is None :
        dlab, flab = "Data", "Fit"
    elif legend == False :
        dlab, flab = None, None
    else : 
        dlab, flab = legend[0:2]
    datahist, edges = np.histogram(data, bins=bins, range=range, weights = data_weights)
    dataarr = np.array([datahist, datahist]).T.flatten()
    left, right = edges[:-1], edges[1:]
    xarr = np.array([left, right]).T.flatten()

    if isinstance(fit, list) : 
      for i, (f, w) in enumerate(zip(fit, weights)) : 
        fithist1, _ = np.histogram(f, bins=bins, range=range, weights=w)
        fitscale = np.sum(datahist) / np.sum(fithist1)
        fithist = fithist1 * fitscale
        fitarr = np.array([fithist, fithist]).T.flatten()
        ax.plot(xarr, fitarr, label=flab[i], color=color[i] if color else f"C{i}")
    else : 
      fithist1, _ = np.histogram(fit, bins=bins, range=range, weights=weights)
      fitscale = np.sum(datahist) / np.sum(fithist1)
      fithist = fithist1 * fitscale
      fitarr = np.array([fithist, fithist]).T.flatten()
      ax.plot(xarr, fitarr, label=flab, color=fit_color)

    if isinstance(cweights, list):
        cxarr = None
        for i, w in enumerate(cweights):
            if weights:
                w2 = w * weights
            else:
                w2 = w
            chist, cedges = np.histogram(fit, bins=bins, range=range, weights=w2)
            if cxarr is None:
                cleft, cright = cedges[:-1], cedges[1:]
                cxarr = (cleft + cright) / 2.0
            fitarr = chist * fitscale
            if color:
                this_color = color[i]
            else:
                this_color = f"C{i+1}"
            if legend:
                lab = legend[i+2]
            else:
                lab = None
            ax.plot(cxarr, fitarr, color=this_color, label=lab)
            ax.fill_between(cxarr, fitarr, 0.0, color=this_color, alpha=0.1)

    xarr = (left + right) / 2.0
    ax.errorbar(
        xarr,
        datahist,
        np.sqrt(datahist),
        label=dlab,
        color=data_color,
        marker=".",
        linestyle="",
        alpha=data_alpha,
    )

    if not legend == False:
        if legend_ax:
            h, l = ax.get_legend_handles_labels()
            legend_ax.legend(h, l, borderaxespad=0)
            legend_ax.axis("off")
        else:
            ax.legend(loc="best")
    if not log:
        ax.set_ylim(bottom=0.0)
    else:
        ax.set_ylim(bottom=0.1)
        ax.set_yscale("log")
    ax.set_xlabel(label_title(label, units), ha="right", x=1.0)
    ax.set_ylabel(y_label_title(range, bins, units), ha="right", y=1.0)
    if title is None:
        ax.set_title(label + r" distribution")
    elif title:
        ax.set_title(title)
    if pull:
        xarr = np.array([left, right]).T.flatten()
        with np.errstate(divide="ignore", invalid="ignore"):
            pullhist = (datahist - fithist) / np.sqrt(datahist)
            pullhist[datahist == 0] = 0
        # pullhist = np.divide(datahist-fithist, np.sqrt(datahist), out=np.zeros_like(datahist), where=(datahist>0) )
        pullarr = np.array([pullhist, pullhist]).T.flatten()
        ax2 = ax.twinx()
        ax2.set_ylim(bottom=-10.0)
        ax2.set_ylim(top=10.0)
        ax2.plot(xarr, pullarr, color=diff_color, alpha=0.3)
        ax2.grid(False)
        ax2.set_ylabel(r"Pull", ha="right", y=1.0)
        return [ax2]
    return []

def plot_hist1d_comparison(
    data,
    fit,
    ax,
    label,
    log=False,
    units=None,
    pull=False,
    title=None,
    legend=None,
    data_alpha=1.0,
):
    """
    Plot 1D histogram and its fit result.
      hist : histogram to be plotted
      func : fitting function in the same format as fitting.fit_hist1d
      pars : list of fitted parameter values (output of fitting.fit_hist2d)
      ax   : matplotlib axis object
      label : x axis label title
      units : Units for x axis
    """
    if legend is None :
        dlab, flab = "Data", "Fit"
    elif legend == False :
        dlab, flab = None, None
    else : 
        dlab, flab = legend[0:2]
    datahist, edges = data
    bins = len(datahist)
    range = (edges[0], edges[-1])
    dataarr = np.array([datahist, datahist]).T.flatten()
    left, right = edges[:-1], edges[1:]
    xarr = np.array([left, right]).T.flatten()

    fithist1, _ = fit
    fitscale = np.sum(datahist) / np.sum(fithist1)
    fithist = fithist1 * fitscale
    fitarr = np.array([fithist, fithist]).T.flatten()
    ax.plot(xarr, fitarr, label=flab, color=fit_color)

    xarr = (left + right) / 2.0
    ax.errorbar(
        xarr,
        datahist,
        np.sqrt(datahist),
        label=dlab,
        color=data_color,
        marker=".",
        linestyle="",
        alpha=data_alpha,
    )

    if not legend == False:
        ax.legend(loc="best")
    if not log:
        ax.set_ylim(bottom=0.0)
    else:
        ax.set_ylim(bottom=0.1)
        ax.set_yscale("log")
    ax.set_xlabel(label_title(label, units), ha="right", x=1.0)
    ax.set_ylabel(y_label_title(range, bins, units), ha="right", y=1.0)
    if title is None:
        ax.set_title(label + r" distribution")
    elif title:
        ax.set_title(title)
    if pull:
        xarr = np.array([left, right]).T.flatten()
        with np.errstate(divide="ignore", invalid="ignore"):
            pullhist = (datahist - fithist) / np.sqrt(datahist)
            pullhist[datahist == 0] = 0
        # pullhist = np.divide(datahist-fithist, np.sqrt(datahist), out=np.zeros_like(datahist), where=(datahist>0) )
        pullarr = np.array([pullhist, pullhist]).T.flatten()
        ax2 = ax.twinx()
        ax2.set_ylim(bottom=-10.0)
        ax2.set_ylim(top=10.0)
        ax2.plot(xarr, pullarr, color=diff_color, alpha=0.3)
        ax2.grid(False)
        ax2.set_ylabel(r"Pull", ha="right", y=1.0)
        return [ax2]
    return []
