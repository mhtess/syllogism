#!/usr/bin/env sh

HERE=`pwd`
cd $MTURK_CMD_HOME/bin

if [ ! -z $1 ]
then
	NAME_OF_EXPERIMENT_FILES=$1
	if [ ! -z $2 ]
	then
		DIRECTORY=$HERE
	else
		DIRECTORY=$2
	fi
	label=$HERE/$DIRECTORY/$NAME_OF_EXPERIMENT_FILES
	./getResults.sh -successfile $label.success -outputfile $label.results
else
	echo "ERROR: please include name of experiment files"
fi