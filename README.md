The pragmatics of syllogistic reasoning
=================

# Model space


## Pragmatic effects

The space of possible sources of pragmatic effects in syllogistic reasoning are shown in the below model.
	
~~~~
var reasoner1 = function(premises, QUD_e1, QUD_cl0){
	var state = statePrior()
	var conclusion = conclusionPrior()
	
	// QUD_e1 is either State or Conclusion-relation
	var E1 = experimenter1(conclusion, state, QUD_e1)
	condition(pragmaticInterpretation ? E1.score([], premises) : premises)
	
	// QUD_cl0 is either State or premises
	var qudVal = (QUDcl0 == "state") ? state : premises
	var cL0 = conclusionListener(conclusion, QUD_cl0)
	// if pragmatic, communicate qudVal, otherwise condition on premises
	condition(pragmaticProduction ? cL0.score([], qudVal) : premises)
	
	return conclusion
}
~~~~
	
The pragmatic reasoner (`r1`) has uncertainty about the world (`state`) and what the best (`conclusion`) is. (Technically, `conclusion` should be derived from `state` as opposed to having its prior. This is usually handled by having a `uniformDraw` over true conclusions.) 

`r1` either takes the premises at face value (`pragmaticInterpretation==false`) or imagines them to be coming from an informative experimenter (`e1`). `e1` could have had the intention of communicating the world (`QUD_e1=='state'`) or the conclusion. (If communicating the state, the asymmetry between logically valid conclusions will remain.) 

`r1` selects a conclusion (from those that are true) either selecting those that are just true uniformly (`pragmaticProduction==false`) or with the goal of communicating something to the conclusion listener (`cL0`). The communicative goal could plausibly be the state (`QUDcl0=='state'`) or the premises. The high level interpretation of communcating the premises is that the communicative goal is communicating the relations between the properties not already communicated by the conclusion (i.e. A--B, B--C) and that the pragmatic reasoner has knowledge of.


## Task-specific QUDs / linking functions

There are at least two different forms of the syllogistic reasoning task that are relevant to our model.


1. Which conclusion?
2. What conclusions are true?

The Rips (1994) setup is to have the participant respond Agree / Disagree to premise-conclusion pairs, totally independently. That is, on each trial, participant sees premises and a conclusion and responds. Since the alternative conclusions aren't explicit in this task, we will have to assume they are psychologically salient (a task-wide effect). For this paradigm, it's conceivable to have the QUD / return value of `r1` be a single conclusion.

An alternative paradigm (that I've explored in earlier experiments) is presenting all 4 conclusions to the participant at a time. Here, it's conceivable that the the QUD is "which conclusions are true?" with the QUDval being a list of true conclusions. This shouldn't change the qualitative pragmatic effects but the quantiative accuracy (here, there are only really 3 possible conlusions: 1. *some and all* and 2. *some and not all* and 3. *not all and none*). 

It should be noted that the major plausibily pragmatic effects remain irrespective of the response format.

## Null utterance as an alternative

Some experimental setups allow for a *no valid conclusion* response, or can derive this from the relative counts of produced conclusions (<-- is this true?). 

To account for this, the space of possible conclusions could include a null utterance. By definition, this would be highest for the most uninformative premises (thus, intimatedly related to the distribution of argument strengths). It's conceiveably to include a cost term specific to the null utterance (relative cheaper than other conclusions?).

# Experimental data to model

+ Rips (1994) -- NVC could possibly to derived by the frequency of responses by-syllogism
+ Chater & Oaksford (1999) -- with & without NVC
+ Chater & Oaksford (1999) -- most & few with simple threshold semantics
+ Khemlani & Johnson-Laid (2012)

+ what is the reliability of this data (correlations between the 3 data sets)?

### Belief bias experiments
 
+ Klauer et al. (2000), Dube et al. (2010)

# Open questions

How does our space of possible pragmatic sources relate to the analysis of Roberts, Newstead & Griggs (2001)?