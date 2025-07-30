# gnuplot file
reset

set size ratio -1
set sty data points

set xrange [-5:5]
set yrange [-pi:pi]

set ylabel '{/Symbol f}'
set xlabel 'y'

set xtics 1
set grid

set term fig big fontsize 14 linewidth 1
set output "ghost-extent.fig"

set border lw 2

plot '<4momview.pl < ../../example/data/HZ-event-Hmass115.dat' u 1:(abs($1)<3?$2:$2-100) w p pt 7 lt 0 ps 0.5 t ''

set output
