function par(text) {
	return "<p>" + text + "</p>";
}

function fillArray(value, len) {
  var arr = [];
  for (var i = 0; i < len; i++) {
    arr.push(value);
  };
  return arr;
}

function range(value){
    return Array.apply(null, Array(value)).map(function (_, i) {return i;});
}

function sentence(q, p, x, y){
    return syll_dict[q] + " of the " + p + " that " + x + ' ' + y + '.';
}


/* stimulus setup */
var materials = 
[{"P":"lightbulbs",
"X":"are on", 
"Y":"are bright", 
"Z":"are hot",
"notX":"are not on",
"notY":"are not bright",
"notZ":"are not hot"},

{"P":"strawberries",
"X":"are in the freezer", 
"Y":"are soft", 
"Z":"are warm",
"notX":"are not in the freezer",
"notY":"are not soft",
"notZ":"are not warm"},

{"P":"crackers",
"X":"are soggy", 
"Y":"are past expiration date", 
"Z":"have lots of flavor",
"notX":"are not soggy",
"notY":"are not past expiration date",
"notZ":"do not have lots of flavor"},

{"P":"knives",
"X":"are sharp", 
"Y":"are rusty", 
"Z":"cut well",
"notX":"are not sharp",
"notY":"are not rusty",
"notZ":"do not cut well"}]

var syllogisms =
[{"syll":"AO2"},
{"syll":"EA3"},
{"syll":"IE1"},
{"syll":"OA1"}]

// if (Math.floor(Math.random()*2) == 0){
//     var condition = 'radio'}
// else{
//     var condition = 'slide'}

var condition = 'radio'


var syll_dict = {"A":"All",
                "E":"None",
                "I":"Some",
                "O":"Some"}

//var syllogisms= ["AO2","EA3","IE1","OA1"];
var syllogisms = ['AA1', 'AI1', 'EA1', 'EI1']

var syll_shuf = jsPsych.randomization.repeat(syllogisms,1);
var trials_shuf = jsPsych.randomization.repeat(materials,1);

var total_trials = trials_shuf.length;

for(i= 0; i<total_trials; i++){
    trials_shuf[i].syll=syll_shuf[i];}

// syllogism premises
var all_prompts = trials_shuf.map(function(s)
    {switch (s.syll.slice(2)){
            case "1":
                var t1 = s.Y, t2 = s.X, t3 = s.Z, t4 = s.Y, t2n=s.notX, t4n=s.notY;
                if (s.syll.slice(0,1)=='O') {t2=s.notX};
                if (s.syll.slice(1,2)=='O') {t4=s.notY};
                break;
            case "2":
                var t1 = s.X, t2 = s.Y, t3 = s.Z, t4 = s.Y, t2n=s.notY, t4n=s.notY;
                if (s.syll.slice(0,1)=='O') {t2=s.notY};
                if (s.syll.slice(1,2)=='O') {t4=s.notY};
            break;
            case "3":
                var t1 = s.Y, t2 = s.X, t3 = s.Y, t4 = s.Z, t2n=s.notX, t4n=s.notZ;
                if (s.syll.slice(0,1)=='O') {t2=s.notX};
                if (s.syll.slice(1,2)=='O') {t4=s.notZ};
            break;
            }
        return ['"'+sentence(s.syll.slice(0,1),s.P,t1,t2) +
        '<br>' + sentence(s.syll.slice(1,2),s.P,t3,t4)+'"']})


// syllogism conclusions
var all_trials = trials_shuf.map(function (s) 
    {return [sentence("A",s.P,s.Z,s.X)+'\n',
            sentence("E",s.P,s.Z,s.X)+'\n',
            sentence("I",s.P,s.Z,s.X)+'\n',
            sentence("O",s.P,s.Z,s.notX)+'\n']})

/* shuffle order of sliders 
 maintain same order in all trials (all_trials.map)
 shuffle states array to track correct label*/
var states = ["A","E","I","O"]
var i=-1, len= states.length, next, order=[];
order = jsPsych.randomization.repeat(range(len),1);

for(i= 0; i<len; i++){
    next= order[i];
    states.push(states[next]);
    all_trials.map(function (m) {return m.push(m[next])})
};
test = states.splice(0, len);
all_trials.map(function (m) {return m.splice(0, len)});


// var test_stimuli = materials.map(function (m) 
// 	{return m.property1 + ", " + m.property2 + ", and " + m.property3});

//var all_trials = jsPsych.randomization.repeat(test_stimuli, 1);

var scale = [ "Certainly does not follow", "Certainly follows"];
if (condition=='radio'){
    scale = ["Don't know","Certain"];
}

var all_scales = fillArray(fillArray(scale,all_trials[1].length),total_trials);
var all_intervals = fillArray(fillArray(100,all_trials[1].length),total_trials);
var all_orders = fillArray(states,total_trials);
var all_domains = trials_shuf.map(function(m) {return [m.P]});
var all_sylls = syll_shuf.map(function(m) {return [m]});


// var post_trial_gap = function() {
//     return Math.floor(Math.random() * 1500) + 750;
// };

var check_consent = function(elem) {
    if ($('#consent_checkbox').is(':checked')) {
        return true;
    }
    else {
        alert("If you wish to participate, you must check the box next to the statement 'I agree to participate in this study.'");
        return false;
    }
    return false;
};


var check_language = function(elem) {
    if ($('#native_lang').val()=='') {
        alert("Please enter your native language.'");
        return false;
    }
    else {
        return true;
    }
    return false;
};
if (condition=='radio')
    {var depMeas_instruct = "<p>If you think the conclusion follows from the argument, indicate so on the line. In addition, rate your confidence in your response.</p>"
}
else
    {var depMeas_instruct =     "<p>If you think the conclusion follows from the argument, indicate so on the line. Adjust the position of the slider bar to reflect your confidence in your response.</p>"
}

var test_block = 
{type: "vert-slider", 
condition: condition,
instructions: depMeas_instruct,
questions: all_trials,
labels: all_scales,
intervals: all_intervals,
question_order: all_orders,
domains: all_domains,
sylls: all_sylls,
show_ticks: false,
text: all_prompts,
hide_handle: true,
orientation: "vertical"
};

/* text blocks */



// var welcome_block = {
//     type: "text",
//     text: "<img src='../common/stanford.png' alt='Stanford University'>"+
//             "<p class='center-content'>Stanford Computation and Cognition Lab</p>"+
//             "<p class='center-content'>Thank you for participating in our experiment. In this experiment, we are interested in what types of objects people think are plausible. You will answer a set of " + total_trials + " questions. We expect this will take under 5 minutes.</p>"
//         };




var consent_block = {
    type:'html', 
    pages: [{url: "../common/consent_syll.html", 
    cont_btn: "start", 
  //  check_fn: check_consent
}]};

if (condition=='radio')
    {var inst_text = "<p>In this experiment, you will read four (4) randomly selected logical arguments. "+
    "For each argument, you will be presented with different conclusions that might follow from the argument presented."
}
else
{var inst_text = "<p>In this experiment, you will read four (4) randomly selected logical arguments. "+
    "For each argument, you will be presented with different conclusions that might follow from the argument presented."
}


var instructions_block = {
    type: "text-wButton",
    text: inst_text
};


        /* debrief block */

var debrief_block = {
    type: "text",
    text: function() {
        return "Thank you for completing the task. Press fill out the questionnaire on the next slide " + 
        "and then you will be done with the experiment. Press any key to continue.</p>";
    }
};

var questionnaire_block = 
            {type:'questionnaire', 
                pages: [{url: "../common/questionnaire.html", 
                cont_btn: "formsubmit",
                check_fn: check_language}]};

/* define experiment structure */

var experiment_blocks = [];

experiment_blocks.push(consent_block);
// //experiment_blocks.push(welcome_block);
experiment_blocks.push(instructions_block);
experiment_blocks.push(test_block);
experiment_blocks.push(debrief_block);
experiment_blocks.push(questionnaire_block);


/* start the experiment */

jsPsych.init({
    display_element: $('#jspsych-target'),
    experiment_structure: experiment_blocks,
    // on_finish: function() {
    //             jsPsych.dataAPI.displayData();
    //         }
    on_finish: function () {setTimeout(function() 
    { turk.submit(jsPsych.data())}, 1000)}
});