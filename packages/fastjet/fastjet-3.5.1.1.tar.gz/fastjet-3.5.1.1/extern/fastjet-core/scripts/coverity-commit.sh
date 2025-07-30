#!/bin/bash
#
# to view the results point a browser to
# http://lcgapp10.cern.ch:8080/

COV_BIN=/coverity/cov-analysis/bin/
STREAM=FastJetTrunk

# in addition there can be --user and --password arguments (e.g. as in
# the script sent to us by Federico Carminati around 1/2 March 2016.
$COV_BIN/cov-commit-defects --host lcgapp10.cern.ch --port 8080 --stream $STREAM --dir cov-out >>  cov-out/log.txt
