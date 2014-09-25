import itertools as it
import os
from syll_helpers import grouped

def parse_church(fnl,rnm,destination,exp,nvc):
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
    if (exp=='AMFO'):
        match = ['Aps','Mps','Fps','Ops','Asp','Msp','Fsp','Osp']
    if (exp=='MFIE'):
        match = ['Mps','Fps','Ips','Eps','Msp','Fsp','Isp','Esp']
    if (nvc==1): match.append('NVCsp')
    for x, (y,z) in enumerate(grouped(res, 2)):
        for ya, za in zip(y.split(),z.split()):
            fnl[x,match.index(ya)]=za
    return fnl