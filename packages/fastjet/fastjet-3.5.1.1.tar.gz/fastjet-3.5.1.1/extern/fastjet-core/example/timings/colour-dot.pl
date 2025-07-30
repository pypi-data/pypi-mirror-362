#!/usr/bin/perl -w
##
## Script for adding colour to dot files produced by google profiler.
##  pprof --dot kt_algorithm /tmp/profile2 >! original-file.dot
##  colour-dot.pl < original-file.dot > coloured-file.dot
##  
##  Then run: dot -Tps coloured-file.dot >! coloured-file.ps
##
$colors{"CGAL"} = '#ffff80';
$colors{"DnnPlane"} = '#a0ffff';
$colors{"Cylinder"} = '#a0ffa0';
$colors{"ClusterSequence"} = '#ffa0a0';
$colors{"_Rb_tree"} = '#ffa0ff';

$nline = 0;
while ($line = <STDIN>) {
  $nline++;
  
  if ($nline == 2) {
    print "size=\"11,7.5\";\nrotate=90;\n";
  } else {
    foreach $class (keys %colors) {
      $color = $colors{$class};
      if ($line =~ /$class/i) {$line =~ s/(shape=box)/style=filled,fillcolor=\"$color\",$1/ };
    }
  }
  print $line;
}
