#!/usr/bin/python
import subprocess
import os
def run_church(churchfile,rtnQ,rtnR,ndepth,mdepth,serv,prefix,latlis,destination):
    if (serv==1):
        os.chdir('/home/mht/webchurch/')
    else:
        os.chdir('/Users/mht/webchurch/')
    rname = latlis+'_N' + ndepth + '_M' + mdepth +'_' + prefix + '_aq' + str(rtnQ) + '_ar' + str(rtnR) + '.results'
    print 'listening, reasoning, speaking... alpha' + str(rtnQ)
    rid = open(destination + rname, 'w')
    arguments = ndepth + ',' + str(rtnQ)
    subprocess.call(['church', '-a' ,arguments, churchfile],stdout=rid)
    rid.close()