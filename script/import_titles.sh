#!/bin/sh

export LC_ALL=C
export DATADIR=../data;
export OUTPUTDIR=../output;

# grab the latest category file
curl -L "http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz" | \

# unzip it
gunzip | \

# replace the Wikipedia underscores with spaces
sed 's/_/ /g' | \

# get rid of terms starting with non-english characters, paranthesis, whitespace, etc...
egrep '^[a-zA-Z0-9]' | \

# normalize accented characters for search (should do this on the lookup side too!)
./strip_accent.py | sort > $OUTPUTDIR/enwiki-latest-title.txt

