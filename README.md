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