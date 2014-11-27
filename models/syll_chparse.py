import itertools as it
import os
import numpy as np
from syll_helpers import grouped

def parse_church(resfile,destination,experiment,indevals):
    fnl = np.zeros((64,10))
    os.chdir(destination)
    rg = open(resfile)
    line = rg.readline()
    rg.close()
    line1 = line.split('))')
    res = []
    for i in line1:
        for j in i.split(') ('):
            res.append(j.translate(None,'('))
    #match = ['Aps','Eps','Ips','Ops','Asp','Esp','Isp','Osp']
    match = ['all.A-C','none.A-C','some.A-C','not-all.A-C','all.C-A','none.C-A','some.C-A','not-all.C-A','mu']
    if (experiment=='AMFO'):
        #match = ['Aps','Mps','Fps','Ops','Asp','Msp','Fsp','Osp']
        match = ['all.A-C','most.A-C','few.A-C','not-all.A-C','all.C-A','most.C-A','few.C-A','not-all.C-A','mu']
    if (experiment=='MFIE'):
        #match = ['Mps','Fps','Ips','Eps','Msp','Fsp','Isp','Esp']
        match = ['most.A-C','few.A-C','some.A-C','none.A-C','most.C-A','few.C-A','some.C-A','none.C-A','mu']
    if (indevals==1):
        fnl = np.zeros((64,13))
        match = ['all.A-C','none.A-C','some.A-C','not-all.A-C','all.C-A','none.C-A','some.C-A','not-all.C-A',
            'all+some.C-A','some+not-all.C-A','none+not-all.C-A','mu']
    match.append('undefined')
    for x, (y,z) in enumerate(grouped(res, 2)):
        for ya, za in zip(y.split(),z.split()):
            fnl[x,match.index(ya)]=za
    return fnl