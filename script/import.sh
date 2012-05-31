#!/bin/sh

export LC_ALL=C
export DATADIR=../data;
export OUTPUTDIR=../output;

( ./import_titles.sh ; ./import_categories.sh ) | \

# sort and dedupe
sort | uniq > $OUTPUTDIR/dictionary.txt
