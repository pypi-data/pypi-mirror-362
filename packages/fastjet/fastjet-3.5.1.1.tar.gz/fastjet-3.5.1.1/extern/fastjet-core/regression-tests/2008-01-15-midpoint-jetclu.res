
FASTJET regression tests on Tue Jan 15 20:08:07 CET 2008

Reference exec: /home/salam/tmp/fastjet-2.1.0/example/fastjet_timing_plugins
Test exec:      ../example/fastjet_timing_plugins
Data file:      /home/salam/work/fastjet/data/Pythia-PtMin50-LHC-1000ev.dat
Nev used:       1000
Alg list:       midpoint, jetclu
Filter:         grep -v -e '^#' -e 'strategy' -e '^Algorithm:'


******* Running reference result for midpoint (-midpoint)
Running strategy 00 for midpoint
Number of differences wrt ref = 0


******* Running reference result for jetclu (-jetclu)
Running strategy 00 for jetclu
Number of differences wrt ref = 0
./regression-test.pl  279.63s user 2.13s system 99% cpu 4:43.40 total
