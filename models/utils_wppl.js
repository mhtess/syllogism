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
		    conclusionObject[listLabel1] = currVal1 + Math.exp(posteriorERP.score([],s))
		    var currVal2 = conclusionObject[listLabel2]
		    conclusionObject[listLabel2] = currVal2 + Math.exp(posteriorERP.score([],s))
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
  unrollConclusionList: unrollConclusionList,
  normalize: normalize,
  marginalsFromFullList: marginalsFromFullList
};