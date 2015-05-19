var minHeuristic = function(premiseCode){
	var informationalOrdering = ["O","E","I","A"];
	var minConclusion = '';
	var i=0;
	while (minConclusion==''){
		var minConclusion = (premiseCode.indexOf(informationalOrdering[i]) > -1) ? 
								informationalOrdering[i]:'';
		i++;
	}

	return minConclusion
}

var pEntailment = function(premiseCode){
	var pEntailments = {
		"A":"I",
		"E":"O",
		"O":"I",
		"I":"O"
	}
	return pEntailments[minHeuristic(premiseCode)]
}




module.exports = {

	readCSV: readCSV,
	writeCSV: writeCSV,
	minHeuristic: minHeuristic,
	pEntailment:pEntailment

};