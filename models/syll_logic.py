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
    while ((sum(S)==0) | (sum(P)==0) | (sum(M)==0)): # this condition gaurentees there is at least something to talk about
    # it's a bit of strange condition, but the original quantifier meanings are only true if both sets are nonempty
    # hence, this condition still permits worlds in which nothing is true
        probabilities = np.random.multinomial(n_balls,pV)
        count = 0
        for j,i in enumerate(probabilities):
            for _ in range(i):
                S[count] = bool(int(features[j].zfill(3)[2])) # i switched this on 8/7/14;
                M[count] = bool(int(features[j].zfill(3)[1])) # before then, S mapped onto A; and P mapped onto C
                P[count] = bool(int(features[j].zfill(3)[0])) # now it reads like it should  PMS = ABC
                count = count + 1
    return S, M, P

def sample_joint_sansEP(pV,features,n_balls):
    S = np.zeros(n_balls,dtype=bool)
    M = np.zeros(n_balls,dtype=bool)
    P = np.zeros(n_balls,dtype=bool)
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
# There are all written in the reverse direction (P-S), but this is corrected in the syll_model.py

# Set 1: these assume all sets are nonempty (this was used as the standard up to 11/13/14)

# All P are S: False if there is a P which is also not an S.
# ... take the negation of this: ~(P & ~S) --> ~P or S
def A_eval(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))
# Some P are not S <--> Not all P are S
# ... take the negation of All P are S
def O_eval(s,p):
    return (np.array(~np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))
# No P are S: False if something is something is P which is also S
# ... take negation: ~( P & S) --> ~P or ~S
def E_eval(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))
# Some P are S
# ... take the negation of No P are S
def I_eval(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))

# Coextential alternative: As are Bs and Bs are As.

def equality_eval(s,p):
    return (s==p).all(axis=1)&s.any(axis=1)&p.any(axis=1)

# Double conclusion alternatives: 
# This in the hopes of better modeling the task: alternative set is (All, Some, None, Some..not, All and some, Some and some...not, Some...not and None)
# Given the Set 1 semantics, the only novel eval is Some and not all. 

def IO_eval(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&np.array(~np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))

def AI_eval(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1))&np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))

def EO_eval(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1))&np.array(~np.logical_or(s,~p).all(axis=1))&s.any(axis=1)&p.any(axis=1))

# Relaxed universals: All and None are relaxed by the smallest amount
# All: True if All or All-1 have it
# None: True if 0 or 1 have it
def A_eval_slack(s,p):
    return (np.sum(np.logical_and(s,p),axis=1)-np.sum(p,axis=1))>=-1

def E_eval_slack(s,p):
    return np.sum(np.logical_and(s,p),axis=1)<=1

# This is a null utterance. always true.
def NVC(s,p):
    return (np.ones((s.shape[0]),dtype=bool))

# Threshold semantics most and few
def M_eval(s,p):
    return (np.array(np.nan_to_num(np.divide(np.sum(np.logical_and(s,p),axis=1),np.sum(p,axis=1),dtype=float))>(threshold)))
def F_eval(s,p):
    return (np.array(np.nan_to_num(np.divide(np.sum(np.logical_and(s,p),axis=1),np.sum(p,axis=1),dtype=float))<(threshold)))
#####

# Set 2: Aristotle's presuppositions.
###      Universal quantifiers (All / None) can be vacuously true.
###      Particular quantifiers (Some / Not all) must have some P.
###### "Some" additional must have some S. "Not all" additionally must have some ~S.

def A_evalnoEP(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1)))
def O_evalnoEP(s,p):
    return (np.array(~np.logical_or(s,~p).all(axis=1))&p.any(axis=1)&(~s).any(axis=1))
def E_evalnoEP(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1)))
def I_evalnoEP(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1))
# "No P", returns true is there are no Ps
# note order of operations: any is done before the ~
def N_eval(s,p):
    return np.array(~p.any(axis=1))

# Set 3: Determiner presuppositions.
###      q of the X are Y presupposes some X (not necessarily some Y)
###### "Some" additional must have some S. "Not all" additionally must have some ~S.

def A_evalDPEP(s,p):
    return (np.array(np.logical_or(s,~p).all(axis=1))&p.any(axis=1))
def O_evalDPEP(s,p):
    return (np.array(~np.logical_or(s,~p).all(axis=1))&p.any(axis=1)&(~s).any(axis=1))
def E_evalDPEP(s,p):
    return (np.array(np.logical_or(~p,~s).all(axis=1))&p.any(axis=1))
def I_evalDPEP(s,p):
    return (np.array(~np.logical_or(~p,~s).all(axis=1))&s.any(axis=1)&p.any(axis=1)&p.any(axis=1))

# "No P", returns true is there are no Ps
# note order of operations: any is done before the ~
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