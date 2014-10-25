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
  console.log('hi');
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
var allConditions = [
[ 
{"condition":1, "sentenceID":1,"isValid":1, "isSingle":1, "p1":"All golfers are retired","p2":"No retired people are full-time employees", "S":" full-time employees", "P":"golfers","mood":"AE","v3":"are","figure":4,"def":0,"c1":"Retired person who is a golfer and who doesn't have a full-time job","c2":"Retired person who isn't a golfer and who doesn't have a full-time job","c3":"Retired person who is a golfer and who has a full-time job","c4":"Retired person who isn't a golfer and who has a full-time job","c5":"Person who is NOT retired, who is a golfer and who doesn't have a full-time job","c6":"Person who is NOT retired, who isn't a golfer and who doesn't have a full-time job","c7":"Person who is NOT retired, who isn't a golfer and who has a full-time job","c8":"Person who is NOT retired, who is a golfer and who has have a full-time job"},
{"condition":1, "sentenceID":2, "isValid":1,"isSingle":1, "p1":"Some lazy students make the Dean's List","p2":"All Dean's List students are good students","S":" good students", "P":"lazy students","mood":"IA","v3":"are","figure":4,"def":0,"c1":"A good student who isn't lazy and who made the Dean's List","c2":"A good student who is lazy and who made the Dean's List","c3":"A good student who isn't lazy and who didn't make the Dean's List","c4":"A good student who is lazy and who didn't make the Dean's List","c5":"A person who is NOT a good student who isn't lazy and who made the Dean's List","c6":"A person who is NOT a good student who is lazy and who made the Dean's List","c7":"A person who is NOT a good student who isn't lazy and who didn't make the Dean's List","c8":"A person who is NOT a good student who is lazy and who didn't make the Dean's List"},
{"condition":1, "sentenceID":3, "isValid":1,"isSingle":0,
"p1": "No married tenants are bachelors", "p2":"All married tenants are renters",
"S":"renters", "P":"bachelors", "mood":"EA","v3":"are","figure":3,"def":0,"c1":"An unmarried bachelor who is a renter","c2":"An unmarried bachelor who is NOT a renter", "c3":"A married bachelor who is a renter","c4":"A married bachelor who is NOT a renter","c5":"An unmarried person who is NOT a bachelor and who is a renter","c6":"An unmarried person who is NOT a bachelor and who is NOT a renter", "c7":"A married person who is NOT a bachelor and who is a renter","c8":"A married person who is NOT a bachelor and who is NOT a renter"},
{"condition":1, "sentenceID":4, "isValid":1,"isSingle":0, "p1":"No wine drinkers are Saudis", "p2":"Some wine drinkers are Italians", "S":"Italians", "P":"Saudis", "mood":"EI","v3":"are","figure":3,"def":0,"c1":"A person who is Italian and NOT Saudi and drinks wine","c2":"A person who is Italian and Saudi and drinks wine","c3":"A person who is Italian and NOT Saudi and doesn't drink wine","c4":"A person who is Italian and Saudi and doesn't drink wine","c5":"A person who is NOT Italian and NOT Saudi and drinks wine","c6":"A person who is NOT Italian, who is Saudi and drinks wine","c7":"A person who is NOT Italian and NOT Saudi and doesn't drink wine","c8":"A person who is NOT Italian, who is Saudi and doesn't drink wine"},
{"condition":1, "sentenceID":5, "isValid":0,"isSingle":0, "p1":"All trainers can bench three times their body weight", "p2":"Some people who can bench three times their body weight participate in weight lifting competitions", "S":" people who participate in weight-lifting competitions", "P":"trainers", "mood":"AI", "v3":"are","figure":4,"def":0,"c1":"A trainer who can bench three times his or her body weight and who participates in weight-lifting competitions","c2":"A trainer who CANNOT bench three times his or her body weight and who participates in weight-lifting competitions","c3":"A trainer who can bench three times his or her body weight and who DOES NOT participate in weight-lifting competitions","c4":"A trainer who CANNOT bench three times his or her body weight and wwho DOES NOT participate in weight-lifting competitions","c5":"A person who is NOT a trainer, who can bench three times his or her body weight and who participates in weight-lifting competitions","c6":"A person who is NOT a trainer, who CANNOT bench three times his or her body weight and who participates in weight-lifting competitions","c7":"A person who is NOT a trainer, who can bench three times his or her body weight and who DOES NOT participate in weight-lifting competitions","c8":"A person who is NOT a trainer, who CANNOT bench three times his or her body weight and who DOES NOT participate in weight-lifting competitions"},
{"condition":1, "sentenceID":6,  "isValid":0,"isSingle":0,"p1":"All church-goers are religious people","p2":"All priests are religious people", "S":"priests", "P":"church-goers", "mood":"AA", "v3":"are","figure":2,"def":0, "c1":"A priest who is religious and who goes to church","c2":"A priest who is NOT religious and who goes to church","c3":"A priest who is religious and who DOES NOT goes to church","c4":"A priest who is NOT religious and who DOES NOT goes to church","c5":"A person who is NOT a priest, who is religious and who goes to church","c6":"A person who is NOT a priest, who is NOT religious and who goes to church","c7":"A person who is NOT a priest, who is religious and who DOES NOT goes to church","c8":"A person who is NOT a priest, who is NOT religious and who DOES NOT goes to church"}
],[
{"condition":2, "sentenceID":1,"isValid":1, "isSingle":1, "p1":"All actresses are hikers","p2":"No hikers are jugglers", "S":"jugglers", "P":"actresses","mood":"AE","v3":"are","figure":4,"def":0,"c1":"An actress who is a hiker and who is a juggler","c2":"An actress who is NOT a hiker, and who is a juggler","c3":"An actress who is a hiker and who is NOT a juggler","c4":"An actress who is NOT a hiker and who is NOT a juggler","c5":"A person who is NOT an actress, who is a hiker and who is a juggler","c6":"A person who is NOT an actress, who is NOT a hiker, and who is a juggler","c7":"A person who is NOT an actress, who is a hiker and who is NOT a juggler","c8":"A person who is NOT an actress, who is NOT a hiker and who is NOT a juggler"},
{"condition":2, "sentenceID":2, "isValid":1,"isSingle":1, "p1":"Some scientists are bowlers","p2":"All bowlers are husbands","S":"husbands", "P":"scientists","mood":"IA","v3":"are","figure":4,"def":0,"c1":"A scientist who is a bowler and a husband","c2":"A scientist who is a bowler and NOT a husband","c3":"A scientist who is a husband and NOT a bowler","c4":"A scientist who is NOT a bowler NOR a husband","c5":"A person who is NOT a scientist, who is a bowler and a husband","c6":"A person who is NOT a scientist, who is a bowler and NOT a husband","c7":"A person who is NOT a scientist, who is a husband and NOT a bowler","c8":"A person who is NOT a scientist, NOT a bowler and NOT a husband"},
{"condition":2, "sentenceID":3, "isValid":1,"isSingle":0,
"p1": "No artists are bakers", "p2":"All artists are canoeists",
"S":"canoeists", "P":"bakers", "mood":"EA","v3":"are","figure":3,"def":0,"c1":"An artist who is a baker and a canoeist","c2":"An artist who is a baker and NOT a canoeist", "c3":"An artist who is NOT a baker and who is a canoeist","c4":"An artist who is a NOT baker and who is NOT a canoeist","c5":"A person who is NOT an artist, who is a baker and a canoeist","c6":"A person who is NOT an artist, who is a baker and NOT a canoeist", "c7":"A person who is NOT an artist, who is NOT a baker and who is a canoeist","c8":"A person who is NOT an artist, who is NOT a baker and who is NOT a canoeist"},
{"condition":2, "sentenceID":4, "isValid":1,"isSingle":0, "p1":"No firemen are Italians", "p2":"Some firemen are Saudis", "S":"Saudis", "P":"Italians", "mood":"EI","v3":"are","figure":3,"def":0,"c1":"A fireman who is Italian and NOT Saudi","c2":"A fireman who is Italian and Saudi","c3":"A fireman who is Italian and NOT Saudi","c4":"A fireman who is Italian and Saudi","c5":"A person who is NOT a fireman and is NOT Italian and NOT Saudi","c6":"A person who is NOT a fireman and who is NOT Italian and who is Saudi","c7":"A person who is NOT a fireman and who is NOT Italian and NOT Saudi","c8":"A person who is NOT a fireman and who is NOT Italian and who is Saudi"},
{"condition":2, "sentenceID":5, "isValid":0,"isSingle":0, "p1":"All movers are butchers", "p2":"Some butchers are Quakers", "S":"Quakers", "P":"butchers", "mood":"AI", "v3":"are","figure":4,"def":0,"c1":"A mover who is a Quaker and a butcher","c2":"A mover who is a Quaker and NOT a butcher","c3":"A mover who is NOT a Quaker and who is a butcher","c4":"A mover who is NOT a Quaker and NOT a butcher","c5":"A person who is NOT a mover, and who is a Quaker and a butcher","c6":"A person who is NOT a mover, and who is a Quaker and NOT a butcher","c7":"A person who is NOT a mover, and who is NOT a Quaker and who is a butcher","c8":"A person who is NOT a mover, and who is NOT a Quaker and NOT a butcher"},
{"condition":2, "sentenceID":6,  "isValid":0,"isSingle":0,"p1":"All the nurses are chemists","p2":"All the attendants are chemists", "S":"attendants", "P":"nurses", "mood":"AA", "v3":"are","figure":2,"def":0, "c1":"A nurse who is a chemist and who is an attendant","c3":"A nurse who is a chemist and who NOT is an attendant","c3":"A nurse who is NOT a chemist and who is an attendant","c4":"A nurse who is NOT a chemist and who is NOT an attendant","c5":"A person who is NOT a nurse and who is a chemist and who is an attendant","c6":"A person who is NOT a nurse and who is a chemist and who is NOT an attendant","c7":"A person who is NOT a nurse and who is NOT a chemist and who is an attendant","c8":"A person who is NOT a nurse and who is NOT a chemist and who is NOT an attendant"}]
];

/*
Set variables
*/

// Number of conditions in experiment
var numConditions = allConditions.length;

// Randomly select a condition number for this particular participant
var chooseCondition = random(0, numConditions-1);

// Based on condition number, choose set of input (trials)
var allTrialOrders = allConditions[chooseCondition];

// Number of trials in each condition
var numTrials = allTrialOrders.length;
//var numTrials = 1;
// Produce random order in which the trials will occur
var shuffledOrder = shuffledArray(numTrials);

// Keep track of current trial 
var currentTrialNum = 0;

// A variable special for this experiment because we're randomly
// choosing word orders as well
var wordOrder = 100;
var trial;
var nTargets = 4;
var shuffledTargets = shuffledArray(nTargets);
console.log(shuffledTargets);
var nPropPermute = 7;
var shuffledProp = shuffledArray(nPropPermute+1);

// Keep track of how many trials have been completed
var numComplete = 0;
var	num2Complete = 0
var quantifiers = ["A","I","E","O","N"]

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
	
var experiment = {
	// Which condition was run
	
  data: {
	 windowWidth:window.innerWidth,
	 windowHeight:window.innerHeight,
	 browser:BrowserDetect.browser,
	 trialInfo:[],
	 condition: chooseCondition + 1,
	 quantifierSliders: shuffledTargets,
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
    description: function() {
    	showSlide("description");
    	$("#tot-num").html(numTrials);	
    },
	
	description2: function() {
    	showSlide("description2");
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
    	if (numComplete >= numTrials) {
    		$('.bar').css('width', (200.0 * numComplete/numTrials) + 'px');
    		$("#trial-num").html(numComplete);
    		$("#total-num").html(numTrials);
			experiment.description2();
    	// Otherwise, if trials not completed yet, update progress bar
    	// and go to next trial based on the order in which trials are supposed
    	// to occur
    	} else {
			$("#targetError").hide(); 
			currentTrialNum = shuffledOrder[numComplete];
			trial = allTrialOrders[currentTrialNum];		
    		$('.bar').css('width', (200.0 * numComplete/numTrials) + 'px');
    		$("#trial-num").html(numComplete);
    		$("#total-num").html(numTrials);
    		$("#condition").html(experiment.condition);
/* 			pConclusionDef = ["All "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " not "+trial.P, "None "+trial.S+" " + trial.v3 + " "+trial.P, "None of these conclusions"] */
			pConclusion = ["All "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " "+trial.P, "Some "+trial.S+" " + trial.v3 + " not "+trial.P, "No "+trial.S+" " + trial.v3 + " "+trial.P, "None of these conclusions"]
			var bowls = '';
			var responses = {};
			var nResponses = 0;
			for (var i=0; i < nTargets; i++) {
/* 				if (trial.def == 1) {
				bowls = bowls.concat('<td class="bowltd"><div>'+pConclusionDef[shuffledTargets[i]]+'</div><br><div>Definitely follows</div><div id="slidy'+i+'" align="center"></div><div>Definitely does not follow</div></td><td width="8px"></td>');} */
/* 				else{ */
				bowls = bowls.concat('<td class="bowltd"><div>'+pConclusion[shuffledTargets[i]]+'</div><br><div>Definitely follows</div><div id="slidy'+i+'" align="center"></div><div>Definitely does not follow</div></td><td width="8px"></td>');//}
			};
			bowls = bowls.concat('<td class="bowltd"><div>'+pConclusion[pConclusion.length-1]+'</div><br><div>Definitely follows</div><div id="slidy'+i+'" align="center"></div><div>Definitely does not follow</div></td><td width="8px"></td>');
			
			$("#vagueBowls").html(bowls);
		
			function changeCreator(ind, caseLabel) {
				return function(value) {
				//console.log(ind);
				if (responses['target' + ind] == null)
						{
						nResponses++;
					}				
					responses['target' + ind] = $("#"+caseLabel).slider("value");           
				$("#"+caseLabel).css({"background":"#E6E6E6",
					"border-color": "#001F29"});
				  $("#"+caseLabel+" .ui-slider-handle").css({
				   "background":"#E62E00",
				   "border-color": "#001F29" }); 
					}	
				}    

			for (var i=0; i <= nTargets; i++) {
				 var caseLabel = "slidy" + i;
				 $("#"+caseLabel).slider({
					   animate: "fast",
					   orientation: "vertical",
					   max: 1 , 
					   min: 0, 
					   step: 0.01, 
					   value: 0.5,
					   /* slide: function( event, ui ) {
						   $("#"+caseLabel+" .ui-slider-handle").css({
							  "background":"#8A1C00",//"#E0F5FF",
							  "border-color": "#001F29"
						   });
					   },                */
					   change: //function( event, ui) {
		//	               	console.log(ui);
							changeCreator(i, caseLabel)
		//					if (responses['qudcheck' + i] == null) { nqudResponses++; }				
		//					responses['qudcheck' + i] = ui.value;         
					   //}
				});
			}     
			
			$("#sliderMoveon").click(function() {
			if ( nResponses <= nTargets ) {   	
				$("#targetError").show();
	   			//console.log("hi");
			} else {
				$("#sliderMoveon").unbind("click");
			   responses["trial"] = currentTrialNum;
			   responses["figure"] = trial.figure;
			   responses["mood"] = trial.mood;
			   responses["isValid"] = trial.isValid;
			   responses["isSingle"] = trial.isSingle;
			   var trialData = experiment.data["trialInfo"].push(responses);
				experiment.next();	
			}});        
 
			currentTrialNum = shuffledOrder[numComplete];
			trial = allTrialOrders[currentTrialNum];
			var mood = trial.mood
			var premise1;
			showSlide("stage");
			$("#premise1").html(trial.p1);
			$("#premise2").html(trial.p2);

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
			currentTrialNum = shuffledOrder[num2Complete];
			trial = allTrialOrders[currentTrialNum];		
    		$('.bar').css('width', (200.0 * num2Complete/numTrials) + 'px');
    		$("#trial-num").html(num2Complete);
    		$("#total-num").html(numTrials);
    		$("#condition").html(experiment.condition);
		/* 	propPermute = [trial.S+" and are " + trial.M + " and are "+trial.P, trial.S+" and are " + trial.M + " and are not "+trial.P, trial.S+" and are not " + trial.M + " and are "+trial.P, "not " + trial.S+" and are " + trial.M + "and are "+trial.P, trial.S+" and are not " + trial.M + " and are not "+trial.P, "not " + trial.S+ " and are not" + trial.M + " and are not "+trial.P, "not" + trial.S+" and are " + trial.M + " and are not "+trial.P, "not " + trial.S+" and are not " + trial.M + " and are not "+trial.P,] */
			propPermute = [trial.c1,trial.c2,trial.c3,trial.c4,trial.c5,trial.c6,trial.c7,trial.c8];
			var priorchecktext = '';
			var priorResponses = {};
			var nResponses = 0;
/* 			for (var j=0; j <= nPropPermute; j++){
				bowls = '';
				bowls = bowls.concat('<tr><td class="bowltd" colspan=5><div>'+propPermute[j]+'</div></td></tr><tr><td><p>Very Unlikely</p></td><td width = "5"></td><td><div id="slidyr'+j+'"></div></td><td width = "5"></td><td><p>Very Likely</p></td></tr>');
				$("#vagueRow"+(j+1)).html(bowls);
				} */
			 for (var i=0; i <= nPropPermute; i++) {
				 priorchecktext = priorchecktext.concat('<tr cellspacing="10"><td width="350" align="left">'+propPermute[shuffledProp[i]]+'</td><td width="20"></td><td><span class="sliderLabel"> Very Unlikely </span></td><td width="5"></td><td valign="middle"><div id="slidyr'+i+'"></div></td><td width="5"></td><td><span class="sliderLabel">Very Likely</span></td></div></tr><tr height="5"></tr>');
			 }
     // 2. measure question
	// priorchecktext = 'string balh'
			 $("#priorCheck").html(priorchecktext);				
				
				
			function changeCreator(ind, caseLabel) {
				return function(value) {
				//console.log(ind);
				if (priorResponses['property' + ind] == null)
						{
						nResponses++;
					}				
					priorResponses['property' + ind] = $("#"+caseLabel).slider("value");					
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
			if ( nResponses <= nPropPermute ) {   	
				$("#targetError2").show();
			} else {
				$("#sliderMoveon2").unbind("click");
			   priorResponses["trial"] = currentTrialNum;
			   priorResponses["figure"] = trial.figure;
			   priorResponses["mood"] = trial.mood;
			   priorResponses["isValid"] = trial.isValid;
			   priorResponses["isSingle"] = trial.isSingle;
			   var trialData = experiment.data["trialInfo"].push(priorResponses);
				experiment.priors();	
			}});        
 
			currentTrialNum = shuffledOrder[num2Complete];
			trial = allTrialOrders[currentTrialNum];

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


