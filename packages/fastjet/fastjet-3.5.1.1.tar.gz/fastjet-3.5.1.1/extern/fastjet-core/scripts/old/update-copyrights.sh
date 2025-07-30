#!/bin/zsh
# script to update all copyright strings.
# Run it from the main directory

# get parameters
if [[ x`uname` == xDarwin ]];
then
    inplace=(-i .bak)
else
    inplace=(-i.bak)
fi
year=`date +%Y`


echo inplace is $inplace
echo year is $year


sedstring='s/\/\/ *Copyright .*Matteo Cacciari.*/\/\/ Copyright \(c\) 2005-'$year', Matteo Cacciari, Gavin P. Salam and Gregory Soyez/'

# check that things look sensible
echo New copyright string is
sed  $sedstring src/ClusterSequence.cc | grep Copyright

# go ahead with the copyright change
echo "Do you wish to change all copyright strings?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) 
            sed $
            echo about to proceed; 
            echo proceeding; 
            break;;
        No ) exit;;
    esac
done
