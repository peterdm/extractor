#!/bin/sh

export LC_ALL=C
export DATADIR=../data;
export OUTPUTDIR=../output;

# grab the latest category file
curl -L "http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-category.sql.gz" | \

# unzip it
gunzip | \

# convert SQL inserts to tsv (https://github.com/fizx/redump)
redump/redump | \

# grab only the column containing the text strings
cut -f 2 | \

# replace the Wikipedia underscores with spaces
sed 's/_/ /g' | \

# get rid of terms starting with non-english characters, paranthesis, whitespace, etc...
egrep '^[a-zA-Z0-9]' | \

# normalize accented characters for search (should do this on the lookup side too!)
./strip_accent.py > $OUTPUTDIR/enwiki-latest-category.txt

# grams will create seperate files for 1-grams, 2-grams, 3-grams, 4-grams
./grams.sh
