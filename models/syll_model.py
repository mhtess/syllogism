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
                    lis='lis', EPin=1, altset=1, semantics='tight',madworld=1, indevals=0):

    n_balls = int(n_b)
    base_rate = float(br)
    vc = int(vcstr)
    nvc = int(nvcstr)
    serv = int(serv)
    ndepth = str(int(qdepth))
    mdepth = str(int(rdepth))
    EP = int(EPin)
    altset = int(altset)
    madworld = int(madworld)
    indevals = int(indevals)
    latlis = lis
    qud=1

    n_samples = 100
    bs_samples = 1000
    ### FOR MOST / FEW, Set threshold; right now, same threshold for the two
    threshold = 0.5

    if (semantics=='tight'):
        prefix = ('%s%s_qud%sMW%dfig%s_%sc%d%sEP%dAlt%dIndevals%s_n%d_base%.2f_s%dk' % 
              (priortype,domain,qud,madworld,fig,exp,vc,vcord,EP,altset,indevals,n_balls,base_rate,n_samples))
    else:
        prefix = ('%s%s_qud%sMW%dfig%s_%sc%d%sEP%dAlt%dSem%sIndevals%s_n%d_base%.2f_s%dk' % 
              (priortype,domain,qud,madworld,fig,exp,vc,vcord,EP,altset,semantics,indevals,n_balls,base_rate,n_samples))

    high_passingdict = {'n_balls':n_b,'base_rate':br,'ndepth':ndepth,'mdepth':mdepth,\
    'rationalityQ':rationalityQ,'rationalityR':rationalityR,'serv':serv,'latlis':latlis,\
    'exp':exp,'altset':altset}

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
    destfold = ('%s%s/' % (qdepth,rdepth))
    if (serv==1):
        macpth = ('/home/mht/projectsyll/MODELDATA/%s/' % macfold)
    else:
        macpth = ('/Users/mht/Documents/research/syllogism/models/modeldata/%s/' 
            % macfold)


    if not os.path.exists(macpth):
        os.mkdir(macpth)
    destination = macpth+destfold
    if not os.path.exists(destination):
        os.mkdir(destination)
    os.chdir(destination)


    high_passingdict['prefix'] = prefix
    high_passingdict['destination']=destination
    high_passingdict['macpath']=macpth

    priordict = {'Q_XYZ':'111', 'Q_XYnZ':'110', 'Q_XnYZ':'101', 'Q_XnYnZ':'100', \
                'Q_nXYZ':'011', 'Q_nXYnZ':'010','Q_nXnYZ':'001', 'Q_nXnYnZ':'000'}

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


    if (semantics=='loose'):
        Relations = [syll_logic.A_eval_slack,syll_logic.E_eval_slack,
                    syll_logic.I_eval,syll_logic.O_eval]


    RelationsnoEP = [syll_logic.A_evalnoEP,syll_logic.E_evalnoEP,
                    syll_logic.I_evalnoEP,syll_logic.O_evalnoEP]
    
    RelationsDPEP = [syll_logic.A_evalDPEP,syll_logic.E_evalDPEP,
                syll_logic.I_evalDPEP,syll_logic.O_evalDPEP]
                
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
        prelations = ['A','E','I','O'] 
        if (altset==6): 
            RelationsnoEP = [syll_logic.A_evalnoEP,syll_logic.E_evalnoEP,syll_logic.I_evalnoEP,syll_logic.O_evalnoEP,syll_logic.N_eval]
            prelations = ['A','E','I','O','N'] 
        propsorig = list(itertools.product(termpairs,RelationsnoEP))
        #if (altset==3):
         #   propsorig.append((('S','P'),syll_logic.N_eval))
    elif (EP ==2): # determiner phrase presupposition { q (X,Y) --> there exists some X}
        prelations = ['A','E','I','O']
        #if (altset==5):
        #    RelationsnoEP.append(syll_logic.N_eval)
        #    prelations.append('N')        
        propsorig = list(itertools.product(termpairs,RelationsDPEP))
    else: # Standard with EP=1
        prelations = ['A','E','I','O']
        if (altset==8):
            Relations.append(syll_logic.equality_eval)
            prelations.append('Q')
        propsorig = list(itertools.product(termpairs,Relations))
        if (nvc==1): propsorig.append((('S','P'),syll_logic.NVC))
        if (indevals==1): 
            propsorig.append((('S','P'),syll_logic.AI_eval))
            propsorig.append((('S','P'),syll_logic.IO_eval))
            propsorig.append((('S','P'),syll_logic.EO_eval))
      #  propsqud = list(it.product(qud,Relations))
      #  propsalt = list(it.product(termpairsalt,Relations))
    props = propsorig#+propsalt
    propositions = list(itertools.product(termpairs,prelations))
    if (nvc==1): propositions.append((('S','P'),'NVC'))
    if (indevals==1): 
        propositions.append((('S','P'),'AI'))
        propositions.append((('S','P'),'IO'))
        propositions.append((('S','P'),'EO'))
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

    def logic_check(prems):
        if ('N' in prems[2:4]):
            no_what = prems[prems.index('N')-2][0] # There are no what?
            if ('I' in prems[2:4]):
                return not(no_what in prems[prems.index('I')-2])
            if ('O' in prems[2:4]):
                return not(no_what in prems[prems.index('O')-2][0])
            return True
        else:
            return True

    posspremises = [prems for prems in posspremises if logic_check(prems)]

    alementsalt = ['np','pn']
    blementsalt = ['sn','ns']
    premisesalt = list(itertools.product(blementsalt,alementsalt,relations,relations))
    p1s = list(itertools.product(relations,alements)) 
    p2s = list(itertools.product(relations,blements))
    figdict = {'mpsm':1, 'pmsm': 2, 'mpms': 3, 'pmms':4}

    passdict = {'qud':qud,'listener':latlis,'nvc':nvc,"vc":vc,
    "vcord":vcord,'posspremises':posspremises,'premises':premises,
    'propositions':propositions,'figdict':figdict,'fig':fig,
    'ndepth':ndepth,'mdepth':mdepth,'n_balls':n_balls,'exp':exp,
    "EP":EP,"altset":altset,"madworld":madworld,'indevals':indevals}
    

    # preprocessing/lifting (equivalence class)

    if (EP==0):
        sampler = syll_logic.sample_joint_sansEP
    elif (EP==2):
        sampler = syll_logic.sample_joint_sansEP
    else:
        sampler = syll_logic.sample_joint

    # NOTE: I'm not sure why sample_joint is the way it is.
    # The 'naive' sampler doesn't have any existential madness...

    if (domain=='naive'):
        sampler = syll_logic.sample_fig1

    # madworld hypothesis requires 2 samplers

    if (madworld==1): 
        if (serv==0):
            priorpath = ('/Users/mht/Documents/research/syllogism/data/03syllogism_prior_psychjs/')
        else:
            priorpath = ('/home/mht/projectsyll/EXPDATA/03syllogism_prior_psychjs/')

        expname = 'prior-exp-mturk_means_n71'
        if (priortype=='tfbt'):
            expname = 'prior-exp-mturk_collapsed_means_n71'

        priorfile = priorpath + expname +'.csv'
        sampler_abstract = syll_logic.sample_fig1
        sampler_rl = syll_logic.sample_joint
        fname = latlis+ '_' + prefix + '_Smean.church'
        churchfile = macpth+'church/'+fname
        high_passingdict['churchfile']=churchfile
        passdict['fname']=fname
        high_passingdict['bs']='mean'

        if not os.path.exists(churchfile):
            print 'sampling and featurizing...abstract world br= ' + str(base_rate)
            samples_ab = np.array([sampler_abstract(n_balls,base_rate) for _ in range(1000*n_samples)])
            S, M, P = samples_ab.transpose(1, 0, 2)
            rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
            rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
            equiv_rs0_ab, equiv_count_ab = myunique(rs1)
            equiv_prob_ab = [float(ec)/len(rs1) for ec in equiv_count_ab]
            passdict['equiv_rs0_ab']=equiv_rs0_ab
            passdict['equiv_prob_ab']=equiv_prob_ab


            print 'sampling and featurizing... real world ' + str(n_balls) + ' ' + domain + 's' + ' ' + priortype
            phead = pd.read_csv(priorfile,dtype='string',index_col=0)
            features = phead.columns.values[2::]
            domain_priors = phead[((phead.domain == domain) & (phead.condition == priortype))][features]
            
            priorVector = np.array(domain_priors,dtype=float)[0]
            samples = np.array([sampler_rl(priorVector,features,n_balls) 
                                for _ in range(1000*n_samples)])
            S, M, P = samples.transpose(1, 0, 2)
            rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
            rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])

            equiv_rs0_rl, equiv_count_rl = myunique(rs1)
            equiv_prob_rl = [float(ec)/len(rs1) for ec in equiv_count_rl]
            passdict['equiv_rs0_rl']=equiv_rs0_rl
            passdict['equiv_prob_rl']=equiv_prob_rl

        syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

    else: # NO madworld hypothesis

        if (domain=='naive'): # Abstract priors
            fname = latlis+ '_' + prefix + '_Smean.church'
            churchfile = macpth+'church/'+fname
            high_passingdict['churchfile']=churchfile
            passdict['fname']=fname
            high_passingdict['bs']='mean'
            
            if not os.path.exists(churchfile):
                print 'sampling and featurizing... br=' + str(base_rate)
                samples = np.array([sampler(n_balls,base_rate) for _ in range(1000*n_samples)])
                S, M, P = samples.transpose(1, 0, 2)
                rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
                rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
                equiv_rs0, equiv_count = myunique(rs1)
                equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
                passdict['equiv_rs0']=equiv_rs0
                passdict['equiv_prob']=equiv_prob
            
            syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

        else: # Empirical priors

            if (serv==0):
                priorpath = ('/Users/mht/Documents/research/syllogism/data/03syllogism_prior_psychjs/')
            else:
                priorpath = ('/home/mht/projectsyll/EXPDATA/03syllogism_prior_psychjs/')

            if (priortype=='bootstrap'): # bootstrap priors
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
                        samples = np.array([sampler(priorVector,features,n_balls) 
                                        for _ in range(1000*n_samples)])
                        S, M, P = samples.transpose(1, 0, 2)
                        rs0 = np.array([p[1](eval(p[0][1]),eval(p[0][0])) for p in props])
                        rs1 = np.array([rw for rw in np.transpose(rs0) if sum(rw) != 0])
                        equiv_rs0, equiv_count = myunique(rs1)
                        equiv_prob = [float(ec)/len(rs1) for ec in equiv_count]
                        passdict['equiv_rs0']=equiv_rs0
                        passdict['equiv_prob']=equiv_prob

                    syllrows, nz_final = f_e_t_e(high_passingdict,passdict)

            else: # just using mean priors

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
                    samples = np.array([sampler(priorVector,features,n_balls) 
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
