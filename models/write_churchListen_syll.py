#!/usr/bin/python

def write_church(rtnQ,pd):
    import numpy as np
    print str(rtnQ) + ' = rationalityQ'
    print str(pd['n_balls']) + ' = n balls'
    # <codecell>
    fid = open(pd['fname'],'w')
    # <rawcell>
    # fid.write('(define premise-prior (lambda (target)\n')
    # fid.write('\t(case target\n')
    # for e in range(int(len(pd['premises']))):
    #     fid.write("\t\t(((list '%s '%s)) (uniform-draw " % ((pd['premises'][e][2]+pd['premises'][e][1]),(pd['premises'][e][3]+pd['premises'][e][0])))
    #     fid.write("(list '%s '%s)\t" % ((pd['premises']alt[e][2]+pd['premises']alt[e][1]),(pd['premises']alt[e][3]+pd['premises']alt[e][0])))
    #     fid.write("(list '%s '%s)))\n" % ((pd['premises'][e][2]+pd['premises'][e][1]),(pd['premises'][e][3]+pd['premises'][e][0])))
    # fid.write(')))\n\n')
    # <codecell>
    fid.write('(define premise-prior (lambda (figure)\n')
    fid.write('\t(case figure\n')
    lp = int(len(pd['posspremises'])/4)
    for h in range(1,5):
        fid.write('\t\t((%d) (uniform-draw (list ' % h)
        for e in range(lp):
            fid.write("(list '%s '%s) " % ((pd['posspremises'][e+(lp*(h-1))][2]+pd['posspremises'][e+(lp*(h-1))][1]),(pd['posspremises'][e+(lp*(h-1))][3]+pd['posspremises'][e+(lp*(h-1))][0])))
        fid.write(')))\n')
    fid.write(')))\n\n')
    # <codecell>
    fid.write('%s' % '(define (state-prior) (multinomial (list ')
    for a,b in enumerate(pd['equiv_prob']):
        fid.write('\t%s%d' % ("'f",a))
    fid.write(")\n'(")
    for score in pd['equiv_prob']:
        fid.write('%.6f ' % score)
    fid.write(')))\n\n')
    # <codecell>
    fid.write('%s\n\t' % '(define sentence-eval (lambda (premise feature)')
    fid.write("%s" % "(case premise")
    for i, line in enumerate(pd['propositions']):
        fa = "(('"+line[1]+line[0][0].lower()+line[0][1].lower()+') (or '
        fid.write('\n%s' % (fa))
        if sum(pd['equiv_rs0'][:,i])==0:
            fid.write('%s' % ('false))'))    
        else:
            for j, term in enumerate(pd['equiv_rs0'][:,i]):
                if term:
                    fid.write('%s%s%s' % ('(equal? feature ',term*("'f"+str(j)),') '))
            fid.write('))')
    for j, prm in enumerate(pd['posspremises']):
        fa = "(((list '"+prm[2]+prm[1]+" '"+prm[3]+prm[0]+')) (or '
        fid.write('\n%s' % (fa))
        a = pd['equiv_rs0'][:,pd['propositions'].index(((prm[1][0].upper(),prm[1][1].upper()), prm[2].upper()))]
        b = pd['equiv_rs0'][:,pd['propositions'].index(((prm[0][0].upper(),prm[0][1].upper()), prm[3].upper()))]
        if sum(np.multiply(a,b))==0:
            fid.write('%s' % ('false))'))    
        else:
            for k, term in enumerate(np.multiply(a,b)):
                if term:
                    fid.write('%s%s%s' % ('(equal? feature ',term*("'f"+str(k)),') '))
            fid.write('))')      
    #for j, prm in enumerate(premisesalt):
    #    fa = "(((list '"+prm[2]+prm[1]+" '"+prm[3]+prm[0]+')) (or '
    #    fid.write('\n%s' % (fa))
    #    a = pd['equiv_rs0'][:,pd['propositions'].index(((prm[1][0].upper(),prm[1][1].upper()), prm[2].upper()))]
    #    b = pd['equiv_rs0'][:,pd['propositions'].index(((prm[0][0].upper(),prm[0][1].upper()), prm[3].upper()))]
    #    if sum(np.multiply(a,b))==0:
    #        fid.write('%s' % ('false))'))    
    #    else:
    #        for k, term in enumerate(np.multiply(a,b)):
    #            if term:
    #                fid.write('%s%s%s' % ('(equal? feature ',term*("'f"+str(k)),') '))
    #        fid.write('))')            
    fid.write(')))\n\n')
    # <codecell>
    fid.write('(define allprems (list ')
    for p in pd['premises']:
        fid.write('%s%s%s %s%s%s%s\t' % ("(list '",p[2],p[1],"'",p[3],p[0],")"))
    fid.write('))\n\n')
    for z in range(int(pd['ndepth'])+1):
        if z == int(pd['ndepth']):
            fid.write('(define Ndepths (list ')
        else:
            fid.write(';(define Ndepths (list ')
        for q, p in enumerate(pd['premises']):
            fid.write('%d ' % (z))
        fid.write('))\n')
    fid.write('\n')
    fid.write('(define figures (list')
    for h in range(1,5):
        for e in range(int(len(pd['premises'])/4)):
            fid.write(' %d' % h)
    fid.write('))\n\n')
    if (pd['nvc']==1):
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'Asp 'Isp 'Esp 'Osp 'Aps 'Isp 'Esp 'Ops 'NVCsp)))")
    else:
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'Asp 'Isp 'Esp 'Osp 'Aps 'Isp 'Esp 'Ops)))")
    fid.write('\n(define (raise-to-power dist alph)\n')
    fid.write('\t(list (first dist) (map (lambda (x) (pow x alph)) (second dist))))\n\n')
    fid.write('(define alphaQ %s)\n\n' % str(rtnQ))
    # <codecell>
    fid.write('(define questioner\n')
    fid.write('  (mem (lambda (conclusion figure n)\n')
    fid.write('\t(enumeration-query\n')
    fid.write('\t (define premises  (premise-prior figure))\n')
    fid.write('\t (define state  (state-prior))\n\n')
    fid.write('\t premises\n\n')   
    fid.write('\t (equal? conclusion (apply multinomial (raise-to-power (reasoner premises figure n) alphaQ))\n')
    fid.write('\t\t)))))\n\n')
    fid.write('(define reasoner\n')
    fid.write('  (mem (lambda  (premises figure n)\n')
    fid.write('\t(enumeration-query\n')
    fid.write('\t (define state (state-prior))\n')
    fid.write('\t (define conclusion (conclusion-prior))\n\n')
    fid.write('\t conclusion\n\n')
    fid.write('\t (if (= n 0)\n')
    fid.write('\t\t(and \n')
    if (rtnQ==0):
        fid.write('\t\t\ttrue\n')
    else:
        fid.write('\t\t\t(sentence-eval premises state)\n')
    fid.write('\t\t\t(sentence-eval conclusion state))\n')
    fid.write('\t\t(equal? premises (apply multinomial (questioner conclusion figure (- n 1)))))))))\n\n')
    fid.write('(map reasoner allprems figures Ndepths)\n')
    fid.close()
