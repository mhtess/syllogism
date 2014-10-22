from multinom_lklhd import log_factorial, multinomial
from scipy.special import gammaln
from numpy import array, log, exp, prod
from math import gamma

def log_factorial(x):
    """Returns the logarithm of x!
    Also accepts lists and NumPy arrays in place of x."""
    return gammaln(array(x)+1)
    
def log_multinomial(n, xs, ps):
	xs, ps = array(xs), array(ps)
	result = log_factorial(n) - sum(log_factorial(xs)) + sum(xs * log(ps))
	return result

def log_dirichlet(scale, xs, alphas):
	xs, alphas = array(xs), array(alphas)
	result = sum((alphas-1)*log(xs))\
			 - sum(gammaln(alphas))\
			 + log(gamma(sum(alphas)))

def log_poisson(lmda, k):
	return k*log(lmda)-lmbda+log_factorial(k)

def model_given_data(log_likelihood, log_prior):
	return log_likelihood+log_prior

mgd = model_given_data(