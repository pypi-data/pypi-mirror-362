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
General-purpose functions (e.g. not specifically related to PID samples)
useful for density estimation: dataset filtering, variable transformation, 
normalisation, etc.
"""

#from jax import numpy as np
#from jax import scipy as scipy
#from jax import jit, lax
#import numpy as onp
import numpy as np
import scipy
import functools
from scipy.interpolate import RegularGridInterpolator

def filter_data(data, ranges) : 
  """
  Perform filtering of the 2D numpy array to select 
  only the data in a specified range. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array. 

  Returns: 
    filtered 2D array with only the events where all variables are in the specified range
  """
  assert data.shape[1] == len(ranges), "shape of data array does not correspond to the number of ranges"
  cond = functools.reduce(np.logical_and, [ np.logical_and(data[:,i]>ranges[i][0], data[:,i]<ranges[i][1] ) for i in range(data.shape[1]) ] )
  return data[cond]

def create_normaliser(data, ranges, bins, weights = None) : 
  """
  Create normaliser structure based on 2D numpy array of data. 

  Normaliser is effectively a list of cumulative distributions for each dimension of 
  the data array, that can be used to e.g. flatten or normalise the data by applying 
  variable transformation. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array.
    bins: tuple of numbers of bins for each data dimension. 
          Length of the tuple should be equal to the 2nd dimension of the data array.
    weights: array of weights for data events (not used if None)

  Returns: 
    Normaliser structure that can be used later by reweight, normalise, unnormalise etc. 
    functions. 
  """
  assert data.shape[1] == len(ranges), "shape of data array does not correspond to the number of ranges"
  assert data.shape[1] == len(bins), "shape of data array does not correspond to the length of the bins list"
  norm = []
  for i in range(data.shape[1]) : 
    counts, edges = np.histogram(data[:,i], bins = bins[i], range = ranges[i], weights = weights)
    cum_values = np.concatenate( ( np.array([0.]), np.cumsum(counts*np.diff(edges)) ) )
    cum_values /= cum_values[-1]
    norm += [ (cum_values, edges) ]
  return norm

def create_normaliser_from_histograms(hists) : 
  """
  Create normaliser structure from the list of histograms for each data dimension

  Normaliser is effectively a list of cumulative distributions for each dimension of 
  the data array, that can be used to e.g. flatten or normalise the data by applying 
  variable transformation. 

  Args: 
    hists: list of histograms (e.g. produced by create_histograms)

  Returns: 
    Normaliser structure that can be used later by reweight, normalise, unnormalise etc. 
    functions. 
  """
  norm = []
  for h in hists : 
    counts, edges = h
    cum_values = np.concatenate( ( np.array([0.]), np.cumsum(counts*np.diff(edges)) ) )
    cum_values /= cum_values[-1]
    norm += [ (cum_values, edges) ]
  return norm

def create_normaliser_vector(data, ranges, bins, weights = None) : 
  """
  Create normaliser structure based on 2D numpy array of data. 

  Normaliser is effectively a list of cumulative distributions for each dimension of 
  the data array, that can be used to e.g. flatten or normalise the data by applying 
  variable transformation. 

  Args: 
    data: vector of 2D numpy arrays (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array.
    bins: tuple of numbers of bins for each data dimension. 
          Length of the tuple should be equal to the 2nd dimension of the data array.
    weights: array of weights for data events (not used if None)

  Returns: 
    Normaliser structure that can be used later by reweight, normalise, unnormalise etc. 
    functions. 
  """

  norm = []

  for i in range(len(ranges)) : 

    edges = None
    counts = None
  
    for n,d in enumerate(data) : 
      w = None
      if not weights is None : w = weights[n]
      assert d.shape[1] >= len(ranges), "shape of data array does not correspond to the number of ranges"
      assert d.shape[1] >= len(bins), "shape of data array does not correspond to the length of the bins list"

      c, e = np.histogram(d[:,i], bins = bins[i], range = ranges[i], weights = w)
      if counts is None : 
        counts = c
        edges = e
      else : 
        #print(counts, c)
        counts += c

    cum_values = np.concatenate( ( np.array([0.]), np.cumsum(counts*np.diff(edges)) ) )
    cum_values /= cum_values[-1]
    norm += [ (cum_values, edges) ]

  return norm

def create_histograms(data, ranges, bins, weights = None) : 
  """
  Create 1D histograms for projections of 2D numpy array of data. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array.
    bins: tuple of numbers of bins for each data dimension. 
          Length of the tuple should be equal to the 2nd dimension of the data array.
    weights: array of weights for data events (not used if None)

  Returns: 
    List of histograms, one for for each dimension of data array. 
  """
  assert data.shape[1] == len(ranges), "shape of data array does not correspond to the number of ranges"
  assert data.shape[1] == len(bins), "shape of data array does not correspond to the length of the bins list"
  norm = []
  for i in range(data.shape[1]) : 
    counts, edges = np.histogram(data[:,i], bins = bins[i], range = ranges[i], weights = weights)
    norm += [ (counts, edges) ]
  return norm

def create_histograms_vector(data, ranges, bins, weights = None) : 
  """
  Create 1D histograms for projections of 2D numpy array of data. 

  Args: 
    data: vector of 2D numpy arrays (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array.
    bins: tuple of numbers of bins for each data dimension. 
          Length of the tuple should be equal to the 2nd dimension of the data array.
    weights: array of weights for data events (not used if None)

  Returns: 
    List of histograms, one for for each dimension of data array. 
  """
  norm = []
  for i in range(len(ranges)) : 
    edges = None
    counts = None
  
    for n,d in enumerate(data) : 
      w = None
      if not weights is None : w = weights[n]
      assert d.shape[1] >= len(ranges), "shape of data array does not correspond to the number of ranges"
      assert d.shape[1] >= len(bins), "shape of data array does not correspond to the length of the bins list"
      c, e = np.histogram(d[:,i], bins = bins[i], range = ranges[i], weights = w)
      if counts is None : 
        counts = c
        edges = e
      else : 
        counts += c

    norm += [ (counts, edges) ]

  return norm

def append_histograms(data, ranges, bins, hists = None, weights = None) : 
  """
  Append to the list of 1D histograms for projections of multidim numpy array of data. 

  Args: 
    hists: list of 1D histograms to append to
    data: numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    ranges: tuple of 2-element tuples corresponding to variable ranges.
            Length of the tuple should be equal to the 2nd dimension of the data array.
    bins: tuple of numbers of bins for each data dimension. 
          Length of the tuple should be equal to the 2nd dimension of the data array.
    weights: array of weights for data events (not used if None)

  Returns: 
    Appended list of histograms, one for for each dimension of data array. 
  """
  assert data.shape[1] >= len(ranges), "shape of data array does not correspond to the number of ranges"
  assert data.shape[1] >= len(bins), "shape of data array does not correspond to the length of the bins list"
  norm = []
  for i in range(len(ranges)) : 
    if hists is not None : 
      counts, edges = hists[i]
    else : 
      counts, edges = (None, None)
  
    c, e = np.histogram(data[:,i], bins = bins[i], range = ranges[i], weights = weights)
    if counts is None : 
      counts = c
      edges = e
    else : 
      counts += c

    norm += [ (counts, edges) ]

  return norm

def reweight(data, norm, max_weights, weights = None) : 
  """
  Calculate per-event weights for the data sample entries such that the weighted dataset is flat in 
  each 1D projection. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    norm: normaliser structure created with create_normaliser function. 
    max_weights: list of maximal weights per each dimension used to avoid events with too 
                 large weights. 

  Returns:
    1D array of per-event weights (of the size equal to the 1st dimension of data array). 
  """
  if weights is None : 
    w = np.ones_like(data[:,0])
  else : 
    w = weights
  for i in range(data.shape[1]) :
    counts, edges = norm[i]
    w = w/np.maximum(np.interp(data[:,i], 0.5*(edges[1:]+edges[:-1]), counts, left = 1., right = 1.)/\
                                   np.amax(counts), 1./max_weights[i])
  return w

def normalise(data, norm, methods) :
  """
  Perform normalisation of a 2D array to make it more uniform for further 
  density estimation with a specific normalisation method applied to each veriable. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    norm: normaliser structure created with create_normaliser function.
    methods: list of normalisation methods for each variable of the data array. 
             The possible methods are: 
      "flatten" : transform the variable such that its distribution is uniform in the range (0, 1)
      "gauss" : transform the variable such that it has the normal distribution (Gauissian with 
                the mean of 0 and sigma of 1)
      "scale" : make a linear transformation of the variable such that its range of values 
                is from 0 to 1. 

  Returns: 
    Normalised 2D numpy array with the same shape as "data". 
  """
  norm_data = []
  for i in range(data.shape[1]) :
    cum_values, edges = norm[i]
    #dx = edges[1]-edges[0]
    if methods[i] == "flatten" : 
      norm_data += [ np.interp(data[:,i], edges, cum_values, left = 0., right = 1.) ]
    elif methods[i] == "gauss" : 
      flat = np.interp(data[:,i], edges, cum_values, left = 0., right = 1.)
      norm_data += [ scipy.special.erfinv( flat*2. - 1. ) ]
    elif methods[i] == "scale" : 
      left = edges[0]
      right = edges[-1]
      norm_data += [ (data[:,i]-left)/(right-left) ]
  return np.stack(norm_data, axis = 1)

def unnormalise(data, norm, methods) : 
  """
  Perform the transformation of a 2D numpy array that is inverse to the normalisation transformation
  used by the "normalise" function. 

  Args: 
    data: 2D numpy array (1st dimension is event, 2nd dimension corresponds to variable)
    norm: normaliser structure created with create_normaliser function.
    methods: list of normalisation methods for each variable of the data array. 
             The possible methods are: 
      "flatten" : transform the variable such that its distribution is uniform in the range (0, 1)
      "gauss" : transform the variable such that it has the normal distribution (Gauissian with 
                the mean of 0 and sigma of 1)
      "scale" : make a linear transformation of the variable such that its range of values 
                is from 0 to 1. 

  Returns: 
    Un-normalised 2D numpy array with the same shape as "data". 
  """
  denorm_data = []
  for i in range(data.shape[1]) :
    cum_values, edges = norm[i]
    #dx = edges[1]-edges[0]
    if methods[i] == "flatten" : 
      denorm_data += [ np.interp(data[:,i], cum_values, edges, left = edges[0], right = edges[-1]) ]
    elif methods[i] == "gauss" : 
      flat = 0.5*(scipy.special.erf( data[:,i] ) + 1.)
      denorm_data += [ np.interp(flat, cum_values, edges, left = edges[0], right = edges[-1]) ]
    elif methods[i] == "scale" : 
      left = edges[0]
      right = edges[-1]
      denorm_data += [ data[:,i]*(right-left)+left ]
  return np.stack(denorm_data, axis = 1)

def resample(counts, edges, data, rnd, range = (-2.5, 2.5), bins = 100) : 
  """
  Perform random sampling of a single variable following the binned 
  multidimensional density function and the array of input data. 

  Args: 
    counts: N-dim numpy array for multidimensional density, where the 1st column 
            corresponds to the variable being sampled. 
    edges: list of N 2-element tuples defining the ranges (minimum, maximum) of 
           N-dim distribution dimensions 
    data: 2D numpy array with the 2nd dimension of size N-1 with input data to be 
          used for sampling.
    range: 2-element tuple with minimum and maximum values of the sampled random variable
    bins: number of bins in the distribution of the sampled variable 

  Returns: 
    Tuple with 2 numpy arrays (rnd, sum), where
      rnd: 1D array of the same length as 1st dimension of "data" array with the sampled variable
      sum: Total number of events in the density for each event in data array (effective 
        calibration statistics for each event).
  """
  centres = [ 0.5*(e[:-1]+e[1:]) for e in edges ]

  # Pad each dimension by 1 bin in each dimension, and calculate additional bin centres linearly
  # Needed to improve interpolation at the edges (when data points are less than half bin size from the boundary)
  end_values = [ (2.*c[0]-c[1], 2.*c[-1]-c[-2] ) for c in centres ]
  counts2 = np.pad(counts, [(1,1) for c in centres ], 'edge')
  centres2 = [ np.pad(c, (1, 1), 'constant', constant_values = e) for c,e in zip(centres, end_values) ]
  
  interp_func = RegularGridInterpolator(centres2, counts2, bounds_error = False, fill_value = 0.)
  out = []
  for i in np.linspace(range[0], range[1], bins) : 
    arr = np.concatenate([ i*np.ones_like(data[:,0:1]), data], axis = 1)
    out += [ interp_func(arr) ]
  hist = np.stack(out, axis = 1)
  histsum = np.sum(hist, axis = 1, keepdims = True)
  cumsum = np.cumsum(hist, axis = 1)/histsum
  diff = cumsum - rnd[..., np.newaxis]
  ind = np.maximum(1, np.argmax(diff>0., axis = 1)[..., np.newaxis])
  val2 = np.take_along_axis(diff, ind, axis = 1)
  val1 = np.take_along_axis(diff, ind-1, axis = 1)
  return (ind-val2/(val2-val1))/float(bins-1)*(range[1]-range[0]) + range[0], histsum

def probability(counts, edges, data, x, range = (-2.5, 2.5), bins = 100) : 
  """
  Perform random sampling of a single variable following the binned 
  multidimensional density function and the array of input data. 

  Args: 
    counts: N-dim numpy array for multidimensional density, where the 1st column 
            corresponds to the variable being sampled. 
    edges: list of N 2-element tuples defining the ranges (minimum, maximum) of 
           N-dim distribution dimensions 
    data: 2D numpy array with the 2nd dimension of size N-1 with input data to be 
          used for sampling.
    range: 2-element tuple with minimum and maximum values of the sampled random variable
    bins: number of bins in the distribution of the sampled variable 

  Returns: 
    Tuple with 2 numpy arrays (prob, sum), where
      prob: 1D array of the same length as 1st dimension of "data" array with the sampled variable
      sum:  Total number of events in the density for each event in data array (effective 
        calibration statistics for each event).
  """
  centres = [ 0.5*(e[:-1]+e[1:]) for e in edges ]

  # Pad each dimension by 1 bin in each dimension, and calculate additional bin centres linearly
  # Needed to improve interpolation at the edges (when data points are less than half bin size from the boundary)
  end_values = [ (2.*c[0]-c[1], 2.*c[-1]-c[-2] ) for c in centres ]
  counts2 = np.pad(counts, [(1,1) for c in centres ], 'edge')
  centres2 = [ np.pad(c, (1, 1), 'constant', constant_values = e) for c,e in zip(centres, end_values) ]
  
  interp_func = RegularGridInterpolator(centres2, counts2, bounds_error = False, fill_value = 0.)
  out = []
  for i in np.linspace(range[0], range[1], bins) : 
    arr = np.concatenate([ i*np.ones_like(data[:,0:1]), data], axis = 1)
    out += [ interp_func(arr) ]
  hist = np.stack(out, axis = 1)
  histsum = np.sum(hist, axis = 1, keepdims = True)
  cumsum = np.cumsum(hist, axis = 1)/histsum

  ind = (x-range[0])/(range[1]-range[0])*float(bins-1)
  ind1 = np.clip(np.floor(ind).astype(int), 0, bins-1)
  ind2 = np.clip(ind1+1, 0, bins-1)
  frac = (ind-np.floor(ind))[...,np.newaxis]

  val1 = np.take_along_axis(cumsum, ind1[...,np.newaxis], axis = 1)
  val2 = np.take_along_axis(cumsum, ind2[...,np.newaxis], axis = 1)

  #print(f"val1[{val1.shape}]={val1}")
  #print(f"val2[{val2.shape}]={val2}")
  #print(f"frac[{frac.shape}]={frac}")

  return (val1 + (val2-val1)*frac)[:,0], histsum
