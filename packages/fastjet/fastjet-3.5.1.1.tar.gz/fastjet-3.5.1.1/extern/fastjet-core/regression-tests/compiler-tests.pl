#!/usr/bin/perl -w
#
# Script to help us perform an extended tests of compilers and compilation flags
#
#    -mail        sends mail to all authors, otherwise output goes to screen
#    -mailgregory sends mail to just gregory
#    -verbose     output goes to screen even if we also ask for mail
#    -only index  runs only the setup corresponding to the index that's 
#                 requested (can also take a comma-separated list of indices)
#    -list        lists the different setups and the index of each
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

use Cwd;
use English;
$OUTPUT_AUTOFLUSH = 1;

# things to configure
$mailAddr='salam@lpthe.jussieu.fr cacciari@lpthe.jussieu.fr soyez@lpthe.jussieu.fr';

# the CGAL path
# GPS: updated this 2013-04-27 to point to new build by Matteo
$CGAL_DIR='/ada1/lpthe/cacciari/lib/CGAL-4.1';

@setups = ();

# the list of things we want to test
#
# - common options:
#     --disable-static --enable-debug --enable-allcxxplugins
#   
# - gcc tests (v 4.4,4.6-4.9, 5.1) [5.2 and 5.3 desired] (on tycho)
#   for each we want the following set of options
#     --enable-extra-warnings
#     CXXFLAGS='-O2 -Wall -std=c++11' (-std=c++0x for gcc<4.7)
#     --enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++11'
#   
#   we probably also want one test w CGAL (only the latest gcc)
#     --enable-cgal 
#     --enable-cgal CXXFLAGS='-O2 -Wall -std=c++11'
#
# - clang (v3.5-3.8) (on fractal)
#
# - Intel (v15.0.0) (on tycho)
#
# setup formay is as follows:
#   0. tag
#   1. host
#   2. configure options (includes compiler and flags)

$common_options="--disable-static --enable-debug --enable-allcxxplugins";
#$default_host="talos";

#----------------------------------------------------------------------
#------------  gcc version scan ---------------------------------------
#----------------------------------------------------------------------
push @setups, ["gcc4.4-extra",       "", "--enable-extra-warnings"];
push @setups, ["gcc4.4-c++0x",       "", "CXXFLAGS='-O2 -Wall -std=c++0x'"];
push @setups, ["gcc4.4-extra-c++0x", "", "--enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++0x'"];

push @setups, ["gcc4.6-extra",       "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-4.6 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.6 --enable-extra-warnings"];
push @setups, ["gcc4.6-c++0x",       "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-4.6 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.6 CXXFLAGS='-O2 -Wall -std=c++0x'"];
push @setups, ["gcc4.6-extra-c++0x", "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-4.6 CXX=/ada1/lpthe/cacciari/local/bin/g++-4.6 --enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++0x'"];

foreach $version ("4.7", "4.8", "4.9", "5.1", "5.2", "5.3"){
    push @setups, ["gcc".$version."-extra",       "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-".$version." CXX=/ada1/lpthe/cacciari/local/bin/g++-".$version." --enable-extra-warnings"];
    push @setups, ["gcc".$version."-c++11",       "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-".$version." CXX=/ada1/lpthe/cacciari/local/bin/g++-".$version." CXXFLAGS='-O2 -Wall -std=c++11'"];
    push @setups, ["gcc".$version."-extra-c++11", "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-".$version." CXX=/ada1/lpthe/cacciari/local/bin/g++-".$version." --enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++11'"];
}
push @setups, ["gcc5.3-cgal",        "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-5.3 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.3 --enable-cgal --with-cgaldir=".$CGAL_DIR];
push @setups, ["gcc5.3-cgal-c++11",  "", "CC=/ada1/lpthe/cacciari/local/bin/gcc-5.3 CXX=/ada1/lpthe/cacciari/local/bin/g++-5.3 --enable-cgal --with-cgaldir=".$CGAL_DIR." CXXFLAGS='-O2 -Wall -std=c++11'"];

# 5.3 is the default on fractal (CGAL seems v4.7 which is the latest stable so we include it in the tests)
push @setups, ["gcc5.3-extra",       "fractal:work/fastjet", "--enable-extra-warnings"];
push @setups, ["gcc5.3-c++11",       "fractal:work/fastjet", "CXXFLAGS='-O2 -Wall -std=c++11'"];
push @setups, ["gcc5.3-extra-c++11", "fractal:work/fastjet", "--enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++11'"];
push @setups, ["gcc5.3-cgal",        "fractal:work/fastjet", "--enable-cgal"];
push @setups, ["gcc5.3-cgal-c++11",  "fractal:work/fastjet", "--enable-cgal CXXFLAGS='-O2 -Wall -std=c++11'"];

#----------------------------------------------------------------------
#------------  clang version scan -------------------------------------
#----------------------------------------------------------------------
foreach $version ("3.5", "3.6", "3.7", "3.8"){
    push @setups, ["clang".$version."-extra",       "fractal:work/fastjet", "CC=clang-".$version." CXX=clang++-".$version." --enable-extra-warnings"];
    push @setups, ["clang".$version."-c++11",       "fractal:work/fastjet", "CC=clang-".$version." CXX=clang++-".$version." CXXFLAGS='-O2 -Wall -std=c++11'"];
    push @setups, ["clang".$version."-extra-c++11", "fractal:work/fastjet", "CC=clang-".$version." CXX=clang++-".$version." --enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++11'"];
}

#----------------------------------------------------------------------
#------------  intel version scan -------------------------------------
#----------------------------------------------------------------------
push @setups, ["icpc-extra",       "", "CC=/opt/intel/bin/icc CXX=/opt/intel/bin/icpc --enable-extra-warnings"];
push @setups, ["icpc-c++11",       "", "CC=/opt/intel/bin/icc CXX=/opt/intel/bin/icpc CXXFLAGS='-O2 -Wall -std=c++11'"];
push @setups, ["icpc-extra-c++11", "", "CC=/opt/intel/bin/icc CXX=/opt/intel/bin/icpc --enable-extra-warnings CXXFLAGS='-O2 -Wall -std=c++11'"];


# process command-line
$mail=0;
$remote=0;
$remotetag="unknown";
$usetarball=0;
$command=$0;
$commandArgs=join(" ",@ARGV);
$origDir=getcwd();
$tarName="";
$verbose="";
%only=(); $only="";
$listSetups="";
while ($arg = shift @ARGV) {
  if    ($arg eq "-mail")        {$mail = 1;}
  elsif ($arg eq "-mailgregory") {$mail = 1; $mailAddr='soyez@lpthe.jussieu.fr';}
  elsif ($arg eq "-verbose")     {$verbose = 1;}
  elsif ($arg eq "-only")        {
    $only = shift @ARGV;
    foreach $index (split(",",$only)) {$only{$index} = 1;}
  }
  elsif ($arg eq "-list")      {$listSetups = 1;}
  # the following args are only for internal treatment of execution
  # on remote hosts
  elsif ($arg eq "-remote")    {$remote=1;}
  elsif ($arg eq "-tar")       {$tarName = shift @ARGV; $usetarball=1;}
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
$verbose = $verbose || (! ($mail || $remote));
$svnrev = "";
$date = "";


MAIN: while (1) {

    if (!$remote) {
        #--- get where we are in FJ --------------------------------------------
        @tmparray=split("/fastjet/", $origDir);
        $fjdir=$tmparray[0]."/fastjet";
        $fjsubdir=$tmparray[1];

        #GS-note: see how svnShortURL is constructed below for an alternative
        &message("* Current FastJet dir set to $fjdir with internal subdir $fjsubdir\n");
               
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


        #--- make dist ------------------------------------------------------
        # this creates a tarball in the original FJ directory
        &message("* running make dist");
        $makedist=`make dist 2>&1`;
        if ($makedist =~ / error[: ]/i || $makedist !~ />(.*?tar.gz)/) {
            &message("\n");
            &fail ("make dist", $makedist);
        } else {
            $tarName = $1;
            &message(" -> $tarName\n");
        }

        #--- create dir for compilation results -----------------------------
        $resDir = "$origDir/regression-tests/compiler-results";
        &message("* making tmp directory $resDir\n");
        if (! -e $resDir){
            if (! (mkdir $resDir)) {
                $resDir = "";
                &fail("* creating result directory","$resDir could not be created; stopping");
            }
        }
        
        #--------------------------------------------------------------------
        # now run the rest, either remotely, or from setups array, or from a setup file
        for ($i = 0; $i <= $#setups; $i++) {
            if ($only ne "" && ! exists($only{$i})) {next;}
            if ($setups[$i][1]) {
                # run test on a remote host 
                &message("* transferring execution to remote host $setups[$i][1]\n");

                # connect to remote host and run there
                #
                # get host and path
                @tmparray=split(":", $setups[$i][1]);
                $host=$tmparray[0];
                $path=$tmparray[1];
                $ssh =`scp $tarName $host:$path/$fjsubdir/`;
                $ssh =~ s/^.*in the future\n//mg;   # because karnak's time is wrong
                $ssh =~ s/^.*slocate.db.*\n//mg;    # because zetes has out-of-date locate
                $ssh =~ s/^.*updatedb.*\n//mg; # (which I use on logon...)
                $ssherr = $?;
                if ($ssh || $ssherr) {
                    &fail("tar copy to $setups[$i][1]", "ssh output should have been empty, but was:\n------------------------------\n".$ssh."\n".$ssherr);}

                $ssh=`ssh $host "cd $path/$fjsubdir; ./regression-tests/compiler-tests.pl -remote -only $i -tar $tarName 2>&1"`;
                $ssh =~ s/^.*in the future\n//mg;   # because karnak's time is wrong
                $ssh =~ s/^.*slocate.db.*\n//mg;    # because zetes has out-of-date locate
                $ssh =~ s/^.*updatedb.*\n//mg; # (which I use on logon...)
                $ssherr = $?;
                if ($ssh || $ssherr) {
                    &fail("test on to $setups[$i][1]", "ssh output should have been empty, but was:\n------------------------------\n".$ssh."\n".$ssherr);}

                $tag = $setups[$i][0];
                $ssh=`scp $host:$path/$fjsubdir/regression-tests/compiler-results/$tag.* $resDir`;
                $ssh =~ s/^.*in the future\n//mg;   # because karnak's time is wrong
                $ssh =~ s/^.*slocate.db.*\n//mg;    # because zetes has out-of-date locate
                $ssh =~ s/^.*updatedb.*\n//mg; # (which I use on logon...)
                $ssherr = $?;
                if ($ssh || $ssherr) {
                    &fail("copying results from $setups[$i][1]", "ssh output should have been empty, but was:\n------------------------------\n".$ssh."\n".$ssherr);}
            } else {
                # run the test locally
                &build_and_check($setups[$i][0], $setups[$i][2]) || last MAIN;
            }
        }
        
    } else {
        $index=0;
        for ($i = 0; $i <= $#setups; $i++) {
            if ($only ne "" && ! exists($only{$i})) {next;}
            $index=$i;
        }
        # remote case
        &build_and_check($setups[$index][0], $setups[$index][2]) || last MAIN;
    }

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
        $mailSubject = 'fastjet nightly: '.OKUnavail($allMessages)." [".$svnShortURL."@".$svnrev."]";
    }

    # send mail if relevant, or deposit a message for the program that called us
    if ($mail) {
        open (MAIL, "|mail -s '$mailSubject' $mailAddr") || die "could not open pipe for mail message";
        print MAIL $summary."\n\n";
        print MAIL $allMessages;
        close MAIL;
    } elsif ($remote) {
        open (MSG, "> $origDir/regression-tests/compiler-results/$remotetag.log") || die "Remote host could not write to $origDir/regression-tests/compiler-results/$remotetag.log";
        print MSG $allMessages;
        close MSG;
        open (SUM, "> $origDir/regression-tests/compiler-results/$remotetag.sum") || die "Remote host could not write to $origDir/regression-tests/compiler-results/$remotetag.sum";
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
    $summary .= "   FAILED on $fail\n";
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
# Untars, configures, compiles
#
# This assumes we're in the correct FJ dir with a rtarball in the same
# dir
#
# - $tag:      a string tagging this setup
# - $config:   the configure-time flags
#
sub build_and_check($$) {
    my ($tag,$config) = @_;
    $remotetag=$tag;

    # make sure we have a directlry where the results can be stores
    $resDir = "$origDir/regression-tests/compiler-results";
    &message("* making tmp directory $resDir\n");
    if (! (-e $resDir)){
        if (! (mkdir $resDir)) {
            $resDir = "";
            &fail("* creating result directory","$resDir does not exists and could not be created; stopping");
        }
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
";

    # some detailed info about the system
    $uname = `uname -a`; chomp $uname;
    &message("* running on $uname\n");
    &message("* c++ compiler: $cxx, $compiler\n");

    # create a temporary dir for compilation
    $tmpDir="$origDir/tmp-compilers";
    if ( -e $tmpDir || ! (mkdir $tmpDir)) {
        #$tmpDir = "";
        &fail("* creating temporary working directory","$tmpDir already exists or could not be created; stopping");
    }
    chdir $tmpDir;

    #--- untar -----------------
    &message("* untarring $origDir/$tarName in tmp dir\n");
    $untar=`tar zxvf $origDir/$tarName 2>&1 `;
    if ($?) {
        &fail("untar",$untar);
    }
    ($distDir=$tarName) =~ s/.tar.gz//;
    chdir $distDir;
    
    #--- configure -----------------
    &message("* running configure $common_options $config\n");
    ($distDir=$tarName) =~ s/.tar.gz//;
    $configOut=`./configure $common_options $config > $origDir/regression-tests/compiler-results/$tag.cfg 2>&1`;
    if ($configOut =~ /error[: ]/i || $?) {
        &fail("configure",$configOut);
    }

    #--- run make -------------------
    &message("* running make\n");
    $make=`make -j4  > $origDir/regression-tests/compiler-results/$tag.bld 2>$origDir/regression-tests/compiler-results/$tag.err`;
    # be careful about how we check for errors in case we trigger
    # intel warnings
    if ($make =~ /^[Ee]rror[: ]/ || $make =~ / [Ee]rror[: ]/ || $?) {
        &fail("make",$make);
    }
    
    #--- run make check -------------------
    &message("* running make check\n");
    $makecheck=`make check  > $origDir/regression-tests/compiler-results/$tag.chk 2>&1`;
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
    
    # return things to their initial state (and hopefully avoid "missing-directory" issues)
    chdir $origDir;

    # remove the temporary dir
    system("rm -Rf $tmpDir");
    
    return 1;
}
