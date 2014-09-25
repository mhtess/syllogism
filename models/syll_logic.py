import itertools
import numpy as np

# SAMPLE WORLDS
def sample_fig1(n_balls,base_rate):
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
                S[count] = bool(int(features[j].zfill(3)[2])) # i switched this on 8/7/14;
                M[count] = bool(int(features[j].zfill(3)[1])) # before then, S mapped onto A; and P mapped onto C
                P[count] = bool(int(features[j].zfill(3)[0])) # now it reads like it should  PMS = ABC
                count = count + 1
    return S, M, P

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
    return (np.array(~np.logical_or(s,~p).all(axis=1))&p.any(axis=1)&(~s).any(axis=1))
def E_evalnoEP(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1)))
def I_evalnoEP(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))
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