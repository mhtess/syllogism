

def syllogism_model(n_b, br, qdepth, rdepth, rationalityQ, rationalityR, serv, nvcstr, vcstr, vcord, exp):
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
    from write_churchLattice_syll import write_church
    #dn, n_b, br, qdepth, rdepth, serv, nvcstr, vcstr, vcord = sys.argv
    n_balls = int(n_b)
    base_rate = float(br)
    vc = int(vcstr)
    nvc = int(nvcstr)
    serv = int(serv)
    ndepth = str(int(qdepth))
    mdepth = str(int(rdepth))
    fig = 'Full'
    #print sys.argv
    ### SET UP FOLDERS FOR WRITING
    if (nvc==1):
        if (exp=='AIEO'):
            macfold = ('LATTICE_%d_withNVC/' % vc)
        else:
            macfold = ('LATTICE_%s%s_withNVC/' % (exp,vc))
    else:
        if (exp=='AIEO'):
            macfold = ('LATTICE_%d/' % (vc))
        else:
            macfold = ('LATTICE_%s%s/' % (exp,vc))
    #destfold = destpref +'_'+str(vc)+'c/'
    destfold = ('%s%s/' % (qdepth,rdepth))
    if (serv==1):
        macpth = ('/home/mht/MODEL/%s' % macfold)
    else:
        macpth = ('/Users/mht/Documents/research/syllogism/models/modeldata/%s' % macfold)
    if not os.path.exists(macpth):
        os.mkdir(macpth)
    destination = macpth+destfold
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
        rationQrange = np.arange(1,5.00,1.00)
    else:
        rationQrange = np.arange(1,1.20,0.25)
    if int(rdepth) > 0:
        rationRrange = np.arange(1,5.00,1.00)
    else:
        rationRrange = np.arange(1,1.20,0.25)
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
    def run_church(churchfile,rtnQ,rtnR,ndepth,mdepth):
        # if (exp=='AIEO'):
        #     prefix = 'fig%s_c%d%sEP%d_n%d_base%.2f_s%dk' % (fig,vc,vcord,EP,n_balls,base_rate,n_samples)
        # else:
        #     prefix = 'fig%s_%sc%d%sEP%d_n%d_base%.2f_s%dk' % (fig,exp,vc,vcord,EP,n_balls,base_rate,n_samples)
        # fname = 'lattice_' + prefix + '.church'
        if (serv==1):
            os.chdir('/home/mht/webchurch/')
        else:
            os.chdir('/Users/mht/webchurch/')
        rname = 'lattice_N' + ndepth + '_M' + mdepth +'_' + prefix + '_aq' + str(rtnQ) + '_ar' + str(rtnR) + '.results'
        print 'listening, reasoning, speaking...' + str(rtnQ) + str(rtnR)
        rid = open(destination + rname, 'w')
    #    subprocess.call(['node','test/run_sandbox.js', destination+fname],stdout=rid)
        arguments = str(rtnQ) +',' + str(rtnR) + ',' + ndepth + ',' + mdepth
        subprocess.call(['church', '-a' ,arguments, churchfile],stdout=rid)
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
        if (exp=='AMFO'):
            match = ['Aps','Mps','Fps','Ops','Asp','Msp','Fsp','Osp']
        if (exp=='MFIE'):
            match = ['Mps','Fps','Ips','Eps','Msp','Fsp','Isp','Esp']
        if (nvc==1): match.append('NVCsp')
        for x, (y,z) in enumerate(grouped(res, 2)):
            for ya, za in zip(y.split(),z.split()):
                fnl[x,match.index(ya)]=za
        return fnl
    ######################
    ######################
    ######################
    if (exp=='AIEO'):
        prefix = 'fig%s_c%d%sEP%d_n%d_base%.2f_s%dk' % (fig,vc,vcord,EP,n_balls,base_rate,n_samples)
    else:
        prefix = 'fig%s_%sc%d%sEP%d_n%d_base%.2f_s%dk' % (fig,exp,vc,vcord,EP,n_balls,base_rate,n_samples)
    fname = 'lattice_' + prefix + '.church'
    termpairs = list(it.permutations(['S','M','P'],2))
    if (fig=='1'):
        termpairs = list((('S','M'),('M','P'),('S','P')))
    #termpairsalt = list([('S', 'N'), ('N', 'S'), ('N', 'P'), ('P', 'N')])
    #qud = list([('S','P'),('P','S')])
    Relations = [A_eval,E_eval,I_eval,O_eval]
    RelationsnoEP = [A_evalnoEP,E_evalnoEP,I_evalnoEP,O_evalnoEP,N_eval]
    relations = ['A','E','I','O']
    if (exp=='AMFO'):
        Relations = [A_eval,M_eval,F_eval,O_eval]
        relations = ['A','M','F','O']
    if (exp=='MFIE'):
        Relations = [M_eval,F_eval,I_eval,E_eval]
        relations = ['M','F','I','E']
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
        prelations = relations
      #  propsqud = list(it.product(qud,Relations))
      #  propsalt = list(it.product(termpairsalt,Relations))
    props = propsorig#+propsalt
    propositions = list(it.product(termpairs,prelations))
    if (nvc==1): propositions.append((('S','P'),'NVC'))
    alements = ['mp','pm']
    blements = ['sm','ms']
    if (fig=='1'): 
        alements = ['mp']
        blements = ['sm']
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
    churchfile = macpth+'church/'+fname
    if not os.path.exists(churchfile):
        print 'sampling and featurizing... br=' + str(base_rate)
        samples = np.array([sample_fig1() for _ in range(1000*n_samples)])
        S, M, P = samples.transpose(1, 0, 2)
        rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
        rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
        equiv_rs0, equiv_count = myunique(rs1)
        equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
        passdict = {'nvc':nvc,"vc":vc,"vcord":vcord,'posspremises':posspremises,'premises':premises,'equiv_prob':equiv_prob,'propositions':propositions,'equiv_rs0':equiv_rs0,'ndepth':ndepth,'mdepth':mdepth,'n_balls':n_balls,'exp':exp}
        #for rtnQ in rationQrange:
        if (exp=='AIEO'):
            prefix = 'fig%s_c%d%sEP%d_n%d_base%.2f_s%dk' % (fig,vc,vcord,EP,n_balls,base_rate,n_samples)
        else:
            prefix = 'fig%s_%sc%d%sEP%d_n%d_base%.2f_s%dk' % (fig,exp,vc,vcord,EP,n_balls,base_rate,n_samples)
        fname = 'lattice_' + prefix + '.church'
        passdict['fname'] = fname
        write_church(passdict)
        if not os.path.exists((macpth+'church/')):
            os.mkdir((macpth+'church/'))
        for data in glob.glob((macpth+'*.church')):
            shutil.copy(data,(macpth+'church/'))
            os.remove(data)
    #   prefix = 'EP%d_alphQ%.1f_n%d_base%.2f_s%dk' % (EP,0,n_balls,base_rate,n_samples)
    #  fname = 'listener_N' + ndepth + '_' + prefix + '.church'
    #  passdict['fname'] = fname
    #  write_church(0,passdict)
    head = 'Aps,Eps,Ips,Ops,Asp,Esp,Isp,Osp,NVCsp'
    if (exp=='AMFO'):
        head = 'Aps,Mps,Fps,Ops,Asp,Msp,Fsp,Osp,NVCsp'
    if (exp=='MFIE'):
        head = 'Mps,Fps,Ips,Eps,Msp,Fsp,Isp,Esp,NVCsp'
  #  for rationalityQ in rationQrange:
   #     for rationalityR in rationRrange:
    final_out = np.zeros((64,9))
    run_church(churchfile,rationalityQ,rationalityR,ndepth,mdepth)
    rname = 'lattice_N' + ndepth + '_M' + mdepth +'_' + prefix + '_aq' + str(rationalityQ) + '_ar' + str(rationalityR) + '.results'
    final_out = parse_church(final_out,rname)
    if (exp=='AIEO'):
        aprefix = 'fig%s_c%d%sEP%d_alphQ%.1f_alphR%.1f_n%d_base%.2f_s%dk' % (fig,vc,vcord,EP,rationalityQ,rationalityR,n_balls,base_rate,n_samples)
    else:
        aprefix = 'fig%s_%sc%d%sEP%d_alphQ%.1f_alphR%.1f_n%d_base%.2f_s%dk' % (fig,exp,vc,vcord,EP,rationalityQ,rationalityR,n_balls,base_rate,n_samples)
    afname = 'lattice_N' + ndepth + '_M' + mdepth +'_' + aprefix + '.csv'
    np.savetxt(afname, final_out, delimiter=',',header=head)
    # run and parse the prior predictions###############
    ####################################################
    rname = 'lattice_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + '_ar' + str(0) + '.results'
    if not os.path.exists((destination+'results/'+rname)):
        final = np.zeros((64,9))
        run_church(churchfile,0,0,ndepth,mdepth)
        rname = 'lattice_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + '_ar' + str(0) + '.results'
        final = parse_church(final,rname)
        if (exp=='AIEO'):
            aprefix = 'priorFig%s_c%d%s_n%d_base%.2f_s%dk' % (fig,vc,vcord,n_balls,base_rate,n_samples)
        else: 
            aprefix = 'priorFig%s_%sc%d%s_n%d_base%.2f_s%dk' % (fig,exp,vc,vcord,n_balls,base_rate,n_samples)
        afname = 'lattice_N' + ndepth + '_M' + mdepth + '_' + aprefix + '.csv'
        np.savetxt(afname, final, delimiter=',',header=head)
    ##################################################
    fname = ('syllattice_%sfig%s_premiseorder.csv' % (exp,fig))
    figdict = {'mpsm':1, 'pmsm': 2, 'mpms': 3, 'pmms':4}
    syll = [decode_premises(p) for p in premises]
    if not os.path.exists((destination+'csv/'+fname)):
        fid = open(fname,'w')
        for s,p in zip(syll,premises):
            fid.write('%s,%s%s%s %s%s%s%s\n' % (s, "(list '",p[2],p[1],"'",p[3],p[0],")"))
        fid.close()
    if not os.path.exists((destination+'results/')):
        os.mkdir((destination+'results/'))
    if not os.path.exists((destination+'csv/')):
        os.mkdir((destination+'csv/'))
    for data in glob.glob((destination+'*.results')):
        shutil.copy(data,(destination+'results/'))
        os.remove(data)
    for data in glob.glob((destination+'*.csv')):
        shutil.copy(data,(destination+'csv/'))
        os.remove(data)
    return syll, final_out

