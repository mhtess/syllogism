#!/usr/bin/python
import subprocess
import os
def run_church(churchfile,rtnQ,rtnR,ndepth,mdepth,serv,rname,destination):
    if (serv==1):
        os.chdir('/home/mht/webchurch/')
    else:
        os.chdir('/Users/mht/webchurch/')
    print 'listening, reasoning, speaking... depth' +str(ndepth) + ' alpha' + str(rtnQ)
    rid = open(destination + rname, 'w')
    arguments = ndepth + ',' + str(rtnQ)
    subprocess.call(['church', '-a' ,arguments, churchfile],stdout=rid)
    rid.close()