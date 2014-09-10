#!/usr/bin/env python

import os
import sys
import json
import re

def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        print "reading config file: " + config_file
        if len(sys.argv) > 2:
            output_dir = sys.argv[2]
            print "saving files in: " + output_dir
        else:
            print "saving files in current directory"
            output_dir = ""
    else:
        print "ERROR: please give the name of your config file"
        return False

    # config_file = sys.argv[1]
    # output_dir = sys.argv[2]

    settings = open(config_file, 'r')
    json_string = settings.read()
    settings.close()
    dict = json.loads(re.sub("\n", "", json_string))

    locationofCLT = os.environ['MTURK_CMD_HOME']
    # dict={}
    # for line in lines:
    #     if not (line == "\n" or line == ""):
    #         while (line[0] == "\n" or line[0] == "\t" or line[0] == " "):
    #             line = line[1:]
    #         if not (line[0:3] == "###"):
    #             x=line.split("::")
    #             key = x[0]
    #             possvalues = x[1].split("###")
    #             value = possvalues[0]
    #             while (key[0] == "\n" or key[0] == "\t" or key[0] == " "):
    #                 key = key[1:]
    #             while (key[-1] == "\n" or key[-1] == "\t" or key[-1] == " "):
    #                 key = key[:-1]
    #             while (value[0] == "\n" or value[0] == "\t" or value[0] == " "):
    #                 value = value[1:]
    #             while (value[-1] == "\n" or value[-1] == "\t" or value[-1] == " "):
    #                 value = value[:-1]
    #             dict[x[0]] = value

    if not os.path.exists(locationofCLT) or locationofCLT == '/':
        raise Exception("Error: please set your 'MTURK_CMD_HOME' environment variable to your AWS directory.")

    if dict["rewriteProperties"] == "yes":
        old_properties_file = open(locationofCLT + "/bin/mturk.properties", 'r').readlines()
        backup = open(locationofCLT + "/bin/mturk.properties.backup", 'w')
        for line in old_properties_file:
            backup.write(line + '\n')
        backup.close()
        new_properties_file = open(locationofCLT + "/bin/mturk.properties", 'w')
        if (dict["liveHIT"] == "yes"):
            for line in old_properties_file:
                if "://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
                    new_properties_file.write("# service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
                elif "://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
                     new_properties_file.write("service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
                else:
                    new_properties_file.write(line)
        else:
            for line in old_properties_file:
                if "://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
                    new_properties_file.write("service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
                elif "://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
                    new_properties_file.write("# service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
                else:
                    new_properties_file.write(line)
        new_properties_file.close()
        print "Old mturk.properties file backed up at " + locationofCLT + "/bin/mturk.properties.backup" 

    # write the .question file, which tells MTurk where to find your external HIT.
    question = open(output_dir + dict["nameofexperimentfiles"] + ".question", 'w')
    question.write("<?xml version='1.0'?><ExternalQuestion xmlns='http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd'><ExternalURL>" + dict["experimentURL"] + "</ExternalURL><FrameHeight>"+ dict["frameheight"] +"</FrameHeight></ExternalQuestion>")
    question.close()

    #write the .properties file.
    properties = open(output_dir + dict["nameofexperimentfiles"] + ".properties", 'w')
    properties.write("title: " + dict["title"] + "\ndescription: " + dict["description"] + "\nkeywords: " + dict["keywords"] + "\nreward: " + dict["reward"] + "\nassignments: " + dict["numberofassignments"] + "\nannotation: ${condition}\nassignmentduration:" + dict["assignmentduration"] + "\nhitlifetime:" + dict["hitlifetime"] + "\nautoapprovaldelay:" + dict["autoapprovaldelay"])
    if (dict["USonly?"] == "y" or dict["USonly?"] == "Y" or dict["USonly?"] == "yes" or dict["USonly?"] == "Yes" or dict["USonly?"] == "true" or dict["USonly?"] == "True" or dict["USonly?"] == "T" or dict["USonly?"] == "1"):
        properties.write("\nqualification.1:00000000000000000071\nqualification.comparator.1:EqualTo\nqualification.locale.1:US\nqualification.private.1:false")
    if (dict["minPercentPreviousHITsApproved"] != "none"):
        properties.write("\nqualification.2:000000000000000000L0\nqualification.comparator.2:GreaterThanOrEqualTo\nqualification.value.2:" + dict["minPercentPreviousHITsApproved"] + "\nqualification.private.2:false")
    properties.close()

    #write the .input file. "conditions::" in the file experiment-settings.txt can be followed by any number of condition names, separated by a comma.
    input = open(output_dir + dict["nameofexperimentfiles"] + ".input", 'w')
    input.write("condition\n")
    num = 1
    conditions = dict["conditions"]
    conditionlist = conditions.split(",")
    for x in conditionlist:
        input.write(str(num) + " " + x + " \n")
        num = num + 1
    input.close()

main()