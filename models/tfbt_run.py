# bootstrap syll model
import os
import sys
from syll_model import syllogism_model
from numpy import arange

srv = sys.argv[1]
n = sys.argv[2]

#extra parameters, set to their defaults so no reason to pass\
nvc, vc, vcord, exp, fig, lis, EPin = 0, 4,'CA','AIEO', 'Full', 'lis', 1

allpriors = ['lightbulb','cracker','strawberry','knife'] 
#allpriors = ['naive']

number_of_objects = [n]

list_of_alphas = [1]
#list_of_alphas = arange(1,6,0.5)

#base_rates = arange(0.05,1,0.1)
base_rates = [0]
#base_rates = [0.3]

pt = 'tfbt'
depth = 0

exispresupp = 1 # 1 for plentify, 0 for aristotle, 2 for determiner (see documentation)
alternatives = 1 # 1 for basic, 0 for all possible, 2 - N (see documentation)
semntics = 'tight'
madwrld = 0 # 1 for madworld r.v.
ievals = 1 # 0 for basic, 1 for "independent evaluation of conclusions and combination of conclusions"

if (srv=='0'):
	os.chdir("/Users/mht/Documents/research/syllogism/models")
else:
	os.chdir("/home/mht/projectsyll/MODELS")

# domain = {'naive' or {'cracker', 'lightbulb', etc.}}
# priortype = {'bootstrap' or 'tfbt' or anything}

for n_obj in number_of_objects:
    for prior in allpriors:
        for alpha in list_of_alphas:
            for baserate in base_rates:
                syllorder, model_data = syllogism_model(n_b=n_obj,br=baserate,qdepth=depth,rdepth=0,\
                                                        rationalityQ=alpha,rationalityR=1,\
                                                        domain=prior,priortype=pt, serv=srv, \
							EPin=exispresupp, altset=alternatives, semantics=semntics, madworld=madwrld,indevals=ievals)
