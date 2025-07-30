#!/usr/bin/perl -w
##

# basic number of repetitions. To be adjusted on different machines to
# give a "decent" run time, neither too fast (for small N) nor too 
# slow (for large N). Ideally, of the order of 1 second. 
# On the PowerPC G5 1.8 GHz $baserep = 100-200 looks fine.
$baserep = 700;

#############################################
#
# -3, -2, -1   -> N^2 algorithm
#  0           -> N^3
# 2, 3, 4      -> N ln N 
# 10           -> ktjet   
# 11, 12       -> JetClu , MidPoint
#
#############################################

# set of strategies to run
#@strategy = (-2,-1,0,2,10);
#@strategy = (-3,-1,2);
#@strategy = (3,4);
@strategy = (2);
#@strategy = (-3,-1,0,2,10,11,12);
#@strategy = (-3);
#@strategy = (11,12);
#@strategy = (-3,-1,2);
#@strategy = (12);
#@strategy = (11,12);

# number of runs to average over when getting
# timings. Remember that first run will be discarded
$nstat=6;
# if run time exceeds this, pare down the number of nstat
$runtimelimit=100; 

$datadir="../../../data/";

#$datafile="14TeV-1000ev.dat";
#$datafile="Pythia-Minbias-LowPt-LHC-10kev.dat";
$datafile="Pythia-PtMin1000-LHC-10kev.dat";
#$datafile="Pythia-Minbias-LowPt-LHC-1000ev.dat";
#$datafile="Pythia-PtMin50-TeV-1000ev.dat";
#$datafile="Pythia-1PtMin50+nMinBias-LHC-1001ev-semisorted.dat";
#$datafile="Pythia-1PtMin50+nMinBias+200-LHC-1001ev-semisorted.dat";
#$datafile= "Pythia-1PtMin50+nMinBias-mansorted.dat";

$datafile= $datadir.$datafile;

$hostname=`hostname -s`;
chomp($hostname);
#$filename="timings-".$hostname.".dat";
#$filename="timings-LHC50+minbias+mansorted-".$hostname.".dat";
#$filename="timings-Minbias-LowPt-LHC-".$hostname.".dat";
#$filename="timings-Minbias-LowPt-LHC-highN-".$hostname.".dat";
$filename="timings-PtMin1000+area-degenerate-LHC-highN-".$hostname.".dat";
#$filename="timings.dat";
open(OUT,">>$filename");

$uname=`uname -a`;
print OUT "# ",$uname;
if ( $uname =~ m/Darwin/ ) { $proc=`machine`; }   # to be improved
if ( $uname =~ m/Linux/ ) { 
      $proc=`grep "model name" /proc/cpuinfo | awk -F: '{ print \$2}' | sed s/\\(/[/g | sed s/\\)/]/g`; 
      chomp($proc);
      $proc = $proc." -- ".`grep "cpu MHz" /proc/cpuinfo | awk -F: '{ print \$2" MHz"}'`;
} 
print OUT "# ",$proc;
print OUT "# \n";



for (my $k=0; $k <= $#strategy; $k++ ) {

$strategy = $strategy[$k];
print OUT "# strategy = ",$strategy,"\n";

my $base_command = "";
if ( $strategy < 5 ) {
  # NB brackets are needed to get time to output to a stderr I can grab!!
  $base_command = "../../areas/areas-native -combine 1 -strategy $strategy -grid_scatter 0.0 < $datafile "
    #@lines=`(time -p ../../areas/areas-native -cell_area $cell_area -strategy $strategy -combine 1 -repeat $local_repeat < $datafile) 2>&1`;
}

#if ( $strategy == 10 ) {  # run ktjet 
#  #@lines=`(time -p ../ktjet_timing  -combine $combine -repeat $local_repeat < $datafile > /dev/null) 2>&1`;
#}
#
#if ( $strategy == 11 || $strategy == 12 ) { # run JetClu or MidPoint
#  #@lines=`(time -p ../run-JetCluMidPoint/JCMP_algorithm  $algo -combine $combine -repeat $local_repeat < $datafile > /dev/null) 2>&1`;
#}

print OUT "# running: ",$base_command,"\n";


# if ( $strategy >= 2 )  {$maxj = 16;}
# if ( $strategy <= -1 ) {$maxj = 13;}
# if ( $strategy == 0 )  {$maxj = 5;}
# if ( $strategy == 10)  {$maxj = 6;}
# if ( $strategy == 11)  {$maxj = 10; $algo = "-jetclu";}
# if ( $strategy == 12)  {$maxj = 6; $algo = "-midpoint";}

#$maxj = 100;
#if ( $strategy >= 2 )  {$maxcomb = 500;}
#if ( $strategy <= -1 ) {$maxcomb = 200;}
#if ( $strategy == 0 )  {$maxcomb = 13;}
#if ( $strategy == 10)  {$maxcomb = 20;}
#if ( $strategy == 11)  {$maxcomb = 200; $algo = "-jetclu";}
#if ( $strategy == 12)  {$maxcomb = 20; $algo = "-midpoint";}

$maxj = 100;
#if ( $strategy >= 2 )  {$maxcomb = 500;}
if ( $strategy >= 2 )  {$maxcomb = 9999;}
#if ( $strategy >= 2 )  {$maxcomb = 4000;}
if ( $strategy <= -1 ) {$maxcomb = 150;}
if ( $strategy == 0 )  {$maxcomb = 13;}
if ( $strategy == 10)  {$maxcomb = 13;}
if ( $strategy == 11)  {$maxcomb = 70; $algo = "-jetclu";}
if ( $strategy == 12)  {$maxcomb = 13; $algo = "-midpoint";}


print "Strategy = $strategy\n";
my $npart;
my $time = 0;
my $readtime;
for (my $j=1; $j <= $maxj; $j++) {
  $combine = $j;
  #if ( $j > 5 ) { $combine = int(exp($j/3)); }
  if ( $j > 13 ) { $combine = int(exp($j/5)); }
  if ($combine > $maxcomb) {last;}

  # arrange for situations where we have only 1 repeat?
  if ( $strategy >= 2 ) {$repeat = 1 + int($baserep/$combine);}
  if ( $strategy <= -1 ) {$repeat = 1 + int($baserep/$combine/$combine);}
  if ( $strategy == 0 || $strategy >= 10) {$repeat = 2 + int($baserep/5/$combine/$combine/$combine);}

  $cumultime = 0;

  # Adjust nstat so as not to run for too long (say > 100 s), based on
  # previous timing (nstat * time < 100 -> nstat = 100/time,
  # Always run at least twice...
  $nstat_local = int($runtimelimit/($time+1))+2;
  if ($nstat_local > $nstat) {$nstat_local = $nstat;}
  for (my $i=0; $i<$nstat_local; $i++) {

    # have two runs -- one where one just reads the data, and
    # one where one runs the algorithm 
    # Following definition of cell area should give a number of
    # particles that is the same as combine with 200 particles per event 
    $cell_area = 0.01 / ($combine*200/7600);
    print "combine = $combine, cell_area = $cell_area\n";
    for (my $irun = 0; $irun <2; $irun++) {
      my $local_repeat;
      my $command = "";
      if ($irun == 0) {$local_repeat = 0} else {$local_repeat = $repeat;}

      (my $full_command = $base_command) =~ s/\</\-repeat $local_repeat -cell_area $cell_area \</;
      #print $full_command."\n";
      @lines = `( time $full_command  ) 2>&1`;

      #print join("",@lines);
      foreach my $line (@lines) {
	if ($line =~ /number of particles = ([0-9]+)/) {$npart = $1;}
	if ($line =~ /user ([0-9\.]+)/) {$time = $1;}
	if ($line =~ /user\s+([0-9]+)m([0-9\.]+)/) {$time = $1*60+$2;} # alternative time format
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

    # discard first run. It's often slower. Caching?
    if ( $i > 0 ) { $cumultime = $cumultime + $time; }
    else {
      # choose an adaptive number of repeats
      if ($time < 1.0) {$repeat *= (1.0/$time); $repeat = int($repeat);}
      if ($time > 10.0) {
	$newrepeat = int(10.0/($time/$repeat))+1;
	if ($newrepeat < $repeat) {$repeat = $newrepeat}
      }
    }
  }
  
  print $npart." ".$cumultime/$repeat/($nstat_local-1)."\n";
  print OUT $npart." ".$cumultime/$repeat/($nstat_local-1)."\n";
}
# two blank lines for easy gnuplot separation
print OUT "\n\n";

}
