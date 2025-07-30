#!/bin/bash
#
# Script to create fjcore from the current (configured) version
# of the code
# It must be run from the scripts/ directory inside the main fastjet directory
#
# 

scriptsdir=$PWD
cmakebuild=$scriptsdir/build-fjcore
fjdir=$PWD/..

# set up some colours for headers, errors
RED='\033[0;31m'
GREEN='\033[0;32m'
BOLD='\033[1m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
ERROR="${RED}ERROR:${NC}"
function header() { 
  echo -e "\n======================================================================"
  echo -e "${BOLD}$1${NC}\n";
  }
function error()  { echo -e "\n${ERROR} $1 ${NC}\n"; exit 1;}


# check that we are in the scripts directory by looking to see if the the
# mkfjcore.sh script is in this directory
if [[ ! -f $scriptsdir/mkfjcore.sh ]]; then
  error "This script must be run from the scripts/ directory of a fastjet clone"
fi

# run cmake with specific options so as to generate the config file
header "Using cmake to generate config file"
if [[ -d ${cmakebuild} ]]; then
  error "A previous ${cmakebuild} directory exists. Exiting."
fi
cmake -S .. -B build-fjcore -DFASTJET_HAVE_THREAD_SAFETY=OFF -DFASTJET_HAVE_LIMITED_THREAD_SAFETY=OFF \
      || error "CMake failed"

# extra info we need from the cmake build
configauto=${cmakebuild}/include/fastjet/config_auto.h
version=$(grep "FASTJET_PACKAGE_VERSION" ${configauto} | sed 's/.*VERSION "//;s/".*$//') \
 || error "could not deduce FastJet version"
cxxstd=c++$(grep "set.CMAKE_CXX_STANDARD " $fjdir/CMakeLists.txt | sed 's/.*CXX_STANDARD *//;s/[^0-9]$//') \
 || error "could not deduce C++ standard used by FastJet"

echo -e "${BOLD}FastJet version: ${YELLOW}$version${NC}, to be built with C++ standard: ${YELLOW}${cxxstd}${NC}"
buildflags="-std=$cxxstd -Wall -Woverloaded-virtual -pedantic -Wextra -Wshadow -O2 -g"
#-Wl,--enable-new-dtags 

# directory where to create the fjcore directory and the tarball at 
# the end of the extraction process, passed as first argument from
# command line ($1). This directory will have been created by something else.
# An empty argument does nothing, and the fjcore directory is created in scripts/
if [[ ! x$1 = 'x' ]]; then
   cd $1
fi

# create fjcore directory, move into it
mkdir fjcore-$version || { error "A previous fjcore-$version exists. Exiting."; }
cd fjcore-$version

# 2016-03-03: GS Note: we could in principle simply add these as
# internal/whatever.hh to the "fastjet_headers" list below
fastjet_headers="\
  config.h\
  internal/base.hh\
  internal/thread_safety_helpers.hh\
  internal/numconsts.hh\
  internal/IsBase.hh\
  internal/deprecated.hh\
  SharedPtr.hh\
  LimitedWarning.hh\
  Error.hh\
  PseudoJetStructureBase.hh\
  PseudoJet.hh\
  FunctionOfPseudoJet.hh\
  Selector.hh\
  JetDefinition.hh\
  CompositeJetStructure.hh\
  ClusterSequenceStructure.hh\
  ClusterSequence.hh\
  NNBase.hh\
  NNH.hh"

internal_sources="version.hh\
  internal/ClusterSequence_N2.icc\
  internal/DynamicNearestNeighbours.hh\
  internal/SearchTree.hh\
  internal/MinHeap.hh\
  internal/ClosestPair2DBase.hh\
  internal/ClosestPair2D.hh\
  internal/LazyTiling9Alt.hh\
  internal/LazyTiling9.hh\
  internal/LazyTiling25.hh\
  internal/TilingExtent.hh"

fastjet_sources="ClosestPair2D.cc\
  ClusterSequence.cc\
  ClusterSequence_CP2DChan.cc\
  ClusterSequence_Delaunay.cc\
  ClusterSequence_DumbN3.cc\
  ClusterSequence_N2.cc\
  ClusterSequenceStructure.cc\
  ClusterSequence_TiledN2.cc\
  CompositeJetStructure.cc\
  Error.cc\
  FunctionOfPseudoJet.cc\
  JetDefinition.cc\
  LimitedWarning.cc\
  MinHeap.cc\
  PseudoJet.cc\
  PseudoJetStructureBase.cc\
  Selector.cc\
  LazyTiling25.cc\
  LazyTiling9.cc\
  LazyTiling9Alt.cc\
  TilingExtent.cc"


# create the directory structure
mkdir include
mkdir include/fastjet
mkdir include/fastjet/internal
mkdir src

# copy the internal headers, headers and sources
header "Copying FastJet headers and sources"
cp $configauto include/fastjet/ || error "Could not copy config_auto.h"

echo "copying internal headers" 
# for hh in $internal_headers; do
#     cp $fjdir/include/fastjet/internal/$hh include/fastjet/internal/
# done
# echo "copying FastJet headers"
for hh in $fastjet_headers; do
    cp $fjdir/include/fastjet/$hh include/fastjet/$hh || error "Could not copy $hh"
done
echo "copying internal sources"
for icc in $internal_sources; do
    cp $fjdir/include/fastjet/$icc include/fastjet/$icc || error "Could not copy $icc"
done
echo "copying FastJet sources"
for cc in $fastjet_sources; do
    cp $fjdir/src/$cc src/ || error "Could not copy $cc"
done

# create a rough Makefile (for testing)
header "creating a temporary Makefile for testing"
TAB="$(printf '\t')"

cat >Makefile <<EOF
all:
${TAB}@cd src && \$(MAKE)
clean:
${TAB}@cd src && \$(MAKE) clean
EOF

cat >src/Makefile <<EOF
SRCS = $fastjet_sources
OBJS =  \$(patsubst %.cc,%.o,\$(SRCS))
CFLAGS = ${buildflags} -D__FASTJET_ONLY_CORE__ -I../include

%.o: %.cc
${TAB}g++ -c \$(CFLAGS) \$<

all: \$(OBJS) 
${TAB}ar cru libfjcore.a \$(OBJS)
${TAB}ranlib libfjcore.a

clean:
${TAB}rm -f *~ *.o
EOF

# try to build the library
header "building the extracted code"
make -j || error "Failed to build" 
    

# then, for each header, try to include it and build it against the lib
header "checking individual headers"
for hh in $fastjet_headers; do
    echo $hh
    if [[ "$hh" == "version.hh" ]]; then
	echo "Skipped"
	continue;
    fi
    cat >tmp.cc <<EOF
#include "include/fastjet/${hh}"

int main(){
  return 0;
}
EOF
    g++ -Lsrc -lfjcore -I. -Iinclude ${buildflags} -D__FASTJET_ONLY_CORE__ tmp.cc  || error "Failed to build with $hh"
done
# a.out* is needed on mac because mac creates a bunch of a.out* directories and files
rm -r tmp.cc a.out*

# now merge everything in a single header and a single source
#echo "======================================================================"
header "Merging all the files into fjcore.hh and fjcore.cc"
echo "Creating basic header"
cat >fjcore.hh <<EOF
#ifndef __FJCORE_HH__
#define __FJCORE_HH__

#define __FJCORE_ONLY_CORE__  // remove all the non-core code (a safekeeper)
#define DROP_CGAL    // disable CGAL support

EOF

# for hh in $internal_headers; do
#     cat include/fastjet/internal/$hh >> fjcore.hh
# done

echo "Merging the headers into fjcore.hh"
cat $configauto >> fjcore.hh || error "Could not copy config_auto.h to fjcore.hh"
rm -rf ${cmakebuild} # should no longer be needed
for hh in $fastjet_headers; do
    cat include/fastjet/$hh >> fjcore.hh || error "Could not copy $hh to fjcore.hh"
done

echo "#endif" >> fjcore.hh

# copy the source
echo; echo "Merging all the sources into fjcore.cc"
cat >fjcore.cc <<EOF
#include "fjcore.hh"
EOF

for icc in $internal_sources; do
    cat include/fastjet/$icc >> fjcore.cc || error "Could not copy $icc to fjcore.cc"
done

for cc in $fastjet_sources; do
    cat src/$cc >> fjcore.cc || error "Could not copy $cc to fjcore.cc"
done

# add the string "[fjcore]" to fastjet version number in function
# returning it and in banner
# VERY fragile replacement!
sed \
  -e 's/return "FastJet version "+string(fastjet_version)/return "FastJet version "+string(fastjet_version)+" [fjcore]"/' \
  -e 's/    FastJet release " << fastjet_version/FastJet release " << fastjet_version << " [fjcore]"/' \
  fjcore.cc > fjcore.cc.tmp
mv fjcore.cc.tmp fjcore.cc 


echo; echo "Cleaning the #include directives"
for pattern in $fastjet_headers $internal_sources fastjet/config_auto.h ; do
    grep -v "include.*$pattern" fjcore.hh > tmp
    mv tmp fjcore.hh
    grep -v "include.*$pattern" fjcore.cc > tmp
    mv tmp fjcore.cc
done

echo; echo "Cleaning the resulting files:"
wc -cl fjcore.{hh,cc}
echo "  - removing ifdef'ed code"
for fn in fjcore.hh fjcore.cc; do
    awk 'BEGIN{level=0;outcore=0;elsecore=0}{if (NF==0){next;} if ($1~/^#if/){level=level+1} if ($1=="#ifndef" && $2=="__FASTJET_ONLY_CORE__"){outcore=level} if (outcore==0){print $0} if ($1~/^#endif/){ if (level==outcore){elsecore=0;outcore=0} level=level-1}  if (elsecore==1){ print $0} if ($1~/^#else/ && level==outcore){elsecore=1}}' $fn > tmp
    mv tmp $fn
done
wc -cl fjcore.{hh,cc}
echo "  - removing comment lines and the plugin enable tags"
# GPS: on macs sed has a different command line (and there's
#      no way of writing a line that's compatible with macs and linux)
#      so just use a simple copy and move
#     remove //... comments              remove plugin enable tags                remove /* ... */ comments         remove multiline /* ... */ comments
#                                                                                  (single-line only first,
#                                                                            only lines with comment exclusively)                          
#
sed '/^ *\/\/.*$/d' fjcore.hh | sed '/^#ifndef FASTJET_ENABLE_PLUGIN/,/#endif.*$/d'| sed '/^\s*\/\*.*\*\/\s*$/d' | sed '/^\s*\/\*/,/\*\/\s*$/d' > fjcore.hh.nocomments
sed '/^ *\/\/.*$/d' fjcore.cc | sed '/^#ifndef FASTJET_ENABLE_PLUGIN/,/#endif.*$/d'| sed '/^\s*\/\*.*\*\/\s*$/d' | sed '/^\s*\/\*/,/\*\/\s*$/d' > fjcore.cc.nocomments
# further removal of ifndef WIN32 block from fjcore.hh (nothing similar in .cc)
# (this effectively removes the whole of config.h, which however was needed 
# during the initial compilation tests)
sed '/^#ifndef WIN32/,/#endif.*$/d' fjcore.hh.nocomments > fjcore.hh
# removal of "#define FASTJET_HAVE_EXECINFO 1" line from fjcore.hh. 
# Guards are instead kept, because they are used in Error.hh|cc
sed '/^#define FASTJET_HAVE_EXECINFO_H.*$/d' fjcore.hh > fjcore.hh.tmp; mv fjcore.hh.tmp fjcore.hh
# same story for a bunch of other compiler-related flags
sed '/^#define FASTJET_HAVE_AUTO_PTR_INTERFACE.*$/d;/^#define FASTJET_HAVE_DEMANGLING_SUPPORT.*$/d;/^#define FASTJET_HAVE_OVERRIDE.*$/d;/^#define FASTJET_HAVE_GNUCXX_DEPRECATED.*$/d;/^#define FASTJET_HAVE_CXX14_DEPRECATED.*$/d;/^#define FASTJET_HAVE_EXPLICIT_FOR_OPERATORS.*$/d' fjcore.hh > fjcore.hh.tmp; mv fjcore.hh.tmp fjcore.hh


# renaming and removal of unnecessary files
rm fjcore.hh.nocomments
mv fjcore.cc.nocomments fjcore.cc
wc -cl fjcore.{hh,cc}

echo; echo "Renaming the fastjet namespace to fjcore"
sed 's/namespace fastjet/namespace fjcore/g' fjcore.hh > tmp$$
mv tmp$$ fjcore.hh
for fn in fjcore.hh fjcore.cc; do
  # replace fastjet namespace with fjcore one 
  # replace all other __FASTJET guards with __FJCORE ones, to avoid interfering with 
  # a possible run with also the "real" fastjet linked together;
  # we also rename the FASTJET_PACKAGE lines (etc. from configure) -> FJCORE_PACKAGE
  sed -e 's/fastjet::/fjcore::/g' \
      -e 's/FASTJET_BEGIN_NAMESPACE/FJCORE_BEGIN_NAMESPACE/g' \
      -e 's/FASTJET_END_NAMESPACE/FJCORE_END_NAMESPACE/g' \
      -e 's/__FASTJET/__FJCORE/g' \
      -e 's/define FASTJET/define FJCORE/g' \
      -e 's/define _FASTJET/define _FJCORE/g' \
      -e 's/ifdef FASTJET/ifdef FJCORE/g' \
      -e 's/ifdef _FASTJET/ifdef _FJCORE/g' \
      -e 's/ifndef FASTJET/ifndef FJCORE/g' \
      -e 's/ifndef _FASTJET/ifndef _FJCORE/g' \
      -e 's/DROP_CGAL/__FJCORE_DROP_CGAL/g' \
      -e 's/FASTJET_PACKAGE/FJCORE_PACKAGE/g' \
      -e 's/FASTJET_HAVE/FJCORE_HAVE/g' \
      -e 's/FASTJET_STDC/FJCORE_STDC/g' \
      -e 's/FASTJET_LT/FJCORE_LT/g' \
      -e 's/FASTJET_OVERRIDE/FJCORE_OVERRIDE/g' \
      -e 's/FASTJET_DEPRECATED/FJCORE_DEPRECATED/g' \
      -e 's/FASTJET_VERSION/FJCORE_VERSION/g' \
      -e 's/INCLUDE_FASTJET_CONFIG/INCLUDE_FJCORE_CONFIG/g' \
      -e 's/FASTJET_WINDLL/FJCORE_WINDLL/' \
      -e 's/FASTJET_TOOLS_WINDLL/FJCORE_WINDLL/' \
      -e 's/FASTJET_PLUGINS_WINDLL/FJCORE_WINDLL/' \
      -e 's/fastjet_EXPORTS/fjcore_EXPORTS/g' \
      -e 's/fastjettools_EXPORTS/fjcore_EXPORTS/g' \
      -e 's/fastjetplugins_EXPORTS/fjcore_EXPORTS/g' \
       $fn \
       > tmp$$
  mv tmp$$ $fn
  #sed 's/FASTJET_END_NAMESPACE/FJCORE_END_NAMESPACE/g' tmp$$ > $fn
  #sed 's/__FASTJET/__FJCORE/g' $fn > tmp$$
  #mv tmp$$ $fn  
done


# add preamble to fjcore.hh|cc (if done earlier, it gets canceled by comments 
# removal)
# Also put it into a README file
echo; echo "Including preamble with appropriate version number"
for i in cc hh; do
  cat $scriptsdir/preamble-fjcore.txt fjcore.$i > tmp$$
  sed "s/--FJVERSION--/$version/" tmp$$ > fjcore.$i
done
rm tmp$$
sed "s/--FJVERSION--/$version/" $scriptsdir/preamble-fjcore.txt > README

# now testing the final product by compiling the examples
header "Now compiling and running examples for checking:"
echo "  CC [fjcore.cc]"
time g++ -c ${buildflags} fjcore.cc
echo
for idx in 01 02 04 05 08 09 10; do
    fname=$(ls $fjdir/example/$idx-*.cc)
    fname=${fname##*/}

    # get the example
    cat $fjdir/example/$fname | 
             sed 's/fastjet::/fjcore::/g' | \
             sed 's/namespace fastjet/namespace fjcore/g' | \
	     sed 's/\/\/FJENDHEADER/#include "fjcore.hh"/;s/^#include "fastjet\/.*$//g' > $fname

    echo "  CC   [$fname]"
    g++ -c ${buildflags} $fname || { echo "Failed."; exit 1; }
    echo "  LD   [${fname%.cc}]"
    # GPS: removed -g from the following line, which was generating .dSYM 
    #      debugging symbol directories on a mac
    g++ -o ${fname%.cc} ${fname%cc.o} fjcore.o -lm || { echo "Failed."; exit 1; }
    echo "  CHK  [${fname%.cc}] --- currently unimplemented"
    if [[ $idx == "01" ]]; then
      echo "The banner is "
      echo
      ./${fname%.cc} < $fjdir/example/data/single-event.dat | grep '^#'
      echo
    fi
    if [ $idx -ne "01" ]; then # keep 01-basic example, to distribute
        rm ${fname%.cc}* 
    fi
done
    

# remove the temporary files
header "Cleaning unnecessary files"
rm -Rf src include Makefile *.o
rm -Rf 01-basic # left over from rm above

# Add a few items needed for distribution of fjcore package
cp -p $fjdir/example/data/single-event.dat . # copy event file, for distribution
sed 's/data\///' 01-basic.cc > tmp$$ # change location of event file in usage
mv tmp$$ 01-basic.cc
cp -p $scriptsdir/Makefile-fjcore.txt Makefile
cp -p $fjdir/fortran_wrapper/fjcorefortran.cc .
cp -p $fjdir/fortran_wrapper/fjcore_fortran_example.f .

echo "======================================================================"
echo "fjcore-${version}/fjcore.{hh,cc} are now ready"
echo "======================================================================"
cd ..

# now make a tarball
echo "Now making fjcore-$version.tar.gz tarball"
tar zcvf fjcore-$version.tar.gz fjcore-$version
rm -rf fjcore-$version

