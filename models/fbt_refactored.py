
import subprocess
import sys
from numpy import arange

model = sys.argv[1]
n = sys.argv[2]

churchfile = 'syllogism_' + model + '.church'

alldomains = ['lightbulb','cracker','strawberry','knife'] 

number_of_objects = [n]
#number_of_objects = arange(3,6,1)
#list_of_alphas = [1]
list_of_alphas = arange(1,6,0.5)

for n_obj in number_of_objects:
    for domain in alldomains:
        for alpha in list_of_alphas:
        	arguments = n_obj + ',' + str(alpha) + ',' + domain
        	print(model + arguments)
        	subprocess.call(['church', '-a' ,arguments, churchfile])
