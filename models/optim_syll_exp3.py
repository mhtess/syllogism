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

datatype = 'experiment'
datatype = 'meta'
expname = '02syllogism-4ac'
#expname = 'AMFO'
#expname = 'AIEO'
#ctypes = 'AMFO'
ctypes = 'AIEO'
serv = '0'
n_obj = sys.argv[1]
br0 = sys.argv[2]

ndepth = sys.argv[3]
mdepth = sys.argv[4]

alphq0 = sys.argv[5]
alphr0 = sys.argv[6]

vc_in = sys.argv[7]
nvc = sys.argv[8]

EPin=sys.argv[9]
#fig = '1'
fig = 'Full'
lis = 'lis'
#lis = 'lat'

if (datatype == 'experiment'):
	if (serv=='0'):
		destination = ('/Users/mht/Documents/research/syllogism/data/%s/' % (expname))
	else:
		destination = ('/home/mht/DATA/%s/')
	data0 = np.loadtxt((destination+'meanCncl_syll02_n100.csv'),skiprows=1,delimiter=",",usecols = (1,2,3,4,5))
	syllReader = csv.reader(open((destination+'meanCncl_syll02_n100.csv'), 'rb'), delimiter=',', skipinitialspace=True)
	dataorder = np.array([row[0] for row in syllReader])[1::]
if (datatype=='meta'):
	if (serv=='0'):
		destination = '/Users/mht/Documents/research/syllogism/models/metadata/'
	else:
		destination = '/home/mht/DATA/META-data/'
	if (expname=='AIEO'):
		datafile = 'oc_phm_appC_mAnalysis.tsv'
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
	vc_in = vc_in +1

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
	qdepth, rdepth, vc, vcord, exp = ndepth, mdepth, vc_in, 'CA', ctypes
	#rq = 1
	#rr = 1
	#cost = 2.00
	from lattice_syll_fnc import syllogism_model
	syllorder, model_data = syllogism_model(n_obj,br,qdepth,rdepth,alphq,alphr,serv,nvc,vc,vcord,exp,fig,lis,EPin)
	if sum(np.sum(model_data,axis=0)!=0)==4:
		model = np.array(model_data[:,np.sum(model_data,axis=0)!=0])
		modeltype = '4choice'
		if (nvc=='1'):
			model=model[:,np.array([0,2,1,3,4])]
		else:
			model=model[:,np.array([0,2,1,3])]
	elif sum(np.sum(model_data,axis=0)!=0)==6:
		model = np.concatenate((np.array(model_data[:,0:4]+model_data[:,4:8]),np.array(model_data[:,8:9])),axis=1)
		modeltype = '6choice'
		if (nvc=='1'):
			model=model[:,np.array([0,2,1,3,4])]
		else:
			model=model[:,np.array([0,2,1,3])]
	else:
		model = np.concatenate((np.array(model_data[:,0:4]+model_data[:,4:8]),np.array(model_data[:,8:9])),axis=1)
		modeltype = '8choice'
		if (nvc=='1'):
			model=model[:,np.array([0,2,1,3,4])]
		else:
			model=model[:,np.array([0,2,1,3])]
	model_mc = 	np.array(model[np.argsort(syllorder)]) #this 0,2,1,3 switch is for phmeta, not sure if needed otherwise
	model_mc = model_mc + 0.01
	liklhood = -sum([multinomial((model_mc).shape[0],d,m) for d,m in zip(model_mc,data)])
	corr = np.corrcoef(np.ravel(data),np.ravel(model_mc))[1,0]
	print corr
	return liklhood


if (ndepth=='1'): #if interpretation model, optimize alpha for interpretation + br
	print 'intepretation'
	x0 = np.array([br0,alphq0])
elif (mdepth=='1'): #if production model, optimize alpha for production + br
	x0 = np.array([br0,alphr0])
	print 'production'
else:
	x0 = np.array([br0])
	rranges = np.arange(0.05, 0.45, 0.05)
	print 'literal'
#resNM = optimize.minimize(syll_optimize,x0, method='nelder-mead',options={'maxiter':100, 'disp': True})
#resNM = optimize.brute(syll_optimize,rranges, full_output=True)
for brz in np.arange(0.15,0.45,0.05):
	#syll_optimize([brz,alphq0])
	syll_optimize(brz)


#print resNM['x']
#print resNM['x']
#sys.stdout = open((destination+'simplex_%s_%s%s.txt' % (expname,ndepth,mdepth)),'w')
#sys.stdout = open((destination+'brute%s_%s%s.txt' % (expname,ndepth,mdepth)),'w')
#print resNM['x']
#sys.stdout.close()
