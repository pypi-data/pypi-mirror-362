#!/usr/bin/perl -w
##

# basic number of repetitions. To be adjusted on different machines to
# give a "decent" run time, neither too fast (for small N) nor too 
# slow (for large N). Ideally, of the order of 1 second. 
# On the PowerPC G5 1.8 GHz $baserep = 100-200 looks fine.
$baserep = 700;

#############################################
#
# -4           -> mixed N^2 (tiled geometrical) and N ln N (for min dij)
# -3, -2, -1   -> N^2 algorithm
#  0           -> N^3
# 2, 3, 4      -> N ln N 
# 12,13,14     -> N ln N for cam
# 100          -> ktjet   
# 101, 102     -> JetClu , MidPoint
#
# 100X         -> cambridge series
# 200X         -> antikt series

# 201, 202     -> plugins for JetClu and MidPoint
# 203          -> plugin for pxcone
# 204          -> plugin for siscone
# 212          -> MidPoint with seed threshold = 0?
#############################################

# set of strategies to run
#@strategy  = (-6);
#@strategy  = (1,-4,-5,-6,-7);
#@strategy  = (2000+1,2000+2,2000-4,2000-5,2000-6,2000-7);
@strategy  = (2000+1,2000-6,2000-7);
#@strategy  = (2000+1);
#@strategy  = (1,-4,-3,2,101);
#@strategy = (-2,-1,0,2,10);
#@strategy = (-3,-1,2);
#@strategy = (3,4);
#@strategy = (-4,-3,-1,2,12);
#@strategy = (1);
#@strategy = (1001,1012,996,2001,2012,1996);
#@strategy = (1);
#@strategy = (12);
#@strategy = (102);
#@strategy = (-3,-1,0,2,10,11,102);
#@strategy = (-3);
#@strategy = (11,102);
#@strategy = (-3,-1,2);
#@strategy = (102);
#@strategy = (2);
# for cones
#@strategy = (204);
#@strategy = (1,204,203,101,201,202,212);
#@strategy = (204);
#@strategy = (11,102);

#$radius=0.4;
#$radius=0.7;
#$radius=0.45;
$radius=1.0;

#$etamax=1e100;
$etamax=5.0;

# number of runs to average over when getting
# timings. Remember that first run will be discarded
$nstat=6;
# if run time exceeds this, exit the program
$runtimelimit=100; 

$datadir="../../../data/";

#$datafile="14TeV-1000ev.dat";
#$datafile="Pythia-Minbias-LowPt-LHC-10kev.dat";
#$datafile="Pythia-PtMin1000-LHC-10kev.dat";
#$datafile="Pythia-Minbias-LowPt-LHC-1000ev.dat";
#$datafile="Pythia-PtMin50-TeV-1000ev.dat";
#$datafile="Pythia-1PtMin50+nMinBias-LHC-1001ev-semisorted.dat";
#$datafile="Pythia-1PtMin50+nMinBias+200-LHC-1001ev-semisorted.dat";
$datafile= "Pythia-1PtMin50+nMinBias-mansorted.dat";

$datafile= $datadir.$datafile;

$hostname=`hostname -s`;
chomp($hostname);
#$filename="timings-".$hostname.".dat";
#$filename="timings-LHC50+minbias+mansorted-".$hostname.".dat";
#$filename="timings-LHC50+minbias+mansorted-R$radius-".$hostname.".dat";
#$filename="timings-LHC50+minbias+mansorted-R$radius-cones-".$hostname.".dat";
#$filename="timings-".$hostname."OSX-fj31devel-etamax5-akt100.dat";
$filename="tmp-".$hostname."-v31-akt100.dat";
#$filename="timings-Minbias-LowPt-LHC-".$hostname.".dat";
#$filename="timings-Minbias-LowPt-LHC-highN-".$hostname.".dat";
#$filename="timings-PtMin1000-LHC-highN-".$hostname.".dat";
#$filename="timings.dat";
open(OUT,">>$filename");

$uname=`uname -a`;
print OUT "# ",$uname;
if ( $uname =~ m/Darwin/ ) { $proc=`machine`; }   # to be improved
if ( $uname =~ m/Linux/ ) { 
      $proc=`grep "model name" /proc/cpuinfo | awk -F: '{ print \$2}' | sed s/\\(/[/g | sed s/\\)/]/g | sed 's/^/# /'`; 
      chomp($proc);
      $proc = $proc." -- ".`grep "cpu MHz" /proc/cpuinfo | awk -F: '{ print \$2" MHz"}' | sed 's/^/# /'`;
} 
print OUT "# $proc \n";
print OUT "# \n";



for (my $k=0; $k <= $#strategy; $k++ ) {

$strategy = $strategy[$k];
print OUT "# strategy = ",$strategy,"\n";

$maxj = 120;
$algo = "";
# allow for other seq.rec. algs
if (int($strategy/1000+0.5) == 1) {$algo = "-cam";     $strategy -= 1000;}
if (int($strategy/1000+0.5) == 2) {$algo = "-antikt" ; $strategy -= 2000; print "HELLO, doing anti-kt\n"}
#if ( $strategy >= 2 )  {$maxcomb = 500;}
#if ( $strategy >= 2 )  {$maxcomb = 9999;}
#if ( $strategy >= 2 )  {$maxcomb = 4000;}
if ( $strategy >= 1 )  {$maxcomb = 700;}
#if ( $strategy >= 1 )  {$maxcomb = 200;}
if ( $strategy <= -1 ) {$maxcomb = 150;}
if ( $strategy <= -3 ) {$maxcomb = 270;}
if ( $strategy <= -4 ) {$maxcomb = 700;}
if ( $strategy == 0 )  {$maxcomb = 13;}
if ( $strategy >= 12 && $strategy <= 14) {$algo = "-cam";}
if ( $strategy == 100)  {$maxcomb = 30;}
if ( $strategy == 101)  {$maxcomb = 350; $algo = "-jetclu";}
if ( $strategy == 102)  {$maxcomb = 13; $algo = "-midpoint";}
# the plugin versions of the algorithms
if ( $strategy == 201)  {$maxcomb = 70; $algo = "-jetclu";}
if ( $strategy == 202)  {$maxcomb = 50; $algo = "-midpoint";}
if ( $strategy == 212)  {$maxcomb = 10; $algo = "-midpoint -seed 0.0";}
if ( $strategy == 203)  {$maxcomb = 22; $algo = "-pxcone";}
if ( $strategy == 204)  {$maxcomb = 140; $algo = "-siscone";}


print "Strategy = $strategy, writing to $filename\n";
my $npart;
my $time = 0;
my $readtime;
my $algorithm;
for (my $j=1; $j <= $maxj; $j++) {
  $combine = $j;
  # use the following line with Pythia-1PtMin50+nMinBias-mansorted.dat
  if ( $j > 5 ) { $combine = int(exp($j/3)); }
  # use this for Pythia-PtMin1000-LHC-10kev.dat
  #if ( $j > 13 ) { $combine = int(exp($j/5)); }

  if ($combine > $maxcomb) {last;}

  # arrange for situations where we have only 1 repeat?
  if ( $strategy >= 1 )  {$repeat = 1 + 2*int($baserep/$combine);}
  if ( $strategy <= -1 ) {$repeat = 1 + 4*int($baserep/$combine/$combine);}
  if ( $strategy == 0 || $strategy >= 100) {$repeat = 2 + int($baserep/5/$combine/$combine/$combine);}

  $cumultime = 0;

  # Adjust nstat so as not to run for too long (say > 100 s), based on
  # previous timing (nstat * time < 100 -> nstat = 100/time,
  # Always run at least twice...
  $nstat_local = int($runtimelimit/($time+1))+2;
  if ($nstat_local > $nstat) {$nstat_local = $nstat;}
  for (my $i=0; $i<$nstat_local; $i++) {

    # have two runs -- one where one just reads the data, and
    # one where one runs the algorithm
    for (my $irun = 0; $irun <2; $irun++) {
      my $local_repeat;
      if ($irun == 0) {$local_repeat = 0} else {$local_repeat = $repeat;}
      if ( $strategy < 5 || ($strategy >= 12 && $strategy <= 14 || $strategy >= 200)) {
	# NB brackets are needed to get time to output to a stderr I can grab!!
	#@lines=`(time -p ../fastjet_timing -strategy $strategy $algo -combine $combine -repeat $local_repeat -r $radius < $datafile) 2>&1`;
          $cmdline="time -p ../fastjet_timing_plugins -strategy $strategy $algo -combine $combine -repeat $local_repeat -r $radius  -etamax $etamax < $datafile";
          #$cmdline="time -p $ENV{HOME}/work/jets/fjr-branches/fastjet-3.0.X-devel/example/fastjet_timing_plugins -strategy $strategy $algo -combine $combine -repeat $local_repeat -r $radius < $datafile";
          #print $cmdline,"\n";
	@lines=`($cmdline) 2>&1`;
      }

      if ( $strategy == 100 ) {  # run ktjet 
	@lines=`(time -p ../ktjet_timing  -r $radius -combine $combine -repeat $local_repeat < $datafile ) 2>&1`;
      }

      if ( $strategy == 101 || $strategy == 102 ) { # run JetClu or MidPoint
	@lines=`(time -p ../../../run-JetCluMidPoint/JCMP_algorithm  $algo -combine $combine -repeat $local_repeat < $datafile > /dev/null) 2>&1`;
      }

      foreach my $line (@lines) {
	if ($line =~ /number of particles *= *([0-9]+)/i) {$npart = $1;}
        if ($line =~ /^Jet Definition:/) {$algorithm = $line; chomp $algorithm;}
	if ($line =~ /user ([0-9\.]+)/) {$time = $1;}
      }
      # record the read time on the first round
      if ($irun == 0) {$readtime = $time;}
    }

    #@tmp = split " ",$lines[0];
    #$npart = $tmp[$#tmp];
    #
    #@tmp = split " ",$lines[2];
    #$time = $tmp[$#tmp];
    print "npart = $npart, repeat = $repeat, time = $time, readtime = $readtime\n";

    # now ensure that we deal with actual run time.
    $time -= $readtime;
    
    # protection in case our time comes out zero or negative
    # we increase the "repeat" and try again
    if ($i==0 && $time <= 0) {
      $i--;
      $repeat *= 3;
      next;
    }

    # discard first run. It's often slower. Caching?
    if ( $i > 0 ) { $cumultime = $cumultime + $time; }
    else {
      # choose an adaptive number of repeats
        print "time was $time\n";
      if ($time < 1.0) {$repeat *= (1.0/$time); $repeat = int($repeat);}
      if ($time > 5.0) {
	$newrepeat = int(5.0/($time/$repeat))+1;
	if ($newrepeat < $repeat) {$repeat = $newrepeat}
      }
    }
  }
  
  if ($j == 1) {
    print "# $algorithm\n";
    print OUT "# $algorithm\n";
  }
  print $npart." ".$cumultime/$repeat/($nstat_local-1)."\n";
  print OUT $npart." ".$cumultime/$repeat/($nstat_local-1)."\n";

  # don't go beyond this limit
  if ($time > $runtimelimit*0.5) {last;}
}
# two blank lines for easy gnuplot separation
print OUT "\n\n";

}
