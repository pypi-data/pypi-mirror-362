#!/bin/bash
# simple script to run coverity
#
# After running this, upload to the coverity web server with the
# coverity-commit.sh script

if [ ! -d cov-out ]; then
  mkdir cov-out
fi

COV_BIN=/coverity/cov-analysis/bin/

# build
$COV_BIN/cov-build --dir cov-out make -j 24 || exit 4
tail cov-out/build-log.txt || exit 5

# run 
$COV_BIN/cov-analyze --dir cov-out  --cpp -j auto --enable-callgraph-metrics --enable-parse-warnings || exit 6

