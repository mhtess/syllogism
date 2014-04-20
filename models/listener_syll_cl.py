

#def syllogism_model(n_balls,base_rate,qdepth,serv,nvc):
#### IMPORT LOTS OF STUFF

import itertools as it
import random
import numpy as np
import os
import subprocess
import math
import sys
import csv
import scipy
import shutil
import glob
from write_churchListen_syll import write_church
dn, n_b, br, qdepth, serv, nvc = sys.argv
n_balls = int(n_b)
base_rate = float(br)
ndepth = str(int(qdepth))
print sys.argv
### SET UP FOLDERS FOR WRITING
if (nvc==1):
    destfold = ('LISTENER_withNVC_%s/' % (qdepth))
else:
    destfold = ('LISTENER_%s/' % (qdepth))
if (serv==1):
    destination = ('/home/mht/MODEL/%s' % destfold)
else:
    destination = ('/Users/mht/Documents/research/syllogism/models/modeldata/%s' % destfold)
if not os.path.exists(destination):
    os.mkdir(destination)
os.chdir(destination)
### SET NUMBER OF SAMPLES (*1000)
n_samples = 100
### FOR MOST / FEW, Set threshold; right now, only one threshold for the two
threshold = 0.5
### if literal model, don't iterate over rationalities
### if pragmatics model, iterate over different rationalities
if int(qdepth) > 0:
    rationQrange = np.arange(1,5.00,0.25)
else:
    rationQrange = np.arange(1,1.20,0.25)
### existential presupposition, WARNING: has not been updated to work with EP = 0
EP = 1
# This is the logic of the model, the definitions of all, some, not-all, none
def A_eval(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def O_eval(s,p):
    return (np.array(~np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def E_eval(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def I_eval(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def NVC(s,p):
    return (np.ones((s.shape[0]),dtype=bool))
def M_eval(s,p):
    return (np.array(np.nan_to_num(np.divide(np.sum(np.logical_and(s,p),axis=1),np.sum(p,axis=1),dtype=float))>(threshold)))
def F_eval(s,p):
    return (np.array(np.nan_to_num(np.divide(np.sum(np.logical_and(s,p),axis=1),np.sum(p,axis=1),dtype=float))<(threshold)))
def A_evalnoEP(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1)))
def O_evalnoEP(s,p):
    return (np.array(~np.logical_or(s,~p).all(axis=1)))
def E_evalnoEP(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1)))
def I_evalnoEP(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1)))
def N_eval(s,p):
    return np.array(~p.any(axis=1))
def A_evaln(s,p):
    return (np.array(np.logical_or(s,abs(1-p)).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def O_evaln(s,p):
    return (np.array(~np.logical_or(s,abs(1-p)).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def E_evaln(s,p):
    return (np.array(np.logical_or(abs(1-p),abs(1-s)).all(axis=1))&s.any(axis=1)&p.any(axis=1))
def I_evaln(s,p):
    return (np.array(~np.logical_or(abs(1-p),abs(1-s)).all(axis=1))&s.any(axis=1)&p.any(axis=1))
# This is the sampling procedure of the model. This amounts to flipping <code>n_ball</code> coins of <code>base_rate</code> weight.
def sample_fig1():
    S,M,P = [False, False],[False, False],[False, False]
    S = np.random.uniform(size=n_balls) < base_rate
    M = np.random.uniform(size=n_balls) < base_rate
    P = np.random.uniform(size=n_balls) < base_rate
    return S, M, P
def sample_joint(pV,features,n_balls):
    S = np.zeros(n_balls,dtype=bool)
    M = np.zeros(n_balls,dtype=bool)
    P = np.zeros(n_balls,dtype=bool)
    while ((sum(S)==0) | (sum(P)==0) | (sum(M)==0)):
        probabilities = np.random.multinomial(n_balls,pV)
        count = 0
        for j,i in enumerate(probabilities):
            for _ in range(i):
                S[count] = bool(features[j][0])
                M[count] = bool(features[j][1])
                P[count] = bool(features[j][2])
                count = count + 1
    return S, M, P
# This is fancy procedue for finding the unique rows of matrix, and their respective frequencies
def myunique(a):
    u = np.array([np.array(x) for x in set(tuple(x) for x in a)])
    return u, np.array([len(a[np.all(a==x, axis=1)]) for x in u],dtype=int)
def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return it.izip(*[iter(iterable)]*n)
def decode_premises(premise):
    mood = premise[2]+premise[3]
    figure = figdict[premise[1]+premise[0]]
    return mood+str(figure)
### RUNS CHURCH
def run_church(rtnQ):
    prefix = 'EP%d_n%d_base%.2f_s%dk' % (EP,n_balls,base_rate,n_samples)
    fname = 'listener_' + prefix + '.church'
    if (serv==1):
        os.chdir('/home/mht/webchurch/')
    else:
        os.chdir('/Users/mht/webchurch/')
    rname = 'listener_N' + ndepth + '_' + prefix + '_a' + str(rtnQ) + '.results'
    print 'listening, reasoning...' + str(rtnQ)
    rid = open(destination + rname, 'w')
#    subprocess.call(['node','test/run_sandbox.js', destination+fname],stdout=rid)
    arguments = str(rtnQ) +',' + ndepth
    subprocess.call(['church', '-a' ,arguments, destination+fname],stdout=rid)
    rid.close()
def parse_church(fnl,rnm):
    os.chdir(destination)
    rg = open(rnm)
    line = rg.readline()
    rg.close()
    line1 = line.split('))')
    res = []
    for i in line1:
        for j in i.split(') ('):
            res.append(j.translate(None,'('))
    match = ['Aps','Eps','Ips','Ops','Asp','Esp','Isp','Osp']
    if (nvc==1): match.append('NVCsp')
    for x, (y,z) in enumerate(grouped(res, 2)):
        for ya, za in zip(y.split(),z.split()):
            fnl[x,match.index(ya)]=za
    return fnl
######################
######################
######################
termpairs = list(it.permutations(['S','M','P'],2))
#termpairsalt = list([('S', 'N'), ('N', 'S'), ('N', 'P'), ('P', 'N')])
#qud = list([('S','P'),('P','S')])
Relations = [A_eval,E_eval,I_eval,O_eval]
RelationsnoEP = [A_evalnoEP,E_evalnoEP,I_evalnoEP,O_evalnoEP,N_eval]
relations = ['A','E','I','O']
#propositionsalt = list(it.product(termpairsalt,relations))
#propositions = propositionsorig + propositionsalt
#qudpropositions = list(it.product(qud,relations))
#relations = ['A','I','E','O']
if (EP == 0):
    prelations = ['A','E','I','O','N']
    propsorig = list(it.product(termpairs,RelationsnoEP))
  #  propsalt = list(it.product(termpairsalt,RelationsnoEP))
else:
    propsorig = list(it.product(termpairs,Relations))
    if (nvc==1): propsorig.append((('S','P'),NVC))
    prelations = ['A','E','I','O']
  #  propsqud = list(it.product(qud,Relations))
  #  propsalt = list(it.product(termpairsalt,Relations))
props = propsorig#+propsalt
propositions = list(it.product(termpairs,prelations))
if (nvc==1): propositions.append((('S','P'),'NVC'))
alements = ['mp','pm']
blements = ['sm','ms']
premises = list(it.product(blements,alements,relations,relations))
posspremises = list(it.product(blements,alements,prelations,prelations))
alementsalt = ['np','pn']
blementsalt = ['sn','ns']
premisesalt = list(it.product(blementsalt,alementsalt,relations,relations))
p1s = list(it.product(relations,alements)) 
p2s = list(it.product(relations,blements))
####################
####################
####################
print 'sampling and featurizing...'
samples = np.array([sample_fig1() for _ in range(1000*n_samples)])
S, M, P = samples.transpose(1, 0, 2)
rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
equiv_rs0, equiv_count = myunique(rs1)
equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
passdict = {'nvc':nvc,'posspremises':posspremises,'premises':premises,'equiv_prob':equiv_prob,'propositions':propositions,'equiv_rs0':equiv_rs0,'ndepth':ndepth,'n_balls':n_balls}
#for rtnQ in rationQrange:
prefix = 'EP%d_n%d_base%.2f_s%dk' % (EP,n_balls,base_rate,n_samples)
fname = 'listener_' + prefix + '.church'
passdict['fname'] = fname
write_church(passdict)
#   prefix = 'EP%d_alphQ%.1f_n%d_base%.2f_s%dk' % (EP,0,n_balls,base_rate,n_samples)
#  fname = 'listener_N' + ndepth + '_' + prefix + '.church'
#  passdict['fname'] = fname
#  write_church(0,passdict)
for rationalityQ in rationQrange:
    final = np.zeros((64,9))
    run_church(rationalityQ)
    rname = 'listener_N' + ndepth + '_' + prefix + '_a' + str(rationalityQ) + '.results'
    final = parse_church(final,rname)
    aprefix = 'EP%d_alphQ%.1f_n%d_base%.2f_s%dk' % (EP,rationalityQ,n_balls,base_rate,n_samples)
    afname = 'listener_N' + ndepth + '_' + aprefix + '.csv'
    np.savetxt(afname, final, delimiter=',',header='Aps,Eps,Ips,Ops,Asp,Esp,Isp,Osp,NVCsp')
# run and parse the prior predictions
final = np.zeros((64,9))
run_church(0)
rname = 'listener_N' + ndepth + '_' + prefix + '_a' + str(0) + '.results'
final = parse_church(final,rname)
aprefix = 'prior_n%d_base%.2f_s%dk' % (n_balls,base_rate,n_samples)
afname = 'listener_N' + ndepth + '_' + aprefix + '.csv'
np.savetxt(afname, final, delimiter=',',header='Aps,Eps,Ips,Ops,Asp,Esp,Isp,Osp,NVCsp')
figdict = {'mpsm':1, 'pmsm': 2, 'mpms': 3, 'pmms':4}
syll = [decode_premises(p) for p in premises]
fname = 'syllistener_premiseorder.csv' 
fid = open(fname,'w')
for s,p in zip(syll,premises):
    fid.write('%s,%s%s%s %s%s%s%s\n' % (s, "(list '",p[2],p[1],"'",p[3],p[0],")"))
fid.close()
if not os.path.exists((destination+'results/')):
    os.mkdir((destination+'results/'))
if not os.path.exists((destination+'csv/')):
    os.mkdir((destination+'csv/'))
for data in glob.glob((destination+'*.csv')):
    shutil.copy(data,(destination+'csv/'))
    os.remove(data)
for data in glob.glob((destination+'*.results')):
    shutil.copy(data,(destination+'results/'))
    os.remove(data)

