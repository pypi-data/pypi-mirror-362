#!/bin/bash
#
# This script sets all necessary version-number information across
# FastJet (including doxygen and manual). It should be run from the
# top-level fastjet-release directory.
#

if [ $# -ne 1 ]
then
 echo "Usage: scripts/set-version.sh version-number"
 exit
fi

version=$1
versionNumber=`echo $version | sed 's/-.*//'`
# if there is a dash in the version number, take everything afterwards
# for versionPreRelease, otherwise set versionPreRelease to an empty string
if echo $version | grep -q '-'
then
  versionPreRelease=$(echo $version | sed 's/.*-/-/')
else
  versionPreRelease=""
fi


echo "------------ Will set FastJet version to $version -----------" 
echo "versionNumber = $versionNumber"
echo "versionPreRelease = $versionPreRelease"

echo
echo "------------ Setting it in CMakeLists.txt -------------------"
sed -i.bak 's/^project.FastJet VERSION [0-9.]*/project(FastJet VERSION '$versionNumber'/' CMakeLists.txt
sed -i.bak 's/^set.PROJECT_VERSION_PRERELEASE.*/set(PROJECT_VERSION_PRERELEASE "'$versionPreRelease'")/' CMakeLists.txt
diff CMakeLists.txt.bak CMakeLists.txt

echo
echo "------------ Setting it in configure.ac ---------------------"
#sed -i.bak 's/\(AC_INIT.*\)])/\1-'$extralabel'])/' configure.ac
sed -i.bak 's/^\(AC_INIT(\[.*\],\[\).*/\1'$version'])/' configure.ac
diff configure.ac.bak configure.ac 
#AC_INIT([FastJet],[3.0.2-devel])

# now make sure the windows config file is consistent
echo
echo "------------ Setting it in include/fastjet/config_win.h -----"
cp -p include/fastjet/config_win.h include/fastjet/config_win.h.bak
cd src
./genconfig.sh ../include/fastjet/config_win.h
cd ..
diff include/fastjet/config_win.h.bak include/fastjet/config_win.h 

echo
echo "------------ Setting it in Doxyfile -------------------------"
sed -i.bak 's/^\(PROJECT_NUMBER.*=\).*/\1 '$version'/' Doxyfile
diff Doxyfile.bak Doxyfile


echo
echo "------------ Setting it in doc/fastjet-doc.tex --------------"
sed -i.bak 's/^\( *\)[^%]*\(%.*VERSION-NUMBER.*\)/\1'$version'\2/' doc/fastjet-doc.tex
diff doc/fastjet-doc.tex.bak doc/fastjet-doc.tex

echo
echo "------------ Recommended ChangeLog entry --------------------"
# NB: -e option of echo ensures that \t translates to a tab character
echo -e "\t* configure.ac:"
echo -e "\t* include/fastjet/config_win.h:"
echo -e "\t* Doxyfile:"
echo -e "\t* tex/fastjet-doc.tex:"
echo -e "\t  changed version to $version"
