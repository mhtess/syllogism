library(gtools)
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


# log factorial
## lfactorial(n)
# log multinomial likelihood
## dmultinom(x=data,size=n,prob=predictions,log=TRUE)
# log poisson probability
## dpois(x, lambda, log = TRUE)
# log dirichlet likelihood
## log(ddirichlet(x, alpha))
# log beta likelihood
## dbeta(x, shape1, shape2, ncp = 0, log = FALSE)


# dirichlet likelihood 
# poisson prior over models (i.e. over parameter: n_objects)
posterior<- function(model,data,dir_concentration,pois_lambda,n_objects){
	log(ddirichlet(data,model*dir_concentration))+
	dpois(n_objects,pois_lambda,log=TRUE)
}
