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

function flattenData(data_object, append_data) {

    append_data = (typeof append_data === undefined) ? {} : append_data;

    var trials = [];

    // loop through data_object
    for (var i = 0; i < data_object.length; i++) {
        for (var j = 0; j < data_object[i].length; j++) {
            var data = $.extend({}, data_object[i][j], append_data);
            trials.push(data);
        }
    }

    return trials;
}

/* frequency setup */
// var materials = 
// [{"type":"CC-EE",
// "prompt":"The historian for the city council of Springfield tracks years where major natural disasters occur. Springfield is an American city that suffers from a relatively large number of earthquakes. Estimate how many of the next 100 years will certain situations occur in Springfield.",
// "X":"a major earthquake", 
// "Y":"the city hall collapses", 
// "Z":"the main highway needs major repairs",
// "notX":"NO major earthquake",
// "notY":"the city hall does NOT collapse",
// "notZ":"the main highway is NOT in need of major repairs"},

// {"type":"CC-PP",
// "prompt":"Josiah walks around his neighborhood every night and has noticed the kids in his neighborhood are relatively reckless. Estimate on how many of the 100 nights will Josiah see the following situations.",
// "X":"a group of kids is playing with fireworks", 
// "Y":"fireworks do NOT make a pretty display in the sky", 
// "Z":"NO kid gets injured",
// "notX":"group of kids NOT playing with fireworks",
// "notY":"fireworks make a pretty display in the sky",
// "notZ":"a kid gets injured"},

// {"type":"CC-EP",
// "prompt":"Dr. Fills is a new dentist in Chesterville and is scheduled to see 100 new patients in the next month. Estimate how many of the 100 patients will fit the following descrption.",
// "X":"patient has NO alignment issue", 
// "Y":"has NO difficulty chewing", 
// "Z":"needs braces",
// "notX":"patient has an alignment issue",
// "notY":"has difficulty chewing",
// "notZ":"does NOT need braces"},

// {"type":"CE-EE",
// "prompt":"Sophie works for a towing company and is in charge of answering the phones. Estimate how many of the next 100 calls Sophie gets will have the following profile:",
// "X":"car lights left on overnight", 
// "Y":"car battery is old", 
// "Z":"car battery is now dead",
// "notX":"car lights were NOT left on overnight",
// "notY":"car battery is NOT old",
// "notZ":"car battery is now NOT dead"},

// {"type":"CE-PP",
// "prompt":"Estimate how many of the next 100 bicycles commuting to work will fit the following descriptions:",
// "X":"bicyclist riding a new bike", 
// "Y":"riding in light traffic", 
// "Z":"getting into an accident",
// "notX":"bicyclist riding a bike that's NOT new",
// "notY":"riding in traffic that's NOT light",
// "notZ":"NOT getting into an accident"},

// {"type":"CE-EP",
// "prompt":"Estimate how many of the next 100 laptops Steven sees will have the following characteristics:",
// "X":"laptop computer is unplugged all day", 
// "Y":"laptop is new", 
// "Z":"laptop battery is now dead",
// "notX":"laptop computer is NOT unplugged all day",
// "notY":"laptop is NOT new",
// "notZ":"laptop battery is now NOT dead"}

// ]


// // likely/probable setup
// var materials = 
// [{"type":"CC-EE",
// "domain":"earthquake",
// //"prompt":"The historian for the city council of Springfield records details of major natural disasters in the region. How likely is it that the next natural disaster satisfies the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"The historian for the city council of Springfield records details of major natural disasters in the region. Consider the following events that could occur: (1) there is a major earthquake, (2) the city hall collapses, (3) the main highway needs major repairs. How likely is it that the next natural disaster satisfies the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"there is a major earthquake", 
// "Y":"the city hall collapses", 
// "Z":"the main highway needs major repairs",
// "notX":"there is NOT a major earthquake",
// "notY":"the city hall does NOT collapse",
// "notZ":"the main highway is NOT in need of major repairs"},

// {"type":"CC-PP",
// "domain":"fireworks",
// //"prompt":"Springfield Heights is a neighborhood for young families in the city of Springfield. How likely is it that the next group of kids playing in the neighborhood fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"Springfield Heights is a neighborhood for young families in the city of Springfield. Consider the following events that could occur: (1) a group of kids is playing with fireworks, (2) fireworks go off and explode high in the sky, (3) none of the kids suffers any injuries. How likely is it that the next group of kids playing in the neighborhood fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"the group of kids is playing with fireworks", 
// "Y":"fireworks go off high in the sky", 
// "Z":"NO kid in the group gets injured",
// "notX":"the group of kids is NOT playing with fireworks",
// "notY":"fireworks don't go off high in the sky",
// "notZ":"a kid in the group gets injured"},

// {"type":"CC-EP",
// "domain":"braces",
// "prompt":"Dr. Fills is a dentist in Springfield. Consider the following types of dental circumstnaces: (1) teeth alignment is fine, (2) no difficulty chewing, (3) needs braces. How likely is it that his next patient will fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"patient's teeth alignment is fine", 
// "Y":"has NO difficulty chewing", 
// "Z":"needs braces",
// "notX":"patient's teeth alignment is NOT fine ",
// "notY":"has difficulty chewing",
// "notZ":"does NOT need braces"},

// {"type":"CE-EE",
// "domain":"carBattery",
// "prompt":"The receptionist at Springfield Towing is in charge of recording the types of calls received. Consider the following circumstances: (1) car lights were left on overnight, (2) the car battery is old, (3) car battery is completely drained. How likely is it that the next call will fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"car lights were left on overnight", 
// "Y":"car battery is old", 
// "Z":"car battery is completely drained",
// "notX":"car lights were NOT left on overnight",
// "notY":"car battery is NOT old",
// "notZ":"car battery is NOT completely drained"},

// {"type":"CE-PP",
// "domain":"cyclist",
// "prompt":"Many residents in the city of Springfield commute to work by bicycle. Consider the following circumstances: (1) bicyclist rides a new bicycle, (2) the traffic is light, (3) bicyclist gets into an accident. How likely is it that the next bicycle commuter will fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"bicyclist rides a new bike", 
// "Y":"riding in light traffic", 
// "Z":"gets into an accident",
// "notX":"bicyclist rides a bike that's NOT new",
// "notY":"riding in traffic that's NOT light",
// "notZ":"DOESN'T get into an accident"},

// {"type":"CE-EP",
// "domain":"laptop",
// "prompt":"The librarian at the Springfield Public Library requires patrons to fill out a questionnaire whenever they are having laptop issues. Consider the following circumstances: (1) laptop computer hasn't been plugged in at all today, (2) laptop computer is new, (3) laptop battery is drained. How likely is it that the next patron has the following issues? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "X":"laptop computer wasn't plugged in at all today", 
// "Y":"the laptop is new", 
// "Z":"the laptop battery is drained",
// "notX":"laptop computer was plugged in for at least some of the day",
// "notY":"the laptop is NOT new",
// "notZ":"the laptop battery is NOT drained"}
// ]

// // justine's comments / no hint / narrative like
// var materials = 
// [{"type":"CC-EE",
// "domain":"earthquake",
// //"prompt":"The historian for the city council of Springfield records details of major natural disasters in the region. How likely is it that the next natural disaster satisfies the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"The historian for the city council of Springfield records details of major natural disasters in the region. How likely is it that the next natural disaster satisfies the following descriptions? ",
// "X":"There is a major earthquake.", 
// "Y":" The city hall collapses", 
// "Z":" and the main highway needs major repairs.",
// "notX":"There isn't a major earthquake.",
// "notY":" The city hall doesn't collapse",
// "notZ":" and the main highway isn't in need of major repairs."},

// {"type":"CC-PP",
// "domain":"fireworks",
// //"prompt":"Springfield Heights is a neighborhood for young families in the city of Springfield. How likely is it that the next group of kids playing in the neighborhood fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"Springfield Heights is a neighborhood for young families in the city of Springfield. After the 4th of July, there are leftover fireworks outside next to the community center. How likely is it that the next group of kids playing in the neighborhood fit the following descriptions?",
// "X":"The group of kids is playing with the fireworks", 
// "Y":" and the fireworks go off high in the sky.", 
// "Z":" No kid in the group gets injured.",
// "notX":"The group of kids isn't playing with the fireworks",
// "notY":" and the fireworks don't go off high in the sky.",
// "notZ":" A kid in the group gets injured."},

// {"type":"CC-EP",
// "domain":"braces",
// "prompt":"Dr. Fills is a dentist in Springfield. How likely is it that his next patient will fit the following descriptions?",
// "X":"The patient's teeth alignment is fine", 
// "Y":" and the patient has no difficulty chewing.", 
// "Z":" The patient needs braces.",
// "notX":"The patient's teeth alignment isn't fine",
// "notY":" and has the patient has difficulty chewing.",
// "notZ":" The patient doesn't need braces."},

// {"type":"CE-EE",
// "domain":"carBattery",
// "prompt":"The receptionist at Springfield Towing is in charge of recording the types of calls received. How likely is it that the next call will fit the following descriptions?",
// "X":"The car lights were left on overnight", 
// "Y":" and the car battery is old", 
// "Z":", and now the car battery is completely drained",
// "notX":"The car lights weren't left on overnight",
// "notY":" and car battery isn't old",
// "notZ":", and now the car battery isn't completely drained"},

// {"type":"CE-PP",
// "domain":"cyclist",
// "prompt":"Many residents in the city of Springfield commute to work by bicycle. How likely is it that the next bicycle commuter will fit the following descriptions?",
// "X":"The bicyclist rides a new bicycle", 
// "Y":" in light traffic", 
// "Z":" and gets into an accident",
// "notX":"The bicyclist rides a bicycle that isn't new",
// "notY":" in traffic that isn't light",
// "notZ":" and doesn't get into an accident"},

// {"type":"CE-EP",
// "domain":"laptop",
// "prompt":"The librarian at the Springfield Public Library requires patrons to fill out a questionnaire whenever they are having laptop issues. How likely is it that the next patron has the following issues?",
// "X":"The laptop computer hasn't been plugged in at all today", 
// "Y":" and is a new laptop", 
// "Z":", and now the laptop battery is drained",
// "notX":"The laptop computer was plugged in for at least some of today",
// "notY":" and isn't a new laptop",
// "notZ":", and now the laptop battery isn't drained"}
// ]


// noah's comments / no prompt / 3 phrases
// var materials = 
// [{"type":"CC-EE",
// "domain":"lightbulb",
// //"prompt":"The historian for the city council of Springfield records details of major natural disasters in the region. How likely is it that the next natural disaster satisfies the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"How likely are the following situations?",
// "X":"The lightbulb is on.", 
// "Y":" It's bright.", 
// "Z":" It's hot.",
// "notX":"The lightbulb is not on.",
// "notY":" It's not bright.",
// "notZ":" It's not hot."},

// {"type":"CC-PP",
// "domain":"berries",
// //"prompt":"Springfield Heights is a neighborhood for young families in the city of Springfield. How likely is it that the next group of kids playing in the neighborhood fit the following descriptions? [Note: it may be easiest to read through two or three of the statements at a time and judge them simultaneously.]",
// "prompt":"How likely are the following situations?",
// "X":"The berries are in the freezer.", 
// "Y":" They are soft.", 
// "Z":" They are warm.",
// "notX":"The berries aren't in the freezer.",
// "notY":" They aren't soft.",
// "notZ":" They aren't warm."},

// {"type":"CC-EP",
// "domain":"braces",
// "prompt":"How likely are the following situations?",
// "X":"The patient has normal tooth alignment.", 
// "Y":" The patient has no difficulty chewing.", 
// "Z":" The patient needs braces.",
// "notX":"The patient doesn't have normal tooth alignment.",
// "notY":" The patient has difficuty chewing.",
// "notZ":" The patient doesn't need braces."},

// {"type":"CE-EE",
// "domain":"carBattery",
// "prompt":"How likely are the following situations?",
// "X":"The car lights were left on overnight.", 
// "Y":" The car battery is old.", 
// "Z":" The car battery is completely drained in the morning.",
// "notX":"The car lights weren't left on overnight.",
// "notY":" The car battery isn't old.",
// "notZ":" The car battery isn't completely drained in the morning."},

// {"type":"CE-PP",
// "domain":"cyclist",
// "prompt":"How likely are the following situations?",
// "X":"The bicyclist rides a reliable bicycle.", 
// "Y":" The bicyclist is riding in light traffic.", 
// "Z":" The bicyclist is involved in an accident.",
// "notX":"The bicyclist rides a bicycle that isn't reliable.",
// "notY":" The bicyclist is riding in traffic that isn't light.",
// "notZ":" The bicyclist isn't involved in an accident."},

// {"type":"CE-EP",
// "domain":"laptop",
// "prompt":"How likely are the following situations?",
// "X":"The laptop computer is unplugged.", 
// "Y":" It is a new laptop.", 
// "Z":" Its batteries are drained.",
// "notX":"The laptop computer is plugged in.",
// "notY":" It isn't a new laptop.",
// "notZ":" Its batteries are not drained."}
// ]

// noah's comments / no prompt / some new domains
var materials = [
[{"condition":"plaus",
"type":"CC-EE",
"domain":"lightbulb",
"prompt":"Imagine a lightbulb. How likely is it that it: ",
"X":"is on", 
"Y":"is bright", 
"Z":"is hot",
"notX":"isn't on",
"notY":"isn't bright",
"notZ":"isn't hot"},

{"condition":"plaus",
"type":"CC-PP",
"domain":"strawberry",
"prompt":"Imagine a strawberry. How likely is it that it: ",
"X":"is in the freezer", 
"Y":"is soft", 
"Z":"is warm",
"notX":"isn't in the freezer",
"notY":"isn't soft",
"notZ":"isn't warm"},

{"condition":"plaus",
"type":"CC-EP",
"domain":"tomatoplant",
"prompt":"Imagine a tomato plant. How likely is it that it: ",
"X":"receives direct sunlight", 
"Y":"grows tall", 
"Z":"bears healthy fruit",
"notX":"doesn't receive direct sunlight",
"notY":"doesn't grow tall",
"notZ":"doesn't bear healthy fruit"},

{"condition":"plaus",
"type":"CE-EE",
"domain":"painting",
"prompt":"Imagine a painting. How likely is it that it: ",
"X":"receives direct sunlight", 
"Y":"is new", 
"Z":"is faded",
"notX":"doesn't receive direct sunlight",
"notY":"isn't new",
"notZ":"isn't faded"},

{"condition":"plaus",
"type":"CE-PP",
"domain":"cracker",
"prompt":"Imagine a cracker. How likely is it that it: ",
"X":"is soggy", 
"Y":"is past expiration date", 
"Z":"has lots of flavor",
"notX":"isn't soggy",
"notY":"isn't past expiration date",
"notZ":"doesn't have lots of flavor"},

{"condition":"plaus",
"type":"CE-EP",
"domain":"knife",
"prompt":"Imagine a knife. How likely is it that it: ",
"X":"is sharp", 
"Y":"is rusty", 
"Z":"cuts well",
"notX":"isn't sharp",
"notY":"isn't rusty",
"notZ":"doesn't cut well"}],

[{"condition":"freq",
"type":"CC-EE",
"domain":"lightbulb",
"prompt":"Imagine 100 lightbulbs. About how many of them: ",
"X":"are on", 
"Y":"are bright", 
"Z":"are hot",
"notX":"aren't on",
"notY":"aren't bright",
"notZ":"aren't hot"},

{"condition":"freq",
"type":"CC-PP",
"domain":"strawberry",
"prompt":"Imagine 100 strawberries. About how many of them: ",
"X":"are in the freezer", 
"Y":"are soft", 
"Z":"are warm",
"notX":"aren't in the freezer",
"notY":"aren't soft",
"notZ":"aren't warm"},

{"condition":"freq",
"type":"CC-EP",
"domain":"tomatoplant",
"prompt":"Imagine 100 tomato plants. About how many of them: ",
"X":"receive direct sunlight", 
"Y":"grow tall", 
"Z":"bear healthy fruit",
"notX":"don't receive direct sunlight",
"notY":"don't grow tall",
"notZ":"don't bear healthy fruit"},

{"condition":"freq",
"type":"CE-EE",
"domain":"painting",
"prompt":"Imagine 100 paintings. About how many of them: ",
"X":"receive direct sunlight", 
"Y":"are new", 
"Z":"are faded",
"notX":"don't receive direct sunlight",
"notY":"aren't new",
"notZ":"aren't faded"},

{"condition":"freq",
"type":"CE-PP",
"domain":"cracker",
"prompt":"Imagine 100 crackers. About how many of them: ",
"X":"are soggy", 
"Y":"are past expiration date", 
"Z":"have lots of flavor",
"notX":"aren't soggy",
"notY":"aren't past expiration date",
"notZ":"don't have lots of flavor"},

{"condition":"freq",
"type":"CE-EP",
"domain":"knife",
"prompt":"Imagine 100 knives. About how many of them: ",
"X":"are sharp", 
"Y":"are rusty", 
"Z":"cut well",
"notX":"aren't sharp",
"notY":"aren't rusty",
"notZ":"don't cut well"}]

]



var condition = Math.floor(Math.random()*2);

var trials_shuf = jsPsych.randomization.repeat(materials[condition],1);
var total_trials = trials_shuf.length;
var all_trials = trials_shuf.map(function (m) 
    {return [m.X + ', '+ m.Y + ', ' + m.Z,
    m.notX + ', ' + m.Y + ', ' + m.Z,
    m.X + ', ' + m.notY + ', ' + m.Z,
    m.X + ', ' + m.Y + ', ' + m.notZ,
    m.notX + ', ' + m.notY + ', ' + m.Z,
    m.X + ', ' + m.notY + ', ' + m.notZ,
    m.notX + ', ' + m.Y + ', ' + m.notZ,
    m.notX + ', ' + m.notY + ', ' + m.notZ
            ]});


/* shuffle order of situation-sliders 
 maintain same order in all trials (all_trials.map)
 shuffle states array to track correct label*/
var states = ["XYZ","nXYZ","XnYZ","XYnZ","nXnYZ","XnYnZ","nXYnZ","nXnYnZ"]

var i=-1, len= states.length, next, order=[];

// irregular shuffling of sliders
// i suspect this will make it easier on the subjects
// maintain the total ordering of 3 properties > 2 properties > 1 property > 0 props
// shuffle order of 2 properties and 1 property situations
// var twofer=[],thrfer=[];
// var twofer = jsPsych.randomization.repeat(range(len).slice(1,4),1);
// var thrfer = jsPsych.randomization.repeat(range(len).slice(4,7),1);
// order = order.concat(0,twofer,thrfer,7);

// regular shuffling of sliders
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

//var scale = [ "0", "25","50" ,"75","100"];
if (condition == 0){
    var scale = ["Impossible", "&larr;less likely","more likely&rarr;", "Certain"];
}
else{
    var scale = ["0", "25","50","75","100"];
    var scale = ["0", "&larr;fewer", "more&rarr;","100"];
}

//var scale = ["&larr; less probable","more probable &rarr;"]

var all_scales = fillArray(fillArray(scale,all_trials[1].length),total_trials)
var all_intervals = fillArray(fillArray(100,all_trials[1].length),total_trials)
var all_prompts = trials_shuf.map(function(m) {return [m.prompt]});
var all_orders = fillArray(states,total_trials)
var all_domains = trials_shuf.map(function(m) {return [m.domain]});

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
        alert("Please enter your native language.");
        return false;
    }
    else {
        return true;
    }
    return false;
};

var test_block = 
{type: "erin-slider", 
condition: condition,
questions: all_trials,
labels: all_scales,
intervals: all_intervals,
question_order: all_orders,
domains: all_domains,
show_ticks: false,
text: all_prompts,
hide_handle: true,
orientation: "horizontal"
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


if (condition==0){
    instr_text = "<p>In this experiment, you will be asked to imagine a particular object. You will be asked to consider three aspects of the object and rate how plausible they are.</p>"+
    "<p>To rate the plausibility, just click the slider bar. Once you have clicked, you may adjust your answer simply by clicking anywhere else on the slider.</p>"+
    "Press any key to begin."
}
else{
    instr_text = "<p>In this experiment, you will be asked to imagine 100 objects of a particular kind. You will be asked to consider three aspects of the object and rate how many of each there are.</p>"+
    "<p>To rate the quantity, just click the slider bar. Once you have clicked, you may adjust your answer simply by clicking anywhere else on the slider.</p>"+
    "Press any key to begin."
}


var instructions_block = {
    type: "text",
    text: instr_text
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

var finished_block = 
            {type:'text', 
            text: "You're finished -- thank you for participating! Submitting to Mechanical Turk... Press any key to complete"};

/* define experiment structure */

var experiment_blocks = [];

experiment_blocks.push(consent_block);
// // //experiment_blocks.push(welcome_block);
experiment_blocks.push(instructions_block);
experiment_blocks.push(test_block);
experiment_blocks.push(debrief_block);
experiment_blocks.push(questionnaire_block);
experiment_blocks.push(finished_block);

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





