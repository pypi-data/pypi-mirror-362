#!/usr/bin/perl -w
#
# This script is part of the testsuite for all the clustering algorithms
# in FastJet.
#
# It works by running example/fasjet_timing_plugins for a jet
# definition, extracting either the jets (cone algs) or the written-out
# sequence (seq.rec. algs) and then taking the md5sum of the results.
#
# It contains a bunch of stored md5sums for various cases, against which
# it carries out a quick test.
#
#
# Various command-line options are available:

$usage= <<'END_USAGE';

  Usage: ./test-all-algs.pl [options]

  -datadir DIR      location of the directory containing the data with the
                    events that will be clustered. It is available from
                    https://gitlab.com/fastjet/fastjet-validation/data.git

  -fjtp-exec EXEC   location of the fastjet_timing_plugins executable

  -nev NEV          sets the number of events to use (default = 10)

  -alg ALGNAME      sets the alg name and all parameters other than R
                    [things separated by a : become separated by a
                    space in the final command]

  -R   R            sets R

  -strat STRAT      use only this strategy [1 == best]; multiple
                    colon-separated strategies may also be specified
                    (or comma-separated)

  -deposit DIR      puts the (unfiltered) output in a directory DIR
                    together with the sum

  -newdeposit DIR   the same but only deposits the file if it doesn't
                    already exist (whether as such or with a .gz)

  -perl             writes md5 output such that it can be pasted into
                    this program for future reference

  -newperl          similar, but only for things that we don't yet have

  -verbose          writes out a few extra details (e.g. the command
  being run). 

  -areas            run area configurations

  -bkgds            run background estimations

  -fjcore           uses fastjet_timing_plugins_fjcore, a version of
                    fastjet_timing_plugins built with fjcore rather
                    than the full fastjet 

 Full (non-md5) results of a 1000 event run are to be found in the
 following git 

     https://gitlab.com/fastjet/fastjet-validation/validation-ref

END_USAGE
# Or alternatively on tycho in
#
#     ~salam/work/fastjet/validation-ref-2008-10-30
#
# Known issues:
# -------------
# A main weakness is what will happen should we change the output format
# of floating points numbers (e.g. for jet pts, etc.)] (or if the
# compiler changes this)
#
#
# Adding algorithms:
# ------------------
#
# - make sure that "-newalg" (or whatever it's called) runs the new
#   algorithm in fastjet_timing_plugins. 
#
# - run "./test-all-algs.pl -alg newalg -nev {1|10|100|1000} -newperl"
#
#   Extra options can be given too: "newalg:-y:0.8" will run
#   fastjet_timing_plugins with options "-newalg -y 0.8".
#
#   the {1|10|100|1000} means you should carry out separate runs with 1,
#   10, 100, 1000 events, so as to get the checksums for each.
#
#   Each time you'll get a line of perl that is to be added to the
#   initialisation of the %refResults hash (in setRefResults()).
#
# - now rerun the command above, and check that the algorithm is
#   labelled "OK" on each run
#
# - run "./test-all-algs.pl -alg newalg -nev 1000 -deposit
#   SOME-DIRECTORY" 
#
#   that will place the raw results in SOME-DIRECTORY (I use
#   ~salam/work/fastjet/validation-ref-2008-10-30 -- ideally  everything
#   end up in the same place)
#
# - add "newalg" to the @algs array in setDefaults()
#
# - if you want things to be tested in the nightly build, make sure the
#   new algorithm is actually compiled -- i.e. add the appropriate
#   configure options to $configOpts in nightly-check.pl
#
# - commit and then run nightly-check.pl (nightly-check.pl deliberately
#   fails on uncommitted directories -- to avoid giving results based on
#   something not actually in the repository)
#
# - The next automatic run of nightly-check.pl will use an old
#   nightly-check.pl script (it runs the script from a special directory
#   and the script does the update only after starting...) and so your
#   new algorithm won't necessarily be configured (it will then be
#   labelled as unavailable -- or NA in the subject line).
#
#   It's only the following night that things will reach "equilibrium".
#
#
# $Id$
# ----------------------------------------------------------------------
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Cwd;


# set up the location of the data & other defaults (e.g. nev)
&setDefaults;
# set up the reference results
&setRefResults;

$verbose = "";
$depositNew = 0;
$dataDir = "";
$fjtpExec = "";
$unzipcmd = "gunzip -c";

# now allow user to play with things
while ($arg = shift @ARGV) {
  if    ($arg eq "-nev"       ) {$nev = shift @ARGV;}
  elsif ($arg eq "-datadir"   ) {$dataDir = (shift @ARGV); print "Using data directory $dataDir\n";}
  elsif ($arg eq "-alg"       ) {@algs = (shift @ARGV);}
  elsif ($arg eq "-fjtp-exec" ) {$fjtpExec = (shift @ARGV);}
  elsif ($arg eq "-R"         ) {$R = shift @ARGV;}
  elsif ($arg eq "-deposit"   ) {$deposit = shift @ARGV;}
  elsif ($arg eq "-newdeposit") {$deposit = shift @ARGV; $depositNew = 1;}
  elsif ($arg eq "-unzipcmd"  ) {$unzipcmd = (shift @ARGV);}
  elsif ($arg eq "-perl"      ) {$perlOut = "Perl Output:\n";}
  elsif ($arg eq "-newperl"   ) {$perlOut = "New Perl Output:\n";}
  elsif ($arg eq "-verbose"   ) {$verbose = 1;}
  elsif ($arg eq "-areas"     ) {$areas   = 1;}
  elsif ($arg eq "-bkgds"     ) {$bkgds   = 1; $areas=0;} # bkgd superseeds areas
  elsif ($arg eq "-strat" || $arg eq "-strategy")    {$defstrat = shift @ARGV;}
  elsif ($arg eq "-fjcore"    )  {$fjcore="_fjcore"; }
  elsif ($arg eq "-h" || $arg =~ /^--?help$/) {
    print $usage;
    exit 0;
  }
  else  {die "unrecognized argument $arg";}
}

#
&setDataFiles;

# set the executable name
&setExecutable;


# other settings

# now get the md5 sums
$returnCode = 0;
foreach $alg (@algs) {
  
  # the area configurations to support
  @areaconfigs=();
  if ($areas){
      if (exists($areaConfigs{$alg})){
          @areaconfigs = split(",", $areaConfigs{$alg});
      }
  } else {
      @areaconfigs = ("");
  }
  
  # the background estimation to support
  @bkgdconfigs=();
  if ($bkgds){
      if (exists($bkgdConfigs{$alg})){
          @bkgdconfigs = split(",", $bkgdConfigs{$alg});
      }
  } else {
      @bkgdconfigs = ("");
  }
  
  # the strategies to support
  if ($defstrat ne "") {
    @strat = split(/[:,]/,$defstrat);
  }
  elsif (exists($strategies{$alg})) {
    @strat = split(":",$strategies{$alg});
  } else {
    @strat = ("")
  }

  foreach $stratAlias (@strat) {
    # the loop variable is an alias to the member of the array;
    # but we will need to modify it below - so to avoid modifying the 
    # original array, we make a copy and modify that
    $strat = $stratAlias.""; 
    if ($strat ne "") {$stratcmd = "-strategy $strat"} else {$stratcmd=""}
    $strat = "s$strat" ; # =~ s/.*y /s/; # we'll need this in a clean form later
    
    foreach $areaAlias (@areaconfigs) {
      $area = $areaAlias.""; 
      if ($area ne "") {$areacmd = "-area $area"} else {$areacmd = ""}
      $area =~ s/area://g;
      $area =~ s/ /,/g;
      
      foreach $bkgdAlias (@bkgdconfigs) {
        $bkgd = $bkgdAlias."";
        if ($bkgd ne "") {
          $bkgdcmd = "-area -bkgd $bkgd";
        } else {$bkgdcmd = ""}
        $bkgd =~ s/area://g;
        $bkgd =~ s/bkgd://g;
        $bkgd =~ s/ /,/g;
      
        # decide what output to use (jets for cone algs, unique_write for cam, sequence for others)
        $out = $bkgd ? "" : $areas ? "-incl 0" : &isCone($alg) ? "-incl 0" : (($alg =~ /^cam/) ? "-unique_write" : "-write");
      
        # decide from which file we get the events 
        $localdataFile = &isee($alg) ? $eedataFile : $dataFile;
      
        # get the command line
        ($algsp = $alg) =~ s/:/ /g;
        #$cmdline = "$execName -$algsp $stratcmd -R $R $out -nev $nev 2>\&1 < $localdataFile";
        $cmdline = "$execName -$algsp $stratcmd -R $R $areacmd $bkgdcmd $out -nev $nev 2>\&1";
        if ($localdataFile =~ /\.gz$/) {
          $cmdline = "$unzipcmd $localdataFile | $cmdline";
        } else {
          $cmdline = "$cmdline < $localdataFile ";
        }
        if ($verbose) {print "Running $cmdline\n";}
        $res = `$cmdline`;
        $error = $?;
      
        # process the results into some decent form
        if ($res eq "" ) {
          $sum = "unavailable";
        } else {
          # remove all non-numerical lines [since these may change across versions]
          # except the lines containing "rho = " when background estimation is requested
          $filtered = "";
          foreach $line (split("\n",$res)) {
            if ($line =~ /^ *[0-9]/) {$filtered .= $line."\n";}
            if ($bkgds && $line =~ /rho = /) {$filtered .= $line."\n";}
          }
          $sum = $filtered eq "" ? "unavailable" :  md5_hex($filtered)
        }
      
        # now generate output and generate return codes
        $name = &fullName($alg,"$area$bkgd");
        if ($error) {
          $OK = "*** BAD (crash?) ***"
        } elsif (exists($refResults{$name}) && $sum ne "unavailable") {
          # we can have one or more reference results
          if (ref($refResults{$name}) eq "ARRAY") {
            # the default answer is BAD, but then if the answer matches any of
            # the availables references we label it as OK.
            $OK = "*** BAD ***";
            foreach $ref (@{$refResults{$name}}) {
              if ($sum eq $ref) {
                $OK = "OK";
                last;
              }
            }
          } else {
            $OK = ($sum eq $refResults{$name}) ? "OK" : "*** BAD ***";
          }
        } else { 
          $OK = "-";
          if ($sum ne "unavailable") {$refResults{$name} = $sum;}
        }
        if ($OK ne "OK" && $OK ne "-") {
          $returnCode += 1;
        }
        printf ("%-60s %-4s %-32s %s\n", $name, $strat, $sum, $OK);
      
      
        # record things for future, as perl code
        if ($sum ne "unavailable" && !exists($done{$name}) &&
            ($perlOut =~ /^Perl/s || 
             ($perlOut =~ /^New Perl/s && !exists($refResultsOrig{$name})) )) {
          $perlOut .= "  \"$name\" => \"$sum\",\n"
        }
      
        # optionally record things for future, in a file
        if ($deposit && !exists($done{$name}) && $sum ne "unavailable") {
          $depfile = "$deposit/$name.res";
          if (! (-e $depfile || -e "$depfile.gz")) {
            print "          > $depfile.gz\n";
            if (! -e $deposit) {mkdir $deposit || die "Could not create directory $deposit";}
            open (DEP, "> $depfile") || die "Could not open $depfile";
            print DEP $res;
            close DEP;
            system("gzip -f $depfile");
            open (SUM, "> $deposit/$name.sum") || die "Could not open $deposit/$name.sum";
            print SUM  "date ".`date`;
            print SUM  "machine: ".`uname -a`;
            print SUM  "directory: ".getcwd."\n";
            $configlog = "config.log";
            if (! -e $configlog) {$configlog = "../".$configlog;}
            print SUM  "configured: ".`egrep '^ +\\\$' $configlog | head -1`;
            print SUM  "cmdline: $cmdline\n";
            print SUM  "md5sum: ",$sum,"\n";
            close SUM;
          } else {
            print "\nWARNING: $depfile(.gz) already exists, not depositing output\n";
          }
        }
      
        $done{$name} = 1;
      } # bkgd
    } # area
  } # strat
} # alg

if ($perlOut) {print $perlOut;}

# exit with the returncode
if ($returnCode) {print "\n$returnCode test(s) failed\n";}
else             {print "\nAll available tests passed\n";}
exit $returnCode;

#======================================================================
sub isCone {
  (my $alg) = @_;
  return ($alg =~ /cone/i || $alg =~ /midpoint/ || $alg =~ /jetclu/)
}


#======================================================================
sub isee {
  (my $alg) = @_;
  return ($alg =~ /^ee/i || $alg =~ /jade/  || $alg =~ /spheri/ )
}


#======================================================================
sub fullName {
  (my $alg,$areabkgd) = @_;
  
  # decide from which file we get the events 
  $localdataFile = &isee($alg) ? $eedataFile : $dataFile;
  ($dataTail= $localdataFile) =~ s/.*\///;
  $dataTail =~ s/\.gz//;

  #$sep = "\@";
  $sep = ",";
  my $res = sprintf("$dataTail%snev%d%s$alg%sR%.2f",$sep,$nev,$sep,$sep, $R);
  if ($areabkgd ne ""){
      $res = "$res$sep$areabkgd";
  }
  return $res;
}

#======================================================================
sub setDataFiles {

  # if $dataDir was not set (command-line argument -datadir), then
  # try some hard-coded paths
  if (!$dataDir) {
    $username=`whoami`;
    chomp $username;
    if (( $username eq "greg") || ( $username eq "soyez") || ( $username eq "gsoyez")){
        $dataDir="~/work/fastjet/data";
    } elsif ( $username eq "gsalam"){
        $dataDir=$ENV{HOME}."/work/fastjet/data";
    } else {
        $gavinHome = `echo ~salam`;
        chomp $gavinHome;
        $dataDir="$gavinHome/work/fastjet/data";
    }
  }
  
  #$dataFile="$dataDir/Pythia-PtMin50-LHC-1000ev.dat";
  $dataFile="$dataDir/Pythia-PtMin50-LHC-10kev.dat.gz";


  # for the e+e- algorithms, use an e+e- event file
  $eedataFile="$dataDir/Pythia_Q1000_Zprime1000_nev1000.dat";

  # if either of the data files is not there, print out an error message
  # and exit with return code 127
  if (! -e $dataFile) {
    print "Error: data file $dataFile not found\n";
    exit 127;
  }
  if (! -e $eedataFile) {
    print "Error: data file $eedataFile not found\n";
    exit 127;
  }
  print("Using data files:\n- $dataFile\n- $eedataFile\n");


}

#======================================================================
sub setDefaults {


  @algs = ("kt", "cam", "antikt", "genkt:0.5", "siscone:-f:0.75","siscone:-f:0.50",  "jetclu", "pxcone",
            "d0runiicone", #GPS removed 2010-01-19, replace 2010-02-02
           "eekt", "eegenkt:0",  "eegenkt:-1", "eecambridge:-ycut:0.08", "eecambridge:-ycut:0.01",
           "trackjet", "atlascone", "cmsiterativecone", "jade:-excly:0.01", "d0runicone", "d0runipre96cone",
           "gridjet"
      );


  # for some algorithms we have multiple strategies to test
  %strategies = 
    (
     "kt"  => "1:-7:-6:-4:-3:-1:2",
     "antikt"  => "1:-7:-6:-4:-3:-1:2",
     "cam" => "1:-7:-6:-4:-3:-1:2:12",
     "eekt" => "1:31",
     "eegenkt:0" => "1:31",
     "eegenkt:-1" => "1:31",
    );

  # the different area configurations we'll consider
  %areaConfigs = (
      "kt"     => "-area:active,-area:explicit,-area:passive,-area:voronoi 1.0,-area:voronoi 0.9,-area:explicit -area:fj2,-area:active -area:fj2,-area:passive -area:fj2,-area:explicit -area:repeat 2,-area:explicit -ghost-area 0.1,-area:explicit -ghost-maxrap 4.0",
      "cam"    => "-area:active,-area:explicit,-area:passive,-area:voronoi 1.0,-area:explicit -area:fj2",
      "antikt" => "-area:active,-area:explicit,-area:passive,-area:voronoi 1.0,-area:explicit -area:fj2",
      "siscone:-f:0.75" => "-area:passive,-area:passive -area:fj2"
      );

  %bkgdConfigs = (
      "kt" => "-area:explicit -bkgd:jetmedian,-area:active -bkgd:jetmedian,-area:voronoi 1.0 -bkgd:jetmedian,-area:explicit -bkgd:csab,-area:active -bkgd:csab,-area:voronoi 1.0 -bkgd:csab,-area:explicit -bkgd:jetmedian -bkgd:fj2,-area:explicit -bkgd:jetmedian -rapmax 5.0 -ghost-maxrap 4.0,-area:active -bkgd:jetmedian -rapmax 5.0 -ghost-maxrap 4.0,-area:voronoi 1.0 -bkgd:jetmedian -rapmax 5.0 -ghost-maxrap 4.0,-area:explicit -bkgd:jetmedian -rapmax 5.0,-area:active -bkgd:jetmedian -rapmax 5.0,-area:voronoi 1.0 -bkgd:jetmedian -rapmax 5.0",
      # for the jet median subtraction tests, not the use of -bkgd:alt-ktR
      # This is needed because when using the same jet definition for
      # background estimation and subtraction, it is common for one of the
      # jets to coincide with the median background estimation jet, and then
      # the subtraction comparison of jet.pt() v. amount_to_sutract.pt()
      # should show something that is identically equal, but is prone to
      # rounding errors and the behaviour differs according to the system,
      # which affects whether the jet is set to zero pt or instead 4-vector
      # subtracted. 
      "cam" => "-area:explicit -bkgd:jetmedian,-area:active -bkgd:jetmedian,-area:voronoi 1.0 -bkgd:jetmedian,-area:explicit -bkgd:jetmedian -bkgd:alt-ktR 0.5345 -subtractor,-area:explicit -bkgd:jetmedian -bkgd:localrange -bkgd:alt-ktR 0.5345 -subtractor,-area:explicit -bkgd:jetmedian -bkgd:rescaling -bkgd:alt-ktR 0.5345 -subtractor,-area:explicit -bkgd:gridmedian -subtractor,-area:explicit -bkgd:gridmedian -bkgd:rescaling -subtractor",
      "antikt" => "-bkgd -bkgd:gridmedian"
      );

  $fjcore="";

  $defstrat = "";

  $nev = 10;
  $R = 0.6;

  $perlOut = "";
  $deposit = "";

  $areas = 0;
  $bkgds = 0;

  %done = ();

}

#======================================================================
sub setExecutable {
  # find out which executable to use based on what's locally
  # available, and failing that based on where we are
  if ($fjtpExec) {
    $execName = $fjtpExec;
  }  elsif (-x "fastjet_timing_plugins$fjcore") {
    $execName = getcwd."/fastjet_timing_plugins$fjcore"
  } elsif (-x "example/fastjet_timing_plugins$fjcore") {
    $execName = getcwd."/example/fastjet_timing_plugins$fjcore"
  } else {
    $execName  =  getcwd."/$0";
    $execName  =~ s/regression-tests.*//;
    $execName .=  "example/fastjet_timing_plugins$fjcore";
  }
  if (! -x $execName) {
    print "Error: executable $execName not found\n";
    exit 127;
  }
  print "Running $execName\n\n";  
}

#======================================================================
sub setRefResults {
  %refResults = (
  # 1 ev results
  "Pythia-PtMin50-LHC-10kev.dat,nev1,d0runiicone,R0.60" => "722f70cbb66fd5a5ee2a8a7733649daf",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,kt,R0.60" => "cca70ee3afa680bf574d94ccd6d48185",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,cam,R0.60" => "e3632acedd6516ed9c8eccfe515154dc",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,antikt,R0.60" => "13d2795fb237b1cd3459777eda8b1a19",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,genkt:0.5,R0.60" => "3da35b3292637395c41773535e145282",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,siscone:-f:0.75,R0.60" => "2d517cc2b23aad18c4afc8b58f99d842",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,siscone:-f:0.50,R0.60" => "54fd76a24330cf77658ebba9371ad8c5",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,jetclu,R0.60" => "05781404302f156dac9171e37bc09d44",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,pxcone,R0.60" => "c39185086e8ad3e35d13d32f2d03c41a",
  # ee algs ran on pp events
  #"Pythia-PtMin50-LHC-10kev.dat,nev1,eekt,R0.60" => "8caea0f93458e54c518b757793c50d2",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1,eegenkt:0,R0.60" => "d1d52a0e1b45b11590cab257c5af5152",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1,eegenkt:-1,R0.60" => "8923f3b1d1e3b3e58859e7363ad5f538",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,eekt,R0.60" => "6a7c5a8ec3700a82343fe597235c8fd7",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,eegenkt:0,R0.60" => "d251c9efd3c4c304d646aabb252d4280",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,eegenkt:-1,R0.60" => "df18bdb90f1088c7b3b572915a5c9b85",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,eecambridge:-ycut:0.08,R0.60" => "ccbb772f1af5102aa59fc923f3e625cc",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,eecambridge:-ycut:0.01,R0.60" => "cd039768d90103dbdc6dd2722abe712e",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,sisconespheri,R0.60" => "ee82bb2a82e902b36bdf0c50a72d0848",
  # old R def for eegenkt
  #"Pythia-PtMin50-LHC-10kev.dat,nev1,eegenkt:0,R0.60" => "2308c88202e0b0087c256c8a65efb5ce",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1,eegenkt:-1,R0.60" => "21753b7bab26ddb06f75b8eb7b1d3024",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,trackjet,R0.60" => "144b09c5042300633e2f687e16ffc17a",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,atlascone,R0.60" => "929de8bd58c1bc7fc5cbbef781031ad3",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,cmsiterativecone,R0.60" => "d789dbd3daf07e747ca4541e109c8e0a",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1,jade:-excly:0.01,R0.60" => "77ef328afb881e59866d8e72298b019b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,d0runicone,R0.60" => "49a06117d12d018c1c8aebbce38918fd",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,d0runipre96cone,R0.60" => "ceb8fecf1bced37b378b749cf05a673c",
  "Pythia-PtMin50-LHC-10kev.dat,nev1,gridjet,R0.60" => "67cdcbf70da1ee0e49c91519b29b27e3",

  # 10 ev results
  "Pythia-PtMin50-LHC-10kev.dat,nev10,genkt:0.5,R0.60" => "f3befadd9c96dab695310b994dc5cda5",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,eekt,R0.60" => "1ab6f607fc1acec7c4aa337307347ea0",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60"           =>    "d0b1a74bdcdcb9d18b8a129fb4789baa"  ,
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60" => "2d5b08cb9e07c0af81763865c37f8538",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60"       =>    "5ac9c93e9478cd583d2984b23e026af2"  ,
  "Pythia-PtMin50-LHC-10kev.dat,nev10,siscone:-f:0.75,R0.60"=>    "5a1463f29a19fd368cc2821edc39f99b",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,siscone:-f:0.50,R0.60"=>    "2a88c96f6410bf721bdfc48046ac9be1",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,jetclu,R0.60"       =>    "49a43a2db9fe715b47b4e80daacf8edc",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,pxcone,R0.60" => "f25494f08feb0b4398d45e6b2bf60b0a",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,d0runiicone,R0.60" => "f60a1928e1b584078611a257100a99a6",
  # ee algs ran on pp events
  #"Pythia-PtMin50-LHC-10kev.dat,nev10,eegenkt:0,R0.60" => "2c95f0f347a3ba4b35255ffc20da13d5",
  #"Pythia-PtMin50-LHC-10kev.dat,nev10,eegenkt:-1,R0.60" => "07aec8542d7687e0465958d3f2e5e86e",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,eekt,R0.60" => "7e8b864013f28ee0f4d8cbebe79abbd3",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,eegenkt:0,R0.60" => "79ea7d89f47427c3b348e6ff9bba3a66",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,eegenkt:-1,R0.60" => "faac5c2857ed616cd420060e7675466c",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,eecambridge:-ycut:0.08,R0.60" => "9e248c74c5c8b3729f1e96a538daf146",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,eecambridge:-ycut:0.01,R0.60" => "12f7dab534711378bf6809e5e31f13d3",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,sisconespheri,R0.60" => "f5224645e7bbe4580f4a37ec84ae418a",
  # old R def for eegenkt
  #"Pythia-PtMin50-LHC-10kev.dat,nev10,eegenkt:0,R0.60" => "e77d363d2ea067bd62d98e7b62bba772",
  #"Pythia-PtMin50-LHC-10kev.dat,nev10,eegenkt:-1,R0.60" => "aec87012ed66823e2f30862f57307d93",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,trackjet,R0.60" => "c6bbf392b1a1712256f260d7aeb52267",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,atlascone,R0.60" => "212c22dd6f1901657a2ff7df0c07badc",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cmsiterativecone,R0.60" => "069f4c6693f154e67e0e49cd9fc29786",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev10,jade:-excly:0.01,R0.60" => "876ee902b4680c3ec1ef189a82308927",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,d0runicone,R0.60" => "1c6eb67467c3354de464748d8bf67680",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,d0runipre96cone,R0.60" => "178140344e6f6d536ee4f2b1e1ff1a13",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,gridjet,R0.60" => "7b278a890ffc454f48c01eeabb1d0aef",

  # 100 ev results
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60" => "15b23d6d954c796682214d598f526f6a",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60" => "9530ca5b1e1680bd2da6714fa42a13a6",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60" => "66bb86601eaf4daa50aa601af175e8a3",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,genkt:0.5,R0.60" => "6663b7c49724212f279ae3407bf6c8cd",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,siscone:-f:0.75,R0.60" => "8a6cb5d7533dcd8553fefb9dbe38e344",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,siscone:-f:0.50,R0.60" => "ba6fdee02d2fb12d6d49267c428190b9",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,jetclu,R0.60" => "8948d26cacb802bf5e2e6c1cf89dabff",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,pxcone,R0.60" => "a3781182e4a363725b0929023dc27628",
  # result before addition of -fno-inline on 32 bit machines
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,d0runiicone,R0.60" => "a7430e1528ffcf20b3098959c7aa257d",
  # result with inclusion of that (should be consistent across 32 and 64 bits)
  "Pythia-PtMin50-LHC-10kev.dat,nev100,d0runiicone,R0.60" => "7058932e29b3979f4159a384a880770b",
  # ee algs ran on pp events
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,eekt,R0.60" => "7388d3917738969fb7fdf518af0dca78",
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,eegenkt:0,R0.60" => "f4c2804090331b997a1f4fe1ea10ee61",
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,eegenkt:-1,R0.60" => "59e20c82081eb5d584156b82175e9162",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,eekt,R0.60" => "ca2228232a53941082b1e0c4d4b91e28",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,eegenkt:0,R0.60" => "3bf1d61b8837bb42bfc1c00ad9ec1606",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,eegenkt:-1,R0.60" => "dd3222176571e51a4bb4d8d9876dea51",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,eecambridge:-ycut:0.08,R0.60" => "b248aa2ad20544720df26c3886e11e5c",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,eecambridge:-ycut:0.01,R0.60" => "420d8b18e3ecbdd6de1fed5f3533e811",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,sisconespheri,R0.60" => "6d41454cd628fab08b802da7c7461fbe",
  # old R def for eegenkt
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,eegenkt:0,R0.60" => "c210893596b56046573c60603e4a3e5b",
  #"Pythia-PtMin50-LHC-10kev.dat,nev100,eegenkt:-1,R0.60" => "905525747cad0344b6826514cd4cc618",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,trackjet,R0.60" => "bc388ed856a9f20ce6336201ce8f6afa",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,atlascone,R0.60" => "5467ef8e5f63bf3206f781f8d85d2c42",
  # "d5bc5a6427cc7af883b2329e45ee0d7a", # plain 'sort', gcc4.4
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cmsiterativecone,R0.60" => "afd780e095e04bce14dc8587d0736e48",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev100,jade:-excly:0.01,R0.60" => "7ce00dc7a5f676552c447fce5b8a0197",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,d0runicone,R0.60" => "62b7fc59816298800cb5aac3b3424d1c",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,d0runipre96cone,R0.60" => "ba82d640e1763ad03956ee9428cb67e3",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,gridjet,R0.60" => "0cef78fa4910f6519642e8b7f5097a5b",

  # 1000 ev results
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60" => "ae0b4d26e5244cfb551d41097fad3543",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60" => "ed14ae31b5ebd2df39dafae3f800040f",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60" => "d4a7e6146a9856e5be1cf67d59e1ee44",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,genkt:0.5,R0.60" => "22b8a8f3126f7b11d9f42cfe3bc20d73",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,siscone:-f:0.75,R0.60" => "e2333f97f0b69d858ec33ee8537882bf",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,siscone:-f:0.50,R0.60" => "65f5ca86e1db411f55892831ca6aad0b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,jetclu,R0.60" => "57ff3c751ab1d2f82673cd28fdb9e991",
  # pxcone differs between 32/64 bit machines (and compilers?); the answer here is
  # for a 64 bit gfortran
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,pxcone,R0.60" => "a15a20876c52578b9b4b07a96b67a13a",
  # result before addition of -fno-inline on 32 bit machines
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,d0runiicone,R0.60" => "8687da1a072268000a5c0d132fb37596",
  # result with inclusion of that (should be consistent across 32 and 64 bits)
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,d0runiicone,R0.60" => "26796bd9e42aa4b2ccae678074714613",
  # ee algs ran on pp events
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,eekt,R0.60" => "59fe2638f8df87a48bda2b8d1490034e",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,eegenkt:0,R0.60" => "f282981b9ff8e2db65fa0dd7aa1e9e44",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,eegenkt:-1,R0.60" => "719609342c170c7ef74e758f1cc28988",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,eekt,R0.60" => "5d88b51cdc8581ddffe3110081f3c3dd",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,eegenkt:0,R0.60" => "acd7c1540ddf0889ea73d7daddc1a590",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,eegenkt:-1,R0.60" => "3a5cd000d227f72752e4d5bc98a28e3d",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,eecambridge:-ycut:0.08,R0.60" => "00eb9436e2f8458c01b495c58e5b30d3",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,eecambridge:-ycut:0.01,R0.60" => "cb9ea9ba8b46cbbe4f663cd34e53c8f1",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,sisconespheri,R0.60" => "ee84e72d42238d4127df28ea337fa633",
  # old R def for eegenkt
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,eegenkt:0,R0.60" => "48cb5d5a8a5f636d07569745e5be29e4",
  #"Pythia-PtMin50-LHC-10kev.dat,nev1000,eegenkt:-1,R0.60" => "e54ecd5d535f2f3d7ddffc1bfd43462c",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,trackjet,R0.60" => [
    "6ece27a60cc0f49071fd534ddc7de7b2", #< for Intel output with "630: 197 with 301; y = 0.0927494" = 0.0927494499636188 | gitlab issue #6: this comes from a rounding
    "4392b58deff6e965751186ce60cd852b"  #< for M2Pro output with "630: 197 with 301; y = 0.0927495" = 0.0927494500156269 | error in mass of a rap=7.8 particle
  ],
  #    ["865e8763a52f63e43bb5ac781a8087f1","ac8025d4f4a0349f3f9af6538ace8cbb"], # plain 'sort'
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,atlascone,R0.60" => "d9cdb2a3ad52496fc5a1a4b6bfc7a363",
  # "5efdfffa446604f043c0444bc09e0f8a", # plain 'sort' gcc 4.4
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cmsiterativecone,R0.60" => "31a543ee68e64eb67d5b242188cb7aab",
  "Pythia_Q1000_Zprime1000_nev1000.dat,nev1000,jade:-excly:0.01,R0.60" => "b4aef5930856daafb294ddce66834bc7",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,d0runicone,R0.60" => "a475ca9a5bdcf9278ccfe8854095dfef",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,d0runipre96cone,R0.60" => "d9e503ea1cb13767ca5decf53bb001d1",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,gridjet,R0.60" => "e0788aaebe307721157b21255af7d235",

  # area, 10 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active" => "a857d484f8d3e5cb8321eaaf09de4638",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit" => "522c6fcb5f3b8a7560abbd816019a70e",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-passive" => "e606193f78f1f10e6f5c36f61764f297",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,1.0" => "e606193f78f1f10e6f5c36f61764f297",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,0.9" => "12662cb228f3345af42192344789a5cd",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-fj2" => "d0b43e8cb0294daf8d491ecee10300dc",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active,-fj2" => "f30601633041546e2f7ed1b9967909f6",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-passive,-fj2" => "e606193f78f1f10e6f5c36f61764f297",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-repeat,2" => "522c6fcb5f3b8a7560abbd816019a70e",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-ghost-area,0.1" => "b0d12e8546a57fd663f954c0ce18482f",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-ghost-maxrap,4.0" => "992dc0a76b7afc207d28bcfd3771ccab",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-active" => "d3f0ef5e118c751c1318d6f1db2cc7c0",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit" => "c7a1db0f1832097b72f405da3b53e485",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-passive" => "e9904f8e41ba96203a81823120a71a59",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-voronoi,1.0" => "b6e547082b6bffe5d1143ec8e8d72dcf",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-fj2" => "d8ce4026f92569f6a75118a3b0df1951",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-active" => "47608200f99c35d27f5040d7bb7678ed",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-explicit" => "bf11ce6a36164ebe1aff5c46a6d656a3",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-passive" => "47608200f99c35d27f5040d7bb7678ed",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-voronoi,1.0" => "c96bca9f2c4517bfa22f57d5e71bfeed",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-explicit,-fj2" => "77622c640ca3e4fe630e1b6e7dfec695",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,siscone:-f:0.75,R0.60,-passive" => "6cf4e4d825edd8f9daf3dfbfed997c46",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,siscone:-f:0.75,R0.60,-passive,-fj2" => "38c054fd35f87bc4e332c3745bc3a0de",

  # area, 100 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active" => "31e0fe8d8c81b803f9713cacbbf16938",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit" => "9a1f08c3d0d7e6e4f29687ea04e34087",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0" => "215ec264665d5a5d0220d4a8ca519ce0",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-passive" => "215ec264665d5a5d0220d4a8ca519ce0",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,0.9" => "31f941fef9bac1a14b30f372b0b3251b",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-fj2" => "4f52cd1c716131a8982ea79cbcc23290",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-fj2" => "fcc2fbc6a5fef61e83da2c7ebdf53f46",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-passive,-fj2" => "215ec264665d5a5d0220d4a8ca519ce0",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-repeat,2" => "9a1f08c3d0d7e6e4f29687ea04e34087",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-ghost-area,0.1" => "e69f568722c8ce83fc0783266f8bf617",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-ghost-maxrap,4.0" => "7ecb0d70643dc38c4208a92fbcac1b85",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-active" => "52528032687595b40bb0e29a05020325",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit" => "549cca44efdfe827da4d13d65c2b3100",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-passive" => "d5379263f0c778de3be6e48d306434a9",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-voronoi,1.0" => "378aa776c344e9c9bdd0f3f07a117e98",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-fj2" => "b368f513f546e4f40e093390bc9505a3",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-active" => "0ecaebf9695875119ca508a50efa0a08",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-explicit" => "c4e895f2a8b383fbf1ac4aa4b28957cb",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-passive" => "0ecaebf9695875119ca508a50efa0a08",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-voronoi,1.0" => "5b9669a54aac68fc9c62ecb3b663503c",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-explicit,-fj2" => "b9feaabc5b0d071535c1af6bfacd1233",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,siscone:-f:0.75,R0.60,-passive" => "f374fa40e92420107a5d22bc6777c614",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,siscone:-f:0.75,R0.60,-passive,-fj2" => "fc6da7685b78a98401d8e80caa8897d5",

  # area, 1000 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active" => "cfeafd478cb06f6d4088db69332961f1",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit" => "66af0392ecb712f55b0e51d3083fd479",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0" => "2d86e328dad56a5b8711caef484af163",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-passive" => "2d86e328dad56a5b8711caef484af163",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,0.9" => "2ba8d1b311aad775d5482d9bfb33dc3a",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-fj2" => "860901000b0d2d270157138d3ed370dc",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-fj2" => "f9709d772ec5a1c5826524a891dd2a94",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-passive,-fj2" => "2d86e328dad56a5b8711caef484af163",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-repeat,2" => "66af0392ecb712f55b0e51d3083fd479",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-ghost-area,0.1" => "a5428690fcf1da5e7070d6f092345ea8",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-ghost-maxrap,4.0" => "6caad01ff496ed9b37a8ad8b5f1f9266",
      # NB: the folllowing comes out different, on Gavin's macbook pro retina, 126529b37765562384705663b71f2912 
      #     Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
      #     Target: x86_64-apple-darwin13.3.0
      #
      #     An explicit check shows that a single least-significant digit is responsible for the different.
      #     The other cam areas also come out different, but there we haven't yet checked that it is just
      #     a single digit. One test of kt areas also came out different, so this issue may actually be
      #     be there for all areas.
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-active" => "911048ad2b03b38e62d1f8ddb4d95095",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit" => "741df147c16e55768cba1b892b35721f",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-passive" => "9b95ee58eda1fc7cf827410c9e87eee9",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-voronoi,1.0" => "d91cd694340c47e431a0444ac233d31d",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-fj2" => "ee3dafe1f5be9ee4c7af48f5a5dfaf18",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-active" => "16b4a7005ed6de5e826a0435f13ff48b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-explicit" => "81b2fa4fb07682b039f5a649959e9f0b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-passive" => "16b4a7005ed6de5e826a0435f13ff48b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-voronoi,1.0" => "e846d92e5150dd8f055d4aa4110a8cc4",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-explicit,-fj2" => "a27db35a91a061b8be9d4c6fe6ef76e7",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,siscone:-f:0.75,R0.60,-passive" => "84644868977ce3697b627e2c6da5c4df",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,siscone:-f:0.75,R0.60,-passive,-fj2" => "706092cb0ab1ae50ae9b0e5193201985",

  # background estimation, 10 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-jetmedian" => "3d4faa80c3a1faf3eadfc17c3442a0d3",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active,-jetmedian" => "dceadfa4cffcf3098609bc307b460327",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,1.0,-jetmedian" => "b0b188efa3201fc3f21ad97854509428",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-csab" => "3338b89d9440b3ac486719e396112008",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active,-csab" => "423fcc234a5e9ec580dc6893a52955e8",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,1.0,-csab" => "10653d64708760c53078e2451abcc151",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-jetmedian,-fj2" => "3338b89d9440b3ac486719e396112008",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "d8d89d990e1db31aedf199077cad2527",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "db78d31858be7c763def8678e3990f24",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "eb78d9b639ff2f8ef5930951749a8a78",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0" => "a7aa3434e75eb374c24583e385d7db8b",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-active,-jetmedian,-rapmax,5.0" => "ca4e24824ccf136ee5d151d65f8e79a7",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0" => "da13297329357649657f471748337d51",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-jetmedian" => "a2526d91d986caf7e60eb3b3abc5147d",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-active,-jetmedian" => "92970278b93d44dcac89d33d34511392",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-voronoi,1.0,-jetmedian" => "c43248cc949b873772160e1376fb5271",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,antikt,R0.60,-bkgd,-gridmedian" => "acffa42fb1443e6711fd59309047354d",

  # background estimation, 100 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian" => "76a1b4b291461a6d855cdc7c9a4bfe77",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-jetmedian" => "4e4d025bab689c2d98f10318f000dfc4",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-jetmedian" => "0c2822ffd78b6eac49db00278f56e6ca",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-csab" => "017511a0e37f43b776c980230f9a3bee",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-csab" => "c2d225beba88e0fb29a84eb1e33b9557",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-csab" => "9f213b2119656eeeb7bbd6fea6413827",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian,-fj2" => "017511a0e37f43b776c980230f9a3bee",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "450b94cefd3bc202683a4619aa4a8992",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "0b0ff0bb78e561891434119e910eee7e",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "cbe108798cd2726fd27320e5fadf3ae2",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0" => "af18b3e724e9be24789373c242a171aa",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-jetmedian,-rapmax,5.0" => "bba76f02f180948fe6f3c42dde71e690",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0" => "5d18e1c0bb03e4158205a9b84291d79b",
  # old results, from when rapmax (or etamax) was being applied only to +ve rapidities
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "450b94cefd3bc202683a4619aa4a8992",
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "0b0ff0bb78e561891434119e910eee7e",
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "ec3cce22c3de08aea065b5fd07538460",
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0" => "3c6fbf167c4347fa101e3f0be405c634",
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-active,-jetmedian,-rapmax,5.0" => "c07a3d3ac4d0aa95b24502a0a77712a6",
  # "Pythia-PtMin50-LHC-10kev.dat,nev100,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0" => "7a76e0098ea17b50ae0b584241082873",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-jetmedian" => "c81df2cfd3dde6bcf98d23297c31fba8",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-active,-jetmedian" => "bc6878256d7b055834b4314c391513eb",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-voronoi,1.0,-jetmedian" => "a9c0dac86b06184c771773a8654a6911",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,antikt,R0.60,-bkgd,-gridmedian" => "c70b84db6d20765ec343bc79b0da2c6c",

  # background estimation, 1000 ev results (only strategy 1)
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian" => "5510a3094432167877c4468d112e9550",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-jetmedian" => "311f2ea5548c6dd24f469430c970f698",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-jetmedian" => "45fb65abd570a1ad8f7f4c951f27984f",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-csab" => "63f617afc3bbdb5930e4783cfd585c88",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-csab" => "5757c5aeebc440b45a55701a1f3f30d2",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-csab" => "ba0783116682acca53334078f08345c4",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian,-fj2" => "63f617afc3bbdb5930e4783cfd585c88",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "817b10e575d988741e01d77e4826b753",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "f11a3c8c097b526d3014bcf990a49cab",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "11501419b03dcdd16713a46658d1ce2b",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0" => "3686a078c710c8433ec92765ce95385d",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-jetmedian,-rapmax,5.0" => "56236ecc244a82057225302ebf3ebbd8",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0" => "6ee5dace087ddff6922cf6150ff4636c",
  # old results, from when rapmax (or etamax) was being applied only to +ve rapidities
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "5260ed54a82fed944f7817c1dc10babd",
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "363f465770a130fa218b952bdd66d4ad",
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0,-ghost-maxrap,4.0" => "9eaee60e2d8be815487af555b24da6bb",
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-explicit,-jetmedian,-rapmax,5.0" => "6ccb0e1e01eaa44160ac2b3221e28ecb",
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-active,-jetmedian,-rapmax,5.0" => "fc7c1af0c02c45d149891bc8429c5fdd",
  # "Pythia-PtMin50-LHC-10kev.dat,nev1000,kt,R0.60,-voronoi,1.0,-jetmedian,-rapmax,5.0" => "b1531d96dfe7c36a35d168a637bf06ec",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-jetmedian" => "9412ab943b9d86725df068bd5b828000",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-active,-jetmedian" => "d6c00a93e70f0d14100c1e87e53604d3",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-voronoi,1.0,-jetmedian" => "099fcbb79303d70bede72ed4591fe380",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,antikt,R0.60,-bkgd,-gridmedian" => "35a2e74da09f6befd2bbcf9eb89b81d5",
  # 2021-02 background & subtraction additions (with alt-ktR when needed)
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-jetmedian,-alt-ktR,0.5345,-subtractor" => "e547cd35f6a60c62fca0310f64dc7257",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-jetmedian,-localrange,-alt-ktR,0.5345,-subtractor" => "ed486cba8137a2e401dc54dcc8bdbcaa",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-jetmedian,-rescaling,-alt-ktR,0.5345,-subtractor" => "ff34614c551f3ca521d7c9f35ce1d156",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-gridmedian,-subtractor" => "a8aa5125ffb3a822b1f0701f26256e33",
  "Pythia-PtMin50-LHC-10kev.dat,nev10,cam,R0.60,-explicit,-gridmedian,-rescaling,-subtractor" => "e1b06358874249f5375bedc4ed32a634",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-jetmedian,-alt-ktR,0.5345,-subtractor" => "1334c0bf9a2f2616a44d708e2df097fc",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-jetmedian,-localrange,-alt-ktR,0.5345,-subtractor" => "ab98f954017221ec25ba3e69bf227042",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-jetmedian,-rescaling,-alt-ktR,0.5345,-subtractor" => "01c722fe558068322e6b1426b42a5b52",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-gridmedian,-subtractor" => "e7c2442244f9d3412880d5d07a8db856",
  "Pythia-PtMin50-LHC-10kev.dat,nev100,cam,R0.60,-explicit,-gridmedian,-rescaling,-subtractor" => "262cbf3280709cbd7a5c0ffe39d4d73d",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-jetmedian,-alt-ktR,0.5345,-subtractor" => "4401beb61b6dc90fc259bfdd72629072",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-jetmedian,-localrange,-alt-ktR,0.5345,-subtractor" => "4bd05254e91289baadd129781a6f43bf",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-jetmedian,-rescaling,-alt-ktR,0.5345,-subtractor" => "06319d1484213063253fd88be9993e04",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-gridmedian,-subtractor" => "0fffb28f63770c18d2ee77044a415510",
  "Pythia-PtMin50-LHC-10kev.dat,nev1000,cam,R0.60,-explicit,-gridmedian,-rescaling,-subtractor" => "fb3aedadc7745020937eb6b4ff6d64b0"
  );

  %refResultsOrig = %refResults;
}  
