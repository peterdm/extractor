#!/bin/sh

export LC_ALL=C;
export OUTPUTDIR=../output;

for i in {1..5}
do
   cat $OUTPUTDIR/enwiki-latest-category.txt | \
   
   # seperate out all terms composed of i-word-grams
   awk -v i=$i 'NF==i {print $0}' | \

   # sort them
   sort > $OUTPUTDIR/$i-grams.txt
done

