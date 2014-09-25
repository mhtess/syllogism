import itertools
import numpy as np

def myunique(a):
    u = np.array([np.array(x) for x in set(tuple(x) for x in a)])
    return u, np.array([len(a[np.all(a==x, axis=1)]) for x in u],dtype=int)

def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return itertools.izip(*[iter(iterable)]*n)

def decode_premises(premise,figdict):
    mood = premise[2]+premise[3]
    figure = figdict[premise[1]+premise[0]]
    return mood+str(figure)