#!/usr/bin/perl -w
#
# Script to help us perform a nightly check of fastjet
#
#    -mail           sends mail to all authors, otherwise output goes to screen
#    -mailgavin      sends mail to just gavin
#    -mailgregory    sends mail to just gregory
#    -mailmatteo     sends mail to just matteo
#    -verbose        output goes to screen even if we also ask for mail
#    -only index     runs only the setup corresponding to the index that's 
#                    requested (can also take a comma-separated list of indices)
#    -list           lists the different setups and the index of each
#    -no-git-checks  don't run git update , checks for clean git, or git restore at end
#                    (only for development use)
#
# Various other options provide access to internals for running checks
# on remote hosts. The set of configurations that are run is given in
# the setups variable below.
#
#----------------------------------------------------------------------
# The script does the following once:
#   - svn update
#   - make dist
#
# And then the following for each setup
#   - untar
#   - configure from separate dir
#   - make
#   - make check
#   - regression-tests/test-all-algs.pl -nev [some number]
#
#----------------------------------------------------------------------
# Future options:
#
#   - do a build in situ
#
#   - try fastjet-config with --cxxflags and --libs in separate invocations
#
#   - add tests of things like areas, subjets (goes in fastjet_timing_plugins.cc)?
#
# For implementing "options", what one might do is add an optional
# hash entry to the setups, e.g. {BuildInSitu => 1}; then for
# transferring this between machines, use the "Storable" perl
# module.
#
#----------------------------------------------------------------------
# Reminder notes:
#
# NB: $? is command status (non-zero with error)
#
# -------- model crontab file (on toth)--------------------------------
# # select the default shell (to get all paths, etc., e.g. for CGAL)
# SHELL=/bin/zsh
#
# # at 5.34 every morning run the fastjet tests;
# #
# 34 05 * * * cd $HOME/work/jets/fjr-branches/fastjet-trunk-nightly-tests ; regression-tests/nightly-check.pl -mail

use Cwd;
use English;
$OUTPUT_AUTOFLUSH = 1;

# things to configure
$mailAddr='salam@lpthe.jussieu.fr cacciari@lpthe.jussieu.fr soyez@lpthe.jussieu.fr'; #  g@gavin.fr 

# the CGAL path
#
# GS: it was previously using Gavin's environment variable. Until he
# updates it, we're temporarily going to use a fixed path pointing to
# my installation. Note that CGAL is curently only tested on 64-bit
# systems, so I'll use the 64-bit build
#$CGAL_DIR='/ada3/anciens/soyez/jets/utils/CGAL-3.6.1_install';
#$CGAL_DIR='/ada3/anciens/soyez/jets/utils/CGAL-3.6.1_gcc46_install';
#$CGAL_DIR='/ada3/anciens/soyez/jets/utils/CGAL-3.8_gcc46_install';
# GPS: updated this 2013-04-27 to point to new build by Matteo
#$CGAL_DIR='/ada1/lpthe/cacciari/lib/CGAL-4.1';
$CGAL_DIR='/ada1/lpthe/cacciari/lib/CGAL-4.14.3';
#$CGAL_DIR='/ada2/visit/soyez/work/HEP-software/install/CGAL-4.11';

@setups = ();
# for each setup we put the host ("" is current host), the config
# options, the special link-time arguments to fastjet-config, and the
# number of events
#
# The things we want to test are:
#
# - out of the box compilation on linux
# - the same on a mac
# - a full set of algs on toth, mac, a 64 bit machine, gcc 4.4
# - shared/static issues (depending on current defaults)
# - cgal
# - at least one run with 10^3 events
# - at least one run with pxcone


# basic checks without and with CGAL (by default all 64 bit)
push @setups, ["","", "", 10, ""]; # out of the box
push @setups, ["","--enable-allcxxplugins --enable-cgal --disable-cgal-header-only --with-cgaldir=".$CGAL_DIR, "", 10, ""]; # with CGAL & all plugins

# checks of the library system variants (shared/static/monolithic)
push @setups, ["","--enable-allplugins --disable-shared", "", 10, ""]; # with static libs, and pxcone
push @setups, ["","--enable-allplugins --disable-monolithic", "", 10, ""]; # test the non-monolithic build (all plugins in separate libs)
push @setups, ["","--enable-allcxxplugins --enable-shared", "--shared=no", 10, ""]; # with static libs even though shared are built

# checks with different compilers, and 32 instead of 64 bit; all still linux
#push @setups, ["themis","--enable-allcxxplugins", "", 1000, ""]; # a 32 bit SLC6 machine (added 2013-05-01) (themis is out of order, MC 2015-06-15)
#GPS2022-12-08: next line commented out because of icpc licence problems; but it is also an extremely old version of the intel compiler (v10)
# push @setups, ["",'--enable-allcxxplugins CC=icc CXX=icpc --disable-debug', "", 1000, ""]; # with the intel compiler (v10)
# MC 2025-05-11 icpc in next line failing on anubis
#push @setups, ["",'--enable-allcxxplugins CC=/opt/intel/bin/icc CXX=/opt/intel/bin/icpc LDFLAGS=-Wl,-rpath,/opt/intel/lib/intel64  --disable-debug', ":-Wl,-rpath -Wl,/opt/intel/lib/intel64", 1000, ""]; # with the new intel compiler (v14) (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-4.6 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.6", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 4.6 (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-4.7 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.7", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 4.7 (only few evts)
# MC 2025-05-11 gcc-4.8 in next line failing on anubis
#push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-4.8 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.8", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 1000, ""]; # with gcc 4.8
# MC 2025-05-11 gcc-4.9 in next line failing on anubis
#push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-4.9 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.9", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 4.9 (only few evts)
# MC 2025-05-11 gcc-5.1 in next line failing on anubis
#push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-5.1 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.1", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 5.1 (only few evts)
# MC 2025-05-11 gcc-5.2 in next line failing on anubis
#push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-5.2 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.2", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 5.2 (only few evts)
# MC 2025-05-11 gcc-5.3 in next line failing on anubis
#push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-5.3 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.3", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 5.3 (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-5.3 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.3 CXXFLAGS=\"-O2 -Wall -std=c++11\"", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 5.3 and c++11 (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-5.3 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.3 CXXFLAGS=\"-O2 -Wall -std=c++14\"", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 5.3 and c++14 (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada1/lpthe/cacciari/local/bin/gcc-6.1 CXX=/ada1/lpthe/cacciari/local/bin/g++-6.1 CXXFLAGS=\"-O2 -Wall\"", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 6.1 (automatically c++14) (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada4/lpthe/cacciari/local/bin/gcc-10.2 CXX=/ada4/lpthe/cacciari/local/bin/g++-10.2 CXXFLAGS=\"-O2 -Wall\"", ":-Wl,-rpath -Wl,/ada4/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 10.2 (automatically c++??) (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada4/lpthe/cacciari/local/gcc-12.2/bin/gcc-12.2 CXX=/ada4/lpthe/cacciari/local/gcc-12.2/bin/g++-12.2 CXXFLAGS=\"-O2 -Wall\"", ":-Wl,-rpath -Wl,/ada4/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 12.2 (only few evts)
push @setups, ["","--enable-allcxxplugins CC=/ada4/lpthe/cacciari/local/bin/gcc-15.1 CXX=/ada4/lpthe/cacciari/local/bin/g++-15.1 CXXFLAGS=\"-O2 -Wall\"", ":-Wl,-rpath -Wl,/ada4/lpthe/cacciari/local/lib64", 10, ""]; # with gcc 15.1 (only few evts)

# temporary disabled because zetes is down, MC 31/8/2013
#push @setups, ["zetes","--enable-allcxxplugins", "", 10, ""]; # out of the box + all plugins on zetes (SLC4, gcc 3.4.6, 64 bit)
#push @setups, ["","--enable-allcxxplugins CC=gcc34 CXX=g++34", "", 10, ""]; # with gcc-3.4 [suspended 2013-04, but we have zetes for now]

## GPS 2021-01-08: temporarily removing all karnak tests
# checks on macs 
# push @setups, ["karnak","CC=cc CXX=c++", "", 10, ""]; # out of the box on new karnak (OS X 10.8.5) with clang [Apple LLVM version 5.0 (clang-500.2.79) (based on LLVM 3.3svn)]
# push @setups, ["karnak","--enable-allcxxplugins CC=cc CXX=c++", "", 1000, ""]; # full monty on new karnak with clang [Apple LLVM version 5.0 (clang-500.2.79) (based on LLVM 3.3svn)]
# push @setups, ["karnak","--enable-allcxxplugins CC=/usr/local/bin/gcc-4.4 CXX=/usr/local/bin/g++-4.4", "", 10, ""]; # full set with gcc 4.4.7

# extra tests for areas
push @setups, ["","--disable-static --enable-allcxxplugins --enable-cgal --disable-cgal-header-only --with-cgaldir=".$CGAL_DIR, "", 1000, "-strat 1 -areas"]; # locally
# push @setups, ["karnak","--disable-static --enable-allcxxplugins", "", 1000, "-strat 1 -areas"]; # remotely

# extra tests for background estimation
push @setups, ["","--disable-static --enable-allcxxplugins --enable-cgal --disable-cgal-header-only --with-cgaldir=".$CGAL_DIR, "", 1000, "-strat 1 -bkgds"]; # locally
# push @setups, ["karnak","--disable-static --enable-allcxxplugins", "", 1000, "-strat 1 -bkgds"]; # remotely

# minimal check that demangling code doesn't break compilation
push @setups, ["","--disable-static --enable-demangling", "", 10, ""]; # locally

# minimal checks of fjcore
push @setups, ["","", "", 1000, "-fjcore"]; # locally
# push @setups, ["karnak","CC=cc CXX=c++", "", 10, "-fjcore"]; # remotely on karnak

# minimal check of the python interface
push @setups, ["","--disable-static --enable-pyext", "", 10, ""];               # locally, just the interface
push @setups, ["","--disable-static --enable-pyext --enable-swig", "", 10, ""]; # locally, interface + swig

# checks of results with thread safety enabled
#push @setups, ["","--disable-static --enable-thread-safety CXXFLAGS=\"-O2 -Wall -std=c++11\"", "", 10, "-strat 1 -bkgds"];               # locally, just the interface
push @setups, ["","--disable-static --enable-thread-safety CXX=/ada1/lpthe/cacciari/local/bin/g++-6.1 CXXFLAGS=\"-O2 -Wall -std=c++11\"", ":-Wl,-rpath -Wl,/ada1/lpthe/cacciari/local/lib64", 10, "-strat 1 -bkgds"];               # locally, just the interface


# GPS 2013-04-29: removed orphee and osiris, since now both standard SLC6
#push @setups, ["osiris","--enable-allcxxplugins", "", 10, ""]; # out of the box + all plugins on osiris (SLC6.3, gcc 4.4.6, 64 bit)
#push @setups, ["orphee","--enable-allcxxplugins", "", 10, ""]; # out of the box + all plugins on orphee (FC17, gcc 4.7.0, 64 bit)
#push @setups, ["tycho","--enable-allcxxplugins", "", 1000, ""]; # tycho: standard SCL6 machine, 64 bits, gcc 4.4.7 [2013-05-01: no longer needed since tycho is identical to others]

# MC 2025-05-11 Added checks with headers-only CGAL v5 and v6
push @setups, ["","--enable-allcxxplugins --enable-cgal", "", 1000, ""]; # with CGAL & all plugins package manager installation of CGAL (v5.6.2 on 2025-05-11)
# NB the following line relies on GMP and MPFR to be findable in standard locations. They are provided by the CGAL installation 
# via a  package manager.
# If they are not in a standard location, one needs to also point to them explicitly with --with-cgal-gmpdir and  --with-cgal-mpfrdir
push @setups, ["","--enable-allcxxplugins --enable-cgal --with-cgaldir=/ada4/lpthe/cacciari/lib/CGAL-6.0.1", "", 10, ""]; # personal installation of CGAL


# process command-line
$mail=0;
$tmpDir="";
$remote=0;
$command=$0;
$commandArgs=join(" ",@ARGV);
$origDir=getcwd();
$tarName="";
$verbose="";
%only=(); $only="";
$listSetups="";
$dogitchecks=1;
while ($arg = shift @ARGV) {
  if    ($arg eq "-mail")      {$mail = 1;}
  elsif ($arg eq "-mailgavin") {$mail = 1; $mailAddr='salam@lpthe.jussieu.fr';}
  elsif ($arg eq "-mailgregory"){$mail = 1; $mailAddr='soyez@lpthe.jussieu.fr';}
  elsif ($arg eq "-mailmatteo"){$mail = 1; $mailAddr='cacciari@lpthe.jussieu.fr';}
  elsif ($arg eq "-verbose")   {$verbose = 1;}
  elsif ($arg eq "-no-git-checks") {$dogitchecks=0;}
  elsif ($arg eq "-only")      {
    $only = shift @ARGV;
    foreach $index (split(",",$only)) {$only{$index} = 1;}
  }
  elsif ($arg eq "-list")      {$listSetups = 1;}
  # the following args are only for internal treatment of execution
  # on remote hosts
  elsif ($arg eq "-remote")    {$tmpDir  = shift @ARGV; $remote=1;}
  elsif ($arg eq "-tar")       {$tarName = shift @ARGV;}
  elsif ($arg eq "-tarcore")   {$tarNameCore = shift @ARGV;}
  elsif ($arg eq "-orig")      {$origDir = shift @ARGV;}
  else {die "Unrecognized argument: $arg";}
}

# allow user to see what is planned
if ($listSetups) {
  for ($i = 0; $i <= $#setups; $i++) {
    print "$i: ",join("; ", @{$setups[$i]}),"\n";
  }
  exit(0);
}

# for some remote hosts, need to remove leading "/misc?" from directory name
$origDir=~ s/^\/misc//; 

$fail="";
$failDetails = "";
$allMessages = "";
$summary = "";
$testall = "";
$verbose = $verbose || (! ($mail || $remote));
$svnrev = ""; $svnShortURL = ""; # (just to make these global variables)
$gitlog = ""; # (just to make this a global variable)
$date = "";
#$tarName="fastjet-2.4-devel.tar.gz"; # TMP 


MAIN: while (1) {

  if (!$remote) {
    #--- make tmpDir -------------------------------------------------------
    #$tmpDir = "$origDir/tmp-nightly";
    $tmpDir = "$origDir/tmp-".$$;
    &message("* making tmp directory $tmpDir\n");
    if (-e $tmpDir || ! (mkdir $tmpDir)) {
      $tmpDir = "";
      &fail("* creating tmp directory","$tmpDir already exists or could not be created; stopping");
    }

    # bits and pieces for transition to git
    # https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git
    # to get description of state (HEAD->master, etc.): git log --pretty='%d' --decorate=short -1
    # to get description of state with abbrev reflog: git log --pretty='%h%d' --decorate=short -1
    # to get current ref: git rev-parse @
    # to see if there are any uncommitted files: git status --porcelain --untracked-files=no
    # remember to do a git pull and a git submodule update

    # sequence to follow:
    # - check nothing uncommitted, with git status --porcelain --untracked-files=no
    # - check we are not ahead with `git status | grep 'Your branch is ahead'`
    # - git pull 
    #   - if conflicts, die (given the first two conditions, there should not be)
    #   - parse output to see if nightly-check updated -- if so, rerun
    # - git submodule update
    #   - if conflicts, die (given the first two conditions, there should not be)
    # - get state description with `git log --pretty='%h%d' --decorate=short -1`


    $usegit=1;

    $dogitchecks=($usegit && $dogitchecks);
    if ($dogitchecks) {
      # check nothing uncommitted
      $gitstatus=`git status --porcelain --untracked-files=no 2>&1`; chomp $gitstatus;
      if ($gitstatus ne '') {&fail("git status is not clean",$gitstatus);}
      # check we are not ahead
      $gitahead=`git status 2>&1`;
      if ($gitahead =~ /Your branch is ahead/) {&fail("local git is ahead wrt remote",$gitahead)}
      # git pull ($? is exit code -- nonzero on failure)
      # NB: we check the output for conflicts, but they
      #     should never occur, given the earlier check on the
      #     state of the repo
      $gitpull=`git pull 2>&1`;
      if ($? || $gitpull =~ /conflict/i) {&fail("error or conflict in git pull", $gitpull)}
      # submodule update
      $gitsub =`git submodule update 2>&1`;
      if ($? || $gitsub =~ /conflict/i) {&fail("error or conflict in git sub", $gitpull)}
      # check for nighly-check.pl update and rerun
      if ($gitpull =~ /nightly-check.pl/) {
          &message("* nightly-check.pl has been updated, rerunning\n\n");
          system("$command $commandArgs");
          last;
      }
      $date=`date`; chomp($date);
      $gitlog = `git log --pretty='%h%d' --decorate=short -1`;
      # this fails on the ancient git version on orphee
      #$giturl = `git remote get-url origin`;
      # this should work more generally (though it is uglier)
      $giturl = `git remote -v`;
      @giturl = split(" ",$giturl);
      $giturl = $giturl[1];
      $summary .= "SUMMARY: $date, git [$giturl] $gitlog ---------------------------------------------------\n\n";
    } elsif (! $usegit) {
      #--- svn update --------------------------------------------------------
      &message("* running svn update\n");
      $svnup=`svn update 2>&1`;
      if ($svnup =~ /external .. revision [0-9]/i && 
          ($svnup =~ /^At revision [0-9]/m || $svnup =~ /^Updated to revision [0-9]/m) &&
          $svnup !~ /conflict/i) {
        # check if we had a merge -- in that case using this script is dangerous, so tell 
        # user
        if ($svnup =~ /^G..*nightly-check.pl/m) {&fail("svn update merged nightly-check.pl", $svnup);}
        # if the script was just updated, then rerun ourselves
        if ($svnup =~ /^U..*nightly-check.pl/m) {
          &message("* nightly-check.pl has been updated, rerunning\n\n");
          system("$command $commandArgs");
          last;
        }
        # all is OK, do nothing
      } else {
        &fail("svn update", $svnup);
      }
      $svninfo = `svn info`;
      if ($svninfo =~ /^URL: (.+)/m) {
        $svnURL = $1;
        &message("* svn URL: $svnURL\n");
      } else {
        &fail("getting svn URL",$svninfo);
      }
      ($svnShortURL = $svnURL) =~ s/.*salam.svn.fastjet.//;
      if ($svninfo =~ /^Revision: ([0-9]+)/m) {
        $svnrev = $1;
        &message("* svn revision: $svnrev\n");
      } else {
        &fail("getting svn revision",$svninfo);
      }
      $svnstatus=`svn status`;
      $svnstatus =~ s/^(\?|X|Performing status).*\n//mg;
      $svnstatus =~ s/^\n//mg;
      if ($?) {
        &fail("svn status",$svnstatus)
      } else {
        &message("* svn status:\n".$svnstatus);
      }
      # some useful stuff for the summary
      $date=`date`; chomp($date);
      $summary .= "SUMMARY: $date, svn [.../$svnShortURL] revision $svnrev\n$svnstatus---------------------------------------------------\n\n";
    }

    #--- make dist ------------------------------------------------------
    &message("* running configure & make dist");
    if (! -d "autobuild") {system("mkdir autobuild");}
    $makedist=`(cd autobuild; ../configure --enable-swig --enable-pyext; make dist; cd .. )2>&1`;
    if ($makedist =~ /error[: ]/i || $makedist !~ />(.*?tar.gz)/) {
      &message("\n");
      &fail ("make dist", $makedist);
    } else {
      $tarName = $1;
      &message(" -> $tarName\n");
      system("mv autobuild/$tarName .");
    }

    #--- extract fjcore ------------------------------------------------------
    &message("* extracting fjcore");
    $makefjcore=`cd scripts; ./mkfjcore.sh $tmpDir 2>&1; cd ..`;
    if ($makefjcore =~ /error[: ]/i || $makefjcore !~ /making (.*.tar.gz) tarball/) {
      &message("\n");
      &fail ("extracting fjcore", $makefjcore);
    } else {
      $tarNameCore = $1;
      &message(" Created $tarNameCore and moving it to $origDir/\n");
      system("mv $tmpDir/$tarNameCore $origDir/");
    }
    


    # now run the rest, either remotely, or from setups array, or from a setup file
    for ($i = 0; $i <= $#setups; $i++) {
      if ($only ne "" && ! exists($only{$i})) {next;}
      if ($setups[$i][0]) {
        # run test on a remote host 
        &message("* transferring execution to remote host $setups[$i][0]\n");

        # first set up a file on remote host with the info of interest
        open(SETUP, "> $tmpDir/setup") || die "Could not write to $tmpDir/setup";
        for ($j=1; $j <=4; $j++) {print SETUP $setups[$i][$j],"\n";}
        close SETUP;

        # connect to remote host and run there
        $ssh=`ssh $setups[$i][0] $origDir/$command -remote $tmpDir -orig $origDir -tar $tarName -tarcore $tarNameCore 2>&1`;
        $ssh =~ s/^.*in the future\n//mg;   # because karnak's time is wrong
        $ssh =~ s/^.*slocate.db.*\n//mg;    # because zetes has out-of-date locate
        $ssh =~ s/^.*updatedb.*\n//mg; # (which I use on logon...)
        $ssherr = $?;

        # collect the results
        $results = "";
        if (-e "$tmpDir/messages") {$results  = `cat $tmpDir/messages 2>&1`;}
        if (-e "$tmpDir/summary") {$summary .= `cat $tmpDir/summary 2>&1`;}

        # check for failures, in ssh or in results
        if ($ssh || $ssherr) {
          &fail("connection to $setups[$i][0]", $results."\nssh output should have been empty, but was:\n------------------------------\n".$ssh);}
        if (!$results || $results =~ /Failed/ || $?) {
          &fail("execution on remote host", $results);
        } else {
          &message($results);
        }
      } else {

        # run the test locally
        &build_and_check($setups[$i][1], $setups[$i][2], $setups[$i][3], $setups[$i][4]) || last MAIN;

      }
    }
      
  } else {
    # remote case, in which tmpDir is already there
    # read the instructions
    open(SETUP, "< $tmpDir/setup") || die "failed to read from $tmpDir/setup;";
    for ($j=0; $j <= 3; $j++) {$setup[$j] = <SETUP>; chomp($setup[$j]);}
    close SETUP;
    # execute them
    &build_and_check($setup[0], $setup[1], $setup[2], $setup[3]) || last MAIN;
  }

  #&build_and_check($configOpts, $fjlibOpts, $nevTestAll) || last;

  # now just exit
  last;
}

&finish();



#======================================================================
sub finish () {
  #if (!$remote) {$summary = "SUMMARY\n-------\n".$summary;}
  #-- mention where failure might arise
  if ($fail) {
    &message("Failed on $fail\n\nDetailed message is:\n------------------\n");
    &message($failDetails);
    &message("\n--------------- END OF FAILURE MESSAGE ---------------\n");
    $mailSubject='fastjet nightly: FAILED on '.$fail;
  } elsif (!$remote) {
    &message("\nAll tests passed\n");
    # try to get more info about test results
    $mailSubject = 'fastjet nightly: '.OKUnavail($allMessages);
    if ($usegit) {$mailSubject .= " $gitlog"}
    else         {$mailSubject .= " [".$svnShortURL."@".$svnrev."]"}
  }

  # clean up
  if ($tmpDir && !$fail && !$remote) { 
    &message("* removing $tmpDir\n");
    system("rm -rf $tmpDir");
    if ($dogitchecks) {
      # if we checked that the git state was clean at the start, then
      # we restore the git state at this point
      &message("* restoring git state, in case of any modified files (e.g. config.h.in)");
      system("git restore .");
      system("pushd plugins/SISCone/siscone; git restore .; popd");
    }
  };

  # send mail if relevant, or deposit a message for the program that called us
  if ($mail) {
    open (MAIL, "|mail -s '$mailSubject' $mailAddr") || die "could not open pipe for mail message";
    print MAIL $summary."\n\n";
    print MAIL $allMessages;
    close MAIL;
  } elsif ($remote) {
    open (MSG, "> $tmpDir/messages") || die "Remote host could not write to $tmpDir/messages";
    print MSG $allMessages;
    close MSG;
    open (SUM, "> $tmpDir/summary") || die "Remote host could not write to $tmpDir/summary";
    print SUM $summary;
    close SUM;
  }

  if ($verbose && !$remote) {
    print "\n\n".$summary;
  }
  
  exit;
}


#======================================================================
sub fail($$) {
  ($fail, $failDetails) = @_;
  $summary .= "   FAILED: $fail\n";
  &finish();
}

#======================================================================
sub message ($) {
  (my $msg) = @_;
  $allMessages .= $msg;
  if ($verbose) {print $msg;}
}


#======================================================================
# given an output string provide, an message containing # of OK / 
# unavailable options.
sub OKUnavail ($) {
  my ($input) = @_;
  my $output;
  @unavail = split("unavailable",$input);
  @areOK   = split("OK",$input);
  $output=sprintf("%d",$#areOK).' OK';
  if ($#unavail >= 0) {$output .= ", ".sprintf("%d",$#unavail)." NA"}
  return $output;
}

#======================================================================
#
# Untars, configures, compiles, does a link with an example program, and runs
# it to check that the output is correct
#
# - $config:       the configure-time flags
# - $link:         flags passed to fastjet-config at link time 
#                  (anything after a ":" is passed to g++ as compile/link flags)
# - $nev:          number of events to actually test
#
sub build_and_check($$$$) {
  my ($config,$link,$nev,$testargs) = @_;
  
  # separate the link flags into two pieces, before and after colon
  my ($linkfj, $linkgcc);
  if ($link =~ /(.*):(.*)/) {
    $linkfj  = $1;
    $linkgcc = $2;
  } else {
    $linkfj = $link;
    $linkgcc = "-O";
  }
  

  # get info about the compiler
  $cxx = "g++";
  # special compilers are deduced from the configure flag
  if ($config=~ /CXX=([^\s]+)/) { $cxx = $1; }
  if ($config=~ /CXXFLAGS="([^"]+)"/) { $cxx .= " ".$1; }
  $compiler = `$cxx --version 2>&1 | head -1`; chomp $compiler;

  # start constructing the summary
  ($host = `uname -n`) =~ s/\..*//; chomp($host);
  $shortuname = `uname -sm`; chomp($shortuname);
  $summary .= "Running on $host: $shortuname, $compiler
   config: $config
   tests:  link($link), nev($nev)
   args:   $testargs
";


  chdir $tmpDir;

  #--- clean up from previous invocation --
  if (-e "build/") {
    &message("\n* removing everything from the tmp dir\n");
    system("rm -rf *");
  }

  # some detailed info about the system
  $uname = `uname -a`; chomp $uname;
  &message("* running on $uname\n");
  &message("* c++ compiler: $cxx, $compiler\n");

  

  #--- untar -----------------
  &message("* untarring $origDir/$tarName in tmp dir\n");
  $untar=`tar zxvf $origDir/$tarName 2>&1 `;
  if ($?) {
    &fail("untar",$untar);
  }
  
  if ( $testargs =~ /fjcore/ ) {
    
    #--- compile externally fastjet_timing_plugins with fjcore -------------------
    system("tar zxf $origDir/$tarNameCore");
    ($distDir=$tarName) =~ s/.tar.gz//;
    ($distDirCore=$tarNameCore) =~ s/.tar.gz//;
    &message("* compiling fastjet_timing_plugins with fjcore\n");
    &message("* command is: $cxx -D__FJCORE__ -I$distDir/example -I$distDirCore $distDir/example/CmdLine.cc $distDir/example/fastjet_timing_plugins.cc  $distDirCore/fjcore.cc -o fastjet_timing_plugins_fjcore 2>&1\n");
    $compile=`$cxx -D__FJCORE__ -I$distDir/example -I$distDirCore $distDir/example/CmdLine.cc $distDir/example/fastjet_timing_plugins.cc  $distDirCore/fjcore.cc -o fastjet_timing_plugins_fjcore 2>&1`;
    if ($compile =~ /error[: ]/i || $?) {
      &fail("external compilation with fjcore",$compile);
    }

  } else {

    #--- configure -----------------
    system("mkdir build/");
    chdir "build";
    &message("* running configure $config --prefix=$tmpDir/inst\n");
    ($distDir=$tarName) =~ s/.tar.gz//;
    $configOut=`../$distDir/configure $config --prefix=$tmpDir/inst 2>&1`;
    if ($configOut =~ /error[: ]/i || $?) {
      &fail("configure",$configOut);
    }

    # figure out the f77 compiler too
    $fcompiler="";
    if (`cat Makefile` =~ /^F(77|C) = ([^\s]+)$/m) {
      $fcompiler = $2;
      $fcompiler .= ", ".`$fcompiler --version 2>&1 | head -1`;
      chomp $fcompiler;
    }
    &message("* fortran compiler: $fcompiler\n");

    #--- run make -------------------
    &message("* running make\n");
    $make=`make -j 2>&1`;
    # be careful about how we check for errors in case we trigger
    # intel warnings
    if ($make =~ /^[Ee]rror[: ]/ || $make =~ / [Ee]rror[: ]/ || $?) {
      &fail("make",$make);
    }

    #--- run make check -------------------
    &message("* running make check\n");
    $makecheck=`make check 2>&1`;
    if ($makecheck =~ /error[: ]/i || $?) {
      # on older autotools presence of word "error" means there's an error!
      # On more modern autotools make check gives different
      # output (always containing lines such as "Error: 0")
      if ($makecheck =~ /TOTAL: *([0-9]+)/i) {
        $expectedTotal= $1;
        $npass = 0;
        if ($makecheck =~ /PASS: *([0-9]+)/i) {$npass = $1;}
        if ($npass != $expectedTotal) {
          &fail("make check",$makecheck);
        }
      } else {
        &fail("make check",$makecheck);
      }
    }
  
    #--- run make install -------------------
    &message("* running make install\n");
    $makeinstall=`make install 2>&1`;
    if ($makeinstall =~ /error[: ]/i || $?) {
      &fail("make install",$makeinstall);
    }

    #--- do external compilation -------------------
    chdir "../";
    &message("* compiling fastjet_timing_plugins externally (with $cxx, fastjet-config ... $link)\n");
    &message("* command is: $cxx $linkgcc -I$distDir/example $distDir/example/CmdLine.cc $distDir/example/fastjet_timing_plugins.cc  \`inst/bin/fastjet-config --cxxflags --libs --plugins $linkfj\` -o fastjet_timing_plugins 2>&1\n");
    $compile=`$cxx $linkgcc -I$distDir/example $distDir/example/CmdLine.cc $distDir/example/fastjet_timing_plugins.cc  \`inst/bin/fastjet-config --cxxflags --libs --plugins $linkfj\` -o fastjet_timing_plugins 2>&1`;
    if ($compile =~ /error[: ]/i || $?) {
      &fail("external compilation",$compile);
    }

  } # end if on fjcore
  
  #--- do test-all-algs -------------------
  &message("* testing all algs\n");
  # use the original test-all-algs.pl prog, since it isn't distributed
  # in the tarball
  $testall=`../regression-tests/test-all-algs.pl -nev $nev $testargs`;
  $summary .= "   status: ".&OKUnavail($testall)."\n\n";
  if ($testall =~ /\sBAD/i || $testall !~ /OK/ || $?) {
    &fail("testing all algs",$testall);
  } else {
    &message($testall);
  }

  # return things to their initial state (and hopefully avoid "missing-directory" issues)
  chdir $origDir;
  return 1;
}
