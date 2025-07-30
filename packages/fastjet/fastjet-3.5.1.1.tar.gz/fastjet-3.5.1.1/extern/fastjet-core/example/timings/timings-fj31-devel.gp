# gnuplot file

reset

set xlabel 'N'

set log x
set macros
set grid

set label 100 '{/*0.5 2.7GHz Intel Core i7, g++ 4.7.3, OS X 10.8.4; 1 hard + n minbias events, |{/Symbol h}| < 5}' at graph 1.04,1 rotate by 270 tc rgb '#808080'

set term postscript eps enhanced size 12cm,12cm font "Helvetica,26" solid lw 3 color
set size square
set xrange [90:110000]

#do for [name in "akt045 akt100"] {
name="akt045"
radius="0.45"
set object 1 rectangle from graph 0.0,0.9 to graph 0.48,1.0 fs fc rgb '#b0f0f0' 
set label 1 'anti-k_t, R = '.radius at graph 0.05,0.95 

merge='<mergeidx.pl -f timings-bisonOSX-fj31devel-etamax5-'.name.'.dat '

set title "Time to cluster N particles" font "HelvetivaBold"
set format "10^{%T}"
set log y
set ylabel 't / s' offset -1

# just fj30 results
filename="timings-fj30-".name.".eps"
set output filename
print merge.'strategy...2001'
plot merge.'strategy...2001' u 1:2 w lp lw 3 lc 0 t ''
set output
!gp-remove-100.pl @filename
!epstopdf @filename

# add in fj31
filename="timings-fj31-devel-".name.".eps"
set output filename
print merge.'strategy...2001'
plot merge.'strategy...2001' u 1:2 w lp lw 3 lc 0 t '',\
     merge.'strategy...1993' u 1:2 w lp lw 3 lc 1 t '',\
     merge.'strategy...1994' u 1:2 w lp lw 3 lc 3 t ''

set output
!gp-remove-100.pl @filename
!epstopdf @filename

#unset log y
set log y2
set format y "% g"
set format y2 "% g"
set yrange [1:12]
set y2range [1:12]
set ytics  ('1' 1, '2' 2, '3' 3, '' 4, '5' 5, '' 6, '' 7, '8' 8, '' 9, '10' 10)
set y2tics ('1' 1, '2' 2, '3' 3, '' 4, '5' 5, '' 6, '' 7, '8' 8, '' 9, '10' 10)
set ylabel 'speedup'
set title "Speed gain for N particles" font "HelvetivaBold"
unset label 100

filename="timings-fj31-devel-speedup-".name.".eps"
set output filename

print merge.'strategy...2001'
plot merge.'strategy...2001 strategy...1993' u 1:($2/$4) w lp lw 3 lc 1 t '',\
     merge.'strategy...2001 strategy...1994' u 1:($2/$4) w lp lw 3 lc 3 t ''

set output
!gp-remove-100.pl @filename
!epstopdf @filename
