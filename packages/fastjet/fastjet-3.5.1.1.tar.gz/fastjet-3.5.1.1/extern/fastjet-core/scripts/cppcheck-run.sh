#!/bin/bash
#
# Run this to get a report from cppcheck
#
if [ ! -e reports ]; then
    mkdir reports/
fi
cppcheck -j4 --xml-version=2 src tools plugins examples \
         --enable=warning,performance,information,style 2>&1 | tee reports/cppcheck-result.xml
cppcheck-htmlreport --file=reports/cppcheck-result.xml --report-dir=reports --source-dir=.

