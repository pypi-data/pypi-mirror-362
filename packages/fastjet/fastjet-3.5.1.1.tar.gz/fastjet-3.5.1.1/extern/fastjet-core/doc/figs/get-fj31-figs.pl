#!/usr/bin/env perl
# small script to get the fj31 figures that have been updated, and make the
# pdf file too.
#
# Usage:  ./get-fj31-figs.pl
use warnings;
use File::Glob ':glob';
use Cwd;

$origdir="../../../issue-tracker/2014-07-auto-strategy-selection";
$thisdir=getcwd;
chdir $origdir;
system("svn up"); if ($? != 0) {die "problems updating svn in $origdir";}
chdir $thisdir;
system("svn up"); if ($? != 0) {die "problems updating svn in $thisdir";}

@files=glob('fj31*.eps');
foreach $file (@files) {
  ($orig = $file) =~ s/fj31[_-]//;
  $orig = "$origdir/$orig";
  $diff=`diff $file $orig`;
  chomp $diff;
  if ($diff) {
    print "$orig != $file\n";
    print "Copy original to here and create pdf? (y/n)";
    $ans = <>;
    if ($ans =~ /^y/i) {
      system ("svn rm --force $file");
      if ($? != 0) {die "problems deleting $file";}
      system ("svn cp $orig $file");
      if ($? != 0) {die "problems copying $orig";}
      system ("epstopdf $file");
      if ($? != 0) {die "problems creating pdf";}
    }
  }
}
#svn rm --force fj31*.eps fj31*.pdf
