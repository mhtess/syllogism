#!/usr/bin/python
import numpy as np
import sys

qdepth = sys.argv[1]
rdepth = sys.argv[2]
nvc = sys.argv[3]
vc = sys.argv[4]
vcord = sys.argv[5]
exp = sys.argv[6]

from lattice_syll_fnc import syllogism_model
for br in np.arange(0.05,0.75,0.10):
	for n_obj in np.array((4,5,6,7,10,15,25)):
		a, b = syllogism_model(n_obj,br,qdepth,rdepth,0,nvc,vc,vcord,exp)