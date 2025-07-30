# gnuplot file

reset
set data sty linespoints
set ylabel 't (s)' 2
set xlabel 'N'
set format "10^{%T}"

set log

set label 1 'KtJet (N^3)'      at 981,3 right   font "courier,18"
set label 2 'FastJet'    at 3000,6.00   font "courier,18"
set label 3 'naive N^2'  at 3000,3.05   font "courier,18"

set label 4 'FastJet'    at 20900,0.6    font "courier,18"
set label 5 'CGAL N{/Symbol &i}ln{/Symbol &i}N' \
                         at 20900,0.3     font "courier,18"
set label 7 'FastJet'    at 1500,40e-4   font "courier,18"
set label 8 'tiled N^2'  at 1500,20e-4   font "courier,18"

set xrange [1e2:1e5]
set yrange [1e-5:2e1]

set label 11 'Tevatron' at 200,8e-5 center  font "Helvetica,18"
set arrow 11 from 200,5e-5 to 200,1.5e-5 lt 7

set label 12 'LHC (single' at 700,15e-5 center font "Helvetica,18"
set label 22 'interaction)' at 700,8e-5 center font "Helvetica,18"
set arrow 12 from 600,5e-5 to 500,1.5e-5 lt 7


set label 13 'LHC (c. 20' at 3000,15e-5 center font "Helvetica,18"
set label 23 'interactions)' at 3000,8e-5 center font "Helvetica,18"
set arrow 13 from 2700,5e-5 to 2500,1.5e-5 lt 7

set label 14 'LHC' at 50000,15e-5 center font "Helvetica,18"
set label 24 'Heavy Ion' at 50000,8e-5 center font "Helvetica,18"
set arrow 14 from 50000,5e-5 to 50000,1.5e-5 lt 7

set label 15 'Tevatron (D0)'   at 14000,15e-5 center font "Helvetica,18"
set label 25 'detector'        at 14000,8e-5 center font "Helvetica,18"
set arrow 15 from 9000,5e-5 to 6000,1.5e-5 lt 7


set pointsize 1.4

# mostly include the original timing results, except for
# N ln N where the new ones seem to be marginally better?

plot '../../../fifth_go/timings/timings-clever10.dat' w lp lt 7 lw 2 t '',\
     '../../../fifth_go/timings/timings-clever-1.dat' w lp lt 1 lw 2 t '',\
     '../../../fifth_go/timings/timings-clever-3.dat' w lp lt 2 lw 2 t '',\
     'timings-LHC50+minbias+mansorted-anubis.dat' i 3 w lp lt 3 lw 2 t ''


#        i 0 w lp lt 7 lw 2 t '',\
#     '' i 1 w lp lt 7 lw 2 t '',\
#    
#     '../../../fifth_go/timings/timings-clever2.dat'  w lp lt 3 lw 2 t '',\
#

#

