reset
set term pdfcairo enhanced size 9cm,9cm
set out 'timings-lecture-notes.pdf'
set colors classic

set title "{/:Bold Time to cluster N particles}"

set xlabel 'N'
set format x "10^{%T}"
set log x
set xrange [90:110000]

set ylabel 'time (ms)'
set log y
set yrange [0.01:10000]
set format y "10^{%T}"
set ytics add ("0.01" 0.01,"0.1" 0.1, "1" 1,"10" 10,"100" 100)

set size square
set macros
set grid
set style textbox opaque noborder

set key bottom right

set label 100 '{/*0.5 2.90GHz Intel Core i7-7700T, g++ 7.3.1, Linux FC27; 1 hard + n minbias events}' at graph 1.04,1 rotate by 270 tc rgb '#666666'

m='< mergeidx.pl -f timings-tellus-fj332-akt050.dat '
radius="0.45"
set label 1 'FastJet 3.3.2, R=0.5' at graph 0.05,0.95 boxed

# just fj30 results
plot m.'"strategy = 202"'  u 1:(1000*$2) w l dt (4,4,4,4)  lw 3 lc 3              t 'CDFMidPoint',\
     m.'"strategy = 204"'  u 1:(1000*$2) w l dt 1          lw 3 lc 3              t 'SISCone',\
     m.'"strategy = 100 "' u 1:(1000*$2) w l dt (12,4,4,4) lw 3 lc 1              t 'k_t (ktjet)',\
     m.'"strategy = 1"'    u 1:(1000*$2) w l dt 1          lw 4 lc 1              t 'k_t (FastJet)',\
     m.'"strategy = 1001"' u 1:(1000*$2) w l dt 1          lw 3 lc rgb "#00cc00"  t 'C/A (FastJet)',\
     m.'"strategy = 2001"' u 1:(1000*$2) w l dt 1          lw 3 lc 7              t 'anti-k_t (FastJet)'

# plot m.'"strategy = 202"'  u 1:(1000*$2) w lp dt (4,4,4,4)  lw 3 lc 3              pt  2 ps 1.0 t 'CDFMidPoint',\
#      m.'"strategy = 204"'  u 1:(1000*$2) w lp dt 1          lw 3 lc 3              pt  7 ps 0.8 t 'SISCone',\
#      m.'"strategy = 100"'  u 1:(1000*$2) w lp dt (12,4,4,4) lw 3 lc 1              pt  9 ps 1.0 t 'k_t (ktjet)',\
#      m.'"strategy = 1"'    u 1:(1000*$2) w lp dt 1          lw 3 lc 1              pt  5 ps 1.0 t 'k_t (FastJet)',\
#      m.'"strategy = 1001"' u 1:(1000*$2) w lp dt 1          lw 3 lc rgb "#00cc00"  pt  6 ps 1.0 t 'C/A (FastJet)',\
#      m.'"strategy = 2001"' u 1:(1000*$2) w lp dt 1          lw 3 lc 7              pt  1 ps 1.0 t 'anti-k_t (FastJet)'

set output
