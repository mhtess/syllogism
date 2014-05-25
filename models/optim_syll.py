#!/usr/bin/python
from scipy import optimize
import numpy as np
import sys
import os
import csv
from itertools import izip
from numpy import array, log, exp
from scipy.special import gammaln
import sys

def log_factorial(x):
    """Returns the logarithm of x!
    Also accepts lists and NumPy arrays in place of x."""
    return gammaln(np.array(x)+1)
def multinomial(n, xs, ps):
	xs, ps = np.array(xs), np.array(ps)
	result = log_factorial(n) - sum(log_factorial(xs)) + sum(xs * np.log(ps))
	return result

#datatype = 'experiment'
datatype = 'meta'
#expname = '02syllogism-1ca'
expname = 'AMFO'
serv = '0'
n_obj = sys.argv[1]
br0 = sys.argv[2]
ndepth = sys.argv[3]
mdepth = sys.argv[4]
alphq0 = sys.argv[5]
alphr0 = sys.argv[6]
nvc = sys.argv[7]

if (datatype == 'experiment'):
	destination = ('/Users/mht/Documents/research/syllogism/data/%s/' % (expname))
	data0 = np.loadtxt((destination+'meanCncl_syll02_n100.csv'),skiprows=1,delimiter=",",usecols = (1,2,3,4,5))
	syllReader = csv.reader(open((destination+'meanCncl_syll02_n100.csv'), 'rb'), delimiter=',', skipinitialspace=True)
	dataorder = np.array([row[0] for row in syllReader])[1::]
if (datatype=='meta'):
	if (serv=='0'):
		destination = '/Users/mht/Documents/research/syllogism/models/metadata/'
	else:
		destination = '/home/mht/DATA/META-data/'
	if (expname=='AMFO'):
		datafile = 'oc_phm_appD_exp1.tsv'
	if (expname=='MFIE'):
		datafile = 'oc_phm_appE_exp2.tsv'
	spamReader = csv.reader(open(destination+datafile, 'rb'),delimiter=' ', skipinitialspace=True)
	dataorder = np.array([row[0] for row in spamReader])[1::]
	data0 = np.loadtxt(destination+datafile,skiprows=1,usecols=(1,3,5,7,9))
	#data0 = phm[np.argsort(np.array(dataorder))]

#premisefile = glob.glob('*lattice*Full*premiseorder.csv')
#syllReader = csv.reader(open(premisefile[0], 'rb'), delimiter=',', skipinitialspace=True)
#syllorder = np.array([row[0] for row in syllReader])

nvc_array = data0[:,4]
if (nvc=='0'):
	data1 = data0[:,0:4]/(np.array(data0[:,0:4]).sum(axis=1))[:,np.newaxis]
	data = data1[np.argsort(dataorder)]
else:
	data = data0[np.argsort(dataorder)]

if (nvc =='1'):
	vc = 5
else:
	vc = 4

def syll_optimize(z):
	if (ndepth=='1'): #if interpretation model, optimize alpha for interpretation + br
		br, alphq = z
		alphr = alphr0
	elif (mdepth=='1'): #if production model, optimize alpha for production + br
		br, alphr = z
		alphq = alphq0
	else:
		br = z
		alphq = 1
		alphr = 1
	qdepth, rdepth, nvc, vc, vcord, exp = ndepth, mdepth, nvc, 4, 'CA', expname
	#rq = 1
	#rr = 1
	#cost = 2.00
	from lattice_syll_fnc import syllogism_model
	syllorder, model_data = syllogism_model(n_obj,br,qdepth,rdepth,alphq,alphr,serv,nvc,vc,vcord,exp)
	if sum(np.sum(model_data,axis=0)!=0)==vc:
		model = np.array(model_data[:,np.sum(model_data,axis=0)!=0])
		modeltype = '4choice'
	else:
		model = np.concatenate((np.array(model_data[:,0:4]+model_data[:,4:8]),np.array(model_data[:,8:9])),axis=1)
		modeltype = '8choice'
	model_mc = 	np.array(model[np.argsort(syllorder)])
	liklhood = -sum([multinomial(vc,d,m) for d,m in zip(model_mc,data)])
	corr = np.corrcoef(np.ravel(data),np.ravel(model_mc))[1,0]
	print corr
	return liklhood

if (ndepth=='1'): #if interpretation model, optimize alpha for interpretation + br
	x0 = np.array([br0,alphq0])
elif (mdepth=='1'): #if production model, optimize alpha for production + br
	x0 = np.array([br0,alphr0])
else:
	x0 = np.array([br0])
resNM = optimize.minimize(syll_optimize,x0, method='nelder-mead',options={'maxiter':100, 'disp': True})
print resNM['x']
sys.stdout = open((destination+'simplex_%s_%s%s.txt' % (expname,ndepth,mdepth)),'w')
print resNM['x']
sys.stdout.close()
