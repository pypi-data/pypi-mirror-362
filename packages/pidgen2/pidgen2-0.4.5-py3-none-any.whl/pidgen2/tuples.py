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
Functions to read and write numpy arrays from/to ROOT ntuples using uproot. 
"""

import uproot
#from jax import numpy as np
#import numpy as onp
import numpy as np
from itertools import product
from timeit import default_timer as timer
import os

from . import init

def read_array_filtered(tree, branches, selection = None, sel_branches = []) : 
  """
  Read numpy 2D array from ROOT tree with filtering applied. 

  Args: 
    tree: ROOT tree object returned by uproot.open()
    branches: list of branches to read in the array
    selection: optional selection string in pandas format
    sel_branches: List of additional selection braches if "selection" string 
                  contains branches not from "branches" list.

  Returns: 
    2D numpy array, where 1st index corresponds to event, 2nd to the variable 
    (in the order given by branches list)
  """

  '''
  arrays = []
  for data in tree.pandas.iterate(branches = branches + sel_branches) : 
      if selection : df = data.query(selection)
      else : df = data
      arr = df[list(branches)].to_numpy()
      arrays += [ arr ]
  return onp.concatenate(arrays, axis = 0)
  '''
  return t.arrays(branches, cut = selection, library = "pd")[list(branches)].to_numpy()

def read_array(tree, branches) : 
  """
  Read numpy 2D array from ROOT tree. 

  Args: 
    tree: ROOT tree object returned by uproot.open()
    branches: list of branches to read in the array

  Returns: 
    2D numpy array, where 1st index corresponds to event, 2nd to the variable 
    (in the order given by "branches" list)
  """
  a = []
  for b in branches : 
    i = tree.array(b)
    if len(i.shape)==1 : a += [ i ]
    else : a += [ i[:,0] ]
  #a = [ tree.array(b) for b in branches ]
  #print("\n".join([ f"{b} : {i.shape}" for i,b in zip(a, branches)]))
  return np.stack(a, axis = 1)

def write_friend_array(rootfile, array, branches, tree="tree") : 
  """
     Store numpy 2D array containing only the output branches in the ROOT file using uproot.

     Args: 
       rootfile : ROOT file name
       array: numpy array to store. The shape of the array should be (N, V), 
               where N is the number of events in the NTuple, and V is the 
               number of branches
       branches : list of V strings defining branch names
       tree : name of the tree
  """
  with uproot.recreate(rootfile, compression=uproot.ZLIB(4)) as file :  
    file[tree] = { b : array[:,i] for i,b in enumerate(branches) }

def write_array(rootfile, array, branches, input, tree="tree", step_size=50000, library="np", verbose=False) :
  """
     Store the output branches and all other branches in the ROOT file iteratively using uproot.
     For the iterative writing of the file uproot converts the data into numpy arrays, pandas DataFrame or awkward arrays.

     Args: 
       rootfile : ROOT output file name
       array: numpy array to store. The shape of the array should be (N, V), 
               where N is the number of events in the NTuple, and V is the 
               number of branches
       branches : list of V strings defining branch names
       input: ROOT output file and tree name
       tree : name of the output tree
       step_size: number of events per iteration
       library: name of library that uproot uses to iterate through the input file and the array,
                supported options are "np", "pd" and "ak"
       verbose: verbosity of prints
  """
  if verbose >= 1 :
    print("arguments of write_array function:\n", locals())

  # When rootfile is only updated, a temporary version of the tree is created
  if input == rootfile+":"+tree:
    rootfile_tmp = rootfile.replace(".root", "_tmp.root")
    if verbose >= 1 :
      print(f"Rename output file from previous step: '{rootfile}'->'{rootfile_tmp}'")
    os.rename(rootfile, rootfile_tmp)
  else:
    rootfile_tmp = input

  chunk_index = 0
  chunk = 0
  num_entries = len(array)
  chunks = (num_entries-1)//step_size+1

  with uproot.recreate(rootfile, compression=uproot.ZLIB(4)) as file :
    for input_chunks in uproot.iterate(rootfile_tmp, step_size=step_size, library=library):

      if verbose >= 0 :
        print(f"Writing chunk {chunk+1}/{chunks}, index={chunk_index}/{num_entries}")

      if library == "ak":
        # input chunks is a highlevel awkward array
        # Create output_dict/convert input chunks to be a dict with branches as keys and awkward arrays as values
        import awkward as ak
        output_dict = { b : ak.from_numpy(np.asarray(array[chunk_index:chunk_index+step_size,i])) for i,b in enumerate(branches)}

        # Work around bug in uproot with writing jagged arrays
        input_fields = []
        for f in input_chunks.fields : 
          if not (f[0] == 'n' and (f[1:] in input_chunks.fields) and ('var' in input_chunks[f[1:]].typestr)) : 
            input_fields += [ f ]

        input_chunks = {f : input_chunks[f] for f in input_fields}

        if chunk_index == 0: #Dump into TTree
          file[tree] = input_chunks | output_dict
        else: #Extend TTree
          file[tree].extend(input_chunks | output_dict)

      elif library == "np":
        # input_chunks is a dict with numpy arrays (with len=step_size) and branches as keys
        # Create a similar dict with branches as keys and the columns of array (which is also a nunpy array) as values
        output_dict = { b : array[chunk_index:chunk_index+step_size,i] for i,b in enumerate(branches) }

        if chunk_index == 0: #Dump into TTree
          file[tree] = input_chunks | output_dict
        else: #Extend TTree
          file[tree].extend(input_chunks | output_dict)

      elif library == "pd":
        # input_chunks is a pandas DataFrame
        # Create a pandas DataFrame for the output
        import pandas as pd
        output_df = pd.DataFrame(array, columns=branches).iloc[chunk_index:chunk_index+step_size]
        
        if chunk_index == 0: #Dump into TTree
          file[tree] = pd.concat([input_chunks, output_df], axis=1)
        else: #Extend TTree
          file[tree].extend(pd.concat([input_chunks, output_df], axis=1))

      else:
        raise ValueError(f"Unknown library {library}; supported options are \"np\", \"pd\" and \"ak\"")

      chunk_index = chunk_index + step_size
      chunk = chunk + 1

  # Delete temporary version of tree
  # Delete old version of tree, asuming there is only one old version
  if input == rootfile+":"+tree:
    if verbose >= 1 :
      print("Delete output file from previous step")
    os.remove(rootfile_tmp)
