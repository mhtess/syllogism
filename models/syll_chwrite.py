#!/usr/bin/python

def write_church(pd):
    import numpy as np
    import pdb
#    print str(rtnQ) + ' = rationalityQ'
 #   pdb.set_trace()
    print str(pd['n_balls']) + ' = n balls'

    # to make church model more readable
    sylldict = {"pm":"A-B","mp":"B-A","ms":"B-C","sm":"C-B","ps":"A-C","sp":"C-A","A":"all.",\
                "E":"none.","I":"some.","O":"not-all.","N":"there-is-no.","P":"A","M":"B","S":"C"}

    fid = open(pd['fname'],'w')
    # <rawcell>
    # fid.write('(define premise-prior (lambda (target)\n')
    # fid.write('\t(case target\n')
    # for e in range(int(len(pd['premises']))):
    #     fid.write("\t\t(((list '%s '%s)) (uniform-draw " % ((pd['premises'][e][2]+pd['premises'][e][1]),(pd['premises'][e][3]+pd['premises'][e][0])))
    #     fid.write("(list '%s '%s)\t" % ((pd['premises']alt[e][2]+pd['premises']alt[e][1]),(pd['premises']alt[e][3]+pd['premises']alt[e][0])))
    #     fid.write("(list '%s '%s)))\n" % ((pd['premises'][e][2]+pd['premises'][e][1]),(pd['premises'][e][3]+pd['premises'][e][0])))
    # fid.write(')))\n\n')



    # write down premise prior
    if (pd['altset']==0):
        fid.write('(define premise-prior (lambda (figure)\n')
        if pd['fig'] == 'Full':
            figs = 4
        else:
            figs = 1

        count = 0
        fid.write('\t\t(uniform-draw (list ')
        while (count<(len(pd['posspremises']))):
            fid.write("(list '%s '%s) " % \
                ((sylldict[pd['posspremises'][count][3]]+sylldict[pd['posspremises'][count][1]]),\
                 (sylldict[pd['posspremises'][count][2]]+sylldict[pd['posspremises'][count][0]])))
            count = count + 1
        if (pd['altset']==3): # Standard + "There are no X" is just first term of conclusion
            fid.write("'there-is-no.C-A ")
        if (pd['altset']==5): # Standard + "There are no X", where X is any term not already presupposed
            fid.write("'there-is-no.C-A 'there-is-no.A-B 'there-is-no.B-C")
            
        fid.write('))))\n\n')

    else:
        fid.write('(define premise-prior (lambda (figure)\n')
        fid.write('\t(case figure\n')
        #lp = 16
        if pd['fig'] == 'Full':
            figs = 4
        else:
            figs = 1

        h = 0
        count = 0
        while h<figs:
            print count
            fid.write('\t\t((%d) (uniform-draw (list ' % (h+1))
            anchor = pd['posspremises'][count][0:2]
            while ((count<(len(pd['posspremises']))) and (pd['posspremises'][count][0:2] == anchor)):
                    fid.write("(list '%s '%s) " % \
                        ((sylldict[pd['posspremises'][count][3]]+sylldict[pd['posspremises'][count][1]]),\
                         (sylldict[pd['posspremises'][count][2]]+sylldict[pd['posspremises'][count][0]])))
                    count = count + 1

            h = h + 1
            # this is the end of the one set of alternatives; last chance to add something
            if (pd['altset']==2): # Standard + "There are no X" where X is the first position of figure
                fid.write("'%s " % (sylldict["N"]+sylldict[anchor[0]]))
                fid.write("'%s " % (sylldict["N"]+sylldict[anchor[1]]))
            if (pd['altset']==3): # Standard + "There are no X" is just first term of conclusion
                fid.write("'there-is-no.C-A ")
            if (pd['altset']==5): # Standard + "There are no X", where X is any term not already presupposed
                fid.write("'there-is-no.C-A 'there-is-no.A-B 'there-is-no.B-C")
            
            fid.write(')))\n')
        fid.write(')))\n\n')

    # write down situation prior
    fid.write('%s' % '(define (situation-prior) (multinomial (list ')
    for a,b in enumerate(pd['equiv_prob']):
        fid.write('\t%s%d' % ("'s",a))
    fid.write(")\n'(")
    for score in pd['equiv_prob']:
        fid.write('%.6f ' % score)
    fid.write(')))\n\n')

    # sentence-eval function: mapping from situations to truth values
    fid.write('%s\n\t' % '(define sentence-eval (lambda (sentence situation)')
    fid.write("%s" % "(case sentence")
    for i, line in enumerate(pd['propositions']):
        fa = "(('"+sylldict[line[1]]+sylldict[line[0][0].lower()+line[0][1].lower()]+') (or '
        fid.write('\n%s' % (fa))
        if sum(pd['equiv_rs0'][:,i])==0: # if no worlds are true of this sentence
            fid.write('%s' % ('false))'))    
        else:
            # this is where the magic happens: 
            # printing the equivalence-class worlds (ECW) true of the sentences
            for j, term in enumerate(pd['equiv_rs0'][:,i]):
                if term:
                    fid.write('%s%s%s' % ('(equal? situation ',term*("'s"+str(j)),') '))
            fid.write('))')

    for j, prm in enumerate(pd['posspremises']):
        fa = "(((list '"+sylldict[prm[2]]+sylldict[prm[1]]+" '"+sylldict[prm[3]]+sylldict[prm[0]]+')) (or '
        fid.write('\n%s' % (fa))
        a = pd['equiv_rs0'][:,pd['propositions'].index(((prm[1][0].upper(),prm[1][1].upper()), prm[2].upper()))]
        b = pd['equiv_rs0'][:,pd['propositions'].index(((prm[0][0].upper(),prm[0][1].upper()), prm[3].upper()))]
        if sum(np.multiply(a,b))==0:
            fid.write('%s' % ('false))'))    
        else:
            for k, term in enumerate(np.multiply(a,b)):
                if term:
                    fid.write('%s%s%s' % ('(equal? situation ',term*("'s"+str(k)),') '))
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
    #### write mapping from situations to sentences
    fid.write('%s\n\t' % '(define true-conclusions (lambda (situation)')
    fid.write("%s" % "(case situation")
    for i, term in enumerate(pd['equiv_rs0']):
        fa = "(('s"+str(i)+") (list "
        fid.write('\n%s' % (fa))
        for j, trth in enumerate(term):
            if trth:
                line = pd['propositions'][j]
                prettier_sentence = "'"+sylldict[line[1]]+sylldict[line[0][0].lower()+line[0][1].lower()]
                fid.write('%s ' % prettier_sentence)
        fid.write('))')
    # for j, prm in enumerate(pd['posspremises']):
    #     fa = "(((list '"+prm[2]+prm[1]+" '"+prm[3]+prm[0]+')) (list '
    #     fid.write('\n%s' % (fa))
    #     a = pd['equiv_rs0'][:,pd['propositions'].index(((prm[1][0].upper(),prm[1][1].upper()), prm[2].upper()))]
    #     b = pd['equiv_rs0'][:,pd['propositions'].index(((prm[0][0].upper(),prm[0][1].upper()), prm[3].upper()))]
    #     if sum(np.multiply(a,b))==0:
    #         fid.write('%s' % ('false))'))    
    #     else:
    #         for k, term in enumerate(np.multiply(a,b)):
    #             if term:
    #                 fid.write('%s%s%s' % ('(equal? feature ',term*("'f"+str(k)),') '))
    #         fid.write('))')      
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
        fid.write('%s%s%s %s%s%s%s\t' % ("(list '",sylldict[p[3]],sylldict[p[1]],"'",sylldict[p[2]],sylldict[p[0]],")"))
    fid.write('))\n\n')

    # for z in range(int(pd['ndepth'])+1):
    #     if z == int(pd['ndepth']):
    #         fid.write('(define Ndepths (list ')
    #     else:
    #         fid.write(';(define Ndepths (list ')
    #     for q, p in enumerate(pd['premises']):
    #         fid.write('%d ' % (z))
    #     fid.write('))\n')
    # fid.write('\n')
    fid.write('(define figures (list')
    for h in range(1,figs+1):
        for e in range(16):
            fid.write(' %d' % h)
    fid.write('))\n\n')
    fid.write('(define args\n\t(map string->number (regexp_split argstring ",")))\n\n')
    fid.write('(define depth (first args))\n')
    fid.write('(define alphaQ (second args))\n')
    #fid.write('(define alphaR (second args))\n')
    #fid.write('(define Ndepths (repeat (length figures) (lambda () (third args))))\n')
    #fid.write('(define Mdepths (repeat (length figures) (lambda () (fourth args))))\n')
    if ((pd['nvc']==1) & (pd['vc']==8)):
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A 'all.A-C 'some.A-C 'none.A-C 'not-all.A-C 'mu)))")
    if ((pd['nvc']==0) & (pd['vc']==8)):
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A 'all.A-C 'some.A-C 'none.A-C 'not-all.A-C)))")
    if ((pd['nvc']==1) & (pd['vc']==6)):
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A 'all.A-C 'not-all.A-C 'mu)))")
    if ((pd['nvc']==0) & (pd['vc']==6)):
        fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A 'all.A-C 'not-all.A-C)))")
    if ((pd['nvc']==1) & (pd['vc']==4)):
        if (pd['vcord']=='CA'):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A 'mu)))")
        if (pd['vcord']=='AC'):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.A-C 'some.A-C 'none.A-C 'not-all.A-C 'mu)))")
    if ((pd['nvc']==0) & (pd['vc']==4)):
        if (pd['vcord']=='CA'):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'some.C-A 'none.C-A 'not-all.C-A)))")
        if (pd['vcord']=='AC'):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.A-C 'some.A-C 'none.A-C 'not-all.A-C)))")
    if (pd['exp']=='AMFO'):
        if ((pd['nvc']==1) & (pd['vc']==8)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'most.C-A 'few.C-A 'not-all.C-A 'all.A-C 'most.A-C 'few.A-C 'not-all.A-C 'mu)))")
        if ((pd['nvc']==0) & (pd['vc']==8)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'most.C-A 'few.C-A 'not-all.C-A 'all.A-C 'most.A-C 'few.A-C 'not-all.A-C)))")
        if ((pd['nvc']==1) & (pd['vc']==4)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'most.C-A 'few.C-A 'not-all.C-A 'mu)))")
        if ((pd['nvc']==0) & (pd['vc']==4)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'all.C-A 'most.C-A 'few.C-A 'not-all.C-A)))")
    if (pd['exp']=='MFIE'):
        if ((pd['nvc']==1) & (pd['vc']==8)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'most.C-A 'few.C-A 'some.C-A 'none.C-A 'most.A-C 'few.A-C 'some.A-C 'none.A-C 'mu)))")
        if ((pd['nvc']==0) & (pd['vc']==8)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'most.C-A 'few.C-A 'some.C-A 'none.C-A 'most.A-C 'few.A-C 'some.A-C 'none.A-C)))")
        if ((pd['nvc']==1) & (pd['vc']==4)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'most.C-A 'few.C-A 'some.C-A 'none.C-A 'mu)))")
        if ((pd['nvc']==0) & (pd['vc']==4)):
            fid.write('%s\n' % "(define (conclusion-prior) (uniform-draw (list 'most.C-A 'few.C-A 'some.C-A 'none.C-A)))")
    fid.write('\n(define (raise-to-power dist alph)\n')
    fid.write('\t(list (first dist) (map (lambda (x) (pow x alph)) (second dist))))\n\n')
    # <codecell>
    if (pd['vc']==8):
        fid.write("(define is-conclusion? (lambda (x) (> (list-index (list 'C-A 'A-C) (second (regexp-split x '.))) -1)))\n\n")
    else:
        #if (pd['EP']==0):
        fid.write("(define is-conclusion? (lambda (x) (and (equal? (second (regexp-split x '.)) 'C-A)\n\t\t\t\t\t(not (equal? (first (regexp-split x '.)) 'there-is-no)))))\n\n")
        #else:
        #    fid.write("(define is-conclusion? (lambda (x) (equal? (second (regexp-split x '.)) 'C-A)))\n\n")

    fid.write('(define reasoner1\n')
    fid.write('  (mem (lambda  (premises figure)\n')
    fid.write('\t(enumeration-query\n')
    fid.write('\t (define situation (situation-prior))\n')
    fid.write('\t (define conclusion (uniform-draw (filter is-conclusion? (true-conclusions situation))))\n\n')
    fid.write('\t conclusion\n\n')
    if (pd['qud']==0):
        fid.write('\t\t (equal? premises (apply multinomial (experimenter situation figure)))))))\n')
    else:
        fid.write('\t\t (equal? premises (apply multinomial (experimenter conclusion figure)))))))\n')
    fid.write('(define experimenter\n')
    if (pd['qud']==0):
        fid.write('  (mem (lambda (situation figure)\n')
    else:
        fid.write('  (mem (lambda (conclusion figure)\n')
    fid.write('\t(enumeration-query\n')
    fid.write('\t (define premises  (premise-prior figure))\n')
    fid.write('\t premises\n\n')
    if (pd['qud']==0):
        fid.write('\t (equal? situation (apply multinomial (raise-to-power (reasoner0 premises figure) alphaQ))\n')
    else:
        fid.write('\t (equal? conclusion (apply multinomial (raise-to-power (reasoner0 premises figure) alphaQ))\n')       
    fid.write('\t\t)))))\n\n')
    fid.write('(define reasoner0\n')
    fid.write('  (mem (lambda  (premises figure)\n')
    fid.write('\t(enumeration-query\n')
    fid.write('\t (define situation (situation-prior))\n')
    fid.write('\t (define conclusion (uniform-draw (filter is-conclusion? (true-conclusions situation))))\n\n')
    if (pd['qud']==0):
        fid.write('\t situation\n\n')
        fid.write('\t\t\t(if (= alphaQ 0)\n')
        fid.write('\t\t\t\ttrue\n')
        fid.write('\t\t\t\t(sentence-eval premises situation))\n')
    else:
        fid.write('\t conclusion\n\n')
        fid.write('\t\t\t(if (= alphaQ 0)\n')
        fid.write('\t\t\t\ttrue\n')
        fid.write('\t\t\t\t(sentence-eval premises situation))\n')
    fid.write('\t\t))))\n\n')
    fid.write('(if (= depth 1)\n')
    fid.write('\t(map reasoner1 allprems figures)\n')
    fid.write('\t(map reasoner0 allprems figures))\n')
    fid.close()
