#!/bin/bash

#-- main part of configuration
#nev=1000
nev=1000
#nev=10
inputfile=~/work/fastjet/data/Pythia-PtMin50-LHC-1000ev.dat
#command="./fastjet_timing -write -nev $nev"
command="./fastjet_timing -unique_write -cam -nev $nev"
#---------------------------

tmpbase=tmp-$$

# create a reference file
strategy=-3
echo Base command is: $command
echo Reference strategy is $strategy, number of events is $nev
reffile=$tmpbase-$strategy
$command -strategy $strategy < $inputfile | grep -v strategy > $reffile


#for strategy in -04 -02 -01 +02 +03 +04 +00 +12 +13 +14
#for strategy in -04 -02 -01 +02 +03 +04 +00
for strategy in -04 +12
#for strategy in -2 -1 +2 +3 +4 +0
#for strategy in +12 +13 +14
#for strategy in -04
do
  echo -n "Strategy $strategy ... "
  thisfile=$tmpbase-$strategy
  $command -strategy $strategy < $inputfile  | grep -v strategy > $thisfile
  echo -n "Number of differences is: "
  diff $thisfile $reffile | wc -l
  rm $thisfile
done

rm $reffile
