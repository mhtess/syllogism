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

/* stimulus setup */
var materials = 
[{"type":"CC-EE",
"premises":"some men are mortal <br> some men aren\'t.",
"A":"all of the men are", 
"E":"none of the men are", 
"I":"some of the men are",
"O":"some of the men are not"},
{"type":"CC-AA",
"premises":"Josiah walks around his neighborhood <br> night and has noticed the kids in his neighborho.",
"A":"all of the boys are", 
"E":"none of the boys are", 
"I":"some of the boys are",
"O":"some of the boys are not"},
]



var trials_shuf = jsPsych.randomization.repeat(materials,1);
var total_trials = trials_shuf.length;

var all_trials = trials_shuf.map(function (m) 
    {return [m.A,m.E,m.I,m.O]});



/* shuffle order of situation-sliders 
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

var scale = [ "0", "25","50" ,"75","100"];

var all_scales = fillArray(fillArray(scale,all_trials[1].length),total_trials)
var all_intervals = fillArray(fillArray(100,all_trials[1].length),total_trials)
var all_prompts = trials_shuf.map(function(m) {return [m.premises]});
var all_orders = fillArray(states,total_trials)

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

var test_block = 
{type: "vert-slider", 
questions: all_trials,
labels: all_scales,
intervals: all_intervals,
question_order: all_orders,
show_ticks: false,
text: all_prompts,
hide_handle: true,
orientation: "vertical"
};

/* text blocks */



var welcome_block = {
    type: "text",
    text: "<img src='../common/stanford.png' alt='Stanford University'>"+
            "<p class='center-content'>Stanford Computation and Cognition Lab</p>"+
            "<p class='center-content'>Thank you for participating in our experiment. In this experiment, we are interested in what types of objects people think are plausible. You will answer a set of " + total_trials + " questions. We expect this will take under 5 minutes.</p>"
        };




var consent_block = {
    type:'html', 
    pages: [{url: "../common/consent.html", 
    cont_btn: "start", 
  //  check_fn: check_consent
}]};



var instructions_block = {
    type: "text",
    text: "<p>In this experiment, you will read six (6) different scenarios and answer some questions about them. "+
    "The questions will ask you estimate certain quantities using a slider bar."+
    "<p>To make a mark, just click the slider bar. Once you have clicked, you may adjust your answer simply by clicking anywhere else on the slider.</p>"+
    "Press any key to begin."
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

// experiment_blocks.push(consent_block);
// //experiment_blocks.push(welcome_block);
// experiment_blocks.push(instructions_block);
experiment_blocks.push(test_block);
// experiment_blocks.push(debrief_block);
// experiment_blocks.push(questionnaire_block);


/* start the experiment */

jsPsych.init({
    display_element: $('#jspsych-target'),
    experiment_structure: experiment_blocks,
    on_finish: function() {
                jsPsych.dataAPI.displayData();
            }
});