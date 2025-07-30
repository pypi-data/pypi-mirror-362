#!/usr/bin/env perl
#----------------------------------------------------------------------
# Script to update all headers
#
# Usage: from fastjet-release directory, run
#
#   ./scripts/update-headers.pl 
#
# Edit the header text down below to set the header you need.
# The program tries to maintain the copyright start year
# and the Id string that was already in there (though usually
# this will anyway be changed after a commit).
#----------------------------------------------------------------------

use warnings;

use File::Find;

@date=localtime();
$endyear=$date[5]+1900;
print "End year for copyright is $endyear\n";


# set up directories where we want to act
@dirs=("include","tools","src","plugins","fortran_wrapper", "scripts", "example");
print "Directories in which to search are: ",join(" ",@dirs),"\n";

print "Do you want to update the files (Y), or just do a dry run (N)?\n";
$answer=<>;
$dryrun = !($answer =~ /^y$/i);
$query=1;
if (!$dryrun) {
  print "Do you want to confirm for each file (Y/N)?\n";
  $answer=<>;
  $query = !($answer =~ /^n$/i);
}

$options={wanted => \&wanted, no_chdir => 1};
find($options, @dirs);

#----------------------------------------------------------------------
# a subroutine that decides if the file is among those we want
# to update, and then looks for the header in order to carry
# out the update
sub wanted($) {
  $file = $_;
  # NB: .txt files are updated notably for the fjcore preamble
  if ($file =~ /\.cc$/ || $file =~ /\.hh$/ || $file =~ /\.icc$/
      || $file =~ /\.f$/ || $file =~ /\.txt$/) {
  } else {
    return;
  }
  print "Examining $file\n";
  open (INFILE, "<$file") || die "Could not read from $file";
  $headerOn = 0;
  $contents = "";
  $header   = "";
  $changedHeader = 0;
  $fjcore = 0;
  $Id = "\$Id\$";
  my $copyrightstart="2005";
  while ($line = <INFILE>) {
    # check to see if we hit the start of the header
    if ($line =~ /^\s*\/\/(FJ)?STARTHEADER/) {
      $headerOn = 1;
    }
    # check for Id string, so as to put it back as it was
    if ($line =~ /\/\/.*(\$Id[^\$]*\$)/) {
      $Id = $1;
    }
    # check for copyright and get starting year
    if ($line =~ /^\s*\/\/ *Copyright .c. ([0-9]{4})-?.*Cacciari/) {
      $copyrightstart = $1;
    }
    if ($line =~ /fjcore/) {$fjcore = 1;}
    if (! $headerOn) {$contents .= $line;}
    else {$header .= $line;}
    if ($line =~ /^\s*\/\/(FJ)?ENDHEADER/) {
      $headerOn = 0;
      $newheader = &header($copyrightstart,$Id);
      if ($fjcore) {$newheader =~ s/FastJet/FastJet (fjcore)/m;}
      $contents .= $newheader;
      $changedHeader=1;
    }
  }
  close(INFILE);
  # if we've made changes, backup the file and write the new version
  if ($changedHeader) {
    if ($newheader eq $header) {
      print "   No change to header\n";
      return;
    }
    print "   Copyright start: $copyrightstart\n";
    print "   Id string: $Id\n";
    if (!$dryrun) {
      if ($query) {
        print "   Proceed for $file (Y/N/A[ll])?\n";
        $answer = <>;
        if ($answer =~ /^A/i) {$query = 0;}
        elsif ($answer !~ /^y$/i) {return;}
      }
      print "   Updating $file (backup will be made as .bak)\n";
      rename $file, $file.".bak";
      open (NEWFILE, ">$file") || die "Could not write to $file";
      print NEWFILE $contents;
      close(NEWFILE);
    }
  }
}

#----------------------------------------------------------------------
sub header($) {
  my ($copyrightstart,$Id) = @_;
  $output=
"//FJSTARTHEADER
// $Id
//
// Copyright (c) $copyrightstart-$endyear, Matteo Cacciari, Gavin P. Salam and Gregory Soyez
//
//----------------------------------------------------------------------
// This file is part of FastJet.
//
//  FastJet is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  The algorithms that underlie FastJet have required considerable
//  development. They are described in the original FastJet paper,
//  hep-ph/0512210 and in the manual, arXiv:1111.6097. If you use
//  FastJet as part of work towards a scientific publication, please
//  quote the version you use and include a citation to the manual and
//  optionally also to hep-ph/0512210.
//
//  FastJet is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with FastJet. If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------
//FJENDHEADER
";
  return $output;
}
