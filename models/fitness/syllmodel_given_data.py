from scipy.special import gammaln
from numpy import array, log, exp, prod
from math import gamma

# helper functions for computing P(model|data)
# a dirichlet likelihood is being used to say that the
	# linking function between our model's predictions
	# and subject's responses is that each subject produces
	# a distribution, which is itself a sample from a dirichlet
	# distribution, parametrized by the model predictions

# a poisson prior is begin used to say that the
	# number of objects in a situation has some mean value
	# and deviations from that incur some cognitive cost
	# (i.e. lower probability)
	# n.b.1: how to parametrize the poisson?
	# n.b.2: it might also be reasonable to assume a 
	# uniform prior over n_objects

def log_factorial(x):
    #"""Returns the logarithm of x!
    #Also accepts lists and NumPy arrays in place of x."""
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
	return k*log(lmda)-lmda+log_factorial(k)

# dirichlet likelihood 
# poisson prior over models (i.e. over parameter: n_objects)
def model_given_data(model, data, dirch_scale, pois_lambda, n_objects):
	log_likelihood = log_dirichlet(dirch_scale, data, model)
	log_prior = log_poisson(pois_lambda, n_objects)
	return log_likelihood+log_prior

mgd = model_given_data(model_predictions, observed_data, 1, 5, 4)