import os
import glob
import shutil
import numpy as np

from syll_chwrite import write_church
from syll_chrun import run_church
from syll_chparse import parse_church
from syll_helpers import myunique, grouped, decode_premises

def f_e_t_e(high_passingdict,passing_dict):
    macpath = high_passingdict['macpath']
    churchfile = high_passingdict['churchfile']
    rationalityQ = high_passingdict['rationalityQ']
    rationalityR = high_passingdict['rationalityR']
    ndepth = high_passingdict['ndepth']
    mdepth = high_passingdict['mdepth']
    serv = high_passingdict['serv']
    prefix = high_passingdict['prefix']
    latlis = high_passingdict['latlis']
    destination = high_passingdict['destination']
    exp = high_passingdict['exp']
    bs = high_passingdict['bs']
    premises = passing_dict['premises']
    figdict = passing_dict['figdict']
    n_b = high_passingdict['n_balls']
    br = high_passingdict['base_rate']
    altset = high_passingdict['altset']
    indevals = passing_dict['indevals']

    if not os.path.exists(churchfile):
        write_church(passing_dict)

    if not os.path.exists((macpath+'church/')):
        os.mkdir((macpath+'church/'))
    for data in glob.glob(('*.church')):
        shutil.copy(data,(macpath+'church/'))
        os.remove(data)

    # parse and write to csv
    head = 'all.A-C,none.A-C,some.A-C,not-all.A-C,all.C-A,none.C-A,some.C-A,not-all.C-A,mu,undefined'
    if (exp=='AMFO'):
        head = 'all.A-C,most.A-C,few.A-C,not-all.A-C,all.C-A,most.C-A,few.C-A,not-all.C-A,mu,undefined'
    if (exp=='MFIE'):
        head = 'most.A-C,few.A-C,some.A-C,none.A-C,most.C-A,few.C-A,some.C-A,none.C-A,mu,undefined'
    if (indevals==1):
        head = 'all.A-C,none.A-C,some.A-C,not-all.A-C,all.C-A,none.C-A,some.C-A,not-all.C-A,all+some.C-A,some+not-all.C-A,none+not-all.C-A,mu,undefined'

    rname = (latlis+'_N' + ndepth + '_M' + mdepth +'_' + prefix + '_aq' + 
                str(rationalityQ) + '_ar' + str(rationalityR) + '_bs'+bs+ '.results')

    run_church(churchfile,rationalityQ,rationalityR,ndepth,mdepth,serv,rname,destination)
    final_out = parse_church(rname,destination,exp,indevals)

    nz_final = final_out[np.sum(final_out, axis=1)!=0]
    aprefix = '%s_alphQ%s_alphR%s' % (prefix,rationalityQ,rationalityR)
    afname = latlis+'_N' + ndepth + '_M' + mdepth +'_' + aprefix + '_bs'+bs+'.csv'
    syllrows = [decode_premises(p,figdict) for p in premises]
    rows = np.array(syllrows, dtype='|S20')[:, np.newaxis]

    # SAVE POSTERIOR MODEL (Reasoning, could be literal or pragmatic)
    with open(afname, 'w') as f:
        np.savetxt(f, np.hstack((rows, nz_final)), delimiter=', ', fmt='%s',
            header='syll,'+head)

    if (ndepth=='0'): # only do prior only for literal reasoner
        # PRIOR MODEL (Conclusion only)
        rname = (latlis+'_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + 
                    '_ar' + str(0) + '_bs'+bs+ '.results')

        if not os.path.exists((destination+'results/'+rname)):
            rname = (latlis+'_N' + ndepth + '_M' + mdepth + '_' + prefix + '_aq' + str(0) + 
                    '_ar' + str(0) + '_bs'+bs+ '.results')

            run_church(churchfile,0,0,ndepth,mdepth,serv,rname,destination)


            final = parse_church(rname,destination,exp,indevals)
            nz_finp = final[np.sum(final, axis=1)!=0]

            aprefix = 'CLonly_%s' % (prefix)
            afname = latlis+'_N' + ndepth + '_M' + mdepth + '_' + aprefix +'_bs'+bs+ '.csv'
            with open(afname, 'w') as f:
                np.savetxt(f, np.hstack((rows, nz_finp)), delimiter=', ', fmt='%s',
                    header='syll,'+head)

    # write syllogism order to file as well, just in case
    fname = ('syllattice_%squd%sfig%s_premiseorder.csv' % (exp,passing_dict['qud'],passing_dict['fig']))
    if not os.path.exists((destination+'csv/'+fname)):
        fid = open(fname,'w')
        for s,p in zip(syllrows,premises):
            fid.write('%s,%s%s%s %s%s%s%s\n' % 
                (s, "(list '",p[3],p[1],"'",p[2],p[0],")"))
        fid.close()

    if not os.path.exists((destination+'results/')):
        os.mkdir((destination+'results/'))
    if not os.path.exists((destination+'csv/')):
        os.mkdir((destination+'csv/'))
    for data in glob.glob((destination+'*Alt'+str(altset)+'*_n'+str(n_b)+'_base'+str(br)+'*results')):
        shutil.copy(data,(destination+'results/'))
        os.remove(data)
    for data in glob.glob((destination+'*Alt'+str(altset)+'*_n'+str(n_b)+'*.csv')):
        shutil.copy(data,(destination+'csv/'))
        os.remove(data)
    return syllrows, nz_final