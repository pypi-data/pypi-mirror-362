# gnuplot file

reset
set data sty linespoints
set ylabel 't / N (s)' 2.5
set xlabel 'N'
set format x "10^{%T}"
set format y "%.0t x 10^{%T}" 

set log x

set xrange [1e2:5e6]
#set grid
set yrange [3.5e-5:9e-5]
set ytics 1e-5

set pointsize 1.4

# 3000:1e5 with first file
a = -1.69e-5
b =  7.77e-6
# 4000:1e5 with first file
a = -1.83e-5
b =  7.89e-6
# 4000:1e5 with second file
#a = -1.93e-5
#b =  8.00e-6
#replot  'timings-LHC50+minbias+mansorted-anubis.dat' i 3 u 1:($2/$1) w p lt 3 lw 2 t ''

set label 10 'points on grid' at 1.1e5,5.1e-5
set label 11 'minimum bias'   at 2e4,6.3e-5 right

fit [3e3:1e7] a+b*log(x) 'timings-PtMin1000+area-LHC-highN-anubis.dat' u 1:($2/$1) via a,b
fit [3e3:1e7] c+d*log(x) 'timings-PtMin1000-LHC-highN-anubis.dat' u 1:($2/$1) via c,d
fit [3e3:1e7] e+f*log(x) 'timings-Minbias-LowPt-LHC-highN-anubis.dat' u 1:($2/$1) via e,f

set key left Left reverse

set label 1 'FastJet CGAL N ln N' at graph 0.47,0.96 center font "courier,bold,20"
set label 2 'measured timings versus fit of form (a + b ln N) N' at graph 0.47,0.9 center font "Helvetica,20"

plot a + b*log(x) w l lt 2 lw 1 t ''
replot e + f*log(x) w l lt 2 lw 1 t ''
replot 'timings-PtMin1000+area-LHC-highN-anubis.dat' u 1:($2/$1) w p lt 1 lw 2 t ''
#replot 'timings-PtMin1000-LHC-highN-anubis.dat' u 1:($2/$1) w p lt 2 lw 2 t ''
replot 'timings-Minbias-LowPt-LHC-highN-anubis.dat' u 1:($2/$1) w p lt 3 lw 2 t ''

#replot      'timings-Minbias-LowPt-LHC-anubis.dat'       i 4 u ($1):($2/$1)  w p lt 1 lw 2 t ''   

exit

#plot  'timings-clever2.dat' u 1:($2/$1) w lp lt 3 lw 2 t ''
#replot  'timings-minbias-thalie.dat' i 3 u 1:($2/$1*0.8) w lp lt 1 lw 2 t ''
#replot  'timings-TeV50GeV-thalie.dat' i 3 u 1:($2/$1) w lp lt 2 lw 2 t ''
#replot  'timings-thalie.dat' i 3 u 1:($2/$1) w lp lt 4 lw 2 t ''
#set auto y
#replot 'timings-OJF.dat' u 1:($2/$1)
