import re
import csv

from collections import OrderedDict
import numpy as np
import pandas as pd
import os
import importlib
import sys
import types
import dill

from .diskIO import *



def cd(path):
    try:
        os.chdir(path)
    except:
        pass
    return 

def save_session(gb,path):
    # gb is globals() in the main session
    # path of a .pkl file
    ss = {}
    gb = globals()
    for k,v in gb.items():
        if '_' != k[0] and not isinstance(v,types.ModuleType):
            ss[k] = v
    rm = ['gb','v','In','Out','exit','quit','NamespaceMagics']
    for x in rm:
        if x in ss:
            del ss[x]
    with open(path,'wb') as fx:
        dill.dump(ss,fx)
    return 0

def load_session(gb,path):
    with open(path,'rb') as fx:
        ss = dill.load(fx)
    for k,v in ss.items():
        gb[k] = v
    return 0

def env(env_name):
    return os.getenv(env_name)
    

def config(glb,mode='default',load_mode='default'):
    default_config_path = os.path.join(os.path.dirname(__file__),'configs')
    config_path = env('PY_CONFIGS') if env('PY_CONFIGS') else default_config_path
    mode_path = os.path.join(config_path,mode+'.py')
    load_mode_path = os.path.join(config_path,load_mode+'_load.py')

    ns = {} # use ns to prevent contaminating the glb namespace
    if os.path.isfile(mode_path):
        code = load(mode_path,'txt')
        # exec(code,global())
        # return _q
        exec(code,ns)
        if '_q' in ns:
            glb['_q'] = ns['_q']
    
    if os.path.isfile(load_mode_path):
        load_code = load(load_mode_path,'txt')
        exec(load_code, ns)
        for lib in ns['libs']:
            glb[lib] = ns[lib]
        


def reload(mod,subs=None):
    if subs is None:
        subs = mod.__all__
    mod_name = mod.__name__
    for sub in subs:
        importlib.reload(sys.modules[f'{mod_name}.{sub}'])
    importlib.reload(sys.modules[mod_name])
    return 0

def pinsplit(string,pattern,rangeValue):
	# split a string by pattern at designated point
	# e.g. pinsplit('a,b,ccd-5,6',',',3) outputs ['a,b,ccd-5','6']
	# e.g. pinaplit('a,b,ccd-5,6',',',[1,-1]) outputs ['a','b,ccd-5','6']

	patternIdx = [m.start() for m in re.finditer(pattern,string)]
	# if string doesn't contain any pattern
	if not patternIdx:
		return string
	if type(rangeValue) is int:
		if rangeValue>0:
			rangeValue = rangeValue - 1
		output = []
		output.append(string[:patternIdx[rangeValue]])
		output.append(string[patternIdx[rangeValue]+1:])
		return output
	else:
		patternCount = len(patternIdx)
		rangeValue = map(lambda x: x-1 if x>0 else patternCount+x,rangeValue)
		rangeValue = sorted(rangeValue)
		output = []
		startIdx = 0
		for val in rangeValue:
			endIdx = patternIdx[val]
			output.append(string[startIdx:endIdx])
			startIdx = endIdx+1
		output.append(string[startIdx:len(string)])
		return output


def getNumber(s):
	# parse string to number without raising error
	try:
		return float(s)
	except ValueError:
		return False

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
    	yield l[i:i+n]

def bins(lst, n):
	"""group elements in lst into n bins"""
	splitted = []
	for i in reversed(range(1, n + 1)):
		split_point = len(lst)//i
		splitted.append(lst[:split_point])
		lst = lst[split_point:]
	return splitted

copydict = lambda dct, *keys: {key: dct[key] for key in keys}

def flatList(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def printEvery(unit,n,string=None):
	if n%unit==0:
		if string:
			print(string.format(n))
		else:
			print(n)

def csv2list(pathx,delim='\t'):
    res = []
    with open(pathx,'r') as pf:
        for line in pf:
            line = line.strip('\r\n\t')
            res.append(line.split(delim))
    return res

def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.

	Author
	--------
	Daniel Himmelstein @ stackflow
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df

def groupby(iterable,keyFunc):
	res = OrderedDict()
	for item in iterable:
		key = keyFunc(item)
		if key not in res:
			res[key] = []
		res[key].append(item)
	return res

def inferSchema(coll,exclude=['_id']):
	projection = {}
	if exclude:
		for key in exclude:
			projection[key] = False

	summary = {}
	total = 0
	for doc in coll.find(projection=projection):
		total+=1
		for key in doc:
			if key not in summary:
				summary[key] = {'count':0,'type':set()}
			summary[key]['count'] += 1
			summary[key]['type'].add(type(doc[key]))

	for key in summary:
		summary[key]['ratio'] = summary[key]['count']/total
		summary[key]['count'] = str(summary[key]['count'])+'/'+str(total)
		summary[key]['type'] = list(summary[key]['type'])

	return summary

def averageByIndex(series):
	return series.groupby(level=0).mean()


def addToDict(target,source,keys):
	for key in keys:
		if isinstance(key,str):
			if key in source:
				target[key] = source[key]
		else:
			if key[1] in source:
				target[key[0]] = source[key[1]]
	return target

def rpSort(objects,functions):
	# vals smaller the better
	from scipy.stats import rankdata
	ranks = []
	for function in functions:
		vals =[function(x) for x in objects]
		ranks.append(rankdata(vals))
	ranks = np.vstack(ranks).T
	rps = np.prod(ranks,axis=1).tolist()
	sortedObjects, _ = zip(*sorted(zip(objects,rps),key=lambda x:x[1]))
	return sortedObjects

def correct_pvals(pvalues, correction_type = "Benjamini-Hochberg"):
    """
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1])
    """
    from numpy import array, empty
    pvalues = array(pvalues)
    n = float(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    return new_pvalues


def vectorize(targets):
    targets_flat = flatList(targets)
    uniq = pd.Series(list(set(targets_flat)))
    arr = []
    for item in targets:
        vec = uniq.isin(item).values.tolist()
        arr.append(vec)
    mat = np.array(arr).astype(np.int)
    return mat
