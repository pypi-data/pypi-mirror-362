#!/bin/bash
#
# Script to update the version number in the locations where it is
# hard-coded.
#
# Usage:
#   ./setversion.sh <number>
# The version number will be read from configure.ac


if [ $# -ne 1 ]
then
 echo "Usage: scripts/set-version.sh version-number"
 exit
fi

version=$1
echo "------------ Will set SISCone version to $version -----------" 

echo
echo "------------ Setting it in configure.ac ---------------------"
sed -i.bak 's/^\(AC_INIT(\[.*\], \[\).*/\1'$version'])/' configure.ac
diff configure.ac.bak configure.ac 

echo
echo "----------- Setting it in CMakeLists.txt --------------------"
version_base=${version%%-*}
version_extra=${version#${version_base}}
sed -i.bak 's/^\(project(SISCone VERSION \).*/\1'$version_base' LANGUAGES CXX)/;s/^\(set(PROJECT_VERSION_PRERELEASE "\).*/\1'$version_extra'")/' CMakeLists.txt
diff CMakeLists.txt.bak CMakeLists.txt

echo
echo "------------ Setting it in Doxyfile -------------------------"
sed -i.bak 's/^\(PROJECT_NUMBER.*=\).*/\1 '$version'/' Doxyfile
diff Doxyfile.bak Doxyfile

echo
echo "------------ Setting it in documentation---------------------"
for fn in algorithm.html download.html index.html perfs.html sm_issue.html usage.html; do
    sed -i.bak 's/Version .*</Version '$version'</' doc/html/${fn}
    diff doc/html/${fn}.bak doc/html/${fn}
done

echo
echo "------------ Recommended ChangeLog entry --------------------"
# NB: -e option of echo ensures that \t translates to a tab character
echo -e "\t* configure.ac:"
echo -e "\t* CMakeLists.txt:"
echo -e "\t* Doxyfile:"
echo -e "\t* doc/html/*.html:"
echo -e "\tchanged version to $version"


