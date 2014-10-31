import itertools
import numpy as np
import pandas as pd
import os
import csv
import shutil
import glob
import pdb
import random

import syll_logic
from syll_helpers import myunique, grouped, decode_premises
from syll_chwrite import write_church
from syll_chrun import run_church
from syll_chparse import parse_church

from equiv_to_end import f_e_t_e


def syllogism_model(n_b, br, qdepth, rdepth, rationalityQ, rationalityR, domain, priortype,
                    serv=0, nvcstr=0, vcstr=4, vcord='CA', exp='AIEO', fig='Full', 
                    lis='lis', EPin=1):

    n_balls = int(n_b)
    base_rate = float(br)
    vc = int(vcstr)
    nvc = int(nvcstr)
    serv = int(serv)
    ndepth = str(int(qdepth))
    mdepth = str(int(rdepth))
    EP = int(EPin)
    latlis = lis
    qud=1
    n_samples = 100
    bs_samples = 1000
    #fig = 'Full'
    ### FOR MOST / FEW, Set threshold; right now, only one threshold for the two
    threshold = 0.5

    high_passingdict = {'n_balls':n_b,'base_rate':br,'ndepth':ndepth,'mdepth':mdepth,'rationalityQ':rationalityQ,\
        'rationalityR':rationalityR,'serv':serv,'latlis':latlis,'exp':exp}

    # Set up folders and file names
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
    if (domain!='naive'):
        macfold = ('%s_%s/' % (macfold[:-1],priortype))
    #destfold = destpref +'_'+str(vc)+'c/'
    destfold = ('%s%s/' % (qdepth,rdepth))
    if (serv==1):
        macpth = ('/home/mht/projectsyll/MODELDATA/%s/%s/' % (macfold,domain))
    else:
        macpth = ('/Users/mht/Documents/research/syllogism/models/modeldata/%s/' 
            % macfold)
    #expname = '02syllogism-4ac'
    #expname = '03causalbelief_tests'


    if not os.path.exists(macpth):
        os.mkdir(macpth)
    destination = macpth+destfold
    if not os.path.exists(destination):
        os.mkdir(destination)
    os.chdir(destination)

    prefix = ('%s%s_qud%sfig%s_%sc%d%sEP%d_n%d_base%.2f_s%dk' % 
              (priortype,domain,qud,fig,exp,vc,vcord,EP,n_balls,base_rate,n_samples))
    high_passingdict['prefix'] = prefix


    high_passingdict['destination']=destination
    high_passingdict['macpath']=macpth

    priordict = {'Q_XYZ':'111', 'Q_XYnZ':'110', 'Q_XnYZ':'101', 'Q_XnYnZ':'100', 'Q_nXYZ':'011', 'Q_nXYnZ':'010',
       'Q_nXnYZ':'001', 'Q_nXnYnZ':'000'}

    # Define syllogistic space

    termpairs = list(itertools.permutations(['S','M','P'],2))
    if (fig=='1'):
        termpairs = list((('S','M'),('M','P'),('S','P')))
    if (fig=='4'):
        termpairs = list((('M','S'),('P','M'),('S','P')))
    #termpairsalt = list([('S', 'N'), ('N', 'S'), ('N', 'P'), ('P', 'N')])
    #qud = list([('S','P'),('P','S')])


    Relations = [syll_logic.A_eval,syll_logic.E_eval,
                syll_logic.I_eval,syll_logic.O_eval]
    RelationsnoEP = [syll_logic.A_evalnoEP,syll_logic.E_evalnoEP,
                    syll_logic.I_evalnoEP,syll_logic.O_evalnoEP]
    relations = ['A','E','I','O']
    if (exp=='AMFO'):
        Relations = [syll_logic.A_eval,syll_logic.M_eval,syll_logic.F_eval,syll_logic.O_eval]
        relations = ['A','M','F','O']
    if (exp=='MFIE'):
        Relations = [syll_logic.M_eval,syll_logic.F_eval,syll_logic.I_eval,syll_logic.E_eval]
        relations = ['M','F','I','E']
    #propositionsalt = list(it.product(termpairsalt,relations))
    #propositions = propositionsorig + propositionsalt
    #qudpropositions = list(it.product(qud,relations))
    #relations = ['A','I','E','O']
    if (EP == 0):
        #prelations = ['A','E','I','O','N']
        prelations=relations
        propsorig = list(itertools.product(termpairs,RelationsnoEP))
      #  propsalt = list(it.product(termpairsalt,RelationsnoEP))
    else:
        propsorig = list(itertools.product(termpairs,Relations))
        if (nvc==1): propsorig.append((('S','P'),syll_logic.NVC))
        prelations = relations
      #  propsqud = list(it.product(qud,Relations))
      #  propsalt = list(it.product(termpairsalt,Relations))
    props = propsorig#+propsalt
    propositions = list(itertools.product(termpairs,prelations))
    if (nvc==1): propositions.append((('S','P'),'NVC'))
    alements = ['mp','pm']
    blements = ['sm','ms']
    if (fig=='1'): 
        alements = ['mp']
        blements = ['sm']
    if (fig=='4'):
        alements = ['pm']
        blements = ['ms']
    premises = list(itertools.product(blements,alements,relations,relations))
    posspremises = list(itertools.product(blements,alements,prelations,prelations))
    alementsalt = ['np','pn']
    blementsalt = ['sn','ns']
    premisesalt = list(itertools.product(blementsalt,alementsalt,relations,relations))
    p1s = list(itertools.product(relations,alements)) 
    p2s = list(itertools.product(relations,blements))
    figdict = {'mpsm':1, 'pmsm': 2, 'mpms': 3, 'pmms':4}

    passdict = {'qud':qud,'listener':latlis,'nvc':nvc,"vc":vc,
    "vcord":vcord,'posspremises':posspremises,'premises':premises,
    'propositions':propositions,'figdict':figdict,'fig':fig,
    'ndepth':ndepth,'mdepth':mdepth,'n_balls':n_balls,'exp':exp}
    



    # preprocessing (equivalence class)

    if (domain=='naive'):
        fname = latlis+ '_' + prefix + '_Smean.church'
        churchfile = macpth+'church/'+fname
        high_passingdict['churchfile']=churchfile
        passdict['fname']=fname
        high_passingdict['bs']='mean'
        
        if not os.path.exists(churchfile):
            print 'sampling and featurizing... br=' + str(base_rate)
            samples = np.array([syll_logic.sample_fig1(n_balls,base_rate) for _ in range(1000*n_samples)])
            S, M, P = samples.transpose(1, 0, 2)
            rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
            rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
            equiv_rs0, equiv_count = myunique(rs1)
            equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
            passdict['equiv_rs0']=equiv_rs0
            passdict['equiv_prob']=equiv_prob
        
        syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

    else:

        if (serv==0):
            priorpath = ('/Users/mht/Documents/research/syllogism/data/03syllogism_prior_psychjs/')
        else:
            priorpath = ('/home/mht/projectsyll/EXPDATA/03syllogism_prior_psychjs/')

        if (priortype=='bootstrap'):
            expname = 'prior-exp-mturk_all_n71'
            priorfile = priorpath + expname +'.csv'
            phead = pd.read_csv(priorfile,dtype='string',index_col=0)
            pr_dom = phead[phead['domain']==domain].reset_index(drop=True) # get priors for this domain
            pr_dist = pr_dom.iloc[:,1:9].astype(float) # remove other columns
            #pr_norm = pr_dist.div(pr_dist.sum(axis=1), axis=0)
            #pr_norm = pr_norm.replace(0,0.00001) # replace 0s with epsilons

            # bootstrap 1000 times
            for bs in range(bs_samples):
                fname = latlis+ '_' + prefix + '_bs' +str(bs) +'.church'
                churchfile = macpth+'church/'+fname
                high_passingdict['churchfile']=churchfile
                passdict['fname']=fname
                high_passingdict['bs']=str(bs)
                if not os.path.exists(churchfile):
                    print 'sampling and featurizing ' + str(n_balls) + ' ' + domain + ' bssamp ' + str(bs)
                    smp_wr = np.array([np.random.randint(0,pr_dist.shape[0]) for _ in range(pr_dist.shape[0])])
                    smp_pr = pr_dist.iloc[smp_wr]
                    norm_pr = smp_pr.div(smp_pr.sum(axis=1),axis=0)
                    mean_pr = norm_pr.mean(axis=0)
                    priorVector = np.array(mean_pr)
                    features = [priordict[m] for m in mean_pr.index.values]
                    samples = np.array([syll_logic.sample_joint(priorVector,features,n_balls) 
                                    for _ in range(1000*n_samples)])
                    S, M, P = samples.transpose(1, 0, 2)
                    rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
                    rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
                    equiv_rs0, equiv_count = myunique(rs1)
                    equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
                    passdict['equiv_rs0']=equiv_rs0
                    passdict['equiv_prob']=equiv_prob

                syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

        else:

            high_passingdict['bs']='mean'
            fname = latlis+ '_' + prefix + '_Smean.church'
            churchfile = macpth+'church/'+fname
            high_passingdict['churchfile']=churchfile
            passdict['fname']=fname
            expname = 'prior-exp-mturk_means_n71'
            if (priortype=='tfbt'):
                expname = 'prior-exp-mturk_collapsed_means_n71'
            #expname = 'prior-exp-mturk_means_CAswitch_n71'
            #expname = 'prior-exp-mturk_means_samenode_n71'
            priorfile = priorpath + expname +'.csv'

            print 'sampling and featurizing ' + str(n_balls) + ' ' + domain + 's' + ' ' + priortype
            phead = pd.read_csv(priorfile,dtype='string',index_col=0)
            features = phead.columns.values[2::]
            domain_priors = phead[((phead.domain == domain) & (phead.condition == priortype))][features]
            
            if not os.path.exists(churchfile):

                priorVector = np.array(domain_priors,dtype=float)[0]
                samples = np.array([syll_logic.sample_joint(priorVector,features,n_balls) 
                                    for _ in range(1000*n_samples)])
                S, M, P = samples.transpose(1, 0, 2)
                rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
                rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
                equiv_rs0, equiv_count = myunique(rs1)
                equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
                passdict['equiv_rs0']=equiv_rs0
                passdict['equiv_prob']=equiv_prob

            syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

    return syllrows, nz_final


        # run model


    #     write_church(passdict)

    #     if not os.path.exists((macpth+'church/')):
    #         os.mkdir((macpth+'church/'))
    #     for data in glob.glob(('*.church')):
    #         shutil.copy(data,(macpth+'church/'))
    #         os.remove(data)

    # # parse and write to csv
    # head = 'all.A-C,none.A-C,some.A-C,not-all.A-C,all.C-A,none.C-A,some.C-A,not-all.C-A,mu,undefined'
    # if (exp=='AMFO'):
    #     head = 'all.A-C,most.A-C,few.A-C,not-all.A-C,all.C-A,most.C-A,few.C-A,not-all.C-A,mu,undefined'
    # if (exp=='MFIE'):
    #     head = 'most.A-C,few.A-C,some.A-C,none.A-C,most.C-A,few.C-A,some.C-A,none.C-A,mu,undefined'
    # final_out = np.zeros((64,10))
    # run_church(churchfile,rationalityQ,rationalityR,ndepth,mdepth,serv,prefix,latlis,
    #     destination)
    # rname = (latlis+'_N' + ndepth + '_M' + mdepth +'_' + prefix + '_aq' + 
    #             str(rationalityQ) + '_ar' + str(rationalityR) + '.results')

    # final_out = parse_church(rname,destination,exp)
    # nz_final = final_out[np.sum(final_out, axis=1)!=0]

    # aprefix = '%s_alphQ%s_alphR%s' % (prefix,rationalityQ,rationalityR)
    # afname = latlis+'_N' + ndepth + '_M' + mdepth +'_' + aprefix + '.csv'

    # syllrows = [decode_premises(p,figdict) for p in premises]
    # rows = np.array(syllrows, dtype='|S20')[:, np.newaxis]

    # with open(afname, 'w') as f:
    #     np.savetxt(f, np.hstack((rows, nz_final)), delimiter=', ', fmt='%s',
    #         header='syll,'+head)

    # # run conclusion only model
    # rname = (latlis+'_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + 
    #             '_ar' + str(0) + '.results')

    # if not os.path.exists((destination+'results/'+rname)):
    #     run_church(churchfile,0,0,ndepth,mdepth,serv,prefix,latlis,destination)
    #     rname = (latlis+'_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + 
    #             '_ar' + str(0) + '.results')

    #     final = parse_church(rname,destination,exp)
    #     nz_finp = final[np.sum(final, axis=1)!=0]

    #     aprefix = 'CLonly_%s' % (prefix)
    #     afname = latlis+'_N' + ndepth + '_M' + mdepth + '_' + aprefix + '.csv'
    #     with open(afname, 'w') as f:
    #         np.savetxt(f, np.hstack((rows, nz_finp)), delimiter=', ', fmt='%s',
    #             header='syll,'+head)

    # # write syllogism order to file as well, just in case

    # fname = ('syllattice_%squd%sfig%s_premiseorder.csv' % (exp,qud,fig))
    # if not os.path.exists((destination+'csv/'+fname)):
    #     fid = open(fname,'w')
    #     for s,p in zip(syllrows,premises):
    #         fid.write('%s,%s%s%s %s%s%s%s\n' % 
    #             (s, "(list '",p[2],p[1],"'",p[3],p[0],")"))
    #     fid.close()

    # if not os.path.exists((destination+'results/')):
    #     os.mkdir((destination+'results/'))
    # if not os.path.exists((destination+'csv/')):
    #     os.mkdir((destination+'csv/'))
    # for data in glob.glob((destination+'*'+str(n_b)+'*results')):
    #     shutil.copy(data,(destination+'results/'))
    #     os.remove(data)
    # for data in glob.glob((destination+'*'+str(n_b)+'*.csv')):
    #     shutil.copy(data,(destination+'csv/'))
    #     os.remove(data)
