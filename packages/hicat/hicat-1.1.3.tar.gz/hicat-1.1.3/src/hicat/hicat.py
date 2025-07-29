import math, random, warnings, copy, time
import pandas as pd
import numpy as np
from scipy.stats import hypergeom
from scipy.special import erf
import sklearn.linear_model as lm
import sklearn.model_selection as mod_sel
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.decomposition import PCA, IncrementalPCA, TruncatedSVD
from sklearn import cluster, mixture
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import kneighbors_graph
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import TSNE
from sklearn.exceptions import ConvergenceWarning
from scipy.sparse import csr_matrix, csc_matrix
import scanpy as sc

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. GMM will be used for clustering.')
    CLUSTERING_AGO = 'gmm'
    SKNETWORK = False

SEABORN = True
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
except ImportError:
    SEABORN = False
    print('WARNING: matplotlib or seaborn not installed. Install them if you want to check out the summary.')    


MHC1_prefix_lst = ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-E', 'HLA-F', 'HLA-G']
MHC2_prefix_lst = ['HLA-DM', 'HLA-DO', 'HLA-DP', 'HLA-DQ']
HLA_DR_prefix_lst = ['HLA-DR']
PNSH12 = '101000'
LOGREG_TOL = 1e-3
LOGREG_MAX_ITER = 1000
LOGREG_NCV = 5
LOGREG_PARAM_GRID = { 'C': [0.5,1,2,4,8,16], \
                   'l1_ratio': [0.2, 0.5, 0.9, 1] } 
CLUSTER_BASIS_CORECTION_DIST_SCALE = [2]
CLUSTER_BASIS_CORECTION_N_NEIGHBORS = 3
CLUSTER_BASIS_CORECTION_MIN_PCT_TO_INVALIDATE = 0.00
SEPARABILITY_THRESHOLD = 0.95
SEPARABILITY_MIN_NUM_CELLS = 100
SEPARABILITY_AUC_INIT_VALUE = 2
# PTH_CUTOFF_MARGIN_MULTIPLIER = 3
PCT_THRESHOLD_MAX = 0.6
PCT_THRESHOLD_MIN = 0.2
GMM_MIN_SCORE = -100


def check_start_with_a_key(s, key):
    if s[:len(key)] == key:
        return True
    else:
        return False

def check_start_with(s, keys):
    for key in keys:
        r = check_start_with_a_key(s, key)
        if r:
            break
    return r
 
def get_markers_from_df(df, target_cell_lst, pnsh12 = PNSH12, verbose = False):
    
    pos = bool(int(pnsh12[0]))
    neg = bool(int(pnsh12[1]))
    sec = bool(int(pnsh12[2]))
    hla_dr = bool(int(pnsh12[3]))
    mhc1 = bool(int(pnsh12[4]))
    mhc2 = bool(int(pnsh12[5]))

    mkr_lst_dict = {}
    for target_cell in target_cell_lst:
        dfs = df.loc[df['cell_type_minor'] == target_cell, :]

        cell_type_minor_lst =  list(set(dfs['cell_type_subset'].unique()))
        cell_type_minor_lst.sort()
        cell_type_minor_lst

        exp_lst = []
        if pos: exp_lst.append('pos')
        if neg: exp_lst.append('neg')
        if sec: exp_lst.append('sec')

        for c in cell_type_minor_lst:
            mkr_lst = []
            for e in exp_lst:
                b = (dfs['cell_type_subset'] == c) & (dfs['exp'] == e)
                if np.sum(b) == 1:
                    idx = dfs.index.values[b][0]
                    mkrs = []
                    items = dfs.loc[idx,'markers'].split(',')
                    for item in items:
                        mkrs.append(item.strip())
                    mkr_lst = mkr_lst + mkrs
                elif np.sum(b) > 1:
                    print('ERROR: get_markers_from_df .. ', dfs.index.values[b] )

            if not mhc1:
                mkr_lst2 = []
                for mkr in mkr_lst:
                    if not check_start_with(mkr, MHC1_prefix_lst):
                        mkr_lst2.append(mkr)
                mkr_lst = copy.deepcopy(mkr_lst2)
                
            if not hla_dr:
                mkr_lst2 = []
                for mkr in mkr_lst:
                    if not check_start_with(mkr, HLA_DR_prefix_lst):
                        mkr_lst2.append(mkr)
                mkr_lst = copy.deepcopy(mkr_lst2)

            if not mhc2:
                mkr_lst2 = []
                for mkr in mkr_lst:
                    if not check_start_with(mkr, MHC2_prefix_lst):
                        mkr_lst2.append(mkr)
                mkr_lst = copy.deepcopy(mkr_lst2)

            mkr_lst_dict[c] = list(set(mkr_lst))

        # if verbose: print_mkrs(mkr_lst_dict) 
        
    return mkr_lst_dict


def remove_common( mkr_dict, verbose = False ):

    cts = list(mkr_dict.keys())
    mkrs_all = []
    for c in cts:
        mkrs_all = mkrs_all + mkr_dict[c]
    mkrs_all = list(set(mkrs_all))
    df = pd.DataFrame(index = mkrs_all, columns = cts)
    df.loc[:,:] = 0

    for c in cts:
        df.loc[mkr_dict[c], c] = 1
    Sum = df.sum(axis = 1)
    
    to_del = []
    s = ''
    for c in cts:
        b = (df[c] > 0) & (Sum == 1)
        mkrs1 = list(df.index.values[b])
        if verbose & (len(mkr_dict[c]) != len(mkrs1)):
            s = s + '%s: %i > %i, ' % (c, len(mkr_dict[c]), len(mkrs1))
        
        if len(mkrs1) == 0:
            to_del.append(c)
        else:
            mkr_dict[c] = mkrs1

    # if (verbose) & len(s) > 0:
    #     print(s[:-2])

    if len(to_del) > 0:
        for c in cts:
            if c in to_del:
                del mkr_dict[c]
                
    return mkr_dict


def load_marker_file( file, to_upper = True ):

    if isinstance(file, str):
        df = pd.read_csv(file, sep = '\t')
    elif isinstance(file, pd.DataFrame):
        df = file.copy(deep = True)
    else:
        print('ERROR: marker input not properly formatted.')
        return file

    ## Convert marker names to upper case
    b = ~df['markers'].isnull()
    mkr_lst = list(df.loc[b, 'markers'])
    mkr_lst_new = []
    if to_upper:
        for s in mkr_lst:
            mkr_lst_new.append(s.upper())
    else:
        for s in mkr_lst:
            mkr_lst_new.append(s)
        
    df.loc[b, 'markers'] = mkr_lst_new

    return df

def get_target_cell_types( file, target_tissues ):
    
    df = pd.read_csv(file, sep = '\t')
    if len(target_tissues) == 0:
        target_cell_types = list(df['cell_type_major'].unique())
    else:
        b = df['tissue'] == target_tissues[0]
        for tt in list(target_tissues):
            b = b | (df['tissue'] == tt)
        target_cell_types = list(df.loc[b,'cell_type_major'].unique())

    return target_cell_types

        
def get_markers_major_type(file, target_cells = [], pnsh12 = PNSH12,
                           rem_common = True, to_upper = True, verbose = False):
    
    if verbose: print('Load markers .. ', end = '', flush = True)
    df = load_marker_file( file, to_upper )

    if target_cells is None:
        target_cells = list(df['cell_type_major'].unique())
    elif len(target_cells) == 0:
        target_cells = list(df['cell_type_major'].unique())
    
    major_type_lst = list(df['cell_type_major'].unique())
        
    mkr_lst = {}
    mkr_lst_neg = {}
    for c in target_cells:
        if c in major_type_lst:
            b = df['cell_type_major'] == c
            cell_type_lst = list(df.loc[b, 'cell_type_minor'].unique())
            pnsh12_t = '%s0%s' % (pnsh12[0], pnsh12[2:])
            mkrs = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_t, verbose = verbose)
            mkr_c = []
            for key in list(mkrs.keys()):
                mkr_c = mkr_c + mkrs[key]
            mkr_lst[c] = list(set(mkr_c))
        
            mkr_c_neg = []
            if pnsh12[1] == '1':
                pnsh12_n = '010%s' % (pnsh12[3:])
                mkrs_neg = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_n, verbose = verbose)
                for key in list(mkrs_neg.keys()):
                    mkr_c_neg = list(set(mkr_c_neg).intersection(mkrs_neg[key]))
            mkr_lst_neg[c] = list(set(mkr_c_neg))
            
    if rem_common:
        mkr_lst = remove_common( mkr_lst, verbose = verbose )
        mkr_lst_neg = remove_common( mkr_lst_neg, verbose = verbose )
        
    sm = ''
    cell_types = list(mkr_lst.keys())
    cell_types.sort()
    for key in cell_types:
        sm = sm + '%s,' % key

    if verbose & (len(sm) > 1) : print(' %i types. \n%s' % (len(mkr_lst.keys()), sm[:-1]))
        
    return mkr_lst, mkr_lst_neg

def get_markers_cell_type(file, target_cells = [], pnsh12 = PNSH12,
                          rem_common = True, to_upper = True, verbose = False):
    
    if verbose: print('Load markers .. ', end = '', flush = True)
    df = load_marker_file( file, to_upper )

    if target_cells is None:
        target_cells = list(df['cell_type_major'].unique())
    elif len(target_cells) == 0:
        target_cells = list(df['cell_type_major'].unique())
    
    major_type_lst = list(df['cell_type_major'].unique())
        
    mkr_lst = {}
    mkr_lst_neg = {}
    pnsh12_t = '%s0%s' % (pnsh12[0], pnsh12[2:])
    for c in target_cells:
        if c in major_type_lst:
            b = df['cell_type_major'] == c
            cell_type_lst = list(df.loc[b, 'cell_type_minor'].unique())
            for c2 in cell_type_lst:

                mkrs = get_markers_from_df(df, [c2], pnsh12 = pnsh12_t, verbose = verbose)
                mkr_c = []
                for key in list(mkrs.keys()):
                    mkr_c = mkr_c + mkrs[key]
                mkr_lst[c2] = list(set(mkr_c))
    
                mkr_c_neg = []
                if pnsh12[1] == '1':
                    pnsh12_n = '010%s' % (pnsh12[3:])
                    mkrs_neg = get_markers_from_df(df, [c2], pnsh12 = pnsh12_n, verbose = verbose)
                    cnt = 0
                    for key in list(mkrs_neg.keys()):
                        if cnt == 0:
                            mkr_c_neg = copy.deepcopy(mkrs_neg[key])
                        else:
                            mkr_c_neg = list(set(mkr_c_neg).intersection(mkrs_neg[key]))
                        cnt += 1
                    if 'common' in list(mkrs_neg.keys()):
                        mkr_c_neg = list(set(mkr_c_neg).union(mkrs_neg['common']))
                mkr_lst_neg[c2] = list(set(mkr_c_neg))

    if rem_common:
        mkr_lst = remove_common( mkr_lst, verbose = verbose )
        mkr_lst_neg = remove_common( mkr_lst_neg, verbose = verbose )
        
    sm = ''
    cell_types = list(mkr_lst.keys())
    cell_types.sort()
    for key in cell_types:
        sm = sm + '%s,' % key
        
    if verbose & (len(sm) > 1): print(' %i types. \n%s' % (len(mkr_lst.keys()), sm[:-1]))
        
    return mkr_lst, mkr_lst_neg


def get_cell_type_dict(file, to_upper = True):
    
    df = load_marker_file( file, to_upper )
    
    target_cells = list(df['cell_type_major'].unique())    
        
    cell_type_dict = {}
    for c in target_cells:
        b = df['cell_type_major'] == c
        cell_type_lst = list(df.loc[b, 'cell_type_minor'].unique())
        for c2 in cell_type_lst:
            cell_type_dict[c2] = c
        
    return cell_type_dict

def comb_markers(mkr_lst_in, maj_dict = None, min_dict = None):
    
    mkr_lst = copy.deepcopy(mkr_lst_in)
    Keys = mkr_lst.keys()
    if ('ILC3 (NCR+)' in Keys) & ('ILC3 (NCR-)' in Keys):
        mkr_lst['ILC3'] = mkr_lst['ILC3 (NCR+)']
        mkr_lst['ILC3'] = mkr_lst['ILC3'] + mkr_lst['ILC3 (NCR-)']
        mkr_lst['ILC3'] = list(set(mkr_lst['ILC3']))
        del mkr_lst['ILC3 (NCR+)']
        del mkr_lst['ILC3 (NCR-)']
        
        if maj_dict is not None:
            maj_dict['ILC3'] = maj_dict['ILC3 (NCR+)']
            del maj_dict['ILC3 (NCR+)']
            del maj_dict['ILC3 (NCR-)']
        
        if min_dict is not None:
            min_dict['ILC3'] = min_dict['ILC3 (NCR+)']
            del min_dict['ILC3 (NCR+)']
            del min_dict['ILC3 (NCR-)']
        
    
    if ('Macrophage (M2A)' in Keys) & ('Macrophage (M2B)' in Keys) & \
        ('Macrophage (M2C)' in Keys) & ('Macrophage (M2D)' in Keys):
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2A)']
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2)'] + mkr_lst['Macrophage (M2B)']
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2)'] + mkr_lst['Macrophage (M2C)']
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2)'] + mkr_lst['Macrophage (M2D)']
        mkr_lst['Macrophage (M2)'] = list(set(mkr_lst['Macrophage (M2)']))
        del mkr_lst['Macrophage (M2A)']
        del mkr_lst['Macrophage (M2B)']
        del mkr_lst['Macrophage (M2C)']
        del mkr_lst['Macrophage (M2D)']
        
        if maj_dict is not None:
            maj_dict['Macrophage (M2)'] = maj_dict['Macrophage (M2A)']
            del maj_dict['Macrophage (M2A)']
            del maj_dict['Macrophage (M2B)']
            del maj_dict['Macrophage (M2C)']
            del maj_dict['Macrophage (M2D)']
        
        if min_dict is not None:
            min_dict['Macrophage (M2)'] = min_dict['Macrophage (M2A)']
            del min_dict['Macrophage (M2A)']
            del min_dict['Macrophage (M2B)']
            del min_dict['Macrophage (M2C)']
            del min_dict['Macrophage (M2D)']
        
    if ('Macrophage' in Keys) & ('Macrophage (M1)' in Keys) & ('Macrophage (M2)' in Keys):
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2)'] + mkr_lst['Macrophage']
        mkr_lst['Macrophage (M2)'] = list(set(mkr_lst['Macrophage (M2)']))
        mkr_lst['Macrophage (M1)'] = mkr_lst['Macrophage (M1)'] + mkr_lst['Macrophage']
        mkr_lst['Macrophage (M1)'] = list(set(mkr_lst['Macrophage (M1)']))
        del mkr_lst['Macrophage']

        if maj_dict is not None:
            del maj_dict['Macrophage']
        
        if min_dict is not None:
            del min_dict['Macrophage']
            
    elif ('common' in Keys) & ('Macrophage (M1)' in Keys) & ('Macrophage (M2)' in Keys):       
        mkr_lst['Macrophage (M2)'] = mkr_lst['Macrophage (M2)'] + mkr_lst['common']
        mkr_lst['Macrophage (M2)'] = list(set(mkr_lst['Macrophage (M2)']))
        mkr_lst['Macrophage (M1)'] = mkr_lst['Macrophage (M1)'] + mkr_lst['common']
        mkr_lst['Macrophage (M1)'] = list(set(mkr_lst['Macrophage (M1)']))
        del mkr_lst['common']

        if maj_dict is not None:
            del maj_dict['common']
        
        if min_dict is not None:
            del min_dict['common']
        
    if (maj_dict is not None) & (min_dict is not None):
        return mkr_lst, maj_dict, min_dict
    else:
        return mkr_lst


def comb_common(mkr_lst_in):
    
    mkr_lst = copy.deepcopy(mkr_lst_in)
    Keys = list(mkr_lst.keys())
    
    if ('common' in Keys) & (len(Keys) > 1):
        for key in Keys:
            if key != 'common':
                mkr_lst[key] = mkr_lst[key] + mkr_lst['common']
                mkr_lst[key] = list(set(mkr_lst[key]))
        del mkr_lst['common']

    return mkr_lst


def get_markers_minor_type2(file, target_cells = [], pnsh12 = PNSH12,
                            rem_common = False, comb_mkrs = False, 
                            to_upper = True, verbose = False):
    
    if verbose: print('Load markers .. ', end = '', flush = True)
    df = load_marker_file( file, to_upper )
    
    if target_cells is None:
        target_cells = list(df['cell_type_minor'].unique())
    elif len(target_cells) == 0:
        target_cells = list(df['cell_type_minor'].unique())
    else:
        ## It shold be a list of minor types
        pass
    
    major_type_lst = list(df['cell_type_minor'].unique())
    
    mkr_lst = {}
    mkr_lst_neg = {}
    pnsh12_t = '%s0%s' % (pnsh12[0], pnsh12[2:])
    for c in target_cells:
        if c in major_type_lst:
            b = df['cell_type_minor'] == c
            cell_type_lst = list(df.loc[b, 'cell_type_minor'].unique())
            mkrs = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_t, verbose = verbose)
            mkrs = comb_common(mkrs)
            mkr_lst.update(mkrs)
        
            if pnsh12[1] == '1':
                pnsh12_n = '010%s' % (pnsh12[3:])
                mkrs_neg = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_n, verbose = verbose)
                mkrs_neg = comb_common(mkrs_neg)
                mkr_lst_neg.update(mkrs_neg)
        
    if len(mkr_lst.keys()) == 0:
        return mkr_lst, mkr_lst_neg

    if comb_mkrs:
        mkr_lst = comb_markers(mkr_lst)
        mkr_lst_neg = comb_markers(mkr_lst_neg)
    
    if rem_common:
        mkr_lst = remove_common( mkr_lst, verbose = verbose )
        mkr_lst_neg = remove_common( mkr_lst_neg, verbose = verbose )
        
    sm = ''
    cell_types = list(mkr_lst.keys())
    # cell_types.sort()
    for key in cell_types:
        sm = sm + '%s,' % key
        
    if verbose & (len(sm) > 1): print(' %i types. \n%s' % (len(mkr_lst.keys()), sm[:-1]))
        
    return mkr_lst, mkr_lst_neg


def print_mkrs(mkr_lst_dict):
    
    for key in list(mkr_lst_dict.keys()):
        if len(mkr_lst_dict[key]) > 0:
            s = mkr_lst_dict[key][0]
            for mkr in mkr_lst_dict[key][1:]:
                s = s + ',%s' % mkr
            print('%s (%i): %s' % (key, len(mkr_lst_dict[key]), s))
        else:
            print('%s (%i): ' % (key, len(mkr_lst_dict[key])))

    
def load_markers_all(file, target_cells = [], pnsh12 = '111111', comb_mkrs = True,  
                     to_upper = True, verbose = False):
    
    if verbose: print('Load markers .. ', end = '', flush = True)
    df = load_marker_file( file, to_upper )
    
    if len(target_cells) == 0:
        target_cells = list(df['cell_type_major'].unique())
    
    major_type_lst = list(df['cell_type_major'].unique())
    
    mkr_lst = {}
    mkr_lst_neg = {}
    mkr_lst_sec = {}
    major_dict = {}
    minor_dict = {}
    pnsh12_t = '%s00%s' % (pnsh12[0], pnsh12[3:])
    for c in target_cells:
        if c in major_type_lst:
            b = df['cell_type_major'] == c
            cell_type_lst = list(df.loc[b, 'cell_type_minor'].unique())
            mkrs = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_t, verbose = verbose)
            mkrs = comb_common(mkrs)
            mkr_lst.update(mkrs)
        
            if pnsh12[1] == '1':
                pnsh12_n = '010%s' % (pnsh12[3:])
                mkrs_neg = get_markers_from_df(df, cell_type_lst, pnsh12 = pnsh12_n, verbose = verbose)
                mkrs_neg = comb_common(mkrs_neg)
                mkr_lst_neg.update(mkrs_neg)
            
            if pnsh12[2] == '1':
                pnsh12_n = '001%s' % (pnsh12[3:])
                mkrs_sec = get_markers_from_df(df, cell_type_lst, pnsh12 =pnsh12_n, verbose = verbose)
                mkrs_sec = comb_common(mkrs_sec)
                mkr_lst_sec.update(mkrs_sec)
            
            for c2 in cell_type_lst:
                mkrs = get_markers_from_df(df, [c2], pnsh12 = pnsh12_t, verbose = verbose)
                mkrs = comb_common(mkrs)                
                for key in mkrs.keys():
                    minor_dict[key] = c2
                    major_dict[key] = c
            
    if len(mkr_lst.keys()) == 0:
        return mkr_lst, mkr_lst_neg, mkr_lst_sec

    if comb_mkrs:
        mkr_lst, major_dict, minor_dict = comb_markers(mkr_lst, major_dict, minor_dict)
        mkr_lst_neg = comb_markers(mkr_lst_neg)
        mkr_lst_sec = comb_markers(mkr_lst_sec)

    sm = ''
    cell_types = list(mkr_lst.keys())
    cell_types.sort()
    for key in cell_types:
        sm = sm + '%s,' % key
        
    if verbose & (len(sm) > 1): print(' %i types. \n%s' % (len(mkr_lst.keys()), sm[:-1]))
        
    return mkr_lst, mkr_lst_neg, mkr_lst_sec, major_dict, minor_dict


def save_markers_all(mkr_lst, mkr_lst_neg, mkr_lst_sec, major_dict, minor_dict, file):
    
    cols = ['cell_type_major', 'cell_type_minor', 'cell_type_subset', 'exp', 'markers'] 
    df_pos = pd.DataFrame(columns = cols)
    df_neg = pd.DataFrame(columns = cols)
    df_sec = pd.DataFrame(columns = cols)

    mkr_lst_tmp = mkr_lst
    ct_lst = list(mkr_lst_tmp.keys())
    mkrs = []
    ct_lst_new = []
    for c in ct_lst:
        if len(mkr_lst_tmp[c]) > 0:
            mkr_lst_tmp[c].sort()
            s = mkr_lst_tmp[c][0]
            if len(mkr_lst_tmp[c]) > 1:
                for mkr in mkr_lst_tmp[c][1:]:
                    s = s + ',%s' % mkr
            mkrs.append(s)
            ct_lst_new.append(c)
    
    df_pos['cell_type_subset'] = ct_lst_new
    df_pos['markers'] = mkrs
    df_pos['exp'] = ['pos']*len(mkrs)
    
    mkr_lst_tmp = mkr_lst_neg
    ct_lst = list(mkr_lst_tmp.keys())
    mkrs = []
    ct_lst_new = []
    for c in ct_lst:
        if len(mkr_lst_tmp[c]) > 0:
            mkr_lst_tmp[c].sort()
            s = mkr_lst_tmp[c][0]
            if len(mkr_lst_tmp[c]) > 1:
                for mkr in mkr_lst_tmp[c][1:]:
                    s = s + ',%s' % mkr
            mkrs.append(s)
            ct_lst_new.append(c)
            
    
    df_neg['cell_type_subset'] = ct_lst_new
    df_neg['markers'] = mkrs
    df_neg['exp'] = ['neg']*len(mkrs)
    
    df = pd.concat([df_pos, df_neg], axis = 0)
    
    mkr_lst_tmp = mkr_lst_sec
    ct_lst = list(mkr_lst_tmp.keys())
    mkrs = []
    ct_lst_new = []
    for c in ct_lst:
        if len(mkr_lst_tmp[c]) > 0:
            mkr_lst_tmp[c].sort()
            s = mkr_lst_tmp[c][0]
            if len(mkr_lst_tmp[c]) > 1:
                for mkr in mkr_lst_tmp[c][1:]:
                    s = s + ',%s' % mkr
            mkrs.append(s)
            ct_lst_new.append(c)
            
    
    df_sec['cell_type_subset'] = ct_lst_new
    df_sec['markers'] = mkrs
    df_sec['exp'] = ['sec']*len(mkrs)
    
    df = pd.concat([df, df_sec], axis = 0)
    
    df['cell_type_major'] = df['cell_type_subset'].copy(deep = True)
    df['cell_type_minor'] = df['cell_type_subset'].copy(deep = True)
    df['cell_type_major'].replace(major_dict, inplace = True)
    df['cell_type_minor'].replace(minor_dict, inplace = True)
    df.sort_values(by = ['cell_type_major', 'cell_type_major', 'cell_type_subset'], inplace = True)

    if file is None:
        return df
    else:
        df.to_csv(file, sep = '\t', index = False)
        return df
    
def Tiden_check_key_genes( gene_lst, key_genes ):
    
    b = True
    for g in list(key_genes):
        if g not in gene_lst:
            b = False
            break
    return b

def Tiden_print_error(error_code = 0):    
    if error_code == 1:
        print('ERROR: One or more of key genes for T cell subtyping (CD4, CD8A, CD8B) are not in the gene list.')
    else:
        print('ERROR: X_cell_by_gene must be a DataFrame with its columns being gene names having CD4, CD8A, CD8B')
        print('ERROR: Or, gene_names must be provided with its length equal to the column size of X_cell_by_gene, containing CD4, CD8A, CD8B.')

        
def get_stat2(df_score):

    df = df_score
    maxv = list(df.max(axis = 1))
    subtype = list(df.idxmax(axis = 1))
    #tc_subtype = [trans_dict[k] for k in tc_subtype]

    maxv2 = []
    idx2 = []
    subtype_lst = list(df.columns.values)

    for i in range(df.shape[0]):
        x = np.array(df.iloc[i])
        odr = (-x).argsort()
        if len(x) > 1:
            maxv2.append(x[odr[1]])
            idx2.append(subtype_lst[odr[1]])
        else:
            maxv2.append(0)
            idx2.append(None)

    # df_res = pd.DataFrame({'CD4+ T cell subtype': tc_subtype, 'NegLogPval': neg_log_pval}, index = df.index.values)
    df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                           'cell_type(1st)': subtype, 'cell_type(2nd)': idx2, 
                           'Clarity': ['-']*df.shape[0], 'Score': maxv, 'Score(2nd)': maxv2}, 
                          index = df.index.values)
    df_res['dScore'] = df_res['Score'] - df_res['Score(2nd)']
    
    return df_res


def plot_GSA_score_hist(df_score, title = 'GSA', histtype = 'bar'):
    
    df_sum = get_stat2(df_score)
    score_name = 'Score'
    target_types = list(df_sum['cell_type(1st)'].unique())
    thresholds = {}
    m1m2_ratio = {}
    plot_hist = True
    
    for t in target_types:
        target = t

        b1 = (df_sum['cell_type(1st)'] == target) #& (df_sum['-logP'] > -np.log10(pval_th))
        v1 = df_sum.loc[b1, score_name]
        m1 = df_sum.loc[b1, score_name].max() #.mean()
        n1 = np.sum(b1)

        b2 = (df_sum['cell_type(2nd)'] == target) # & (df_sum['-logP(2nd)'] > -np.log10(pval_th))
        if np.sum(b2) > 0:
            v2 = df_sum.loc[b2, '%s(2nd)' % score_name]
            m2 = df_sum.loc[b2, '%s(2nd)' % score_name].max() #.mean()
            n2 = np.sum(b2)
            
        if plot_hist:
            x1 = df_sum.loc[b1, score_name]
            mnv = x1.min()
            mxv = x1.max()
            X = x1
            if np.sum(b2) > 0:
                x2 = df_sum.loc[b2, '%s(2nd)' % score_name]
                mnv = min(mnv, x2.min())
                mxv = max(mxv, x2.min())
                X = np.array([x1,x2])
                
            if mnv < mxv:
                bins = np.arange(mnv, mxv, (mxv-mnv)/50)
                plt.figure(figsize = (5,3))
                # df_sum.loc[b1, score_name].hist(bins = 50, log = True, alpha = 0.7)
                plt.hist(X, bins = bins, log = True, alpha = 0.8, histtype = histtype)
                plt.title('Histogram for %s %s score' % (t, title))
                plt.xlabel('score')
                plt.ylabel('Number of cells')
                if np.sum(b2) > 0:
                    # df_sum.loc[b2, '%s(2nd)' % score_name].hist(bins = 50, log = True, alpha = 0.5)
                    # plt.hist(x2, bins = bins, log = True, alpha = 0.5, density = True)
                    plt.legend(['Primary', 'Secondary'])
                else:
                    plt.legend(['Primary'])
            else:
                print('ERROR: Histogram for %s %s not available.' % (t, title))
    return 


def plot_GSA_score_violin(df_score, title = 'GSA', split = True, 
                          scale = 'width', inner = 'quartile', log = True, 
                          width = 1, fig_scale = 1):
    
    df_sum = get_stat2(df_score)
    if log:
        df_score = np.log2(df_score + 1)
        
    score_name = 'Score'
    target_types = list(df_score.columns.values) # list(df_sum['cell_type(1st)'].unique())
    thresholds = {}
    m1m2_ratio = {}
    plot_hist = True
    
    cnt = 0
    for t in target_types:
        target = t

        b1 = (df_sum['cell_type(1st)'] == target) 
        b2 = (df_sum['cell_type(1st)'] != target) 
            
        X = None
        if plot_hist:
            x1 = df_score.loc[b1, t]
            if len(x1) > 10:
                if np.sum(b2) > 10:
                    X = pd.DataFrame( {'Score': x1} )
                    X['cell type'] = 'Target'
                    X['Cell type'] = t
                    
                    x2 = df_score.loc[b2, t] # df_sum.loc[b2, '%s(2nd)' % score_name]
                    # X = np.array([x1,x2])
                    X2 = pd.DataFrame( {'Score': x2} )
                    X2['cell type'] = 'Non-target'
                    X2['Cell type'] = t
                    X = pd.concat([X,X2], axis = 0)
            
                    if X is not None:
                        if cnt == 0:
                            df = X
                        else:
                            df = pd.concat([df,X], axis = 0)
                        cnt += 1
            
    if (cnt > 0) & SEABORN:
        nn = len(list(df['Cell type'].unique()))
        plt.figure(figsize = (1.3*nn*fig_scale, 4*fig_scale), dpi=100)
        sns.violinplot(x="Cell type", y="Score", hue="cell type", inner = inner,
                    data=df, palette="muted", split=split, scale = scale, 
                    width = width, fontsize = 12*fig_scale, linewidth = 0.75, gridsize = 30)
        plt.xticks(rotation = 20, ha = 'center', fontsize = 12*fig_scale)   
        plt.yticks(fontsize = 12*fig_scale)
        plt.title(title, fontsize = 13*fig_scale)
        plt.legend(fontsize = 10*fig_scale)
        # plt.xlabel('Cell type', fontsize = 12)
        plt.xlabel(None)
        if log:
            plt.ylabel('Log2(1+Score)', fontsize = 12*fig_scale)
        else:
            plt.ylabel('Score', fontsize = 12*fig_scale)
        plt.show()
    elif not SEABORN:
        print('WARNING: seaborn is not installed.')
    return 


def plot_roc_result(df_score, y_true, cell_type, method = 'gmm', fig_scale = 1):
    
    label = list(df_score.columns.values)
    
    bs = y_true == label[0] 
    for l in label[1:]:
        bs = bs | (y_true == l)
    
    plt.figure(figsize=(4*fig_scale, 4*fig_scale), dpi=100)
    clst = ['darkorange', 'red', 'gold', 'yellow', 'firebrick', 'orange', \
            'magenta', 'crimson', 'violet', 'mediumorchid', 'purple', \
            'blueviolet', 'lime', 'turquoise']*4

    all_cells = ''
    fprs = []
    tprs = []
    aucs = []
    cells= []
    ss = 0
    for k, l in enumerate(label):
        #if (k%4 == 0) & (k>0):
        if (k>0) & ((len(all_cells) + len(l) + 2 - ss) > 45):
            ss = len(all_cells) + 1
            all_cells = all_cells + '\n'
        all_cells = all_cells + '%s, ' % l
        
        
        y_conf_1 = df_score.loc[bs, l]
        
        label_tmp = copy.deepcopy(label)
        label_tmp.remove(l)
        y_conf_0 = df_score.loc[bs, label_tmp].max(axis = 1)

        y_odd = y_conf_1 # - y_conf_0

        bn = ~np.isnan(y_odd)
        y_odd = y_odd[bn]
        
        y = y_true[bs&bn]

        target = l
        if (y == target).sum() > 1:
            try:
                # fpr, tpr, _ = roc_curve(y.ravel(), y_odd.ravel(), pos_label = target)
                fpr, tpr, _ = roc_curve(y, y_odd, pos_label = target)
                roc_auc = auc(fpr, tpr)
                fprs.append(fpr)
                tprs.append(tpr)
                aucs.append(roc_auc)
                cells.append(target)
            except:
                pass
                # print(y)
                # print(y_odd)

    all_cells = cell_type
    odr = np.array(aucs).argsort()
    for k, o in enumerate(reversed(odr)):
        title = "%s (AUC = %0.3f)" % (label[o], aucs[o])
        plt.plot(fprs[o], tprs[o], label=title) #, color=clst[k])
            
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate", fontsize = 12*fig_scale) #, fontsize = 11)
    plt.ylabel("True Positive Rate", fontsize = 12*fig_scale) #, fontsize = 11)

    if method == 'gmm':
        Method = 'Gaussian Mixture Model'
        title = "ROC for identifying %s\nusing %s" % (all_cells, Method)
    elif method == 'logreg':
        Method = 'Logistic Regression Model'
        title = "ROC for identifying %s\nusing %s" % (all_cells, Method)
    else:
        Method = method
        title = "ROC for identifying\n%s using %s" % (all_cells, Method)

    plt.title(title, fontsize = 13*fig_scale )
    plt.legend(loc="lower right", fontsize = 10*fig_scale)
    # plt.legend(loc="upper left", bbox_to_anchor=(1.03, 1)) # , fontsize = 12)
    plt.show()
    
    return cells, aucs


def show_summary( df_pred, summary, pth_fit_pnt = 0.3, level = 3, 
                    split = True, scale = 'area', inner = 'quartile', 
                    vlog = True, vwidth = 1, fig_scale = 1 ):
    
    smry_res = summary['GSA_summary']
    pval_th, pth_mult, pth_min = summary['parameters']
    
    ## Cluster filter
    y_clust = df_pred['cluster'].astype(int) - 1
    score = smry_res['Major_Type']['-logP']
    pth = pval_th # smry_res['Pval_threshold']
    #'''
    if level > 0:
        find_pct_cutoff(score, y_clust, pth = -np.log10(pth), 
                        pct_fit_pnt = pth_fit_pnt, pct_min_rf = pth_min, 
                        figsize = (5*fig_scale,4*fig_scale), verbose = True)
    #'''

    ## GSA ROC
    smry_score = summary['GSA_scores']
    keys = list(smry_score.keys())

    key = 'Major_Type'
    df_score = smry_score[key]
    ys = smry_res[key]['cell_type']
    # if level > 1:
    cells, aucs = plot_roc_result(df_score, ys, key, 'GSA', fig_scale = fig_scale)    
    df_auc_maj = pd.DataFrame({'AUC using GSA': aucs}, index = cells)
        
    ## ID model ROC
    smry_score = summary['Identification_model_scores']
    keys = list(smry_score.keys())

    key = 'Major_Type'
    df_score = smry_score[key]
    ys = smry_res[key]['cell_type']
    # if level > 1:
    cells, aucs = plot_roc_result(df_score, ys, key, 'gmm', fig_scale = fig_scale)    
    df_auc_maj['AUC using GMM'] = aucs

    ## GSA score histogram
    if level > 2:
        smry_score = summary['GSA_scores']
        for key in smry_score.keys():
            df_score = smry_score[key]
            if isinstance(df_score, pd.DataFrame):
                plot_GSA_score_violin(df_score, title = key, split = split, 
                                      scale = scale, inner = inner, 
                                      log = vlog, width = vwidth, fig_scale = fig_scale)

    ## GSA score histogram
    if level > 2:
        if 'Ref_scores' in list(summary.keys()):
            smry_score = summary['Ref_scores']
        else: 
            smry_score = summary['GSA_scores']
        smry_res = summary['GSA_summary']
        cnt = 0
        for key in smry_score.keys():
            df_score = smry_score[key]
            ys = smry_res[key]['cell_type']
            if ('minor' in key) & (key != 'Major_Type') & (level > 1) & (df_score.shape[1] > 1):
                cells, aucs = plot_roc_result(df_score, ys, key, 'GSA')    
                if cnt == 0:
                    df_auc_min = pd.DataFrame({'AUC using GSA': aucs}, index = cells)
                else:
                    df_auc_min = pd.concat([df_auc_min, pd.DataFrame({'AUC': aucs}, index = cells)], axis = 0)
                cnt += 1
        if cnt == 0:
            df_auc_min = None
                
        cnt = 0
        for key in smry_score.keys():
            df_score = smry_score[key]
            ys = smry_res[key]['cell_type']
            if ('minor' not in key) & (key != 'Major_Type') & (level > 1) & (df_score.shape[1] > 1):
                cells, aucs = plot_roc_result(df_score, ys, key, 'GSA')    
                if cnt == 0:
                    df_auc = pd.DataFrame({'AUC': aucs}, index = cells)
                else:
                    df_auc = pd.concat([df_auc, pd.DataFrame({'AUC': aucs}, index = cells)], axis = 0)
                cnt += 1
                
        if cnt == 0:
            df_auc = None
                 
    ## GSA score histogram
    if level > 2:
        if 'Ref_scores' in list(summary.keys()):
            smry_score = summary['Ref_scores']
            for key in smry_score.keys():
                df_score = smry_score[key]
                if isinstance(df_score, pd.DataFrame):
                    plot_GSA_score_violin(df_score, title = key, split = split, 
                                          scale = scale, inner = inner, 
                                          log = False, width = vwidth, fig_scale = fig_scale)

    return df_auc_maj, df_auc_min, df_auc

    
def X_normalize(X):    
    return X.div(X.sum(axis=1)*0.0001 + 0.0001, axis = 0)


def X_scale(X, max_val = 10):    
    m = X.mean(axis = 0)
    s = X.std(axis = 0)
    
    Xs = X.sub(m).mul((s > 0)/(s+ 0.0001))
    Xs.clip(upper = max_val, lower = -max_val, inplace = True)
    
    return Xs


def select_variable_genes(log1p_X, N_genes = 2000, pm = 0.1, Ns = 40):
    
    Xa = log1p_X 
        
    # sm = (Xa > 0).sum(axis = 0)
    ma = Xa.mean(axis = 0)
    sa = Xa.std(axis = 0)
    
    ## Select genes
    xsm = (Xa).sum(axis = 0)
    odr = np.array(xsm).argsort()
    lc = int(len(odr)*pm)
    uc = int(len(odr)*(1-pm))
    if uc == len(odr):
        uc = int(uc - 1)
    min_xsm = xsm[odr[lc]]
    max_xsm = xsm[odr[uc]]
    b = (ma > 0) & (xsm > min_xsm) & (xsm < max_xsm)
    
    m_sel = ma[b]
    s_sel = sa[b]
        
    ## Fit
    lm_sel = np.log10(m_sel + 1e-10)
    ls_sel = np.log10(s_sel + 1e-10)
    
    z = np.polyfit(lm_sel, ls_sel, 2)
    p = np.poly1d(z)
    
    ## Select genes
    lm = np.log10(ma + 1e-10)    
    s_fit = 10**(p(lm))

    Xt = Xa.sub(ma, axis = 1).mul(1/(s_fit + 1e-10), axis = 1).astype(float)
    uc = np.sqrt(Xt.shape[0])
    Xt.clip(upper = uc, lower = -uc, inplace = True)

    sr = Xt.var(axis = 0)
    
    min_lm = lm.min()
    max_lm = lm.max()
    dx = (max_lm - min_lm)/Ns
    
    rng = np.arange(min_lm, max_lm+dx*2, dx)
    for n in range(Ns):
        lc = rng[n]
        uc = rng[n+1]
        bx = (lm >= lc) & (lm < uc)
        if np.sum(bx) > 0:
            msr = np.mean(sr[bx])
            sr[bx] = sr[bx] - msr
        
    bx = (lm >= uc)
    if np.sum(bx) > 0:
        sr[bx] = 0
    
    odr = np.array(sr).argsort()
    s_th = sr[odr[-N_genes]]
    bx = sr >= s_th
    genes = list(Xt.columns.values[bx])
    
    return genes


def select_variable_genes2(log1p_X, N_genes = 2000, pm = 0.1, Ns = 40):
    
    Xa = log1p_X 
        
    # sm = (Xa > 0).sum(axis = 0)
    ma = Xa.mean(axis = 0)
    sa = Xa.std(axis = 0)
    
    ## Select genes
    xsm = (Xa).sum(axis = 0)
    odr = np.array(xsm).argsort()
    lc = int(len(odr)*pm)
    uc = int(len(odr)*(1-pm))
    if uc == len(odr):
        uc = int(uc - 1)
    min_xsm = np.array(xsm)[odr[lc]]
    max_xsm = np.array(xsm)[odr[uc]]
    b = (ma > 0) & (xsm > min_xsm) & (xsm < max_xsm)
    
    m_sel = ma[b]
    s_sel = sa[b]
        
    ## Fit
    lm_sel = np.log10(m_sel + 1e-10)
    ls_sel = np.log10(s_sel + 1e-10)
    
    z = np.polyfit(lm_sel, ls_sel, 2)
    p = np.poly1d(z)
    
    ## Select genes
    lm = np.log10(ma + 1e-10)    
    s_fit = 10**(p(lm))

    Xt = Xa.sub(ma, axis = 1).mul(1/(s_fit + 1e-10), axis = 1).astype(float)
    uc = np.sqrt(Xt.shape[0])
    Xt.clip(upper = uc, lower = -uc, inplace = True)

    sr = Xt.var(axis = 0)
    
    min_lm = lm.min()
    max_lm = lm.max()
    dx = (max_lm - min_lm)/Ns
    
    rng = np.arange(min_lm, max_lm+dx*2, dx)
    for n in range(Ns):
        lc = rng[n]
        uc = rng[n+1]
        bx = (lm >= lc) & (lm < uc)
        if np.sum(bx) > 0:
            msr = np.mean(sr[bx])
            sr[bx] = sr[bx] - msr
        
    bx = (lm >= uc)
    if np.sum(bx) > 0:
        sr[bx] = 0
    
    odr = np.array(sr).argsort()
    s_th = np.array(sr)[odr[-N_genes]]
    bx = sr >= s_th
    genes = list(Xt.columns.values[bx])
    
    return genes, odr, sr


def X_preprocessing_old( Xs, log_transformed, N_genes = 2000 ):
    
    if not log_transformed:
        Xx = np.log2(1 + X_normalize(Xs))
    else:
        Xx = Xs
        
    if Xs.shape[1] <= N_genes:
        gene_sel = list(Xs.columns.values)
        # Xx = X_scale(Xx, max_val = 10)
        pass
    else:
        gene_sel = select_variable_genes(Xx, N_genes = N_genes )
        # Xx = X_scale(Xx.loc[:,gene_sel], max_val = 10)
        
    return Xx.loc[:,gene_sel]


def X_normalize(X, total_sum = 1e4): 
    if isinstance(X, csr_matrix):
        Xd = np.array(X.sum(axis=1)*(1/total_sum) + 1e-8).transpose()[0,:]
        rows = X.tocoo().row
        data = copy.deepcopy(X.data)
        data = data/Xd[rows]
            
        X_sparse = csr_matrix( (data, X.indices, X.indptr), shape = X.shape)        
        return X_sparse
    elif isinstance(X, csc_matrix):
        Xd = np.array(X.sum(axis=1)*(1/total_sum) + 1e-8).transpose()[0,:]
        rows = X.tocoo().row
        data = copy.deepcopy(X.data)
        data = data/Xd[rows]
            
        X_sparse = csc_matrix( (data, X.indices, X.indptr), shape = X.shape)        
        return X_sparse
    else:
        Xd = 1/(X.sum(axis=1)*(1/total_sum) + 1e-8)
        return X.mul(Xd, axis = 0)

    
def X_preprocessing( Xs, log_transformed ):
    
    if not log_transformed:
        # Xx = np.log2(1 + X_normalize(Xs))
        Xx = X_normalize(Xs)
        if isinstance(Xs, csr_matrix) | isinstance(Xs, csc_matrix):
            Xx.data = np.log2(1 + Xx.data)
        else:
            Xx = np.log2(1 + Xx)
    else:
        Xx = copy.deepcopy(Xs)
        
    return Xx


def X_variable_gene_sel( Xx, N_genes = 2000, N_cells_max = 100000, vg_sel = True ):
    
    if (Xx.shape[1] <= N_genes) | (not vg_sel):
        gene_sel = list(Xx.columns.values)
    else:
        if Xx.shape[0] <= N_cells_max:
            gene_sel, gene_odr, gene_sr = select_variable_genes2(Xx, N_genes = N_genes )
        else:
            lst_full = list(Xx.index.values)
            lst_sel = random.sample(lst_full, k= N_cells_max)
            gene_sel, gene_odr, gene_sr = select_variable_genes2(Xx.loc[lst_sel, :], N_genes = N_genes )
        
    return Xx.loc[:,gene_sel]


def X_variable_gene_sel2( Xx, N_genes = 2000, N_cells_max = 100000, vg_sel = True ):
    
    if (Xx.shape[1] <= N_genes) | (not vg_sel):
        gene_sel = list(Xx.columns.values)
    else:
        if Xx.shape[0] <= N_cells_max:
            gene_sel, gene_odr, gene_sr = select_variable_genes2(Xx, N_genes = N_genes )
        else:
            lst_full = list(Xx.index.values)
            lst_sel = random.sample(lst_full, k= N_cells_max)
            gene_sel, gene_odr, gene_sr = select_variable_genes2(Xx.loc[lst_sel, :], N_genes = N_genes )
        
    return Xx.loc[:,gene_sel], gene_odr, gene_sr


def pca_subsample(Xx, N_components_pca, N_cells_max_for_pca = 100000):
    
    pca = TruncatedSVD(n_components = int(N_components_pca)) # , algorithm = 'arpack')
    
    if Xx.shape[0] <= N_cells_max_for_pca:
        X_pca = pca.fit_transform(Xx)
    else:
        if isinstance(Xx, pd.DataFrame):
            lst_full = list(Xx.index.values)
            lst_sel = random.sample(lst_full, k= N_cells_max_for_pca)
            pca.fit(Xx.loc[lst_sel, :])
        else:
            lst_full = np.arange(Xx.shape[0])
            lst_sel = random.sample(lst_full, k= N_cells_max_for_pca)
            pca.fit(Xx[lst_sel, :])
            
        # X_pca = Xx.dot(pca.components_.transpose()) 
        X_pca = pca.transform(Xx)
        
    return X_pca


def clustering_alg(X_pca, clust_algo = 'lv', N_clusters = 25, resolution = 1, N_neighbors = 10, 
                   mode='connectivity', n_cores = 4):
                   # mode='distance', n_cores = 4):
    
    N_c = N_clusters
    min_N_cells_per_cluster = 50
    if X_pca.shape[0]/N_c < min_N_cells_per_cluster:
        N_c = int( X_pca.shape[0]/min_N_cells_per_cluster )
        if N_c < 1:
            N_c = 1
    
    adj = None
    if clust_algo[:2] == 'gm':
        gmm = mixture.GaussianMixture(n_components = int(N_c), random_state = 0)
        cluster_label = gmm.fit_predict(np.array(X_pca))
        return cluster_label, gmm, adj
    elif clust_algo[:2] == 'km':
        km = cluster.KMeans(n_clusters = int(N_c), random_state = 0)
        km.fit(X_pca)
        cluster_label = km.labels_
        return cluster_label, km, adj
    else:
        adj = kneighbors_graph(X_pca, int(N_neighbors), mode=mode, include_self=True, 
                               n_jobs = n_cores)
        louvain = Louvain(resolution = resolution, random_state = 0)
        if hasattr(louvain, 'fit_predict'):
            cluster_label = louvain.fit_predict(adj)        
        else:
            cluster_label = louvain.fit_transform(adj)        
        return cluster_label, louvain, adj

    
def get_neighbors(adj, n_neighbors):
    
    rows = adj.tocoo().row
    cols = adj.tocoo().col
    data = adj.data    
    
    N = int(np.max(rows) + 1)
    neighbors = np.full([N, n_neighbors], -1)
    distances = np.full([N, n_neighbors], -1)
    cnts = np.zeros(N, dtype = int)
    
    for r, c, d in zip(rows, cols, data):
        neighbors[r, cnts[r]] = c
        distances[r, cnts[r]] = d
        cnts[r] += 1
        
    for i in range(N):
        odr = distances[i,:].argsort()
        distances[i,:] = distances[i,odr]
        neighbors[i,:] = neighbors[i,odr]
        
    return neighbors, distances
    

def set_cluster_for_others( ilst, labels, neighbors, distances ):
    
    label_lst = list(set(labels))
    label_lst.sort()
    label_array = np.array(labels)
    iary = np.array(ilst)
    label_all = np.full(neighbors.shape[0], -1)
    label_all[ilst] = labels
    
    b1 = label_all < 0
    nn = np.sum(b1)
    
    for j in range(neighbors.shape[1]):
        for k in range(len(label_all)):
            nlst = list(neighbors[b1,j])
            label_sel = label_all[nlst]
            label_all[b1] = label_sel

            b1 = label_all < 0
            # print(np.sum(b1))
            if (np.sum(b1) == 0) | (nn == np.sum(b1)):
                break
            else:
                nn = np.sum(b1)

        b1 = label_all < 0
        # print(np.sum(b1), 'AA')
        if (np.sum(b1) == 0):
            break
        
    return label_all


def clustering_subsample( X_vec, neighbors = None, distances = None, 
                          clust_algo = 'lv', N_clusters = 25, resolution = 1, N_neighbors = 10, 
                          mode='connectivity', n_cores = 4, Ns = 10000, Rs = 0.95 ):

    method = clust_algo
    Ns = int(min(Ns, X_vec.shape[0]*Rs))

    adj = None
    if (neighbors is None) | (distances is None):
        start = time.time()
        adj = kneighbors_graph(X_vec, int(N_neighbors), mode = 'distance', # 'connectivity', 
                           include_self=False, n_jobs = 4)
        neighbors, distances = get_neighbors(adj, N_neighbors)
        lapsed = time.time() - start
        # print(lapsed, len(list(set(list(labels)))))
    
    lst_full = list(np.arange(X_vec.shape[0]))
    lst_sel = random.sample(lst_full, k= Ns)

    for k in range(3):
        label_all = set_cluster_for_others( lst_sel, [0]*len(lst_sel), neighbors, distances )
        b = label_all < 0
        if np.sum(b) == 0:
            break
        elif (np.sum(b) < 20) | (k == 2):
            lst_sel2 = list(np.array(lst_full)[b])
            lst_sel = lst_sel + lst_sel2
            break;
        else:
            lst_sel2 = list(np.array(lst_full)[b])
            lst_sel2 = random.sample(lst_sel2, k= int(len(lst_sel2)*Ns/X_vec.shape[0]))
            lst_sel = lst_sel + lst_sel2
    
    if isinstance(X_vec, pd.DataFrame):
        Xs = X_vec.iloc[lst_sel]
    else:
        Xs = X_vec[lst_sel,:]

    start = time.time()
    labels, obj, adj_tmp = clustering_alg(Xs, clust_algo = method, N_clusters = N_clusters, 
                                          resolution = resolution, N_neighbors = N_neighbors, 
                                          mode='connectivity', n_cores = 4)

    lapsed = time.time() - start
    # print(lapsed, len(list(set(list(labels)))))

    label_all = set_cluster_for_others( lst_sel, labels, neighbors, distances )

    return label_all, obj, adj
    

def get_gsa_score_stat( gsa_score, verbose = False ):

    stat = pd.DataFrame( columns = ['N', 'median', 'Q90', 'R'] )
    celltype_dec_tmp = gsa_score.idxmax(axis = 1)
    for c in gsa_score.columns:
        b = celltype_dec_tmp == c
        if np.sum(b) > 0:
            ms = gsa_score[c][b].quantile(0.5)
            q9 = gsa_score[c][b].quantile(0.9)
            if verbose: print('   %20s: %f, %f ' % (c, ms, q9))
            stat.loc[c,:] = [np.sum(b), ms, q9, q9/ms]

    return stat


def adjust_gsa_score( stat, gsa_score, max_Q90 = 12, verbose = 1 ):

    b = (stat['R'] > 2) & (stat['Q90'] > max_Q90)
    lst = stat.index.values[b]
    for c in lst:
        if verbose: 
            print('   %s: %5.2f/%5.2f = %5.2f ' % (c, max_Q90, stat.loc[c, 'Q90'], (max_Q90/stat.loc[c, 'Q90'])))
        gsa_score[c] = gsa_score[c]*(max_Q90/stat.loc[c, 'Q90'])
        
    return gsa_score


def GSA_cell_subtyping( X_cell_by_gene, mkrs_pos, mkrs_neg = None, max_Q90 = 15, score_adj_weight = {}, verbose = False ):

    X = X_cell_by_gene    
    genes = list(X.columns.values)

    mkr_lst_dict = copy.deepcopy(mkrs_pos)
    if mkrs_neg is not None:
        mkr_lst_dict_neg = copy.deepcopy(mkrs_neg)
    for key in list(mkr_lst_dict.keys()):
        mkrs = mkr_lst_dict[key]
        mkrs2 = list(set(mkrs).intersection(genes))    
        if len(mkrs2) < len(mkrs):
            mkr_lst_dict[key] = mkrs2
            s = ''
            cnt = 0
            for mkr in mkrs:
                if mkr not in mkrs2:
                    s = s + '%s,' % mkr
                    cnt += 1
            if len(s) > 1:
                s = s[:-1]
                if verbose:
                    print('   WARNING: %15s pos_mkrs in db: %3i, where %2i missing (%s)' % (key, len(mkrs), cnt, s))
                    
        if mkrs_neg is not None:
            if key in mkr_lst_dict_neg.keys():
                mkrs3 = mkr_lst_dict_neg[key]
                if len(mkrs3) > 0:
                    mkrs4 = list(set(mkrs3).intersection(genes))    
                    if len(mkrs4) < len(mkrs3):
                        mkr_lst_dict_neg[key] = mkrs2
                        s = ''
                        cnt = 0
                        for mkr in mkrs3:
                            if mkr not in mkrs4:
                                s = s + '%s,' % mkr
                                cnt += 1
                        if len(s) > 1:
                            s = s[:-1]
                            if verbose:
                                print('   WARNING: %15s neg_mkrs in db: %3i, where %2i missing (%s)' % (key, len(mkrs), cnt, s))

            
    if verbose: print('GSA .. ', end = '')
    start_time = time.time()
    
    ## Get stats for CD4+ T cells only

    Xb = X > 0
    N = Xb.shape[1]
    k = Xb.sum(axis = 1)

    mkr_stat = {}
    df = pd.DataFrame(index = Xb.index.values, columns = list(mkr_lst_dict.keys()))
    dfn = pd.DataFrame(index = Xb.index.values, columns = list(mkr_lst_dict.keys()))
    dfo = pd.DataFrame(index = Xb.index.values, columns = list(mkr_lst_dict.keys()))
    
    n_mkr = {}
    for key in list(mkr_lst_dict.keys()):
        n_mkr[key] = len(mkr_lst_dict[key])
        if mkrs_neg is not None:
            if key in mkr_lst_dict_neg.keys():
                n_mkr[key] = n_mkr[key] + len(mkr_lst_dict_neg[key])
            
    for key in list(mkr_lst_dict.keys()):
        mkrs = mkr_lst_dict[key]
        b = Xb[mkrs]
        n = b.sum(axis = 1)
        M = len(mkrs)

        if mkrs_neg is not None:
            if key in mkr_lst_dict_neg.keys():
                mkrs_neg = mkr_lst_dict_neg[key]
                b_neg = ~Xb[mkrs_neg]
                n = n + b_neg.sum(axis = 1)
                M = M + len(mkrs_neg)

        neg_log_pval = -hypergeom.logsf(n-1, N, M, k)*np.log10(np.exp(1))
        df[key] = neg_log_pval
        dfn[key] = n

    if isinstance( score_adj_weight, dict ):
        for key in score_adj_weight.keys():
            if key in list(df.columns.values):
                # print('   %20s: %f ' % (key, score_adj_weight[key]))
                df[key] = df[key]*score_adj_weight[key]
    else:
        print('WARNING: score_adj_weight must be a dictionary. Skip score adjustment.')

    stat = get_gsa_score_stat( df, verbose = verbose )
    df = adjust_gsa_score( stat, df, max_Q90 = max_Q90, verbose = verbose )
    
    
    ## Get final results
    num = list(np.arange(df.shape[1]))
    name = list(df.columns.values)
    trans_dict = dict(zip(num,name))
    
    if len(mkr_lst_dict.keys()) == 1:
        c = name[0]
        neg_log_pval = df[c]
        subtype = [c]*df.shape[0]

        k1 = n_mkr[c]
        olst = ['%i/%i' % (i, k1) for i in list(dfn[c])]
        
        # df_res = pd.DataFrame({'CD4+ T cell subtype': tc_subtype, 'NegLogPval': neg_log_pval}, index = df.index.values)
        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype, 'Overlap': olst}, # dfn[c]},
                               # dtype={'cell_type': str, 'cell_type(rev)': str, 'cell_type(1st)': str, 'Overlap': int},
                               index = df.index.values)
        
        df_res['cell_type(2nd)'] = None
        df_res['cell_type(2nd)'] = df_res['cell_type(2nd)'].astype(str)
        df_res['Overlap(2nd)'] = ['-']*df_res.shape[0]
        df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(str)
        df_res['Clarity'] = ['-']*df.shape[0]
        df_res['-logP'] = df[c]
        df_res['-logP(2nd)'] = 0
                               
        df_res['-logP-logP(2nd)'] = df[c]

        # df_res['Overlap'] = df_res['Overlap'].astype(int)        
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(int)
    
    else:
        neg_log_pval = df.max(axis = 1)
        subtype = list(df.idxmax(axis = 1))
        #tc_subtype = [trans_dict[k] for k in tc_subtype]

        maxv = []
        maxv2 = []
        idx2 = []
        Nn = []
        N1 = []
        N2 = []
        subtype_lst = list(df.columns.values)

        for i in range(df.shape[0]):
            x = np.array(df.iloc[i])
            n = np.array(dfn.iloc[i])
            odr = (-x).argsort()
            maxv.append(x[odr[0]])
            maxv2.append(x[odr[1]])
            idx2.append(subtype_lst[odr[1]])

            k1 = n_mkr[subtype_lst[odr[0]]]
            k2 = n_mkr[subtype_lst[odr[1]]]
            n1 = n[odr[0]]
            n2 = n[odr[1]]
            s1 = n1 # '%i/%i' % (n1, k1)
            s2 = n2 # '%i/%i' % (n2, k2)
            N1.append(s1)
            N2.append(s2)
            Nn.append(n1)
            
            nlst = ['%i/%i' % (nn, n_mkr[subtype_lst[j]]) for j, nn in enumerate(list(n))]
            dfo.iloc[i,:] = nlst

        # df_res = pd.DataFrame({'CD4+ T cell subtype': tc_subtype, 'NegLogPval': neg_log_pval}, index = df.index.values)
        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype, 'Overlap': N1,
                               'cell_type(2nd)': idx2, 'Overlap(2nd)': N2,
                               'Clarity': ['-']*df.shape[0], '-logP': maxv, '-logP(2nd)': maxv2}, 
                              index = df.index.values)
        df_res['-logP-logP(2nd)'] = df_res['-logP'] - df_res['-logP(2nd)']

        b = np.array(Nn) == 0
        df_res.loc[b,'cell_type'] = 'unassigned'
        df_res.loc[b,'cell_type(rev)'] = 'unassigned'
        df_res.loc[b,'cell_type(1st)'] = 'unassigned'
        df_res.loc[b,'cell_type(2nd)'] = 'unassigned'

        # df_res['Overlap'] = df_res['Overlap'].astype(int)        
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(int)

    # if verbose: print('done. (%i s)' % round(time.time() - start_time))
    df_score = df
    return df_res, df_score, dfn


def C_major_gmm(X_pca, ys, class_names, method = 'gmm', N_components = 8, 
                N_cells_max = 40000, verbose = False ):
    
    if verbose: print('Fitting GMM .. ', end = '')
    start_time = time.time()

    bs = (ys == class_names[0])
    for cname in list(class_names[1:]):
        bs = bs | (ys == cname)
        
    X = np.array(X_pca.loc[bs,:])
    y = ys[bs]

    ## Select training cells
    df_score = pd.DataFrame(index = X_pca.index.values)
    cnt = 0
    for cname in list(class_names):
    
        X_tmp = X[y == cname,:]
        y_tmp = y[y == cname]
        
        # N_comp = min(max(int(N_components * len(y_tmp)/szmx),1), len(y_tmp))
        # if len(y_tmp) < 50: N_comp = 1
        #'''
        sqrtN = max(int(np.sqrt(X_pca.shape[0])/2), 1)
        if len(y_tmp) <= N_components:
            N_comp = 1
        else:
            N_comp = min(N_components, sqrtN)
        #'''

        if len(y_tmp) > N_comp:
            if method == 'gmm':
                gmm = mixture.GaussianMixture(n_components = int(N_comp), random_state = 0)
            else:
                gmm = mixture.BayesianGaussianMixture(n_components = int(N_comp), 
                                                      max_iter = 1000, random_state = 0)

            if X_tmp.shape[0] <= N_cells_max:
                gmm.fit(np.array(X_tmp))
            else:
                lst_full = list(np.arange(X_tmp.shape[0]))
                lst_sel = random.sample(lst_full, k= N_cells_max)
                gmm.fit(np.array(X_tmp[lst_sel, :]))
                
            y_conf = gmm.score_samples(np.array(X_pca))
            df_score['%s' % cname] = list(y_conf)
            cnt += 1
    
    if cnt > 1:
        y_pred = df_score.idxmax(axis = 1)
    else:
        y_pred = pd.Series(index = X_pca.index.values, dtype = float)
        if cnt == 1:
            y_pred[:] = df_score.columns.values[0]
        else:
            y_pred[:] = 'unassigned'
        
    y_pred[~bs] = 'unassigned'
    
    etime = time.time() - start_time
    if verbose: print('(%i). ' % int(etime), end = '')
    
    # if verbose: print('GMM correction: %i -> %i, %i' % (len(bs), np.sum(bs), np.sum(y_pred == 'unassigned') ))    
    # if verbose: print('done. (%i s)' % round(time.time() - start_time))
    return y_pred, df_score


def C_major_logreg(X_pca, ys, class_names, verbose = False ):
    
    if verbose: print('Fitting Logistic Regression model .. ', end = '')
    start_time = time.time()

    bs = (ys == class_names[0])
    for cname in list(class_names[1:]):
        bs = bs | (ys == cname)
        
    X = np.array(X_pca.loc[bs,:])
    y = ys[bs]

    NCV = LOGREG_NCV
    MAX_ITER = LOGREG_MAX_ITER
    param_grid = LOGREG_PARAM_GRID

    n_samples, n_features = X.shape
    cv = mod_sel.StratifiedKFold(n_splits=NCV)
    classifier = lm.LogisticRegression(penalty = 'elasticnet', 
                                       max_iter = MAX_ITER, solver = 'saga', 
                                       class_weight = 'balanced',tol = LOGREG_TOL)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # warnings.filterwarnings("ignore", category=ConvergenceWarning)
        gs = mod_sel.GridSearchCV(classifier, param_grid, cv=cv, scoring='balanced_accuracy', refit = True, n_jobs = NCV, verbose = 0)

        gs.fit(X,y)
        # print(gs.best_params_, gs.best_score_)

    classifier = gs.best_estimator_
    y_pred = classifier.predict(X_pca)
    y_prob = classifier.predict_proba(X_pca)

    cols = list(classifier.classes_)
    df_score = pd.DataFrame(np.log10(y_prob + 1e-100), index = X_pca.index.values, columns = cols)
            
    y_pred = df_score.idxmax(axis = 1)
    
    # if verbose: print('done. (%i s)' % round(time.time() - start_time))
    return y_pred, df_score
      
    
def get_threshold(values, target_FPR = 0.05, upper = True):
    
    z = np.array(values)
    odr = z.argsort()
    n = int(round(len(odr)*target_FPR))
    if n >= len(odr):
        n = int(len(odr)-1)
    if upper:
        th = z[odr[-n]]
    else:
        th = z[odr[n]]
    return th


def get_threshold_N(values, NN = 1, upper = True):
    
    z = np.array(values)
    odr = z.argsort()
    n = int(NN)
    if n >= len(odr):
        n = int(len(odr)-1)
    if upper:
        th = z[odr[-n]]
    else:
        th = z[odr[n]]
    return th

#'''

def get_normal_pdf( x, mu, var, nbins):
    
    y = np.array(x)
    mn_x = y.min()
    mx_x = y.max()
    L = 100
    # dx = len(y)*(mx_x-mn_x)/L
    dx = (mx_x-mn_x)/nbins
    xs = np.arange(mn_x,mx_x, dx )
    pdf = (dx*len(y))*np.exp(-((xs-mu)**2)/(2*var+1e-10))/(np.sqrt(2*math.pi*var)+1e-10) + 1e-10
    return pdf, xs


def get_threshold_using_param( param, Target_FPR = 0.1 ):
    
    w0, m0, v0, w1, m1, v1 = param 
    mxv = m1+np.sqrt(v1)
    mnv = m0
    z = np.arange(mnv,mxv, (mxv-mnv)/1000)

    e0 = 1 - 0.5*(1 + erf((z - m0)/np.sqrt(v0)))
    e1 = 1 - 0.5*(1 + erf((z - m1)/np.sqrt(v1)))
    fpr = e0/e1
    
    if fpr.min() < Target_FPR:
        i = np.abs(fpr-Target_FPR).argmin()
        threshold = z[i]
    else: 
        i = fpr.argmin()
        threshold = z[i]
            
    return threshold

def bimodal_fit( x_score ):
    
    x = x_score

    gmm = mixture.GaussianMixture(n_components = 2, random_state = 0)
    y = gmm.fit_predict(np.array(x).reshape(-1, 1))

    mns = [m[0] for m in gmm.means_]
    cvs = [cv[0,0] for cv in gmm.covariances_]

    wgs = gmm.weights_           
    if mns[0] < mns[1]:
        w0, w1 = wgs[0], wgs[1]
        m0, m1 = mns[0], mns[1]
        v0, v1 = cvs[0], cvs[1]
    else:
        w0, w1 = wgs[1], wgs[0]
        m0, m1 = mns[1], mns[0]
        v0, v1 = cvs[1], cvs[0]

    return w0, m0, v0, w1, m1, v1
    
    
def get_threshold_from_GSA_result(df_sum, pval_th = 0.05, target_FPR = 0.05, 
                                   verbose = False, plot_hist = False):
    
    target_types = list(df_sum['cell_type(1st)'].unique())
    thresholds = {}
    m1m2_ratio = {}
    
    if verbose:
        print('Thresholds:')
        
    if len(target_types) == 1:
        
        t = target_types[0]
        x_score = df_sum['-logP'] # np.log10(df_sum['-logP'] + 1e-3)
        param = bimodal_fit( x_score )
        thresh = get_threshold_using_param( param, Target_FPR = target_FPR )
        w0, m0, v0, w1, m1, v1 = param 
        # m0 = 10**m0
        # m1 = 10**m1
        # thresh = 10**thresh
        thresholds[t] = thresh
        m1m2_ratio[t] = m1/m0 # (10**m1)/(10**m0)

        if verbose:
            print('   %16s: %5.3f, %5.3f > %5.2f, %5.2f > %i/%i' % \
              (t, m1, m0, thresh, m1/m0, 
               np.sum(x_score >= thresh), len(x_score)))
    else:
        for t in target_types:
            if t != 'unassigned':
                target = t

                b1 = (df_sum['cell_type(1st)'] == target) & \
                     (df_sum['-logP'] >= -np.log10(pval_th))
                n1 = np.sum(b1)

                if n1 > 1:
                    v1 = df_sum.loc[b1, '-logP']
                    m1 = df_sum.loc[b1, '-logP'].mean(axis = 0)

                b2 = (df_sum['cell_type(2nd)'] == target) & \
                     (df_sum['-logP(2nd)'] > -np.log10(pval_th))
                n2 = np.sum(b2)
                
                if n2 > 1:
                    v2 = df_sum.loc[b2, '-logP(2nd)']
                    m2 = df_sum.loc[b2, '-logP(2nd)'].mean(axis = 0)

                # if np.sum(b2) > 0:
                if (n1 > 1) & (n2 > 1):
                    NN = int(n1*target_FPR)
                    thresh = get_threshold_N(v2, NN = NN, upper = True)
                    thresh = max(thresh, -np.log10(pval_th))
                    # th_min = get_threshold(v1, target_FPR = 0.1, upper = False)
                    # if thresh < th_min: 
                    #     thresh = th_min
                    if thresh > m1: thresh = m1
                    elif (thresh < m2) & (m1 > m2): thresh = m2
                    
                elif (n1 > 1): # & (n2 <= 1):
                    # if len(v1) > 1:
                    thresh = get_threshold(v1, target_FPR = 0.1, upper = False)
                    if thresh > m1: thresh = m1
                    thresh = max(thresh, -np.log10(pval_th))
                    m2 = 0.01
                else:
                    thresh = 0
                    m2 = 0.01
                    m1 = 0

                thresholds[t] = thresh
                m1m2_ratio[t] = m1/m2

                if verbose:
                    if (n1 > 1) & (n2 > 1):
                        print('   %16s: %5.3f, %5.3f > %5.2f, %5.2f > %i/%i' % \
                              (t, m1, m2, thresh, m1/m2, np.sum(v1 >= thresh), len(v1) ) )
                    else:
                        print('   %16s: %5.3f, %5.3f > %5.2f, %5.2f' % \
                              (t, m1, m2, thresh, m1/m2 ) )
            
    return thresholds, m1m2_ratio
#'''

def get_stat(df_score):

    df = df_score
    maxv = list(df.max(axis = 1))
    subtype = list(df.idxmax(axis = 1))
    #tc_subtype = [trans_dict[k] for k in tc_subtype]

    maxv2 = []
    idx2 = []
    subtype_lst = list(df.columns.values)

    for i in range(df.shape[0]):
        x = np.array(df.iloc[i])
        odr = (-x).argsort()
        if len(x) > 1:
            maxv2.append(x[odr[1]])
            idx2.append(subtype_lst[odr[1]])
        else:
            maxv2.append(0)
            idx2.append(None)

    # df_res = pd.DataFrame({'CD4+ T cell subtype': tc_subtype, 'NegLogPval': neg_log_pval}, index = df.index.values)
    df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                           'cell_type(1st)': subtype, 'cell_type(2nd)': idx2, 
                           'Clarity': ['-']*df.shape[0], 'Score': maxv, 'Score(2nd)': maxv2}, 
                          index = df.index.values)
    df_res['dScore'] = df_res['Score'] - df_res['Score(2nd)']
    
    return df_res


def get_threshold_from_GMM_result(df_sum, target_FPR = 0.05, 
                                   verbose = False, plot_hist = False):
    
    target_types = list(df_sum['cell_type(1st)'].unique())
    thresholds = {}
    m1m2_ratio = {}
    
    if verbose:
        print('Thresholds:')
        
    for t in target_types:
        target = t

        b1 = (df_sum['cell_type(rev)'] == target) #& (df_sum['-logP'] > -np.log10(pval_th))
        v1 = df_sum.loc[b1, 'Score']
        m1 = df_sum.loc[b1, 'Score'].max() #.mean()
        n1 = np.sum(b1)

        ##############################
        b2 = (df_sum['cell_type(2nd)'] == target) & \
             (df_sum['cell_type(rev)'] != 'unassigned') 
        if np.sum(b2) > 0:
            v2 = df_sum.loc[b2, 'Score(2nd)']
            m2 = df_sum.loc[b2, 'Score(2nd)'].max() #.mean()
            n2 = np.sum(b2)

            NN = int(n1*target_FPR)
            thresh = get_threshold_N(v2, NN = NN, upper = True)
            #thresh = np.max(v2)
            # get_threshold(v2, target_FPR = target_FPR, upper = True)
        else:
            m2 = df_sum.loc[b1, 'Score'].mean()
            v2 = df_sum.loc[b1, 'Score']
            thresh = m2 #get_threshold(v1, target_FPR = target_FPR, upper = False)
            if verbose:
                print('WARNING: thresholds for %s was set to %6.2f - 10 = %6.2f' % (t, m1, thresh))

        thresholds[t] = thresh
        m1m2_ratio[t] = m1-m2

        if verbose:
            print('   %16s: %6.2f, %6.2f > Threshold: %6.2f > %i/%i,  %i/%i' % \
              (t, m1, m2, thresh, np.sum(v1 >= thresh), len(v1), np.sum(v2 >= thresh), len(v2)))
            
    return thresholds, m1m2_ratio


def get_majorities(y, y_clust):
    
    labels_unique, counts = np.unique(y_clust, return_counts=True)
    
    maj_lst = []
    cnt_lst = []
    for c in list(labels_unique):
        b = np.array(y_clust) == c
        cts, cnts = np.unique(y[b], return_counts=True)
        odr = cnts.argsort()
        majority = cts[odr[-1]]
        maj_lst.append(majority)
        cnt_lst.append(cnts[odr[-1]])
        
    maj_dict = dict(zip(labels_unique, maj_lst))
    cnt_dict = dict(zip(labels_unique, cnt_lst))
    
    return maj_dict, cnt_dict


def cluster_basis_correction(X_pca, y, cobj, y_clust, pmaj = 0.7, 
                             cutoff = 0.01, verbose = False ):
    
    ys = pd.Series(y).copy(deep = True)
    
    adj_agg = cobj.aggregate_
    adj_agg_mat = adj_agg.todense().astype(int) 
    labels_unique, counts = np.unique(y_clust, return_counts=True)

    ## Get neighbor clusters
    # cutoff = 0.01
    aj = {}
    for j in range(len(labels_unique)):
        a = []
        b = []
        for k in range(len(labels_unique)):
            if (adj_agg_mat[j,k] >= adj_agg_mat[j,j]*cutoff) & (adj_agg_mat[j,k] >= adj_agg_mat[k,k]*cutoff):
                a.append(k)
                b.append(adj_agg_mat[j,k])
        if len(a) > 0:
            odr = (-np.array(b)).argsort()
            a1 = []
            b1 = []
            bn = []
            for o in odr:
                a1.append(a[o])
                b1.append(b[o])
                nv = int(10*np.log10(b[o]/adj_agg_mat[j,j] + 1e-10))
                bn.append(nv)
            d = dict(zip(a1,bn))
            bn.sort(reverse = True)
            aj[j] = d

    ## Get community list
    communities = []
    for key in aj.keys():
        d = aj[key]
        nodes = list(d.keys())
        if len(nodes) > 1:
            common = nodes
            for n in nodes:
                common = list(set(common).intersection(list(aj[n].keys())))
            if len(common) > 1:
                communities.append(common)
                # print(key, ': ', common)

    to_del = []
    for k, c in enumerate(communities):
        b = False
        for k2, c2 in enumerate(communities):
            if (k2 != k) & (k not in to_del) & (k2 not in to_del):
                if (len(list(set(c) - set(c2))) == 0):
                    to_del.append(k)

    for k in reversed(to_del):
        del communities[k]
    
    clust_maj_dict, clust_cnt_dict = get_majorities(y, y_clust)
    
    for k, community in enumerate(communities):
        if (len(community) > 1):
            ## check if 'unassigned' cluster
            ct_cnt_dict = {}
            for cm in community:
                if clust_maj_dict[cm] in list(ct_cnt_dict.keys()):
                    ct_cnt_dict[clust_maj_dict[cm]] += clust_cnt_dict[cm]
                else:
                    ct_cnt_dict[clust_maj_dict[cm]] = clust_cnt_dict[cm]
                    
            odr = (-np.array(list(ct_cnt_dict.values()))).argsort()
            ct_cnt_dict_new = {}
            keys = list(ct_cnt_dict.keys())
            for o in odr:
                key = keys[o]
                val = ct_cnt_dict[key]
                ct_cnt_dict_new[key] = val
            ct_cnt_dict = ct_cnt_dict_new
                
            if (len(list(ct_cnt_dict.keys())) > 1): # & ('unassigned' in list(ct_cnt_dict.keys())):

                # print(ct_cnt_dict)
                keys = list(ct_cnt_dict.keys())
                cnt_total = np.sum(list(ct_cnt_dict.values()))
                maj_ct = None
                if keys[0] == 'unassigned':
                    if ct_cnt_dict[keys[1]] >= (cnt_total - ct_cnt_dict['unassigned'])*pmaj:
                        maj_ct = keys[1]
                else:
                    if ct_cnt_dict[keys[0]] >= (cnt_total)*pmaj: 
                        maj_ct = keys[0]

                if maj_ct is not None:
                    for cm in community:
                        b = np.array(y_clust) == cm
                        ys[b] = maj_ct

                    if verbose:
                        s = 'Community %i: ' % k
                        for cm in community:
                            s = s + '%s(%i), ' % (clust_maj_dict[cm], int(clust_cnt_dict[cm]))
                        if len(s) > 3: s = s[:-1]
                        s = s + ' -> %s ' % maj_ct
                        print(s[:-1], flush = True)
                    else:
                        print('%s' % maj_ct[0], end = '', flush = True)                        
    return ys


def find_pct_cutoff( score, y_clust, pth = 1.3, pct_fit_pnt = 0.3, 
                     pct_min_rf = 1, verbose = False, 
                     figsize = (5,4), title = 'Cluster filter stats.'):
    
    clust_lst = list(set(y_clust))
    # clust_lst.sort()

    nn = []
    for c in clust_lst:
        b = y_clust == c
        nn.append((score[b] >= pth).sum()/np.sum(b))
    nn.sort()

    y = np.array(nn)
    x = np.arange(len(nn))
    
    L = int(len(y)*pct_fit_pnt) #np.sum(y < PCT_THRESHOLD_MAX)
    if len(y) - L < 10: L = max(len(y) - 10, 2)
        
    if L >= 0:
        z = np.polyfit(x[L:],y[L:], 1, w = y[L:])
        p = np.poly1d(z)
        s = p(x)

        # for i in reversed(range(len(nn))):
        for i in range(len(nn)):
            # if np.abs(s[i] - y[i]) > margin:
            if (s[i] - y[i]) <= 0:
                break

        if i == 0:
            abs_diff = np.abs(y - s)
        else:
            abs_diff = np.abs(y[:i] - s[:i])
        
        margin = np.max(abs_diff)*(1-pct_fit_pnt)
        pct_thresh = max(s[0] - margin, pct_min_rf)
        
        if verbose:
            plt.figure(figsize = figsize, dpi=100)
            plt.plot(x, y)
            plt.plot(x, s)
            a = pct_thresh
            plt.plot([0,len(nn)-1], [a,a])
            a = pct_thresh + margin
            # plt.plot([0,len(nn)-1], [a,a], '--')
            plt.xlabel('Cluster order [$k$]', fontsize = 12)
            plt.ylabel('$q_k=$P[score >=$s_{th}$ in cluster $k$]', fontsize = 12)
            plt.title(title, fontsize = 14)
            plt.ylim([0,1.2])
            plt.grid()
            plt.legend(['$q_k$', 'Linear fit', 'Rejection threshold'])
            pass            
    else:
        pct_thresh = PCT_THRESHOLD_MAX
        margin = 0
    
    return pct_thresh, margin


def run_gsa_and_clf(X_pca, Xs, cobj, y_clust, mkr_lst, mkr_lst_neg, method = 'gmm', 
                     N_components = 8, pval_th = 0.05, pct_fit_pnt = 0.3, pct_min_rf = 1,
                     Target_FPR = 0.05, pmaj = 0, minor_id_sep = True, min_logP_diff = 3,
                     thresholding = False, pct_cutoff = False, cbc_cutoff = 0.01, verbose = False,
                     df_GSA_score = None, N_cells_max_for_gmm = 20000, max_Q90 = 15, score_adj_weight = {} ):
    
    if df_GSA_score is None:
        df_res, df_GSA_score, dfn = GSA_cell_subtyping( Xs, mkr_lst, mkr_lst_neg, max_Q90 = max_Q90, 
                                                        score_adj_weight = score_adj_weight, verbose = verbose )
    else:
        df_res = get_stat_gsa( df_GSA_score )

    #######################################################
    ## Compute GSA thresholds Even if thresholding is False
    
    log_pv_th = -np.log10(pval_th)

    ## Find the GLOBAL threshold for each cell type
    th_dict, m1m2_ratio = get_threshold_from_GSA_result(df_res, 
                                            pval_th = pval_th, 
                                            target_FPR = Target_FPR, 
                                            verbose = verbose)
            
    if (pct_cutoff) & (len(list(set(y_clust))) >= 6):
        score = df_res['-logP'].copy(deep=True)
        pct_thresh, margin = find_pct_cutoff(score, y_clust, log_pv_th,
                                             pct_fit_pnt = pct_fit_pnt, 
                                             pct_min_rf = pct_min_rf, verbose = False)
        # pct_thresh = min(max(pct_thresh, 1-pmaj), PCT_THRESHOLD_MAX)
    else:
        pct_thresh = 0.25

    # print('Before thresholding: ', df_res['cell_type(rev)'].value_counts())

    pct_thresh = min(pct_min_rf, pct_thresh)
    clst_to_exclude = []
        
    ## Apply GSA thresholds If thresholding is True
    if pct_cutoff: ## i.e. for major type
        if thresholding:

            cluster_lst = list(set(y_clust))
            cluster_lst.sort()

            if pct_cutoff & verbose: 
                print('P[Pv<Th] cutoff = %4.2f(%4.2f)' % (pct_thresh, margin), end = '')

            cnt = 0
            for clst in cluster_lst:
            ## For each cluster,
                ## select cells in the cluster
                b = y_clust == clst
                pct = (df_res.loc[b, '-logP'] >= log_pv_th).sum()/np.sum(b)
                if pct < pct_thresh:
                    cnt += 1
                    if verbose:
                        cnt_tbl = df_res.loc[b, 'cell_type(rev)'].value_counts()
                        majority = cnt_tbl.index.values[0]
                        print(', %s(%4.2f, maj:%s)' % (str(clst), pct, majority), end = '')
                        # print('   Cluster %2s : %4.2f' % (str(clst), pct))

                    df_res.loc[b, 'cell_type(rev)'] = 'unassigned'
                    df_res.loc[b, 'Clarity'] = 'Unclear'

                    clst_to_exclude.append(clst)
                else:
                    ## Find majority cell
                    cnt_tbl = df_res.loc[b, 'cell_type(1st)'].value_counts()
                    # idx = cnt_tbl.index.values
                    majority = cnt_tbl.index.values[0]
                    if cnt_tbl[majority] >= cnt_tbl.sum()*pmaj:
                        df_res.loc[b, 'cell_type(rev)'] = majority
                        df_res.loc[b, 'Clarity'] = '-'
                    else:
                        if minor_id_sep:
                            df_res.loc[b, 'cell_type(rev)'] = majority
                            df_res.loc[b, 'Clarity'] = '-'
                        else:
                            pass

            if verbose: 
                if pct_cutoff:
                    print(' --> %i cluster(s) among %i excluded. ' % (cnt, len(cluster_lst)))
            else:
                # print('.', end = '', flush = True)
                pass
                            
        # print('After thresholding: ', df_res['cell_type(rev)'].value_counts())

        celltypes = list(th_dict.keys())
        df_res['>=th'] = True
        for ct in th_dict.keys():
            bt = df_res['cell_type(rev)'] == ct
            bh = df_res['-logP'] < th_dict[ct]
            if np.sum(bt&bh) >= 10:
                df_res.loc[bt&bh, '>=th'] = False
            elif np.sum(bt) < 10:
                df_res.loc[bt, '>=th'] = False
                
    else: ## i.e. minor type or subset 
        
        ## Apply GSA thresholds If thresholding is True
        if thresholding:
            celltypes = list(th_dict.keys())
            df_res['>=th'] = True
            for ct in th_dict.keys():
                bt = df_res['cell_type(rev)'] == ct
                bh = df_res['-logP'] < th_dict[ct]
                df_res.loc[bt&bh, 'cell_type(rev)'] = 'unassigned'
                df_res.loc[bt&bh, '>=th'] = False

            y_pred = df_res['cell_type(rev)']
            if verbose:
                b_cur = y_pred == 'unassigned'
                print('Num of unassigned cells: %i among %i' % (np.sum(b_cur), len(b_cur)))

            df_res['cell_type'] = y_pred
                
    
    ys = df_res['cell_type(rev)'].copy(deep=True)    
    df_res['cell_type(rev2)'] = ys
    
    class_names = list(df_GSA_score.columns.values)     
    if method == 'logreg':
        y_pred, df_score = C_major_logreg(X_pca, ys, class_names, 
                                          verbose = verbose )
    elif method == 'gmm':
        y_pred, df_score = C_major_gmm(X_pca, ys, class_names, 
                                   method = method, 
                                   N_components = N_components, 
                                   N_cells_max = N_cells_max_for_gmm, verbose = verbose )
            
        ## reject if GMM score > 0
        # MinV = df_score.min().min()
        if df_score.shape[1] > 0:
            for i in range(df_score.shape[0]):
                score = df_score.iloc[i].copy(deep = True)
                b = score > 0
                score[b] = 0 # MinV
                df_score.iloc[i] = list(score)
    else: 
        y_pred = ys
        df_score = None

    if pct_cutoff: ## i.e. for major type        
        for clst in clst_to_exclude:
            b = y_clust == clst
            y_pred[b] = 'unassigned'
            
    # df_score = df_score + df_GSA_score.clip(upper = 5)
    
    df_res['cell_type(rev3)'] = y_pred
    # print('After gmm: ', df_res['cell_type(rev3)'].value_counts())
    
    if (method is not None) & (df_score is not None): 
        if (thresholding): 
            if (df_score.shape[1] <= 1):
                y_pred = ys
            else:
                df_summary = get_stat(df_score)                
                th_dict, diff_dict = get_threshold_from_GMM_result(df_summary, 
                                                    target_FPR = Target_FPR, 
                                                    verbose = verbose, 
                                                    plot_hist = False ) # print_report) 

                label_lst = list(y_pred.unique())
                for label in label_lst:
                    if (label != 'unassigned') & (label in th_dict.keys()):
                        b1 = y_pred == label
                        b2 = df_summary['Score'] <  th_dict[label]
                        b3 = df_res['-logP-logP(2nd)'] < min_logP_diff
                        y_pred[b1&b2&b3] = 'unassigned'

                bx = ys == 'unassigned' ##
                bx = y_pred == 'unassigned' # not working
                for clst in cluster_lst:
                    b = y_clust == clst
                    ## If the majority of a cluster is unassigned,
                    ## set all the cells in the cluster unassigned
                    # if False: # np.sum(b&bx) > np.sum(b)*pmaj:
                    #     y_pred[b] = 'unassigned'
                    if np.sum(b&(~bx)) > 0:
                        cnt_tbl = y_pred[b&(~bx)].value_counts()
                        # idx = cnt_tbl.index.values
                        majority = cnt_tbl.index.values[0]
                        if cnt_tbl[majority] >= cnt_tbl.sum()*pmaj:
                            y_pred[b] = majority
                        else:
                            pass
                            
    # print('After gmm th: ', y_pred.value_counts())
    
    df_res['cell_type(rev4)'] = y_pred
    bx = y_pred == 'unassigned'
    
    if SKNETWORK:
        if pct_cutoff & (isinstance(cobj, Louvain)) & (cbc_cutoff > 0): # apply only for major type
            y_pred = cluster_basis_correction(X_pca, y_pred, 
                           cobj, y_clust, pmaj = pmaj, 
                           cutoff = cbc_cutoff, verbose = verbose)
        
    if verbose:
        b_cur = y_pred == 'unassigned'
        print('Num of unassigned cells: %i among %i' % (np.sum(b_cur), len(b_cur)))
    else:
        if pct_cutoff: 
            # print('.', end = '', flush = True)
            pass
        
    df_res['cell_type'] = y_pred
    return df_res, df_score, df_GSA_score


def check_if_separable_pairwise(df_score, y_true):
    
    label = list(df_score.columns.values)        
    aucs = pd.DataFrame( np.ones([len(label),len(label)])*SEPARABILITY_AUC_INIT_VALUE, 
                         index = label, columns = label )
    
    for k, lr in enumerate(label):
        for m, lc in enumerate(label):
            if lr != lc:
                br = y_true == lr
                bc = y_true == lc
                if (np.sum(br) < SEPARABILITY_MIN_NUM_CELLS) | (np.sum(bc) < SEPARABILITY_MIN_NUM_CELLS):
                    aucs.loc[lr,lc] = 1
                    pass
                else:
                    bs = br | bc
                    y_conf_1 = df_score.loc[bs, lr]
                    y_conf_0 = df_score.loc[bs, lc]
                    y_odd = y_conf_1 - y_conf_0
                    y = y_true[bs]

                    bn = (~np.isnan(y_odd))
                    y_odd = y_odd[bn]
                    y = y[bn]

                    target = lr
                    try:
                        # fpr, tpr, _ = roc_curve(y.ravel(), y_odd.ravel(), pos_label = target)
                        fpr, tpr, _ = roc_curve(y, y_odd, pos_label = target)
                        roc_auc = auc(fpr, tpr)
                        aucs.loc[lr,lc] = roc_auc
                    except:
                        print('WARNING: cannot determine the separability for %s' % target)        
    return aucs

def separability_check_pairwise(df_score, ys, mkr_lst, 
                                dict_celltype_comb, verbose = False):
    
    aucs = check_if_separable_pairwise(df_score, ys)
    idxc_vec = aucs.idxmin(axis = 1)
    mina_vec = aucs.min(axis = 1)
    idxr = mina_vec.idxmin()
    idxc = idxc_vec[idxr]
    
    min_auc = aucs.loc[idxr, idxc]
    b_ok = True
    if min_auc < SEPARABILITY_THRESHOLD:
        b_ok = False
    
    if b_ok:
        if verbose: 
            print('Separability check passed: Min.AUC = %6.4f btn %s and %s' % (min_auc, idxr, idxc))
    else:
        if verbose: 
            print('Separability check failed: Min.AUC = %6.4f btn %s and %s' % (min_auc, idxr, idxc))
        names = '%s and %s' % (idxr, idxc)
        new_name = '%s_or_%s' % (idxr, idxc)
        genes = list(set(mkr_lst[idxr] + mkr_lst[idxc]))
        to_comb_name = [idxr, idxc]
        
        dict_celltype_comb[new_name] = to_comb_name
        mkr_lst[new_name] = genes
        
        del mkr_lst[idxr]                        
        del mkr_lst[idxc]                        
        if idxr in dict_celltype_comb.keys():
            del dict_celltype_comb[idxr]
        if idxc in dict_celltype_comb.keys():
            del dict_celltype_comb[idxc]
                
        if verbose: 
            print('Separability check WARNING: %s are not clearly separable.' % names)
            # print('%s are not clearly separable -> combined into one major type.' % names)
    
    return b_ok, mkr_lst, dict_celltype_comb


def rem_minor( mkr_dict, to_rem_lst ):

    cts = list(mkr_dict.keys())
    if len(to_rem_lst) > 0:
        for c in cts:
            if c in to_rem_lst:
                del mkr_dict[c]
                
    return mkr_dict


def get_maj(ivec, cto, p_cells_dict, p_min = 0.1):

    items = list(set(ivec))
    if len(items) == 1:
        return cto
    
    Num = np.zeros(len(items))
    Score = np.zeros(len(items))
    for k, item in enumerate(items):
        b = ivec == item
        Num[k] = np.sum(b)
        
    k = np.argmax(Num)

    b = False
    if items[k] == STR_UNASSIGNED:
        odr = (-Num).argsort()        
        if len(odr) > 1:
            if Num[odr[1]] >= round(np.sum(Num)*(p_min)):
                k = odr[1]
            # elif Num[k] <= round(np.sum(Num)*(1-p_min)):
            #     return cto
       
    return  items[k]


def apply_knn(nei_indices, cell_type, score, pmaj = 0.25, nlog_pval_th = 2):

    cell_type_new = cell_type.copy(deep = True)
    idx_ary = cell_type.index.values
    N_nei = nei_indices.shape[1]
    sidx_ary = score.index.values
    score2 = score.copy(deep = True)
    for k in range( len(cell_type) ):
        
        ## Update Cell type using majority votong
        nlst = list(nei_indices.iloc[k,:].astype(int))
        ilst = idx_ary[nlst]
        cts = cell_type[ list(ilst) ]
        if len(set(list(cts))) <= 1:
            pass
        else:
            cnt_tbl = cts.value_counts()
            majority = cnt_tbl.index.values[0]

            if majority == 'unassigned':
                majority = cnt_tbl.index.values[1]
                cell_type_new[idx_ary[k]] = cnt_tbl.index.values[1]
            else: 
                if (cell_type[k] == 'unassigned'):
                    cell_type_new[idx_ary[k]] = majority
                elif (score.loc[sidx_ary[k], cell_type[k]] < nlog_pval_th):
                    cell_type_new[idx_ary[k]] = majority
                else:
                    if cnt_tbl[majority] > N_nei*pmaj:
                        cell_type_new[idx_ary[k]] = majority
            
            ## Update score
            '''
            sm = score.loc[ilst,:].sum(axis=0)
            score2.iloc[k,:] = list( sm )
            #'''
            
    return cell_type_new, score2
    

def apply_knn1(nei_indices, cell_type, score, pmaj = 0.25, nlog_pval_th = 2):

    cell_type_new = cell_type.copy(deep = True)
    idx_ary = cell_type.index.values
    N_nei = nei_indices.shape[1]
    sidx_ary = score.index.values
    score2 = score.copy(deep = True)
    for k in range( len(cell_type) ):
        
        ## Update Cell type using majority votong
        nlst = list(nei_indices.iloc[k,:].astype(int))
        ilst = idx_ary[nlst]
        cts = cell_type[ list(ilst) ]
        if len(set(list(cts))) <= 1:
            pass
        else:
            cnt_tbl = cts.value_counts()
            majority = cnt_tbl.index.values[0]

            if majority == 'unassigned':
                majority = cnt_tbl.index.values[1]
                cell_type_new[idx_ary[k]] = majority
                
            if cnt_tbl[majority] > N_nei*pmaj:
                cell_type_new[idx_ary[k]] = majority
            
            ## Update score
            #'''
            b = cts == majority
            sm = score.loc[ilst,:].mean(axis=0)
            score2.iloc[k,:] = list( sm )
            #'''
            
    return cell_type_new, score2
    

def apply_knn2(nei_indices, cell_type, score, pmaj = 0.5, nlog_pval_th = 2):

    cell_type_new = cell_type.copy(deep = True)
    idx_ary = cell_type.index.values
    N_nei = nei_indices.shape[1]
    score2 = score.copy(deep = True)
    for k in range( len(cell_type) ):
        nlst = list(nei_indices.iloc[k,:].astype(int))
        ilst = list(idx_ary[nlst])
        sm = score.loc[ilst,:].mean(axis=0)
        score2.iloc[k,:] = list( sm )
        
    ## Update Cell type using updated score
    cell_type_new = score2.idxmax(axis = 1)
            
    return cell_type_new, score2
    

def get_stat_gsa( df_score ):
    
    df = df_score
    name = list(df.columns.values)
    
    if df.shape[1] == 1:
        c = name[0]
        neg_log_pval = df[c]
        subtype = [c]*df.shape[0]
        
        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype, 'Overlap': ['-']*df.shape[0] },
                               index = df.index.values)
        df_res['cell_type(2nd)'] = subtype
        df_res['Overlap(2nd)'] = ['-']*df.shape[0]
        df_res['Clarity'] = ['-']*df.shape[0]
        df_res['-logP'] = df[c]
        df_res['-logP(2nd)'] = [0]*df.shape[0]
        df_res['-logP-logP(2nd)'] = df[c]

        # df_res['Overlap'] = df_res['Overlap'].astype(str)
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(str)
        
    else:
        maxv = list(df.max(axis = 1))
        subtype = list(df.idxmax(axis = 1))
        #tc_subtype = [trans_dict[k] for k in tc_subtype]

        maxv2 = []
        idx2 = []
        subtype_lst = list(df.columns.values)

        for i in range(df.shape[0]):
            x = np.array(df.iloc[i])
            odr = (-x).argsort()
            if len(x) > 1:
                maxv2.append(x[odr[1]])
                idx2.append(subtype_lst[odr[1]])
            else:
                maxv2.append(0)
                idx2.append(None)

        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype, 'Overlap': ['-']*df.shape[0],
                               'cell_type(2nd)': idx2, 'Overlap(2nd)': ['-']*df.shape[0],
                               'Clarity': ['-']*df.shape[0], '-logP': maxv, '-logP(2nd)': maxv2}, 
                              index = df.index.values)
        df_res['-logP-logP(2nd)'] = df_res['-logP'] - df_res['-logP(2nd)']

        # df_res['Overlap'] = df_res['Overlap'].astype(str)
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(str)
    
    return df_res


def get_stat_gsa_250315( df_score ):
    
    df = df_score
    name = list(df.columns.values)
    
    if df.shape[1] == 1:
        c = name[0]
        neg_log_pval = df[c]
        subtype = [c]*df.shape[0]
        
        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype}, # 'Overlap': [-1]*df.shape[0] },
                               index = df.index.values)
        df_res['cell_type(2nd)'] = subtype
        # df_res['Overlap(2nd)'] = [-1]*df.shape[0]
        df_res['Clarity'] = ['-']*df.shape[0]
        df_res['-logP'] = df[c]
        df_res['-logP(2nd)'] = [0]*df.shape[0]
        df_res['-logP-logP(2nd)'] = df[c]

        # df_res['Overlap'] = df_res['Overlap'].astype(int)
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(int)
        
    else:
        maxv = list(df.max(axis = 1))
        subtype = list(df.idxmax(axis = 1))
        #tc_subtype = [trans_dict[k] for k in tc_subtype]

        maxv2 = []
        idx2 = []
        subtype_lst = list(df.columns.values)

        for i in range(df.shape[0]):
            x = np.array(df.iloc[i])
            odr = (-x).argsort()
            if len(x) > 1:
                maxv2.append(x[odr[1]])
                idx2.append(subtype_lst[odr[1]])
            else:
                maxv2.append(0)
                idx2.append(None)

        df_res = pd.DataFrame({'cell_type': subtype, 'cell_type(rev)': subtype, 
                               'cell_type(1st)': subtype, # 'Overlap': [-1]*df.shape[0],
                               'cell_type(2nd)': idx2, # 'Overlap(2nd)': [-1]*df.shape[0],
                               'Clarity': ['-']*df.shape[0], '-logP': maxv, '-logP(2nd)': maxv2}, 
                              index = df.index.values)
        df_res['-logP-logP(2nd)'] = df_res['-logP'] - df_res['-logP(2nd)']

        # df_res['Overlap'] = df_res['Overlap'].astype(int)
        # df_res['Overlap(2nd)'] = df_res['Overlap(2nd)'].astype(int)
    
    return df_res


def get_markers_all(mkr_file, target_lst, pnsh12, level = 1, comb_mkrs = False):
    
    # target = 'Myeloid cell'
    if level == 1:
        mkr_dict, mkr_dict_neg = \
            get_markers_minor_type2(mkr_file, target_cells = target_lst, 
                                    pnsh12 = pnsh12, rem_common = False,
                                    comb_mkrs = comb_mkrs, verbose = False)
    else:
        mkr_dict, mkr_dict_neg = \
            get_markers_cell_type(mkr_file, target_cells = target_lst, pnsh12 = pnsh12,
                          rem_common = False, verbose = False)
        
    mkrs_all = [] #['SELL']
    mkrs_cmn = []
    for ct in mkr_dict.keys():
        mkrs_all = mkrs_all + mkr_dict[ct]
        if len(mkrs_cmn) == 0:
            mkrs_cmn = mkr_dict[ct]
        else:
            mkrs_cmn = list(set(mkrs_cmn).intersection(mkr_dict[ct]))

    mkrs_all = list(set(mkrs_all))
    
    return mkrs_all, mkr_dict


def HiCAT( X_cell_by_gene, marker_file, X_pca = None, log_transformed = False,
               target_tissues = [], target_cell_types = [], minor_types_to_exclude = [], 
               mkr_selector = PNSH12, N_neighbors_minor = 31, N_neighbors_subset = 1,  
               Clustering_algo = 'lv', Clustering_resolution = 1, 
               Clustering_base = 'pca', N_pca_components = 15, 
               N_cells_max_for_pca = 100000, N_cells_max_for_gmm = 20000,
               cycling_cell = False, copy_X = False, verbose = 1, print_prefix = '   ',
               model = 'gmm', N_gmm_components = 10, cbc_cutoff = 0.01,
               Target_FPR = 0.05, pval_th = 0.05, pval_th_subset = 1, 
               pmaj = 0.7, pth_fit_pnt = 0.4, pth_min = 0.5, min_logP_diff = 1, 
               use_minor = True, minor_wgt = 0, use_union = False, use_union_major = True,
               use_markers_for_pca = False, comb_mkrs = False, 
               knn_type = 1, knn_pmaj = 0.3, N_max_to_ave = 1,
               thresholding_minor = False, thresholding_subset = False,
               ident_level = 3, max_Q90 = 12, score_adj_weight = {} ):

    if len(target_cell_types) > 0:
        pass
        # target_cell_types = target_cell_types_in
    elif len(target_tissues) > 0:
            target_cell_types = get_target_cell_types( marker_file, target_tissues )
            # print('Target cell types: ', target_cell_types)

    if CLUSTERING_AGO != 'lv':
        Clustering_algo = CLUSTERING_AGO
        
    rem_cmn_mkr = False
    minor_id_sep = True
    
    gene_names = None
    method = model
    N_components = N_gmm_components
    start_time = time.time()
    dict_summary_res = {}
    dict_summary_score = {}
    dict_summary_score2 = {}
    dict_summary_score3 = {}
    
    if Target_FPR >= 1:
        thresholding = False
    else:
        thresholding = True
        
    if verbose > 1: print('HiCAT running ..', flush = True)
    elif verbose == 1: 
        # print('HiCAT running ..', end = '', flush = True)
        pass
    elif verbose == 0:
        print('HiCAT running ..', end = '', flush = True)
        
    if isinstance(X_cell_by_gene, pd.DataFrame):
        if copy_X:
            Xs = X_cell_by_gene.copy(deep=True)
        else:
            Xs = X_cell_by_gene
        genes_lst_org = list(X_cell_by_gene.columns.values)

        genes_lst = []
        for g in genes_lst_org:
            genes_lst.append(g.upper())
        rend = dict(zip(genes_lst_org, genes_lst))
        Xs.rename(columns = rend, inplace = True)
            
    else:
        Tiden_print_error()
        return -1

    ### Correct Major type
    etime = round(time.time() - start_time)        
    start_time_new = time.time()
    if verbose > 1: print('Preproc .. ', end = '', flush = True)
    elif verbose == 1:     
        # print('.', end = '', flush = True)
        print('%sHiCAT preprocessing ' % print_prefix, flush = True)
    elif verbose == 0:
        print('.', end = '', flush = True)
        
    if use_markers_for_pca:
        if verbose > 1: print('Using Mkrs .. ', end = '', flush = True)
        mkrs_all, mkrs_dict = get_markers_all(marker_file, target_lst = [], pnsh12 = mkr_selector,
                                              level = 1, comb_mkrs = comb_mkrs)
        genes = list(Xs.columns.values)
        mkrs_all = list(set(mkrs_all).intersection(genes))
        Xs = Xs[mkrs_all]
    else:
        mkrs_all = list(Xs.columns.values)

    N_components_pca = N_pca_components
    if X_pca is None:
        Xx = X_preprocessing( csr_matrix(Xs), log_transformed ) 
        Xx = pd.DataFrame( Xx.todense(), index = Xs.index, columns = Xs.columns )
        if verbose > 1: print('(%i), VGS .. ' % int(etime), end = '', flush = True)
        Xx = X_variable_gene_sel( Xx, N_genes = 2000, N_cells_max = N_cells_max_for_pca, vg_sel = True )
        variable_genes = list(Xx.columns.values)
        
        etime = round(time.time() - start_time_new)        
        start_time_new = time.time()
        if verbose > 1: print('(%i), PCA .. ' % int(etime), end = '', flush = True)
        elif verbose == 1: 
            # print('%sHiCAT PCA & clustering ' % print_prefix, flush = True)
            pass
        elif verbose == 0:
            print('P%i.' % etime, end = '', flush = True)
            
        N_components_pca = N_pca_components
        X_pca = pca_subsample(Xx, N_components_pca, N_cells_max_for_pca = N_cells_max_for_pca) 
        del Xx
        
    X_pca = pd.DataFrame(X_pca, index = Xs.index, columns = list(np.arange(int(N_components_pca))))
    
    N_clusters = int(25*np.sqrt(Clustering_resolution))
    MaxNcomp = N_clusters
    sqrtN = int(np.sqrt(X_pca.shape[0])/2)
    N_comp = min(MaxNcomp, sqrtN)
    
    etime = round(time.time() - start_time_new)        
    start_time_new = time.time()
    if verbose > 1: print('(%i), Clustering .. ' % int(etime), end = '', flush = True)
    elif verbose == 1:
        # print('%sHiCAT clustering ' % print_prefix, flush = True)
        pass
    elif verbose == 0: 
        print('P%i.' % etime, end = '', flush = True)
    
    ## Clustering
    if X_pca.shape[0] <= N_cells_max_for_pca:
        y_clust, cobj, adj = clustering_alg( X_pca, clust_algo = Clustering_algo, N_clusters = N_comp, 
                                         resolution = Clustering_resolution,
                                         N_neighbors = 12, mode='connectivity', n_cores = 4 )
    else:
        neighbors, distances = None, None
        y_clust, cobj, adj = clustering_subsample( X_pca, neighbors, distances, 
                                               clust_algo = Clustering_algo, N_clusters = N_comp, 
                                               resolution = Clustering_resolution, N_neighbors = 12, 
                                               mode='connectivity', n_cores = 4, 
                                               Ns = N_cells_max_for_pca, Rs = 0.95 )        
    ## End of Clustering 
    
    rend = {}
    for i in list(X_pca.columns.values):
        rend[i] = str(i)
    X_pca.rename(columns = rend, inplace = True)

    # dict_summary_res['Xpca'] = X_pca
    
    etime = round(time.time() - start_time_new)        
    start_time_new = time.time()
    if verbose > 1: print('(%i), Nc = %i, ' % (int(etime), len(set(y_clust))), end = '', flush = True)
    elif verbose == 1:
        print('%sHiCAT major type identification ' % print_prefix, flush = True)
    elif verbose == 0: 
        print('C%i.' % etime, end = '', flush = True)
       
    ##### Major type identification for target cell selection
    dict_celltype_comb = {}

    if True:
        target_cell = target_cell_types
        mkr_lst, mkr_lst_neg = get_markers_major_type(marker_file, target_cell, 
                                        pnsh12 = mkr_selector, rem_common = rem_cmn_mkr, verbose = (verbose > 1))
        
        ##############################
        ## Get minor type markers
        if not use_union_major:            
            mkr_lst_subset, mkr_lst_subset_neg, mkr_lst_subset_sec, map_dict_sub2maj, map_dict_sub2min = \
                load_markers_all(marker_file, target_cells = target_cell, pnsh12 = mkr_selector, 
                                 comb_mkrs = comb_mkrs,  verbose = False)

            map_dict_maj2sub = {}
            for key in map_dict_sub2maj.keys():
                mjt = map_dict_sub2maj[key]
                if mjt not in list(map_dict_maj2sub.keys()):
                    map_dict_maj2sub[mjt] = [key]
                else:
                    map_dict_maj2sub[mjt].append(key)

            map_dict_min2sub = {}
            for key in map_dict_sub2min.keys():
                mjt = map_dict_sub2min[key]
                if mjt not in list(map_dict_min2sub.keys()):
                    map_dict_min2sub[mjt] = [key]
                else:
                    map_dict_min2sub[mjt].append(key)

            df_res_subset_all, df_GSA_score_subset_all, dfn_subset_all = \
                GSA_cell_subtyping( Xs, mkr_lst_subset, mkr_lst_subset_neg, max_Q90 = max_Q90, 
                                    score_adj_weight = score_adj_weight, verbose = (verbose > 1) )
            
            if verbose == 1: 
                etime = round(time.time() - start_time_new)        
                start_time_new = time.time()
                # print('%i.' % etime, end = '', flush = True)
                # print('.', end = '', flush = True)
        ##############################
        
        if target_cell_types is None:
            target_cell_types = list(mkr_lst.keys())
        elif len(target_cell_types) == 0:
            target_cell_types = list(mkr_lst.keys())
        else:
            sm = ''
            for key in list(set(target_cell_types).difference(list(mkr_lst.keys()))):
                sm = sm + '%s,' % key
            if (verbose > 1) & (len(sm) > 0): 
                print('INFO: The marker db does not contain %s' % sm[:-1])
            target_cell_types = list(set(target_cell_types).intersection(mkr_lst.keys()))
            
        mkrs_all = []
        for key in mkr_lst.keys():
            mkrs_all = mkrs_all + mkr_lst[key]
        mkrs_all = list(set(mkrs_all))
        mkrs_exist = list(set(mkrs_all).intersection(genes_lst))
        
        pct_r = len(mkrs_exist)/len(mkrs_all)
        if pct_r == 0:
            print('ERROR: No marker genes found in the data.')
            return None, None
        
        pval_th = min( pval_th/pct_r, 0.1 )
        pct_th_min = pth_min*pct_r
        
        if (verbose >= 1) & (pct_r < 0.9): 
            # print('PCT reduction factor = %4.2f' % pct_r)
            print('%sWARNING: Some markers not present. pv_th, min_pth -> %5.3f, %5.3f' % \
                  (print_prefix, pval_th, pct_r*PCT_THRESHOLD_MIN))
            # print('INFO: Too many markers not present. min_pth -> %5.3f' % (pct_r*PCT_THRESHOLD_MIN))

        for loop in range(len(target_cell_types)):
        # loop = 0
        # if True:  
            # use_union_major = use_union
            if use_union_major:
                df_pass = None
            else:
                df_GSA_score_subset = df_GSA_score_subset_all
                major_type_lst = list(map_dict_maj2sub.keys())
                df_GSA_score_major = pd.DataFrame(index = Xs.index, columns = major_type_lst)
                dfn_subset = dfn_subset_all
                dfn_major = pd.DataFrame(index = Xs.index, columns = major_type_lst)
                for major in major_type_lst:
                    sub_lst = map_dict_maj2sub[major]
                    if len(sub_lst) == 1:
                        best_score = df_GSA_score_subset[sub_lst[0]]
                        dfn_major[major] = dfn_subset[sub_lst[0]]
                    else:
                        subsets = df_GSA_score_subset[sub_lst].idxmax(axis = 1)
                        for k, s in enumerate(list(subsets)):
                            idx = Xs.index[k]
                            dfn_major.loc[idx,major] = dfn_subset.loc[idx,s]
                        
                        if N_max_to_ave <= 1:
                            best_score = df_GSA_score_subset[sub_lst].max(axis = 1)
                        else:
                            n_max = min(N_max_to_ave, len(sub_lst))
                            best_score = np.sort(df_GSA_score_subset[sub_lst], axis=1)[:, -n_max:].mean(axis = 1)

                    df_GSA_score_major[major] = best_score 
                    
                df_pass = df_GSA_score_major
                
            df_res_major, df_score_major, df_GSA_score_major = \
                run_gsa_and_clf( X_pca, Xs, cobj, y_clust, mkr_lst, mkr_lst_neg, 
                                 method = 'gmm', N_components = N_components, pval_th = pval_th, 
                                 pct_fit_pnt = pth_fit_pnt, pct_min_rf = pct_th_min,
                                 Target_FPR = Target_FPR, pmaj = pmaj, minor_id_sep = minor_id_sep,
                                 min_logP_diff = min_logP_diff, thresholding = thresholding,
                                 pct_cutoff = True, cbc_cutoff = cbc_cutoff, verbose = (verbose > 1),
                                 df_GSA_score = df_pass, N_cells_max_for_gmm = N_cells_max_for_gmm, 
                                 max_Q90 = max_Q90, score_adj_weight = score_adj_weight)
            if not use_union_major:
                idxs = df_res_major.index.values
                for k, idx in enumerate(list(idxs)):
                    ct = df_res_major.loc[idx, 'cell_type(1st)']
                    df_res_major.loc[idx, 'Overlap'] = dfn_major.loc[idx,ct]
                    ct = df_res_major.loc[idx, 'cell_type(2nd)']
                    df_res_major.loc[idx, 'Overlap(2nd)'] = dfn_major.loc[idx,ct]

            y_pred_major = df_res_major['cell_type']
            ys_major = df_res_major['cell_type(rev)']

            # print(df_res_major.shape, df_score_major.shape, df_GSA_score_major.shape)
            if (len(target_cell_types) > 1) & (df_score_major is not None):
                if df_score_major.shape[1] > 0:
                    b_ok, mkr_lst, dict_celltype_comb = \
                        separability_check_pairwise( df_score_major, ys_major, 
                                            mkr_lst, dict_celltype_comb, (verbose > 1))
                else:
                    b_ok = True
                if b_ok: break
            else:
                break
                
        y_pred_correct = y_pred_major
        b_cur = y_pred_correct == 'unassigned'
        if (verbose > 1):
            print('Num of unassigned cells: %i among %i' % (np.sum(b_cur), len(b_cur)))

        etime = round(time.time() - start_time_new)        
        start_time_new = time.time()
        if (verbose > 1):
            print('Major cell type identification done. (%i)' % \
                   round(time.time() - start_time))
        elif verbose == 1: 
            # print('%sHiCAT major type identification done. (%i)' % (print_prefix, etime), flush = True)
            pass
        elif verbose == 0:
            print('M%i.' % etime, end = '', flush = True)

        df_pred2 = pd.DataFrame(index = df_res_major.index.values)
        df_pred2['cluster_rev'] = y_clust + 1
        df_pred2['cluster_rev'] = df_pred2['cluster_rev'].astype(str)
        
        df_pred = pd.DataFrame({'cell_type_major': y_pred_correct},
                                index = df_res_major.index.values)
        df_pred['cell_type_minor'] = 'unassigned'
        df_pred['cell_type_subset'] = 'unassigned'
        df_pred['cluster'] = y_clust + 1
        df_pred['cluster'] = df_pred['cluster'].astype(str)

        df_pred['cell_type_major(1st)'] = df_res_major['cell_type(1st)'].astype(str)
        df_pred['Confidence(1st)'] = df_res_major['-logP'].astype(float)
        df_pred['cell_type_major(2nd)'] = df_res_major['cell_type(2nd)'].astype(str)
        df_pred['Confidence(2nd)'] = df_res_major['-logP(2nd)'].astype(float)
        

        # df_res_major['Overlap'] = df_res_major['Overlap'].astype(str)
        # df_res_major['Overlap(2nd)'] = df_res_major['Overlap(2nd)'].astype(str)

        dict_summary_res['Major_Type'] = df_res_major
        dict_summary_score['Major_Type'] = df_score_major
        dict_summary_score2['Major_Type'] = df_GSA_score_major
        
    #'''
    ##### Minor type identification for selected cells
    if ident_level > 1:
                 
        if verbose == 1:
            print('%sHiCAT minor type identification' % (print_prefix), flush = True)
        
        df_pred['cell_type_minor(1st)'] = df_pred['cell_type_major(1st)'].astype(str)
        df_pred['Confidence_minor(1st)'] = df_pred['Confidence(1st)'].astype(float)
        df_pred['cell_type_minor(2nd)'] = df_pred['cell_type_major(2nd)'].astype(str)
        df_pred['Confidence_minor(2nd)'] = df_pred['Confidence(2nd)'].astype(float)
        
        ## Cluster basis target cells Selection 
        b_sel = y_pred_correct != 'unassigned'
        b_sel[:] = False
        cluster_lst = list(set(y_clust))
        for clst in cluster_lst:
            bc = y_clust == clst
            ba = y_pred_correct == 'unassigned'
            if np.sum(bc&ba) <= np.sum(bc)*pmaj:
                b_sel[bc] = True

        ## Run GSA and perform identification
        X_sel = Xs.loc[b_sel,:]
        X_pca_sel = X_pca.loc[b_sel,:]
        y_clust_sel = y_clust[b_sel]
        y_pred_sel = y_pred_correct[b_sel]

        ## Get cell-type lists
        target_cell_lst = {} # target_cell_types
        for c in mkr_lst.keys():
            if c in dict_celltype_comb.keys():
                target_cell_lst[c] = dict_celltype_comb[c]
            elif c in target_cell_types:
                target_cell_lst[c] = [c]

        mkr_lst = {}
        mkr_lst_neg = {}
        for c in target_cell_lst.keys():
            target_cell = target_cell_lst[c]
            mkr_lst_tmp, mkr_lst_neg_tmp = get_markers_cell_type(marker_file, target_cell, 
                                            pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                                                 verbose = False)
            mkr_lst.update(mkr_lst_tmp)
            mkr_lst_neg.update(mkr_lst_neg_tmp)

        if len(minor_types_to_exclude) > 0:
            mkr_lst = rem_minor( mkr_lst, minor_types_to_exclude )
            mkr_lst_neg = rem_minor( mkr_lst_neg, minor_types_to_exclude )
        
        ### To use in the subset identification
        mkr_lst_sav = copy.deepcopy(mkr_lst)

        idx_sel = X_pca_sel.index.values

        df_GSA_score_minor_all = pd.DataFrame(index = df_pred.index)
        
        cnt = 0
        for tc in target_cell_lst.keys():
            target_cell = target_cell_lst[tc]
            mkr_lst, mkr_lst_neg = get_markers_cell_type(marker_file, target_cell, 
                                            pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                                         verbose = False)

            if len(minor_types_to_exclude) > 0:
                mkr_lst = rem_minor( mkr_lst, minor_types_to_exclude )
                mkr_lst_neg = rem_minor( mkr_lst_neg, minor_types_to_exclude )
    
            sm = ''
            for key in mkr_lst.keys():
                sm = sm + '%s,' % key
            if (verbose > 1) & (len(sm) > 1): print('%s minor type identification: %s' % (tc, sm[:-1]))

            b_cur = y_pred_sel == 'unassigned'
            b_cur[:] = False
            cluster_lst = list(set(y_clust_sel))

            #'''
            ba = y_pred_sel == tc
            for clst in cluster_lst:
                bc = y_clust_sel == clst
                if np.sum(bc&ba) >= np.sum(bc)*pmaj:
                    b_cur[bc] = True
                else:
                    b_cur[ba] = True
                    
            #'''
            
            ## Run GSA and perform identification
            X_cur = X_sel.loc[b_cur,:]
            X_pca_cur = X_pca_sel.loc[b_cur,:]
            y_clust_cur = y_clust_sel[b_cur]
            
            # thresholding_minor = thresholding_ms[0]
            # pct_cutoff_minor = pct_cutoff_ms[0]
            
            ## Redo PCA and Clustering #####
            minor_type_lst_cur = list(mkr_lst.keys())
            
            ### To be used to determine minor type for given subset
            map_dict_sub2min = {}
            map_dict_min2sub = {}
            for cx in minor_type_lst_cur: # for each minor type
                mkr_lst_tmp, mkr_lst_neg_tmp = get_markers_minor_type2(marker_file, [cx], 
                                        pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                        comb_mkrs = comb_mkrs, verbose = False)
                
                for key in mkr_lst_tmp.keys():
                    map_dict_sub2min[key] = cx
                map_dict_min2sub[cx] = list(mkr_lst_tmp.keys())
            
            ########################################################
            if not use_union:
                mkr_lst, mkr_lst_neg = get_markers_minor_type2(marker_file, minor_type_lst_cur, 
                                pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                comb_mkrs = comb_mkrs, verbose = False)

            if (len(list(mkr_lst.keys())) <= 1):
                idx = list(X_cur.index.values)
                ctn = 'unassigned'
                if len(list(mkr_lst.keys())) == 1:
                    ctn = list(mkr_lst.keys())[0]
                    
                df_pred.loc[idx,'cell_type_minor'] = str(ctn)
                df_pred.loc[idx,'cell_type_subset'] = str(ctn)
                
            elif np.sum(b_cur) > 0:   
                if (np.sum(b_cur) < N_neighbors_minor):
                    
                    if use_union:
                        df_res_cur, df_GSA_score_cur, dfn_cur = GSA_cell_subtyping( X_cur, mkr_lst, mkr_lst_neg, max_Q90 = max_Q90, 
                                                               score_adj_weight = score_adj_weight, verbose = (verbose > 1) )
                    else: 
                        # df_GSA_score_subset = df_GSA_score_subset_all.loc[X_pca_cur.index,:]
                        df_res_subset, df_GSA_score_subset, dfn_subset = \
                            GSA_cell_subtyping( X_cur, mkr_lst, mkr_lst_neg, max_Q90 = max_Q90, 
                                                score_adj_weight = score_adj_weight, verbose = (verbose > 1) )
                        
                        df_GSA_score_cur = pd.DataFrame(index = X_pca_cur.index, columns = minor_type_lst_cur)
                        
                        for minor in map_dict_min2sub.keys():
                            if minor in minor_type_lst_cur:
                                sub_lst = map_dict_min2sub[minor]
                                if len(sub_lst) == 1:
                                    best_score = df_GSA_score_subset[sub_lst[0]]
                                else:
                                    best_score = df_GSA_score_subset[sub_lst].max(axis = 1)
                                df_GSA_score_cur[minor] = best_score                             
                        df_res_cur = get_stat_gsa(df_GSA_score_cur)
                        
                    y_pred_cur = df_res_cur['cell_type']
                    df_score_cur = None
                    y_clust_cur[:] = 0
                    
                else:
                    ## Redo PCA and Clustering #####
                    # thresholding_minor = thresholding_ms[0]
                    # pct_cutoff_minor = pct_cutoff_ms[0]

                    '''
                    Xx_cur = X_preprocessing( X_cur, log_transformed ) #, N_genes = 2000, N_cells_max = N_cells_max_for_pca )
                    Xx_cur = X_variable_gene_sel( Xx_cur, N_genes = 2000, N_cells_max = N_cells_max_for_pca, vg_sel = True )

                    # X_pca_cur = pca.fit_transform(Xx_cur)
                    X_pca_cur = pca_subsample(Xx_cur, N_components_pca, N_cells_max_for_pca = N_cells_max_for_pca) 
                    del Xx_cur
                    
                    X_pca_cur = pd.DataFrame(X_pca_cur, index = X_cur.index, 
                                             columns = list(np.arange(int(N_components_pca))))

                    #'''
                    idx = list(X_cur.index.values)
                    X_pca_cur = X_pca.loc[idx,:]
                    
                    if X_pca_cur.shape[0] <= N_cells_max_for_pca:
                        y_clust_cur, cobj, adj = clustering_alg(X_pca_cur, clust_algo = Clustering_algo, 
                                                            N_clusters = N_comp, resolution = Clustering_resolution,
                                                            N_neighbors = 12, mode='connectivity', n_cores = 4)
                    else:
                        neighbors, distances = None, None
                        y_clust_cur, cobj, adj = clustering_subsample( X_pca_cur, neighbors, distances, 
                                               clust_algo = Clustering_algo, N_clusters = N_comp, 
                                               resolution = Clustering_resolution, N_neighbors = 12, 
                                               mode='connectivity', n_cores = 4, 
                                               Ns = N_cells_max_for_pca, Rs = 0.95 )        
                    #'''
    
                    p_maj_tmp = pmaj

                    #################################
                    if use_union:
                        df_pass = None
                    else:
                        # df_GSA_score_subset = df_GSA_score_subset_all.loc[X_pca_cur.index,:]                        
                        # dfn_subset = dfn_subset_all.loc[X_pca_cur.index,:] 
                        
                        df_res_subset, df_GSA_score_subset, dfn_subset = \
                            GSA_cell_subtyping( X_cur, mkr_lst, mkr_lst_neg, max_Q90 = max_Q90, 
                                                score_adj_weight = score_adj_weight, verbose = (verbose > 1) )
                        
                        df_GSA_score_minor_cur = pd.DataFrame(index = X_pca_cur.index, columns = minor_type_lst_cur)
                        dfn_cur = pd.DataFrame(index = X_pca_cur.index, columns = minor_type_lst_cur)
                        for minor in map_dict_min2sub.keys():
                            if minor in minor_type_lst_cur:
                                sub_lst = map_dict_min2sub[minor]
                                if len(sub_lst) == 1:
                                    best_score = df_GSA_score_subset[sub_lst[0]]
                                    dfn_cur[minor] = dfn_subset[sub_lst[0]]
                                else:
                                    subsets = df_GSA_score_subset[sub_lst].idxmax(axis = 1)
                                    for k, s in enumerate(list(subsets)):
                                        idx = X_pca_cur.index[k]
                                        dfn_cur.loc[idx,minor] = dfn_subset.loc[idx,s]
                                        
                                    if N_max_to_ave <= 1:
                                        best_score = df_GSA_score_subset[sub_lst].max(axis = 1)
                                    else:
                                        n_max = min(N_max_to_ave, len(sub_lst))
                                        best_score = np.sort(df_GSA_score_subset[sub_lst], axis=1)[:, -n_max:].mean(axis = 1)

                                df_GSA_score_minor_cur[minor] = best_score 
                        df_pass = df_GSA_score_minor_cur

                    ## X_pca_cur, cobj, y_clust_cur not used as pct_cutoff = False
                    df_res_cur, df_score_cur, df_GSA_score_cur = \
                        run_gsa_and_clf(X_pca_cur, X_cur, cobj, y_clust_cur, mkr_lst, mkr_lst_neg, 
                                         method = None, N_components = N_components, pval_th = pval_th, 
                                         pct_fit_pnt = pth_fit_pnt, pct_min_rf = pct_th_min,
                                         Target_FPR = Target_FPR, pmaj = p_maj_tmp, minor_id_sep = minor_id_sep,
                                         min_logP_diff = min_logP_diff, thresholding = thresholding_minor,
                                         pct_cutoff = False, cbc_cutoff = cbc_cutoff, verbose = (verbose > 1), 
                                         df_GSA_score = df_pass, N_cells_max_for_gmm = N_cells_max_for_gmm, 
                                         max_Q90 = max_Q90, score_adj_weight = score_adj_weight )

                    if not use_union:
                        idxs = df_res_cur.index.values
                        for k, idx in enumerate(list(idxs)):
                            ct = df_res_cur.loc[idx, 'cell_type(1st)']
                            df_res_cur.loc[idx, 'Overlap'] = dfn_cur.loc[idx,ct]
                            ct = df_res_cur.loc[idx, 'cell_type(2nd)']
                            df_res_cur.loc[idx, 'Overlap(2nd)'] = dfn_cur.loc[idx,ct]
                    #'''
                    cts = list(mkr_lst.keys())
                    if len(cts) > 1:
                        bx = df_res_cur['-logP'] < -np.log10( pval_th )
                        df_res_cur.loc[bx, 'cell_type'] = 'unassigned'     
                        pass
                    #'''
                    #################################
                    
                    y_pred_cur = df_res_cur['cell_type']
                    ys_cur = df_res_cur['cell_type(rev)']

                    n_targets = len(list(mkr_lst.keys()))
                    if (N_neighbors_minor > 2) & (len(y_pred_cur) >= N_neighbors_minor) & (n_targets > 1):
                        if (verbose > 1):
                            print('Applying KNN rule to correct minor type .. ', end = '')

                        ## KNN correction
                        # if adj is None:
                        adj = kneighbors_graph(X_pca_cur, int(N_neighbors_minor), mode='connectivity', include_self=True)
                        adj = adj.todense().astype(int)
                        idx_ary = np.arange(X_pca_cur.shape[0], dtype = int) # X_pca.index.values
                        nei_indices = np.zeros([adj.shape[0], N_neighbors_minor])
                        for k in range(adj.shape[0]):
                            idxs = np.array(adj[k,:] > 0)
                            nei_indices[k,:] = idx_ary[idxs[0,:]]
                        nei_indices = pd.DataFrame( nei_indices, index = X_pca_cur.index.values ) 

                        # gsa_score = df_res_cur['-logP']
                        if df_GSA_score_cur is not None:
                            # print(nei_indices.shape, df_GSA_score_cur.shape, flush = True)
                            if knn_type == 0:
                                y_pred_cur, score_up = apply_knn(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                       pmaj = knn_pmaj, nlog_pval_th = -np.log10(pval_th))       
                            elif knn_type == 1:
                                y_pred_cur, score_up = apply_knn1(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                       pmaj = knn_pmaj, nlog_pval_th = -np.log10(pval_th))       
                            else:
                                y_pred_cur, score_up = apply_knn2(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                        pmaj = knn_pmaj, nlog_pval_th = -np.log10(pval_th)) 
                            ## score_up not working
                            ## df_GSA_score_cur = score_up

                        if (verbose > 1): print('done. (%i) ' % (round(time.time() - start_time)))


                idx = idx_sel[b_cur]
                df_pred.loc[idx,'cell_type_minor'] = y_pred_cur
                y_pred_sel[b_cur] = y_pred_cur

                df_pred.loc[idx, 'cell_type_minor(1st)'] = df_res_cur['cell_type(1st)'].astype(str)
                df_pred.loc[idx, 'Confidence_minor(1st)'] = df_res_cur['-logP'].astype(float)
                df_pred.loc[idx, 'cell_type_minor(2nd)'] = df_res_cur['cell_type(2nd)'].astype(str)
                df_pred.loc[idx, 'Confidence_minor(2nd)'] = df_res_cur['-logP(2nd)'].astype(float)

                df_pred2.loc[idx,'cluster_rev'] = y_clust_cur + 1
                df_pred2.loc[idx,'cluster_rev'] = df_pred2.loc[idx,'cluster_rev'].astype(str)
                
                ## To be used in subset identification
                if df_GSA_score_cur is not None:
                    cols = df_GSA_score_cur.columns.values
                    idxs = df_GSA_score_cur.index.values
                    df_GSA_score_minor_all[cols] = 0.0
                    df_GSA_score_minor_all.loc[idxs, cols] = df_GSA_score_cur

                if df_res_cur.shape[0] > 0:

                    df_res_cur['Overlap'] = df_res_cur['Overlap'].astype(str)
                    df_res_cur['Overlap(2nd)'] = df_res_cur['Overlap(2nd)'].astype(str)
                    
                    dict_summary_res[tc + ' minor type'] = df_res_cur
                    dict_summary_score[tc + ' minor type'] = df_score_cur
                    dict_summary_score2[tc + ' minor type'] = df_GSA_score_cur

                if cnt == 0:
                    df_res_sel = df_res_cur
                    # if df_score_cur is not None:
                    df_score_sel = df_score_cur
                    df_GSA_score_sel = df_GSA_score_cur
                else:
                    df_res_sel = pd.concat([df_res_sel, df_res_cur], axis = 0)
                    if (df_score_cur is not None) & (df_score_sel is not None):
                        df_score_sel = pd.concat([df_score_sel, df_score_cur], axis = 0)
                    df_GSA_score_sel = pd.concat([df_GSA_score_sel, df_GSA_score_cur], axis = 0)
                cnt += 1

                if (verbose > 1):
                    print('%s minor type identification done. (%i)' % \
                          (tc, round(time.time() - start_time)))
                    # plot_roc_result(df_score_sel, ys_sel, method)
                elif verbose == 1: 
                    pass
                elif verbose == 0:
                    print('.', end = '', flush = True)

            
        if cnt > 0:
            if np.sum(b_sel) < df_res_sel.shape[0]:
                print('%sWARNING: %i < %i. One or more cluster(s) is mixed.' % \
                      (print_prefix, np.sum(b_sel), df_res_sel.shape[0]))

        etime = round(time.time() - start_time_new)        
        start_time_new = time.time()
        if (verbose > 1):
            print('%s type identification done. (%i)' % (tc, round(time.time() - start_time)))
        elif verbose == 1: 
            # print('%sHiCAT minor type identification done. (%i)' % (print_prefix, etime), flush = True)
            # print('.', end = '', flush = True)
            pass
        elif verbose == 0:
            print('M%i.' % etime, end = '', flush = True)
            # plot_roc_result(df_score_sel, ys_sel, method)
        #'''

        df_pred.loc[b_sel, 'cell_type_minor'] = y_pred_sel
        
        # dict_summary_res['Minor_Type'] = df_res_sel
        # dict_summary_score['Minor_Type'] = df_score_sel
        # dict_summary_score2['Minor_Type'] = df_GSA_score_sel
            
        b_cur = y_pred_sel == 'unassigned'
        if verbose > 1:
            print('Num of unassigned cells: %i among %i' % (np.sum(b_cur), len(b_cur)))

        ## make correction if major type and minor type does not match
        cell_type_map_dict = {}
        for tc in target_cell_lst.keys():
            tc_lst = target_cell_lst[tc]
            mkr_lst, mkr_lst_neg = get_markers_cell_type(marker_file, tc_lst, pnsh12 = mkr_selector, 
                                            rem_common = rem_cmn_mkr, verbose = False)

            cell_type_lst = list(mkr_lst.keys())
            cell_type_map_dict[tc] = cell_type_lst

        #'''
        map_dict = {}
        for key in list(cell_type_map_dict.keys()):
            for c in cell_type_map_dict[key]:
                map_dict[c] = key
        cell_types = list(map_dict.keys())

        y_pred_major = list(df_pred['cell_type_major'])
        y_pred_minor = list(df_pred['cell_type_minor'])

        y_pred_major_new = []
        y_pred_minor_new = []
        for yj, ym in zip(y_pred_major, y_pred_minor):
            if ym in cell_types:
                if map_dict[ym] == yj:
                    y_pred_major_new.append(yj)
                    y_pred_minor_new.append(ym)
                else:
                    y_pred_major_new.append(map_dict[ym])
                    y_pred_minor_new.append(ym)
            else: # 'unassigned'
                y_pred_major_new.append(yj) #'unassigned')
                y_pred_minor_new.append('unassigned')

        df_pred['cell_type_major'] = y_pred_major_new
        df_pred['cell_type_minor'] = y_pred_minor_new
        #'''

        y_pred_major = list(df_pred['cell_type_major'])
        y_pred_minor = list(df_pred['cell_type_minor'])
        
    ########################
    ### Subset identification ###
    ########################

    if ident_level > 2:        

        if verbose == 1:
            print('%sHiCAT subset identification' % (print_prefix), flush = True)
            
        df_pred['cell_type_subset(1st)'] = df_pred['cell_type_minor(1st)']
        df_pred['Confidence_subset(1st)'] = df_pred['Confidence_minor(1st)']
        df_pred['cell_type_subset(2nd)'] = df_pred['cell_type_minor(2nd)']
        df_pred['Confidence_subset(2nd)'] = df_pred['Confidence_minor(2nd)']
        
        cnt = 0
        map_dict_sub2min = {}
        map_dict_min2sub = {}
        for tc in target_cell_lst.keys():

            ## Get minor type markers
            target_cell = target_cell_lst[tc]
            mkr_lst, mkr_lst_neg = get_markers_cell_type(marker_file, target_cell, 
                                            pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                                         verbose = False)
                
            if len(minor_types_to_exclude) > 0:
                mkr_lst = rem_minor( mkr_lst, minor_types_to_exclude )
                mkr_lst_neg = rem_minor( mkr_lst_neg, minor_types_to_exclude )

            cell_type_lst = list(mkr_lst.keys())
            b_cur = np.full(len(y_pred_sel), False)
            for c in cell_type_lst:
                b_cur = b_cur | (y_pred_sel == c)
                
            #'''
            ### To be used to determine minor type for given subset
            for c in cell_type_lst: # for each minor type
                mkr_lst_tmp, mkr_lst_neg_tmp = get_markers_minor_type2(marker_file, [c], 
                                        pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                        comb_mkrs = comb_mkrs, verbose = False)
                
                for key in mkr_lst_tmp.keys():
                    map_dict_sub2min[key] = c
                map_dict_min2sub[c] = list(mkr_lst_tmp.keys())
            #'''
        
            if use_minor:
                lst = []
                for c in cell_type_lst:
                    lst.append( [c] )
            else:
                lst = [cell_type_lst]

            for c in lst:
                if use_minor: b_cur = y_pred_sel == c[0]
                    
                mkr_lst, mkr_lst_neg = get_markers_minor_type2(marker_file, c, 
                                    pnsh12 = mkr_selector, rem_common = rem_cmn_mkr,
                                    comb_mkrs = comb_mkrs, verbose = False)

                if len(minor_types_to_exclude) > 0:
                    mkr_lst = rem_minor( mkr_lst, minor_types_to_exclude )
                    mkr_lst_neg = rem_minor( mkr_lst_neg, minor_types_to_exclude )

                sm = ''
                for key in mkr_lst.keys():
                    sm = sm + '%s,' % key

                if (len(list(mkr_lst.keys())) <= 1) | (np.sum(b_cur) < 10):
                    X_cur = X_sel.loc[b_cur,:]
                    idx = list(X_cur.index.values)
                    ctn = 'unassigned'
                    if len(list(mkr_lst.keys())) == 1:
                        ctn = list(mkr_lst.keys())[0]
                    df_pred.loc[idx,'cell_type_subset'] = str(ctn)
                    if (verbose > 1) & (len(sm) > 1): 
                        print('%s subset identification: %s' % (tc, sm[:-1]))

                else:
                    if (verbose > 1) & (len(sm) > 1): 
                        print('%s subset identification: %s' % (tc, sm[:-1]))
                        
                    X_cur = X_sel.loc[b_cur,:]
                    X_pca_cur = X_pca_sel.loc[b_cur,:]
                    y_clust_cur = y_clust_sel[b_cur]

                    ## Redo PCA and Clustering #####
                    # thresholding_subset = thresholding_ms[1]
                    # pct_cutoff_subset = pct_cutoff_ms[1]
                    
                    if np.sum(b_cur) >= N_components_pca:
                        '''
                        Xx_cur = X_preprocessing( X_cur, log_transformed ) #, N_genes = 2000, N_cells_max = N_cells_max_for_pca )
                        Xx_cur = X_variable_gene_sel( Xx_cur, N_genes = 2000, N_cells_max = N_cells_max_for_pca, vg_sel = True )
                            
                        # X_pca_cur = pca.fit_transform(Xx_cur)
                        X_pca_cur = pca_subsample(Xx_cur, N_components_pca, N_cells_max_for_pca = N_cells_max_for_pca) 
                        del Xx_cur
                        
                        X_pca_cur = pd.DataFrame(X_pca_cur, index = X_cur.index, 
                                                 columns = list(np.arange(int(N_components_pca))))
                        '''
                        idx = list(X_cur.index.values)
                        X_pca_cur = X_pca.loc[idx,:]
                        
                        if X_pca_cur.shape[0] <= N_cells_max_for_pca:
                            y_clust_cur, cobj, adj = clustering_alg(X_pca_cur, clust_algo = Clustering_algo, 
                                                                N_clusters = N_comp, resolution = Clustering_resolution,
                                                                N_neighbors = 12, mode='connectivity', n_cores = 4)
                        else:
                            neighbors, distances = None, None
                            y_clust_cur, cobj, adj = clustering_subsample( X_pca_cur, neighbors, distances, 
                                                   clust_algo = Clustering_algo, N_clusters = N_comp, 
                                                   resolution = Clustering_resolution, N_neighbors = 12, 
                                                   mode='connectivity', n_cores = 4, 
                                                   Ns = N_cells_max_for_pca, Rs = 0.95 )        
                        #'''
                        
                        p_maj_tmp = 0.3
                    else:
                        y_clust_cur[:] = 0
                        cobj = None
                        adj = None
                        p_maj_tmp = 0
                    #################################
                    
                    # print(mkr_lst)
                    if use_union:
                        df_pass = None
                    else:
                        subsets_to_consider = list(mkr_lst.keys())
                        # df_pass = df_GSA_score_subset_all.loc[X_pca_cur.index, subsets_to_consider]
                        # dfn_subset = dfn_subset_all.loc[X_pca_cur.index, subsets_to_consider]

                        df_res_subset, df_pass, dfn_subset = \
                            GSA_cell_subtyping( X_cur, mkr_lst, mkr_lst_neg, max_Q90 = max_Q90, 
                                                score_adj_weight = score_adj_weight, verbose = (verbose > 1) )
                        
                    ## X_pca_cur, cobj, y_clust_cur not used as pct_cutoff = False
                    df_res_cur, df_score_cur, df_GSA_score_cur = \
                        run_gsa_and_clf(X_pca_cur, X_cur, cobj, y_clust_cur, mkr_lst, mkr_lst_neg, 
                                         method = None, N_components = N_components, pval_th = pval_th, 
                                         pct_fit_pnt = pth_fit_pnt, pct_min_rf = pct_th_min,
                                         Target_FPR = Target_FPR, pmaj = p_maj_tmp, minor_id_sep = minor_id_sep,
                                         min_logP_diff = min_logP_diff, thresholding = thresholding_subset,
                                         pct_cutoff = False, cbc_cutoff = cbc_cutoff, verbose = (verbose > 1),
                                         df_GSA_score = df_pass, N_cells_max_for_gmm = N_cells_max_for_gmm, 
                                         max_Q90 = max_Q90, score_adj_weight = score_adj_weight )

                    if not use_union:
                        idxs = df_res_cur.index.values
                        for k, idx in enumerate(list(idxs)):
                            ct = df_res_cur.loc[idx, 'cell_type(1st)']
                            df_res_cur.loc[idx, 'Overlap'] = dfn_subset.loc[idx,ct]
                            ct = df_res_cur.loc[idx, 'cell_type(2nd)']
                            df_res_cur.loc[idx, 'Overlap(2nd)'] = dfn_subset.loc[idx,ct]
                            
                    cts = list(mkr_lst.keys())
                    if len(cts) > 1:
                        bx = df_res_cur['-logP'] < -np.log10( pval_th_subset )
                        df_res_cur.loc[bx, 'cell_type'] = 'unassigned'     
                        pass

                    #################################
                        
                    y_pred_cur = df_res_cur['cell_type']
                    ys_cur = df_res_cur['cell_type(rev)']

                    if use_minor:
                        pass
                    else:
                        if df_GSA_score_cur is not None:
                            
                            cols = df_GSA_score_cur.columns.values
                            idxs = df_GSA_score_cur.index.values
                            minor_type_lst_all = list(df_GSA_score_minor_all.columns.values)
                            
                            minor_type_lst_cur = []
                            for cx in list(cols):
                                minor_type = map_dict_sub2min[cx]
                                if minor_type in minor_type_lst_all:
                                    minor_type_lst_cur.append(minor_type)
                            minor_type_lst_cur = list(set(minor_type_lst_cur))
                            
                            # print(minor_type_lst_cur, flush = True)

                            ## 수정 필요
                            df_GSA_score_minor_cur = df_GSA_score_minor_all.loc[idxs, minor_type_lst_cur].copy(deep = True)
                            
                            #########################################################
                            ## Update subset score
                            #'''
                            for cx in list(cols):
                                minor_type = map_dict_sub2min[cx]
                                if minor_type in minor_type_lst_all:
                                    # print(minor_type)
                                    df_GSA_score_cur[cx] = \
                                        (1-minor_wgt)*df_GSA_score_cur[cx] + minor_wgt*df_GSA_score_minor_cur[minor_type]
                                else:
                                    print('%sWARNING: %s (%s) not in ' % (print_prefix, minor_type, c), minor_type_lst_all) 
                              
                            #'''
                            y_prev = df_res_cur['cell_type'].copy(deep = True)                            
                            df_res_tmp = df_res_cur.copy(deep = True)
                            
                            df_res_cur = get_stat_gsa(df_GSA_score_cur)
                            df_res_cur['Overlap'] = df_res_tmp['Overlap']
                            df_res_cur['Overlap(2nd)'] = df_res_tmp['Overlap(2nd)']
                            
                            y_pred_cur = df_res_cur['cell_type'].copy(deep = True)
                            # print('\n', c, ': ', np.sum(y_prev == y_pred_cur), ' / ', len(y_prev), end = '')
                            #'''
                            ######################################################### 
                    ## End of if use_minor:
    
                    n_targets = len(list(mkr_lst.keys()))
                    if (N_neighbors_subset > 2) & (len(y_pred_cur) >= N_neighbors_subset) & (n_targets > 1):
                        if (verbose > 1):
                            print('Applying kNN to correct cell type subset .. ', end = '')

                        ## KNN correction
                        if df_GSA_score_cur is not None:
                            
                            # if adj is None:
                            adj = kneighbors_graph(X_pca_cur, int(N_neighbors_subset), 
                                                   mode='connectivity', include_self=True)
                            adj = adj.todense().astype(int)
                            idx_ary = np.arange(X_pca_cur.shape[0], dtype = int) # X_pca.index.values
                            nei_indices = np.zeros([adj.shape[0], N_neighbors_subset])
                            for k in range(adj.shape[0]):
                                idxs = np.array(adj[k,:] > 0)
                                nei_indices[k,:] = idx_ary[idxs[0,:]]
                            nei_indices = pd.DataFrame( nei_indices, index = X_pca_cur.index.values )      
                                                
                            # print(nei_indices.shape, df_GSA_score_cur.shape, flush = True)
                            if knn_type == 0:
                                y_pred_cur, score_up = apply_knn(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                                 pmaj = 0.5, nlog_pval_th = -np.log10(pval_th))        
                            elif knn_type == 1:
                                y_pred_cur, score_up = apply_knn1(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                                  pmaj = 0.5, nlog_pval_th = -np.log10(pval_th))        
                            else:
                                y_pred_cur, score_up = apply_knn2(nei_indices, y_pred_cur, df_GSA_score_cur, 
                                                                  pmaj = 0.5, nlog_pval_th = -np.log10(pval_th)) 
                            ## score_up not working
                            ## df_GSA_score_cur = score_up
                            
                        if (verbose > 1): print('done. (%i) ' % (round(time.time() - start_time)))


                    if (verbose > 1):
                        print('%s subset identification done. (%i)' % \
                              (c, round(time.time() - start_time)))
                        # plot_roc_result(df_score_cur, ys_cur, method)
                    elif (verbose == 1): 
                        pass
                    elif verbose == 0:
                        print('.', end = '', flush = True)

                    df_res_cur['cell_type'] = y_pred_cur

                    idx = list(X_cur.index.values)
                    df_pred.loc[idx,'cell_type_subset'] = y_pred_cur
                    
                    if use_minor:
                        pf = c[0]
                    else:
                        pf = tc
                        
                    y_clust_cur = ['%s_%i' % (pf, cx) for cx in list(y_clust_cur)]
                    # df_pred.loc[idx,'cluster'] = y_clust_cur
                    df_pred2.loc[idx,'cluster_rev'] = y_clust_cur

                    df_pred.loc[idx, 'cell_type_subset(1st)'] = df_res_cur['cell_type(1st)'].astype(str)
                    df_pred.loc[idx, 'Confidence_subset(1st)'] = df_res_cur['-logP'].astype(float)
                    df_pred.loc[idx, 'cell_type_subset(2nd)'] = df_res_cur['cell_type(2nd)'].astype(str)
                    df_pred.loc[idx, 'Confidence_subset(2nd)'] = df_res_cur['-logP(2nd)'].astype(float)

                    if df_res_cur.shape[0] > 0:

                        df_res_cur['Overlap'] = df_res_cur['Overlap'].astype(str)
                        df_res_cur['Overlap(2nd)'] = df_res_cur['Overlap(2nd)'].astype(str)
                        
                        dict_summary_res['%s subset' % pf] = df_res_cur
                        dict_summary_score['%s subset' % pf] = df_score_cur
                        dict_summary_score2['%s subset' % pf] = df_GSA_score_cur

        b_cur = y_pred_correct == 'unassigned'
        if (verbose > 1):
            print('Num of unassigned cells: %i among %i' % (np.sum(b_cur), len(b_cur)))
    
    ## end of subset id.

    ### Set minor type based on its subset
    #'''
    if not use_minor:
        y_pred_subset = list(df_pred['cell_type_subset'])
        y_pred_minor = []
        for y in y_pred_subset:
            if y != 'unassigned':
                y_pred_minor.append( map_dict_sub2min[y] )
            else:
                y_pred_minor.append( 'unassigned' )
                
        # print('\n', np.sum(df_pred['cell_type_minor'] == np.array(y_pred_minor)), ' / ', len(y_pred_minor), end = '')
        df_pred['cell_type_minor_org'] = df_pred['cell_type_minor'].copy(deep = True)
        df_pred['cell_type_minor'] = y_pred_minor
    #'''
            
    #'''
    ### Identify cycling cells
    if cycling_cell & ('MKI67' in list(Xs.columns.values)):
        b = Xs['MKI67'] > 0
        
        y_new = []
        # y_pred_major = list(df_pred.loc[b, 'cell_type_minor'])
        y_pred_major = list(df_pred.loc[b, 'cell_type_major'])
        for y in y_pred_major:
            if y != 'unassigned':
                y_new.append('%s Cycling' % y)
            else:
                y_new.append(y)
                
        df_pred.loc[b, 'cell_type_minor'] = y_new
        df_pred.loc[b, 'cell_type_subset'] = y_new
    #'''
    df_pred['cluster_rev'] = df_pred2['cluster_rev'].astype(str)
                
    etime = round(time.time() - start_time_new)        
    start_time_new = time.time()
    if (verbose > 1): 
        print('HiCAT done. (%i)' % round(time.time() - start_time))
    elif (verbose == 1):
        # print('%sHiCAT subset identification done. (%i)' % (print_prefix, etime), flush = True)
        pass
    elif verbose == 0:
        print('S%i.' % etime, end = '', flush = True)
        print(' done. (%i)' % round(time.time() - start_time))
        
    dict_summaries = {}
    dict_summaries['GSA_summary'] = dict_summary_res
    dict_summaries['GSA_scores'] = dict_summary_score2
    dict_summaries['Ref_scores'] = dict_summary_score3
    dict_summaries['Identification_model_scores'] = dict_summary_score
    dict_summaries['parameters'] = [pval_th, pth_fit_pnt, pct_th_min]
    dict_summaries['X_pca'] = X_pca
    
       
    return df_pred # , dict_summaries, X_pca


###################
### Plot_dot ######

import warnings

def remove_common2( mkr_dict, verbose = True ):

    cts = list(mkr_dict.keys())
    mkrs_all = []
    for c in cts:
        mkrs_all = mkrs_all + mkr_dict[c]
    mkrs_all = list(set(mkrs_all))
    df = pd.DataFrame(index = mkrs_all, columns = cts)
    df.loc[:,:] = 0

    for c in cts:
        df.loc[mkr_dict[c], c] = 1
    Sum = df.sum(axis = 1)
    
    to_del = []
    s = ''
    for c in cts:
        b = (df[c] > 0) & (Sum == 1)
        mkrs1 = list(df.index.values[b])
        if verbose & (len(mkr_dict[c]) != len(mkrs1)):
            s = s + '%s: %i > %i, ' % (c, len(mkr_dict[c]), len(mkrs1))
        
        if len(mkrs1) == 0:
            to_del.append(c)
        else:
            mkr_dict[c] = mkrs1

    if verbose & len(s) > 2:
        print(s[:-2])

    if len(to_del) > 0:
        for c in cts:
            if c in to_del:
                del mkr_dict[c]
                
    return mkr_dict


def get_markers_all3(mkr_file, target_lst, pnsh12, genes = None, level = 1, 
                    rem_cmn = False, comb_mkrs = False ):
    
    # target = 'Myeloid cell'
    if level == 0:
        mkr_dict, mkr_dict_neg = \
            get_markers_major_type(mkr_file, target_cells = target_lst, 
                                    pnsh12 = pnsh12, rem_common = False, verbose = False)
    elif level == 1:
        mkr_dict, mkr_dict_neg = \
            get_markers_minor_type2(mkr_file, target_cells = target_lst, 
                                    pnsh12 = pnsh12, comb_mkrs = comb_mkrs, 
                                    rem_common = False, verbose = False)
    else:
        mkr_dict, mkr_dict_neg = \
            get_markers_cell_type(mkr_file, target_cells = target_lst, pnsh12 = pnsh12,
                          rem_common = False, verbose = False)
        
    if rem_cmn:
        mkr_dict = remove_common2( mkr_dict, verbose = True )
        
    mkrs_all = [] #['SELL']
    mkrs_cmn = []
    for ct in mkr_dict.keys():
        if genes is not None:
            ms = list(set(mkr_dict[ct]).intersection(genes))
        else: 
            ms = mkr_dict[ct]
        mkrs_all = mkrs_all + ms
        if len(mkrs_cmn) == 0:
            mkrs_cmn = ms
        else:
            mkrs_cmn = list(set(mkrs_cmn).intersection(ms))

    mkrs_all = list(set(mkrs_all))
    if genes is not None:
        mkrs_all = list(set(mkrs_all).intersection(genes))
    
    return mkrs_all, mkr_dict


def update_markers_dict(mkrs_all, mkr_dict, X, y, rend = None, cutoff = 0.3, 
                        Nall = 20, Npt = 20):
    
    if rend is None:
        lst = list(mkr_dict.keys())
        lst.sort()
        rend = dict(zip(lst, lst))
    else:
        lst = list(rend.keys())
        
    df = pd.DataFrame(index = lst, columns = mkrs_all)
    df.loc[:,:] = 0
        
    for ct in lst:
        b = y == ct
        ms = list(set(mkr_dict[ct]).intersection(mkrs_all))
        pe = list((X.loc[b,ms] > 0).mean(axis = 0))
        for j, m in enumerate(ms):
            df.loc[ct, m] = pe[j]

    if df.shape[0] == 1:
        mkrs_all = list(df.columns.values)
        mkrs_dict = {}
        
        pe_lst = []
        pex_lst = []
        
        for ct in lst:
            b = y == ct
            ms = list(set(mkr_dict[ct]).intersection(mkrs_all))
            pe = np.array((X.loc[b,ms] > 0).mean(axis = 0))
            pex = np.array((X.loc[~b,ms] > 0).mean(axis = 0))
            odr = np.array(-pe).argsort()
            ms_new = []
            for o in odr:
                if (pe[o] >= cutoff):
                    ms_new.append(ms[o])

            pe = pe[~np.isnan(pe)]
            pex = pex[~np.isnan(pex)]
            pe_lst = pe_lst + list(pe)
            pex_lst = pex_lst + list(pex)
            
            if len(ms_new) > 0:
                mkrs_dict[rend[ct]] = ms_new[:min(Npt,len(ms_new))]
            else:
                mkrs_dict[rend[ct]] = ms[:min(Npt,len(ms))]
    else:
        p1 = df.max(axis = 0)
        p2 = p1.copy(deep = True)
        p2[:] = 0
        idx = df.index.values
        for m in list(df.columns.values):
            odr = np.array(-df[m]).argsort()
            p2[m] = df.loc[idx[odr[1]], m]
        nn = (df >= 0.5).sum(axis = 0)

        b0 = p1 > 0
        b1 = (p2/(p1 + 0.0001)) < 0.5
        b2 = nn < 4
        b = b0 # & b1 & b2
        df = df.loc[:,b]
        mkrs_all = list(df.columns.values)

        mkrs = [] 
        cts = [] 
        pes = [] 
        mkrs_dict = {}
        pe_lst = []
        pex_lst = []
        for ct in lst:
            b = y == ct
            ms = list(set(mkr_dict[ct]).intersection(mkrs_all))
            p2t = np.array(p2[ms])
            p1t = np.array(p1[ms])
            pe = np.array((X.loc[b,ms] > 0).mean(axis = 0))
            pex = np.array((X.loc[~b,ms] > 0).mean(axis = 0))
            odr = np.array(-pe).argsort()
            ms_new = []
            for o in odr:
                if (pe[o] >= cutoff) & (~np.isnan(pe[o])):
                    ms_new.append(ms[o])

            pe = pe[~np.isnan(pe)]
            pex = pex[~np.isnan(pex)]
            pe_lst = pe_lst + list(pe)
            pex_lst = pex_lst + list(pex)

            if len(ms_new) > 0:
                mkrs_dict[rend[ct]] = ms_new[:min(Npt,len(ms_new))]
            else:
                mkrs_dict[rend[ct]] = ms[:min(Npt,len(ms))]
                
    return mkrs_dict, df, pe_lst, pex_lst



def remove_mac_common_markers(mkrs_dict):   

    lst2 = list(mkrs_dict.keys())
    lst = []
    Mono = None
    for item in lst2:
        if item[:3] == 'Mac':
            lst.append(item)
        if item[:4] == 'Mono':
            Mono = item
            
    if len(lst) > 1:
        mac_common = mkrs_dict[lst[0]]
        for item in lst[1:]:
            mac_common = list(set(mac_common).intersection(mkrs_dict[item]))
            
        for item in lst:
            for mkr in mac_common:
                mkrs_dict[item].remove(mkr)
        if Mono is not None:
            mono_lst = mkrs_dict[Mono]
            del mkrs_dict[Mono]
            mkrs_dict[Mono] = mono_lst
            
    return mkrs_dict

    
def plot_dot_s(adata, target_lst, type_level, mkr_file, title = None, rend = None, level = 1, 
              cutoff = 0, pnsh12 = '101000', rem_cmn = False, dot_max = 0.5, swap_ax = False,
              to_exclude = [], Npt = 15, comb_mkrs = False, minNcells = 20, vg_rot = 10,
              figsize = (20, 4), ax = None, ret_pe = False ):

    SCANPY = True
    try:
        import scanpy as sc
    except ImportError:
        SCANPY = False
    
    if (not SCANPY):
        print('ERROR: scanpy not installed. ')   
        return
    
    target = ','.join(target_lst)
    genes = list(adata.var.index.values)
    genes = list(set(genes) - set(to_exclude))
    mkrs_all, mkr_dict = get_markers_all3(mkr_file, target_lst, 
                                         pnsh12, genes, level, 
                                         rem_cmn = rem_cmn, 
                                         comb_mkrs = comb_mkrs )
    target_lst2 = list(mkr_dict.keys())
    y = adata.obs[type_level]
    b = y == target_lst2[0]
    for t in target_lst2:
        b = b | (y == t)
        
    nh = 0
    if np.sum(b) > 0: nh = 1
    for t in target_lst2:
        bt = y == t
        if np.sum(bt) > 0:
            b = b | (y == t)
            nh += 1

    adata_t = adata[b,mkrs_all]
    X = adata_t.to_df()
    y = adata_t.obs[type_level]

    mkrs_dict, df, pe_lst, pex_lst = update_markers_dict(mkrs_all, mkr_dict, X, y, rend, 
                                        cutoff = cutoff, Npt = Npt)

    mkrs_dict = remove_mac_common_markers(mkrs_dict)
    if rend is not None: 
        adata_t.obs[type_level].replace(rend, inplace = True)

    nw = 0
    for key in mkrs_dict.keys():
        nw += len(mkrs_dict[key])
        
    plt.rc('font', size=12)          

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dp = sc.pl.dotplot(adata_t, mkrs_dict, groupby = type_level, 
                       categories_order = list(mkrs_dict.keys()), 
                       # ax = ax, figsize = (nw*0.36, nh*0.3),
                       log = True, var_group_rotation = vg_rot, show = False, 
                       standard_scale = 'var', dot_max = dot_max, swap_axes = swap_ax ) 
    
    ax = dp['mainplot_ax']
    if title is not None:
        ax.set_title(title, pad = 40, fontsize = 16) 
    ax.tick_params(labelsize=12)
    ax.set_ylabel('Annotated', fontsize = 14)
    
    if ret_pe:
        return pe_lst, pex_lst
    else:
        return

    
def plot_dot( adata, target_lst, type_level, mkr_file, title = None, rend = None, level = 1, 
              cutoff = 0, pnsh12 = '101000', rem_cmn = False, dot_max = 0.5, swap_ax = False,
              to_exclude = [], Npt = 15, comb_mkrs = False, minNcells = 20, vg_rot = 10,
              figsize = (20, 4), ax = None, ret_pe = False ):

    SCANPY = True
    try:
        import scanpy as sc
    except ImportError:
        SCANPY = False
    
    if (not SCANPY):
        print('ERROR: scanpy not installed. ')   
        return
    
    target = ','.join(target_lst)
    genes = list(adata.var.index.values)
    genes = list(set(genes) - set(to_exclude))
    mkrs_all, mkr_dict = get_markers_all3(mkr_file, target_lst, 
                                         pnsh12, genes, level, 
                                         rem_cmn = rem_cmn, comb_mkrs = comb_mkrs)
    
    target_lst2 = list(mkr_dict.keys())
    y = adata.obs[type_level]
    b = y == target_lst2[0]
    for t in target_lst2:
        b = b | (y == t)
    
    nh = 0
    if np.sum(b) > 0: nh = 1
    for t in target_lst2:
        bt = y == t
        if np.sum(bt) > 0:
            b = b | (y == t)
            nh += 1

    adata_t = adata[b, mkrs_all]
    X = adata_t.to_df()
    y = adata_t.obs[type_level]

    mkrs_dict, df, pe_lst, pex_lst = update_markers_dict(mkrs_all, mkr_dict, X, y, rend, 
                                        cutoff = cutoff, Npt = Npt*2)
    
    mkrs_dict = remove_mac_common_markers(mkrs_dict)
    if rend is not None: 
        adata_t.obs[type_level].replace(rend, inplace = True)
        
    mkall = []
    for key in mkrs_dict.keys():
        mkall = mkall + mkrs_dict[key]

    ## Get number of marker genes for each cell type
    mkall = list(set(mkall))
    nmkr = dict(zip(mkall, [0]*len(mkall)))
    for key in mkrs_dict.keys():
        for m in mkrs_dict[key]:
            nmkr[m] += 1
            
    ## remove the marker genes appering in 3 or more cell types
    to_del = []
    for key in nmkr.keys():
        if nmkr[key] > 2: to_del.append(key)
            
    if len(to_del) > 0:
        for m in to_del:
            for key in mkrs_dict.keys():
                if m in mkrs_dict[key]:
                    mkrs_dict[key].remove(m)
            
    ## Select markers upto Npt
    for key in mkrs_dict.keys():
        ms = mkrs_dict[key]
        if len(ms) > Npt:
            mkrs_dict[key] = ms[:Npt]
            
    ## Select only the cell types that exist in the data and the number of cells >= minNcells
    ps_cnt = adata_t.obs[type_level].value_counts()
    lst_prac = list(ps_cnt.index.values) # list(adata_t.obs[type_level].unique())
    mkrs_dict2 = {}
    for m in mkrs_dict.keys():
        if m in lst_prac: 
            if ps_cnt[m] >= minNcells:
                mkrs_dict2[m] = mkrs_dict[m]
    mkrs_dict = mkrs_dict2        

    ## Remove cell types for which the number of cells below minNcells
    target_lst2 = list(mkrs_dict.keys())
    y = adata_t.obs[type_level]
    b = y == target_lst2[0]
    for t in target_lst2:
        b = b | (y == t)
    
    nh = 0
    if np.sum(b) > 0: nh = 1
    for t in target_lst2:
        bt = y == t
        if np.sum(bt) > 0:
            b = b | (y == t)
            nh += 1

    adata_t = adata_t[b, :]
    if rend is not None: 
        adata_t.obs[type_level].replace(rend, inplace = True)
    
    nw = 0
    for key in mkrs_dict.keys():
        nw += len(mkrs_dict[key])
        
    plt.rc('font', size=12)    
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dp = sc.pl.dotplot(adata_t, mkrs_dict, groupby = type_level, 
                       categories_order = list(mkrs_dict.keys()), 
                       #ax = ax, figsize = (nw*0.36, nh*0.3),
                       log = True, var_group_rotation = vg_rot, show = False, 
                       standard_scale = 'var', dot_max = dot_max, swap_axes = swap_ax ) 

    ax = dp['mainplot_ax']
    if title is not None:
        ax.set_title(title, pad = 40, fontsize = 16) 
    ax.tick_params(labelsize=12)
    ax.set_ylabel('Annotated', fontsize = 14)
    
    if ret_pe:
        return pe_lst, pex_lst
    else:
        return
    

def plot_marker_expression_profile( df_pred, X, mkr_file, pnsh12 = '101000', 
                                    Npt = 15, comb_mkrs = False, minNcells = 20, 
                                    vg_rot = 10, cutoff = 0, dot_mx = 0.5,
                                    title_suffix = ''):

    ANNDATA = True
    try:
        from anndata import AnnData
    except ImportError:
        ANNDATA = False

    if (not ANNDATA):
        print('ERROR: anndata not installed. ')   
        return
        
    adata = AnnData(X= X, obs = df_pred)
    # adata 
    # dot_mx = 0.5
    # cutoff = 0
    rem_cmn = False
    swap_ax = False

    Maj_types_pred = list(set(df_pred['cell_type_major']))

    mkr_dict, mkr_dict_neg = \
        get_markers_major_type(mkr_file, target_cells = [], pnsh12 = pnsh12,
                      rem_common = False, verbose = False)

    Maj_types = list(mkr_dict.keys())
    Maj_types = list(set(Maj_types).intersection(Maj_types_pred))

    mlst_s = []
    mlst_m = []
    for m in Maj_types:

        mkr_dict_minor, mkr_dict_neg = \
            get_markers_cell_type(mkr_file, target_cells = [m], pnsh12 = pnsh12,
                          rem_common = False, verbose = False)

        Min_types = list(mkr_dict_minor.keys())
        mkr_dict, mkr_dict_neg = \
            get_markers_minor_type2(mkr_file, target_cells = Min_types, pnsh12 = pnsh12,
                      rem_common = False, comb_mkrs = comb_mkrs, verbose = False)
        if len(mkr_dict.keys()) > 1:
            # print('%s: %i' % (m, len(mkr_dict.keys())))
            mlst_m.append(m)
        else:
            # print('%s: %i' % (m, len(mkr_dict.keys())))
            mlst_s.append(m)

    # fig, axs = plt.subplots(len(mlst_s)+len(mlst_m), 1)
    acnt = 0
    ## Major 
    target_lst = mlst_s
    rend = None # dict(zip(lst, lst2))
    type_exc = []
    type_col = 'cell_type_major'
    level = 0

    if len(target_lst) > 0:
        title = 'Marker expression of %s' % target_lst[0]
        for t in target_lst[1:]: title = title + ',%s' % t
        if len(title_suffix) > 0:
            title = title + ' for %s' % title_suffix

        plot_dot(adata, target_lst, type_col, mkr_file, title, 
                  rend = rend, level = level, # ax = axs[acnt],
                  cutoff = cutoff, pnsh12 = pnsh12, rem_cmn = rem_cmn, dot_max = dot_mx, 
                  swap_ax = swap_ax, to_exclude = type_exc, Npt = Npt, comb_mkrs = comb_mkrs,
                  vg_rot = vg_rot, minNcells = minNcells)
        acnt += 1
        
    ## Subset 
    level = 1
    type_col = 'cell_type_subset'

    for m in mlst_m:
        mkr_dict_minor, mkr_dict_neg = \
            get_markers_cell_type(mkr_file, target_cells = [m], pnsh12 = pnsh12,
                          rem_common = False, verbose = False)
        if m[0] == 'T':
            target_lst = list(mkr_dict_minor.keys())
            t1 = []
            t2 = []
            for t in target_lst:
                if ('NK' in t.upper()) | ('ILC' in t.upper()):
                    t2.append(t)
                elif ('CD4' in t.upper()) | ('CD8' in t.upper() ):
                    t1.append(t)

            if len(t1) > 0:
                target_lst = t1
                if len(target_lst) > 0:
                    title = 'Marker expression of %s' % target_lst[0]
                    for t in target_lst[1:]: title = title + ',%s' % t
                    if len(title_suffix) > 0:
                        title = title + ' for %s' % title_suffix
                    plot_dot(adata, target_lst, type_col, mkr_file, title, 
                              rend = rend, level = level, # ax = axs[acnt],
                              cutoff = cutoff, pnsh12 = pnsh12, rem_cmn = rem_cmn, dot_max = dot_mx, 
                              swap_ax = swap_ax, to_exclude = type_exc, Npt = Npt, 
                              comb_mkrs = comb_mkrs, vg_rot = vg_rot, minNcells = minNcells)
                    acnt += 1
            if len(t2) > 0:
                target_lst = t2
                if len(target_lst) > 0:
                    title = 'Marker expression of %s' % target_lst[0]
                    for t in target_lst[1:]: title = title + ',%s' % t
                    if len(title_suffix) > 0:
                        title = title + ' for %s' % title_suffix
                    plot_dot(adata, target_lst, type_col, mkr_file, title, 
                              rend = rend, level = level, # ax = axs[acnt],
                              cutoff = cutoff, pnsh12 = pnsh12, rem_cmn = rem_cmn, dot_max = dot_mx, 
                              swap_ax = swap_ax, to_exclude = type_exc, Npt = Npt, 
                               comb_mkrs = comb_mkrs, vg_rot = vg_rot, minNcells = minNcells)
                    acnt += 1

    for m in mlst_m:
        mkr_dict_minor, mkr_dict_neg = \
            get_markers_cell_type(mkr_file, target_cells = [m], pnsh12 = pnsh12,
                          rem_common = False, verbose = False)
        if m[0] != 'T':
            target_lst = list(mkr_dict_minor.keys())
            if len(target_lst) > 0:
                title = 'Marker expression of %s' % target_lst[0]
                for t in target_lst[1:]: title = title + ',%s' % t
                if len(title_suffix) > 0:
                    title = title + ' for %s' % title_suffix
                plot_dot(adata, target_lst, type_col, mkr_file, title, 
                          rend = rend, level = level, # ax = axs[acnt],
                          cutoff = cutoff, pnsh12 = pnsh12, rem_cmn = rem_cmn, dot_max = dot_mx, 
                          swap_ax = swap_ax, to_exclude = type_exc, Npt = Npt, 
                           comb_mkrs = comb_mkrs, vg_rot = vg_rot, minNcells = minNcells)
                acnt += 1
                                                                                                                       
                
def get_perf_ext( df_pred, cell_types_not_consider, truth = 'cell_type_true' ):
    
    cell_type = df_pred[truth]
    bc = np.full(len(cell_type), False)
    for ct in cell_types_not_consider:
        bc = bc | (cell_type == ct)
    df_pred = df_pred.loc[~bc,:]
        
    cols = list(df_pred.columns.values)
    if 'target_cell_types' in cols:
        cols.remove('target_cell_types')
    if truth in cols:
        cols.remove(truth)
    
    df_perf = pd.DataFrame(index = ['C', 'CUA', 'EUA', 'EA', 'E'])
    tcts = list(set(df_pred['target_cell_types']))
    
    bt = np.full( df_pred.shape[0], False )
    for k, tct in enumerate(tcts):
        b1 = df_pred['target_cell_types'] == tct
        tct_lst = tct.split(',')
        for ct in tct_lst:
            b2 = df_pred[truth] == ct
            bt = bt | (b1&b2)
                
    bz = df_pred[truth] != 'Unknown'
    df_perf['ideal'] = [np.sum(bz&bt)/np.sum(bz), \
                        np.sum(bz&(~bt))/np.sum(bz), 0,0,0]
        
    for c in cols:
        tcol = c        
        ba = np.full( df_pred.shape[0], False )
        for k, tct in enumerate(tcts):
            b1 = df_pred['target_cell_types'] == tct
            tct_lst = tct.split(',')
            for ct in tct_lst:
                b2 = df_pred[tcol] == ct
                ba = ba | (b1&b2)                
        bua = ~ba
        b_cua = ((bz) & (~bt) & (bua))
        b_ea = ((bz) & (~bt) & (ba))
        b_eua = ((bz) & (bt) & (bua))
        b_e = ((bz) & (bt) & (~bua) & (df_pred[tcol] != df_pred[truth]))
        b_c = ((bz) & (bt) & (~bua) & (df_pred[tcol] == df_pred[truth]))
        
        n_correctly_unassigned = np.sum(b_cua)/np.sum(bz)
        n_incorrectly_assigned = np.sum(b_ea)/np.sum(bz)
        n_incorrectly_unassigned = np.sum(b_eua)/np.sum(bz)
        n_incorrect = np.sum(b_e)/np.sum(bz)
        n_correct = np.sum(b_c)/np.sum(bz)
        
        df_perf[c] = [n_correct, n_correctly_unassigned, n_incorrectly_unassigned, \
                      n_incorrectly_assigned, n_incorrect]

    df_perf = df_perf*100
    df_perf = df_perf.loc[['C', 'EUA', 'E', 'EA', 'CUA'],:]
    df_m = pd.DataFrame( columns = df_perf.columns.values, index = ['Method'], dtype = str )
    df_m.loc['Method',:] = list(df_perf.columns.values)
    # df_perf.loc['Method',:] = list(df_perf.columns.values)
    df_perf = pd.concat([df_perf, df_m], axis = 0)
    df_perf = df_perf.T

    return df_perf


#######################################

def get_hicat_markers_db( species, tissue = 'Generic' ):

    path = 'https://raw.githubusercontent.com/combio-dku/HiCAT/main/'
    if species.lower() == 'hs':
        file_mkr = path + 'markers_hs_all_tissues.tsv' 
    elif species.lower() == 'mm':
        file_mkr = path + 'markers_mm_all_tissues.tsv' 
    else:
        print('ERROR: species must be either hs or mm.')
        return             
            
    df_mkr_db_all = pd.read_csv(file_mkr, sep = '\t')
    tissue_lst = list(df_mkr_db_all['tissue'].unique())
    tissue_lst.remove('Immune')
    tissue_lst.remove('Immune_ext')
    tissue_lst.remove('Epithelium')
    
    if tissue not in tissue_lst:
        print('ERROR: tissue must be one of ', tissue_lst)
        return
    elif tissue == 'Generic':
        target_tissues = ['Immune', 'Generic', 'Epithelium']
    elif tissue == 'Blood':
        target_tissues = ['Immune', 'Generic', 'Immune_ext', tissue]  
    elif tissue == 'Brain':
        target_tissues = ['Immune', 'Generic', tissue]  
    elif tissue in tissue_lst:
        target_tissues = ['Immune', 'Generic', tissue] 
    else:
        target_tissues = ['Immune', 'Generic', 'Epithelium']

    b = df_mkr_db_all['tissue'].isin(target_tissues)
    df_mkr_db = df_mkr_db_all.loc[b,:].copy(deep = True)

    if tissue != 'Blood':
        if tissue in ['Brain']:
            b = df_mkr_db['cell_type_major'].isin( ['Myeloid cell'] )
            df_mkr_db = df_mkr_db.loc[~b,:]
        else:
            b = df_mkr_db['cell_type_minor'].isin( ['Monocyte'] )
            df_mkr_db = df_mkr_db.loc[~b,:]

    return df_mkr_db
    

def run_hicat( adata, 
               species = 'hs', 
               n_pca_comp = 15,
               clustering_resolution = 1,
               log_transformed = False,
               N_cells_max_for_pca = 20000,
               mkr_db = None, verbose = 1 ):

    """
    Run infercnv py with the following parameters

    Parameters:
    adata: AnnData object for which the inferploidy is run.
    mkr_db (string or DataFrame): Path to the marker DB file (.tsv file) or DataFrame read from the DB file.
    species: must be either 'hs' (for human) or 'mm' (for mouse). If mkr_db is none, the function use the markers DB the package provides.
    n_pca_comp (int): The number of PCA components for dimension reduction of CNV matrix.
    clustering_resolution (positive real number): Clustering resolution for Louvain clustering.
    verbose (int): level of verbosity

    Returns:
    AnnData objects with ['celltype_major', 'celltype_minor', 'celltype_subset'] added to adata.obs
    """

    if mkr_db is None:
        if species.lower() == 'hs':
            mkr_db = get_hicat_markers_db( species = 'hs', tissue = 'Generic' )
        elif species.lower() == 'mm':
            mkr_db = get_hicat_markers_db( species = 'mm', tissue = 'Generic' )
        else:
            print('ERROR: species must be either hs or mm.')
            return             
    
    s = 'Celltype annotation (using HiCAT) ..  ' 
    if verbose: 
        print(s, flush = True)

    start_time_t = time.time()
    
    adata_tmp = adata[:,:]
    if 'log1p' not in list(adata_tmp.uns.keys()):
        sc.pp.normalize_total(adata_tmp, target_sum=1e4)
        sc.pp.log1p(adata_tmp, base = 2)

    if 'highly_variable' not in list(adata_tmp.var.columns.values):
        sc.pp.highly_variable_genes(adata_tmp, n_top_genes = 2000)
        
    if 'X_pca' not in list(adata_tmp.obsm.keys()):
        sc.tl.pca(adata_tmp, n_comps = n_pca_comp, use_highly_variable = True)

    X_pca = adata_tmp.obsm['X_pca']
    X1 = adata_tmp.to_df()
    
    df_pred = HiCAT( X1, mkr_db, X_pca = X_pca,
               log_transformed = log_transformed,
               N_pca_components = n_pca_comp, 
               Clustering_resolution = clustering_resolution, 
               N_cells_max_for_pca = N_cells_max_for_pca,
               verbose = verbose, 
               print_prefix = '   ' )

    adata.obs['celltype_major'] = df_pred['cell_type_major']
    adata.obs['celltype_minor'] = df_pred['cell_type_minor']
    adata.obs['celltype_subset'] = df_pred['cell_type_subset']

    mkr_dict, mkr_dict_neg = \
    get_markers_minor_type2(mkr_db, target_cells = [], 
                            pnsh12 = '100000', comb_mkrs = False, 
                            rem_common = False, verbose = False, to_upper = False)
    adata.uns['subset_markers'] = mkr_dict
        
    return adata
