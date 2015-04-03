var fs = require('fs');
// var csvtojson = require('csvtojson');
var babyparse = require('babyparse');

function readCSV(filename){
  return babyparse.parse(fs.readFileSync(filename, 'utf8'));
};

function writeCSV(jsonCSV, filename){
  fs.writeFileSync(filename, babyparse.unparse(jsonCSV) + "\n");
}

var testIt = function(){
  console.log('yay', readCSV('mh.csv'));
  writeCSV([[5, 6, 7], [8, 9, 10]], 'mh2.csv');
};


// other helper functions

function wpParseFloat(x){
	return parseFloat(x);
};


function sequence(lowEnd,highEnd, interval){
	var list = [];
	for (var i = 0; i <= ((highEnd-lowEnd)/interval); i++) {
	    list.push(lowEnd+i*interval);
	}
	return list
}

// parse the priors

function parsePriorData(priorDM){
	var dfile;
	var dPriors;
	var domainPriors;
	var dfilepath = "/Users/mht/Documents/research/syllogism/data/03syllogism_prior_psychjs/";

	if (priorDM == 'combined') {
	    dfile = dfilepath + "prior-exp-mturk_collapsed_means_n71.csv";
		dPriors = readCSV(dfile).data;
		domainPriors = dPriors.slice(1);
	} else {

	  dfile = dfilepath + "prior-exp-mturk_means_n71.csv";
	  dPriors = readCSV(dfile).data;
	  var conditionCol = dPriors[0].indexOf("condition")
	  domainPriors = _.filter(dPriors,function(row){return row[conditionCol]==priorDM});
	}

	var propertyTuples = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],
                      [1,0,0],[1,0,1],[1,1,0],[1,1,1]]

	var csvPropTup = dPriors[0].slice(3) // property (tuple) labels e.g. 011

	// order csv data to match what's in propertyTuples
	var orderPropertyTuples = function(values){
	  return _.map(propertyTuples,function(x){
	    return parseFloat(values[csvPropTup.indexOf(x.join(""))])
	  })
	}

	// create assoc. array out of domainName and ordered probabilities
	var priorClean = _.object(_.map(domainPriors,function(x){
	  return [x[1],orderPropertyTuples(x.slice(3))]
	}))

	return priorClean
}

// read and concat exp. 1 and 2 data

function readReasoningData(){
	var drfilepath = "/Users/mht/Documents/research/syllogism/data/";
	var drfile1 = drfilepath + "03syllogism_reasoning/syllbelief-exp-mturk_all_n250.csv";
	var drfile2 = drfilepath + "04syllogism_reasoning/syllbelief-exp2-mturk.csv";

	var csvInput1 = readCSV(drfile1).data;
	var csvInput2 = readCSV(drfile2).data;
	return csvInput1.concat(csvInput2)
//	return csvInput2
}


// this takes in lists of conclusions and computes the marginals
function unrollConclusionList(posteriorERP, conclusionListOrder){
	var conclusionObject = 
			_.object(_.map(conclusionListOrder,function(x){
			  return [x.join(),0]
			}));
  	var supp = posteriorERP.support()
  	_.map(supp, function(s){
	    _.map(s, function(x){
		    var listLabel = conclusionListOrder[x].join()
		    var currVal = conclusionObject[listLabel]
		    conclusionObject[listLabel] = currVal + Math.exp(posteriorERP.score([],s))
		  })})
   return conclusionObject
};

// this takes in the list of conclusions, which includes pairs, and computes the marignals 
// over the 4

function marginalsFromFullList(posteriorERP, conclusionOrder ,conclusionListOrder){
	var conclusionObject = 
			_.object(_.map(conclusionOrder,function(x){
			  return [x.join(),0]
			}));
  	var supp = posteriorERP.support();

  	// to test if we're dealing with a double conclusion or not
  	var isObject = function(x){
  		return typeof x == 'object'
  	};
  	 _.map(supp, function(s){

  		if (conclusionListOrder[s].every(isObject)) {
  			var listLabel1 = conclusionListOrder[s][0].join()
  			var listLabel2 = conclusionListOrder[s][1].join()
  			var currVal1 = conclusionObject[listLabel1]
		    conclusionObject[listLabel1] = currVal1 + 0.5*Math.exp(posteriorERP.score([],s))
		    var currVal2 = conclusionObject[listLabel2]
		    conclusionObject[listLabel2] = currVal2 + 0.5*Math.exp(posteriorERP.score([],s))
  		} else {
  			var listLabel = conclusionOrder[s].join()
		    var currVal = conclusionObject[listLabel]
		    conclusionObject[listLabel] = currVal + Math.exp(posteriorERP.score([],s))
		}})

	return conclusionObject

};



function normalize(distributionObject){
	var total = _.map(distributionObject, function(val,key){return val}).reduce(function(a, b){
  					return a + b;});
	return _.object(_.map(distributionObject, function(val,key){
	 	return [key, val/total]
	 }))
}

module.exports = {
  readCSV: readCSV,
  writeCSV: writeCSV,
  wpParseFloat: wpParseFloat,
  sequence: sequence,
  parsePriorData: parsePriorData,
  readReasoningData: readReasoningData,
  unrollConclusionList: unrollConclusionList,
  normalize: normalize,
  marginalsFromFullList: marginalsFromFullList};