/* Sliders all start at 0, except the None of the above follows one, which starts at the midline.


/*
Displays each slide
*/

function showSlide(id) {
  $(".slide").hide();
  $("#"+id).show();
}

/* 
Returns random number between a and b, inclusive
*/

function random(a,b) {
  if (typeof b == "undefined") {
    a = a || 2;
    return Math.floor(Math.random()*a);
  } else {
    return Math.floor(Math.random()*(b-a+1)) + a;
  }
}

/* 
Randomly shuffles elements in an array
*/

Array.prototype.random = function() {
  return this[random(this.length)];
}

/* 
Returns random number between a and b, inclusive
*/


function setQuestion(array) {
    var i = random(0, array.length - 1);
    var q = array[i];
    return q;

js }
/* 
Produces an array with numbers 0~arrLength
in random order. Kind of spurious--use 
Array.prototype.random instead
*/

function shuffledArray(arrLength)
{
  var j, tmp;
  var arr = new Array(arrLength);
  for (i = 0; i < arrLength; i++)
  {
    arr[i] = i;
  }
  for (i = 0; i < arrLength-1; i++)
  {
    j = Math.floor((Math.random() * (arrLength - 1 - i)) + 0.99) + i;
    tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr;
}



/* 
Clears value from form
*/

function clearForm(oForm) {
    
  var elements = oForm.elements; 
    
  oForm.reset();

  for(i=0; i<elements.length; i++) {
      
	field_type = elements[i].type.toLowerCase();
	
	switch(field_type) {
	
		case "text": 
		case "password": 
		case "textarea":
	        case "hidden":	
			
			elements[i].value = ""; 
			break;
        
		case "radio":
		case "checkbox":
  			if (elements[i].checked) {
   				elements[i].checked = false; 
			}
			break;

		case "select-one":
		case "select-multi":
            		elements[i].selectedIndex = -1;
			break;

		default: 
			break;
	}
    }
}


/*
Text input for your experiment. Each array is a condition.
Record all necessary information you may need for each input.
*/

var oldConditions = [
[ 
{"condition":1, "sentenceID":1, "p1":"All artists are bakers","p2":"Some bakers are chemists", "S":"chemist","M":"baker","P":"artist",
"mood":"AI","v3":"are","figure":1,"def":0},

{"condition":1, "sentenceID":2, "p1":"Some dentists are engineers","p2":"Some firefighters are engineers", "S":"firefighter","M":"engineer","P":"dentist",
"mood":"II","v3":"are","figure":2,"def":0},

{"condition":1, "sentenceID":3, "p1":"Some gymnasts are historians","p2":"Some historians are not investors", "S":"investor","M":"historian","P":"gymnast",
"mood":"IO","v3":"are","figure":1,"def":0},

{"condition":1, "sentenceID":4, "p1":"Some judges are not knitters","p2":"Some lawyers are knitters", "S":"lawyer","M":"knitter","P":"judge",
"mood":"OI","v3":"are","figure":2,"def":0},

{"condition":1, "sentenceID":5, "p1":"Some managers are not nudists","p2":"Some oceanographers are not nudists", "S":"oceanographer","M":"nudist","P":"manager",
"mood":"OO","v3":"are","figure":2,"def":0},

{"condition":1, "sentenceID":6, "p1":"Some painters are not rappers","p2":"All quality-control inspectors are rappers", "S":"quality-control inspector","M":"rapper","P":"painter",
"mood":"OA","v3":"are","figure":4,"def":0},

{"condition":1, "sentenceID":7, "p1":"No scientists are tailors","p2":"Some umpires are not tailors", "S":"umpire","M":"tailor","P":"scientist",
"mood":"EO","v3":"are","figure":2,"def":0},

{"condition":1, "sentenceID":8, "p1":"Some valets are welders","p2":"All analysts are welders", "S":"valet","M":"welder","P":"analyst",
"mood":"IA","v3":"are","figure":2,"def":0},

{"condition":1, "sentenceID":9, "p1":"Some bank tellers are not cartoonists","p2":"No bank tellers are dieticians", "S":"cartoonist","M":"bank teller","P":"dietician",
"mood":"OE","v3":"are","figure":3,"def":0},

{"condition":1, "sentenceID":10, "p1":"Some educators are farmers","p2":"No educators are governors", "S":"governor","M":"educator","P":"farmer",
"mood":"IE","v3":"are","figure":3,"def":0}

// {"condition":1, "sentenceID":11, "p1":"No horticulturalists are immunologists","p2":"Some jugglers are horticulturalists", "S":"juggler","M":"horticulturalist","P":"immunologist",
// "mood":"EI","v3":"are","figure":4,"def":0},

// {"condition":1, "sentenceID":12, "p1":"All librarians are masons","p2":"All nurses are masons", "S":"nurse","M":"mason","P":"librarian",
// "mood":"AA","v3":"are","figure":2,"def":0},
]]

var allConditions = [
[{"condition":1, "mood":"AA"},{"condition":1, "mood":"AE"},{"condition":1, "mood":"AI"},{"condition":1, "mood":"AO"},
{"condition":1, "mood":"EA"},{"condition":1, "mood":"EE"},{"condition":1, "mood":"EI"},{"condition":1, "mood":"EO"},
{"condition":1, "mood":"IA"},{"condition":1, "mood":"IE"},{"condition":1, "mood":"II"},{"condition":1, "mood":"IO"},
{"condition":1, "mood":"OA"},{"condition":1, "mood":"OE"},{"condition":1, "mood":"OI"},{"condition":1, "mood":"OO"}],
[{"condition":2, "mood":"AA"},{"condition":2, "mood":"AE"},{"condition":2, "mood":"AI"},{"condition":2, "mood":"AO"},
{"condition":2, "mood":"EA"},{"condition":2, "mood":"EE"},{"condition":2, "mood":"EI"},{"condition":2, "mood":"EO"},
{"condition":2, "mood":"IA"},{"condition":2, "mood":"IE"},{"condition":2, "mood":"II"},{"condition":2, "mood":"IO"},
{"condition":2, "mood":"OA"},{"condition":2, "mood":"OE"},{"condition":2, "mood":"OI"},{"condition":2, "mood":"OO"}]
];

var allMaterials = [{"matID":1,"noun":"ball","adj1":"red","adj2":"large","adj3":"new","suffix":"s","article":"a"},
{"matID":2,"noun":"bike","adj1":"blue","adj2":"small","adj3":"old","suffix":"s","article":"a"},
{"matID":3,"noun":"bottle","adj1":"green","adj2":"empty","adj3":"large","suffix":"s","article":"a"},
{"matID":4,"noun":"car","adj1":"white","adj2":"old","adj3":"fast","suffix":"s","article":"a"},
{"matID":5,"noun":"lamp","adj1":"grey","adj2":"large","adj3":"new","suffix":"s","article":"a"},
{"matID":6,"noun":"couch","adj1":"brown","adj2":"new","adj3":"leather","suffix":"es","article":"a"},
{"matID":7,"noun":"table","adj1":"wooden","adj2":"long","adj3":"new","suffix":"s","article":"a"},
{"matID":8,"noun":"chair","adj1":"orange","adj2":"hard","adj3":"small","suffix":"s","article":"a"},
{"matID":9,"noun":"kite","adj1":"yellow","adj2":"old","adj3":"small","suffix":"s","article":"a"},
{"matID":10,"noun":"building","adj1":"tall","adj2":"new","adj3":"brown","suffix":"s","article":"a"},
{"matID":11,"noun":"pen","adj1":"black","adj2":"small","adj3":"old","suffix":"s","article":"a"},
{"matID":12,"noun":"eraser","adj1":"pink","adj2":"hard","adj3":"new","suffix":"s","article":"an"},
{"matID":13,"noun":"basket","adj1":"purple","adj2":"soft","adj3":"old","suffix":"s","article":"a"},
{"matID":14,"noun":"rug","adj1":"beige","adj2":"new","adj3":"expensive","suffix":"s","article":"a"},
{"matID":15,"noun":"cushion","adj1":"colorful","adj2":"soft","adj3":"small","suffix":"s","article":"a"},
{"matID":16,"noun":"vacuum","adj1":"maroon","adj2":"light","adj3":"powerful","suffix":"s","article":"a"}];


/*
Set variables
*/

// Number of conditions in experiment
var numConditions = allConditions.length;

// Randomly select a condition number for this particular participant
var chooseCondition = random(0, numConditions-1);
var otherCondition = (chooseCondition+1)%2;
// Based on condition number, choose set of input (trials)
var allTrialOrders = allConditions[chooseCondition];
var allPropOrders = allConditions[chooseCondition];
// Number of trials in each condition
var numTrials = allTrialOrders.length;
// Produce random order in which the trials will occur
var shuffledOrder = shuffledArray(numTrials);
var shuffledPorder = shuffledArray(numTrials);
var shuffledNorder = shuffledArray(numTrials);

// Keep track of current trial 
var currentTrialNum = 0;

// Set A-C \ C-A --- left \ right ordering
var termOrder = random(2);

// A variable special for this experiment because we're randomly
// choosing word orders as well
var trial;
var trialNoun;
var trialMaterial;
var adjOrder;
var nTargets = 4;
var shuffledTargets = shuffledArray(nTargets);
var nPropPermute = 7;
var shuffledProp = shuffledArray(nPropPermute+1);

// Keep track of how many trials have been completed
var numComplete = 0;
var	num2Complete = 0;
var currNounNum;
var currMatNum;
var quantifiers = ["A","E","I","O"];
var quantmap = {"A":"All","E":"No","I":"Some","O":"Some not"};
var conclusionTerms = ["sp","ps"];
// SMP
var properties = ["111", "110", "101", "011", "100", "010", "001", "000"];


var termOrderList = [conclusionTerms[termOrder], conclusionTerms[1-termOrder]];

var otherOrderingStuff = {};
otherOrderingStuff["termorder"] = conclusionTerms[termOrder];
otherOrderingStuff["quantifiers"] = shuffledTargets.map(function(i) {return quantifiers[i];});
otherOrderingStuff["properties"] = shuffledProp.map(function(i) {return properties[i];});

function getLabel(index) {
  if (index == 8) {
    return "N";
  } else {
    var quantInd = shuffledTargets[index % 4];
    var ordInd = index > 3 ? 1 : 0;
    return quantifiers[quantInd] + termOrderList[ordInd];
  }
}

function getProperty(index) {
  var propInd = shuffledProp[index];
  return properties[propInd];
}


// Updates the progress bar
$("#trial-num").html(numComplete);
$("#total-num").html(numTrials);

/*
The actual variable that will be returned to MTurk.
An experiment object with various variables that you
want to keep track of and return as results.
*/
	// Show instruction slide
showSlide("instructions");
$("#total1-num").html(numTrials);  
    //console.log(inputs);
	
var experiment = {
	// Which condition was run
	
  data: {
	 windowWidth:window.innerWidth,
	 windowHeight:window.innerHeight,
	 browser:BrowserDetect.browser,
	 trialInfo:[],
	 condition: chooseCondition + 1,
	 quantifierSliders: otherOrderingStuff,
	 propertySliders: shuffledProp},
	
	// An array of subjects' responses to each trial (NOTE: in the order in which
	// you initially listed the trials, not in the order in /* which they appeared)
    results: new Array(numTrials),
    // The order in which each trial appeared
    orders: new Array(numTrials),
    /* 
    Special for this experiment
    */
    // The word order word pair, i.e. [word1, word] vs [word2, word1]
    wordOrders: new Array(numTrials),
	  figures: new Array(numTrials),
    isValids: new Array(numTrials),
    isCorrects: new Array(numTrials), 
    
    // Demographics
    gender: "",
    age:"",
    nativeLanguage:"",
    comments:"",
    
    /* 
    Functions for the experiment. Gets called from html
    when people press a button to the next page or to submit
    results, etc
    */
    
  // Goes to description slide
  // description: function() {
  // 	showSlide("description");
  // 	$("#tot-num").html(numTrials);	
  // },

  description2: function() {
  	showSlide("description2");
    $("#total2-num").html(numTrials);
  	$("#tot-num").html(numTrials);	
  },
    
    // Goes to example slide
/*     example1: function() {
    	showSlide("example1");
		$("#conclusion").hide();
		$("#next1").hide();
		$("#concbutton").click(function() { 
		$("#conclusion").show(); 
		$("#next1").show();
		});
    },
    example2: function() {
    	showSlide("example2");
		$("#conclusion2").hide();
		$("#next2").hide();
		$("#concbutton2").click(function() { 
		$("#conclusion2").show(); 
		$("#next2").show();
		});
    }, */
	
    // Reaches end of survey, submits results
  end: function() {
  
// Records demographics
      var gen = getRadioCheckedValue(1, "genderButton");
      var ag = document.age.ageRange.value;
      var lan = document.language.nativeLanguage.value;
      var comm = document.comments.input.value;
      experiment.gender = gen;
      experiment.age = ag;
      experiment.nativeLanguage = lan;
      experiment.comments = comm;
      clearForm(document.forms[1]);
      clearForm(document.forms[2]);
      clearForm(document.forms[3]);
      clearForm(document.forms[4]);
      
      // Show finished slide
      showSlide("finished");
      setTimeout(function() {turk.submit(experiment) }, 1500);
  },

    // Goes to next trial
    next: function() {

		// If this is not the first trial, record variables
    	if (numComplete > 0) {
    		
    		//var rating = parseFloat(document.rating.score.value);
			//experiment.results[currentTrialNum] = responses;
        	//experiment.orders[currentTrialNum] = numComplete;
        	//experiment.figures[currentTrialNum] = trial.figure;
        	//experiment.isValids[currentTrialNum] = trial.isValid;
        	//experiment.isCorrects[currentTrialNum] = trial.isCorrect;
        	//clearForm(document.forms[0]);
        }
    	// If subject has completed all trials, update progress bar and
    	// show slide to ask for demographic info
    	if ((numComplete) >= numTrials) {
    	// 	$('.bar').css('width', (200.0 * (numComplete)/numTrials) + 'px');
    	// 	$("#trial-num").html(numComplete);
    	// 	$("#total-num").html(numTrials);
     //    $("#total2-num").html(numTrials);
     //    if (otherCondition==0){
     //      var descr = "imagine you've arrived on an alien planet. You've learned that the native population refers properties of objects by single letters."
     //    } else{
     //      var descr = "imagine you're in a preschool play-room with a floor full of objects of various shape, color, and pattern."
     //    }
     //    $("#context").html(descr);  
			  // experiment.description2();

        $('.bar').css('width', (200.0 * num2Complete/numTrials) + 'px');
        $("#trial-num").html(num2Complete);
        $("#total-num").html(numTrials);
        experiment.questionaire();
        
    	// Otherwise, if trials not completed yet, update progress bar
    	// and go to next trial based on the order in which trials are supposed
    	// to occur
    	} else {
			$("#targetError").hide(); 
			currentTrialNum = shuffledOrder[numComplete];
			trial = allTrialOrders[currentTrialNum];
      currMatNum = shuffledNorder[numComplete];
      //pick a random noun
      trialNoun = allMaterials[currMatNum].noun;
      var trialAdj = [];
      var b=[];
      // randomize the adjectives
      var a=Object.keys(allMaterials[currMatNum]).filter(function(x) {return (x.indexOf("adj")==0)})
      while (a.length>0) {
        var item = a.splice(Math.floor(Math.random()*a.length), 1)[0];
        b.push(item);
      }
      for (var i=0; i < b.length; i++){
        trialAdj[i] = allMaterials[currMatNum][b[i]]
        };
      var termP = trialAdj[0]+" "+trialNoun+allMaterials[currMatNum].suffix;
      var termM = trialAdj[1]+" "+trialNoun+allMaterials[currMatNum].suffix;
      var termS = trialAdj[2]+" "+trialNoun+allMaterials[currMatNum].suffix;
    		$('.bar').css('width', (200.0 * (1+numComplete)/numTrials) + 'px');
    		$("#trial-num").html(numComplete+1);
    		$("#total-num").html(numTrials);
    		$("#condition").html(experiment.condition);
/* 			pConclusionDef = ["All "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " not "+trial.P, "None "+trial.S+" " + trial.v3 + " "+trial.P, "None of these conclusions"] */
			pConclusion = ["All "+termS+" are "+termP,"No "+termS+" are "+ termP, "Some "+termS+" are "+ termP, "Some "+termS+" are not "+ termP, "None of these conclusions"]
      //altpConclusion = ["All "+trial.P+"s are "+ trial.S + "s","No "+trial.P+"s are "+ trial.S + "s", "Some "+trial.P+"s are "+ trial.S + "s", "Some "+trial.P+"s are not "+ trial.S + "s", "None of these conclusions"]
			var bowls = '';
			var responses = {};
      var conclusionOrder = {};
			var nResponses = 0;
    for (var i=0; i <nTargets; i++) {

          $("#conclusion" + (i)).html(pConclusion[shuffledTargets[i]]);
          conclusionOrder["conclusion_" + getLabel(i)] = pConclusion[shuffledTargets[i]];
          $("#sliderContainer" + (i)).html("<div id='slidy" + i + "'></div>");
       };
      $("#conclusion4").html("");
      $("#sliderContainer4").html("<div id='slidy4'></div>");
      conclusionOrder["conclusion_" + getLabel(8)] = "none of the above";


			// for (var i=0; i < nTargets; i++) {
			// 	bowls = bowls.concat('<td class="bowltd"><div>'+pConclusion[shuffledTargets[i]]+'</div><br><div>Definitely follows</div><div id="slidy'+i+'" align="center"></div><div>Definitely does not follow</div></td><td width="8px"></td>');
   //      bowls = bowls.concat('<td class="bowltd"><div>'+altpConclusion[shuffledTargets[i]]+'</div><br><div>Definitely follows</div><div id="slidy'+i+'" align="center"></div><div>Definitely does not follow</div></td><td width="8px"></td>');			
   //    };
			// bowls = bowls.concat('<tr cellspacing="10"><td width="350" align="left">'+pConclusion[pConclusion.length-1]+'</td><td width="20"></td><td><span class="sliderLabel"> Definitely does not follow </span></td><td width="5"></td><td valign="middle"><div id="slidyr'+(2*i)+'"></div></td><td width="5"></td><td><span class="sliderLabel">Definitely follows</span></td></div></tr><tr height="5"></tr>');
			
			// $("#vagueBowls").html(bowls);
		
			function changeCreator(ind, caseLabel) {
				return function(value) {
				//console.log(ind);
				if (responses['target_' + getLabel(ind)] == null)
						{
						nResponses++;
					}				
					responses['target_' + getLabel(ind)] = $("#"+caseLabel).slider("value");           
				$("#"+caseLabel).css({"background":"#E6E6E6",
					"border-color": "#001F29"});
				  $("#"+caseLabel+" .ui-slider-handle").css({
				   "background":"#E62E00",
				   "border-color": "#001F29" }); 
					}	
				}    

			for (var i=0; i <= (nTargets); i++) {
				 var caseLabel = "slidy" + i
        if (i == (nTargets)){
            $("#"+caseLabel).slider({
              animate: "fast",
              orientation: "horizontal",
              max: 1 , 
              min: 0, 
              step: 0.01, 
              value: 0.5,
              change: 
              changeCreator(i, caseLabel)
            });
          }
          else
          {
          $("#"+caseLabel).slider({
            animate: "fast",
            orientation: "vertical",
            max: 1 , 
            min: 0, 
            step: 0.01, 
            value: 0.0,
            change: 
            changeCreator(i, caseLabel)
           });
        }};



      // }
      //     {value: 0.5,} else {value:0.0,}
      //       $("#"+caseLabel).slider({
      //         animate: "fast",
      //         orientation: "horizontal",
      //         max: 1 , 
      //         min: 0, 
      //         step: 0.01,
      //         change: 
      //         changeCreator(i, caseLabel)
      //       };



			
			$("#sliderMoveon").click(function() {
		//	if ( nResponses <= nTargets ) {   	
       if ( nResponses < 0 ) {     

				$("#targetError").show();
	   			//console.log("hi");
			} else {
				$("#sliderMoveon").unbind("click");
			   responses["trialID"] = currentTrialNum;
			   responses["mood"] = (trial.mood + trial.figure);
         responses["termContent"] = {"S":trial.S,"M":trial.M,"P":trial.P};
         responses["conclusionsFull"] = conclusionOrder;
         console.log(responses);
			   var trialData = experiment.data["trialInfo"].push(responses);
				experiment.next();	
			}});        
 
			currentTrialNum = shuffledOrder[numComplete];
			trial = allTrialOrders[currentTrialNum];
			var mood = trial.mood
			var premise1;
			showSlide("stage");
      // construct premises; figural considerations etc

      if (trial.condition == 1){
        if (trial.mood.substring(0,1)=="O"){
          p1 = "Some " + termM + " are not " + termP
        } else{
          p1 = quantmap[trial.mood.substring(0,1)] + " " + termM + " are " + termP};
        if (trial.mood.substring(1,2)=="O"){
          p2 = "Some " + termS + " are not " + termM
        } else{
          p2 = quantmap[trial.mood.substring(1,2)] + " " + termS + " are " + termM
      }
    };
      if (trial.condition == 2){
        if (trial.mood.substring(0,1)=="O"){
          p1 = "Some " + termP + " are not " + termM
        } else{
          p1 = quantmap[trial.mood.substring(0,1)] + " " + termP + " are " + termM};
        if (trial.mood.substring(1,2)=="O"){
          p2 = "Some " + termS + " are not " + termM
        } else{
          p2 = quantmap[trial.mood.substring(1,2)] + " " + termS + " are " + termM
      }
    };
      $("#premise1").html(p1);
			$("#premise2").html(p2);

			numComplete++;
        } //end of else
    }, //end of next function
	
	priors: function() {
    	if (num2Complete >= numTrials) {
    		$('.bar').css('width', (200.0 * num2Complete/numTrials) + 'px');
    		$("#trial-num").html(num2Complete);
    		$("#total-num").html(numTrials);
    		experiment.questionaire();
    	// Otherwise, if trials not completed yet, update progress bar
    	// and go to next trial based on the order in which trials are supposed
    	// to occur
    	} else {
			$("#targetError2").hide(); 
			// currentTrialNum = shuffledPorder[num2Complete];
			// trial = allPropOrders[currentTrialNum];		
   //    adjOrder = shuffledArray(allAdjectives.length);
   //    adjOrder = [0,1,2]
   //    currNounNum = shuffledNorder[num2Complete];
   //    //pick a random noun
   //    trialNoun = allNouns[currNounNum].noun;
   //    var trialAdj = [];
   //    var trialNadj = [];
   //    // randomize the adjectives
   //    for (var i=0; i < adjOrder.length; i++){
   //      trialAdj[i] = allAdjectives[adjOrder[i]][random(0,1)].A
   //      trialNadj[i] = allAdjectives[adjOrder[i]][(1+random(0,1))%2].A
   //      };
   //    var termP = trialAdj[0]+" "+trialNoun+"s";
   //    var termM = trialAdj[1]+" "+trialNoun+"s";
   //    var termS = trialAdj[2]+" "+trialNoun+"s";
        currentTrialNum = shuffledOrder[num2Complete];
        trial = allTrialOrders[currentTrialNum];
        currMatNum = shuffledNorder[num2Complete];
        //pick a random noun
        trialNoun = allMaterials[currMatNum].noun;
        var trialobj = allMaterials[currMatNum].article + " " + trialNoun;
        $("#object").html(trialobj);
        var trialAdj = [];
        var b=[];
        // randomize the adjectives
        var a=Object.keys(allMaterials[currMatNum]).filter(function(x) {return (x.indexOf("adj")==0)})
        while (a.length>0) {
          var item = a.splice(Math.floor(Math.random()*a.length), 1)[0];
          b.push(item);
        }
        for (var i=0; i < b.length; i++){
          trialAdj[i] = allMaterials[currMatNum][b[i]]
          };
        var termP = trialAdj[0]+" "+trialNoun+allMaterials[currMatNum].suffix;
        var termM = trialAdj[1]+" "+trialNoun+allMaterials[currMatNum].suffix;
        var termS = trialAdj[2]+" "+trialNoun+allMaterials[currMatNum].suffix;    		
        $('.bar').css('width', (200.0 * num2Complete/numTrials) + 'px');
    		$("#trial-num").html(num2Complete);
    		$("#total-num").html(numTrials);
    		$("#condition").html(experiment.condition);
        // 111, 110, 101, 011, 100, 010, 001, 000
		 	// propPermute = ["A " +trialNoun+ " which is " + trialAdj[2]+", " + trialAdj[1] + ", and "+trialAdj[0], 
    //   "A " +trialNoun+ " which is " + trialAdj[2]+", " + trialAdj[1] + ", and not "+trialAdj[0], 
    //   "A " +trialNoun+ " which is " + trialAdj[2]+", " + trialAdj[0] + ", and not "+trialAdj[1], 
    //   "A " +trialNoun+ " which is " + trialAdj[0]+", " + trialAdj[1] + ", and not "+trialAdj[2],
    //   "A " +trialNoun+ " which is " + trialAdj[2]+", not " + trialAdj[1] + ", and not "+trialAdj[0], 
    //   "A " +trialNoun+ " which is " + trialAdj[1]+", not " + trialAdj[2] + ", and not "+trialAdj[0], 
    //   "A " +trialNoun+ " which is " + trialAdj[0]+", not " + trialAdj[1] + ", and not "+trialAdj[2], 
    //   "A " +trialNoun+ " which is " + "not " + trialAdj[2]+", not " + trialAdj[1] + ", and not "+trialAdj[0]]
      propPermute = ["The " +trialNoun+ " is " + trialAdj[2]+", " + trialAdj[1] + ", and "+trialAdj[0], 
      "The " +trialNoun+ " is " + trialAdj[2]+", " + trialAdj[1] + ", and not "+trialAdj[0], 
      "The " +trialNoun+ " is " + trialAdj[2]+", " + trialAdj[0] + ", and not "+trialAdj[1], 
      "The " +trialNoun+ " is " + trialAdj[0]+", " + trialAdj[1] + ", and not "+trialAdj[2],
      "The " +trialNoun+ " is " + trialAdj[2]+", not " + trialAdj[1] + ", and not "+trialAdj[0], 
      "The " +trialNoun+ " is " + trialAdj[1]+", not " + trialAdj[2] + ", and not "+trialAdj[0], 
      "The " +trialNoun+ " is " + trialAdj[0]+", not " + trialAdj[1] + ", and not "+trialAdj[2], 
      "The " +trialNoun+ " is " + "not " + trialAdj[2]+", not " + trialAdj[1] + ", and not "+trialAdj[0]];			
      var priorchecktext = '';
			var priorResponses = {};
			var nResponses = 0;
      var propertyOrder = {};
/* 			for (var j=0; j <= nPropPermute; j++){
				bowls = '';
				bowls = bowls.concat('<tr><td class="bowltd" colspan=5><div>'+propPermute[j]+'</div></td></tr><tr><td><p>Very Unlikely</p></td><td width = "5"></td><td><div id="slidyr'+j+'"></div></td><td width = "5"></td><td><p>Very Likely</p></td></tr>');
				$("#vagueRow"+(j+1)).html(bowls);
				} */
			 for (var i=0; i <= nPropPermute; i++) {
         propertyOrder["property_" + getProperty(i)] = propPermute[shuffledProp[i]];
				 priorchecktext = priorchecktext.concat('<tr cellspacing="10"><td width="350" align="left">'+propPermute[shuffledProp[i]]+'</td><td width="30"></td><td><span class="sliderLabel"> Very Unlikely </span></td><td width="5"></td><td valign="middle"><div id="slidyr'+i+'"></div></td><td width="5"></td><td><span class="sliderLabel">Very Likely</span></td></div></tr><tr height="5"></tr>');
			 }
     // 2. measure question
	// priorchecktext = 'string balh'
			 $("#priorCheck").html(priorchecktext);				
				
				
			function changeCreator(ind, caseLabel) {
				return function(value) {
				//console.log(ind);
				if (priorResponses['property_' + getProperty(ind)] == null)
						{
						nResponses++;
					}				
					priorResponses['property_' + getProperty(ind)] = $("#"+caseLabel).slider("value");					
				$("#"+caseLabel).css({"background":"#E6E6E6",
					"border-color": "#001F29"});
				  $("#"+caseLabel+" .ui-slider-handle").css({
				   "background":"#E62E00",
				   "border-color": "#001F29" }); 
					}	
				}    

			for (var i=0; i <= nPropPermute; i++) {
				 var caseLabel = "slidyr" + i;
				 $("#"+caseLabel).slider({	
					   animate: "fast",
					   orientation: "horizontal",
					   max: 1 , 
					   min: 0, 
					   step: 0.01, 
					   value: 0.5,
/* 					   slide: function( event, ui ) {
						   $("#"+caseLabel+" .ui-slider-handle").css({
							  "background":"#8A1C00",//"#E0F5FF",
							  "border-color": "#001F29"
						   });
					   },   */             
					   change: //function( event, ui) {
		//	               	console.log(ui);
							changeCreator(i, caseLabel)
		//					if (responses['qudcheck' + i] == null) { nqudResponses++; }				
		//					responses['qudcheck' + i] = ui.value;         
					   //}
				});
			}     
			
			
			$("#sliderMoveon2").click(function() {
		//	if ( nResponses <= nPropPermute ) {   	
     if ( nResponses < 0 ) {     
				$("#targetError2").show();
			} else {
				$("#sliderMoveon2").unbind("click");

         priorResponses["propertiesFull"] = propertyOrder;
         priorResponses["trialID"] = currentTrialNum;
			  // priorResponses["mood"] = (trial.mood + trial.figure);
			   priorResponses["termContent"] = {"A":termS,"B":termM,"C":termP};
         console.log(priorResponses);

			   var trialData = experiment.data["trialInfo"].push(priorResponses);
				experiment.priors();	
			}});        
 
			currentTrialNum = shuffledPorder[num2Complete];
			trial = allPropOrders[currentTrialNum];

			showSlide("priors");
			wordOrder = 0;

			num2Complete++;
        } //end of else
    }, //end of priors function
	
	questionaire: function() {
    $(document).keypress( function(event){
     if (event.which == '13') {
        event.preventDefault();
      }
    });
    $('.bar').css('width', ( "100%"));
    showSlide("questionaire");
    $("#lgerror").hide();
    $("#formsubmit").click(function(){
    rawResponse = $("#questionaireform").serialize();
    pieces = rawResponse.split("&");
    var gen = $('input[name="genderButton"]:checked').val();
	var ag = $('#ageRange').val();
	var logi = $('input[name="logicButton"]:checked').val();
    var lang = pieces[0].split("=")[1];
    var comments = pieces[1].split("=")[1];
    if (lang.length > 0) {
        experiment.data["language"] = lang;
        experiment.data["comments"] = comments;
        experiment.data["age"] = ag;
		experiment.data["logic"] = logi;
		experiment.data["gender"] = gen;
        showSlide("finished");
		//console.log(experiment.data);
        setTimeout(function() { turk.submit(experiment.data) }, 1000);
    }
    });
  }
		
}


