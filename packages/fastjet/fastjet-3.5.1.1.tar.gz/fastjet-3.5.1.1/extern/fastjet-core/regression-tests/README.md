Regression tests
================

This directory is one part of the testing framework for FastJet. For
each of the following scripts, look at the start of the script for usage
information.

- ```nightly-check.pl```: intended to be run every 24h across a range of
  platforms and email the results to the developers. It needs to be run
  before a release

- ```test-all-algs.pl```: runs a whole set of algorithms (uses
  fastjet_timing_plugins) and verifies that checksum of the result
  matches a checksum stored in the code

- ```test-contrib.pl```: downloads the latest fjcontrib and verifies
  that the installed version of FastJet works with it.

Scripts not in current use
--------------------------
- ```compiler-tests.pl```
- ```regression-test.pl```


