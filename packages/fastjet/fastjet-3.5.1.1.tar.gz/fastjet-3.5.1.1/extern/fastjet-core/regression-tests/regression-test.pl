#!/usr/bin/perl -w
#
# Script to help perform regression tests on FastJet, so as to ensure
# that different versions give identical results on some sample input.
#
# Currently certain bits and pieces need to be edited by hand to get
# the exact tests one wants.
#
# $Id$
#

# number of events to do
$nev=1000;

# the name of the input file
$inputfile=`echo -n ~salam/work/fastjet/data/Pythia-PtMin50-LHC-1000ev.dat`;

# executables and some default args
$exec="../example/fastjet_timing_plugins";
$refexec=`echo -n ~salam/tmp/fastjet-2.1.0/example/fastjet_timing_plugins`;
#$refexec=$exec;
$defargs=" -unique_write -nev $nev";


print "\nFASTJET regression tests on ".`date`."\n";

print "Reference exec: $refexec\n";
print "Test exec:      $exec\n";
print "Data file:      $inputfile\n";
print "Nev used:       $nev\n";

# command-line args to get the algorithm
#$alg{'kt'}      = "";
#$alg{'cam'}     = "-cam";
#$alg{'siscone0'} = "-siscone -npass 0";
#$alg{'siscone0ptmin5'} = "-siscone -npass 0 -sisptmin 5";
#$alg{'siscone1'} = "-siscone -npass 1";
#$alg{'antikt'} = "-antikt";
$alg{'midpoint'} = "-midpoint";
$alg{'jetclu'} = "-jetclu";


$strategy{"cam"}="-04:-03:-02:-01:+02:+03:+04:+00:+12:+13:+14";
$strategy{"kt"} ="-04:-03:-02:-01:+02:+03:+04:+00";
$strategy{"siscone"}="00";  # dummy strategy -- unused
$strategy{"siscone1"}="00";  # dummy strategy -- unused
$strategy{'siscone0ptmin5'} = "00";   # dummy strategy -- unused
$strategy{'antikt'} = $strategy{"kt"};
$strategy{'midpoint'} = "00";
$strategy{'jetclu'}   = "00";

# the following prevents trivial differences in the textual description
# of the algorithm from modifying the results
#$filter="grep -v -e '^#' -e 'strategy'";
$filter="grep -v -e '^#' -e 'strategy' -e '^Algorithm:'";

print "Alg list:       ".join(", ",keys %alg)."\n";
print "Filter:         $filter\n";

foreach $alg  (keys %alg) {
  $opt=$alg{$alg};
  $outref="/tmp/$alg-ref";
  print "\n\n******* Running reference result for $alg ($opt)\n";
  system("$refexec $defargs $opt < $inputfile  | $filter > $outref");
  foreach $strat  (split(":",$strategy{$alg})) {
    $out="/tmp/$alg-$strat";
    $outdiff="/tmp/$alg-diff";
    print "Running strategy $strat for $alg\n";
    system("$exec $defargs $opt < $inputfile | $filter > $out");
    system("diff $outref $out > $outdiff");
    $ndiff=`cat $outdiff | wc -l`;
    chomp($ndiff);
    print "Number of differences wrt ref = $ndiff\n";
    if ($ndiff ne 0) {system("head -40 $outdiff");}
    system("rm $out");
    system("rm $outdiff");
  }
  system("rm $outref");
}
