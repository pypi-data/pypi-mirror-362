#!/bin/bash
#
# assume everything has been built
#
# By default, the thread-safety tests are oly run if FastJet has been
# built w thread-safety enabled

function report_failure {
    echo '******* FAILED ******** '
    echo '  on execution of' $1
    exit -1
}

function header {
    echo
    echo "================================================================"
}

header
./PJtiming -n 1000 -sz 1000 || report_failure PJtiming

header
./cs_delete_self < ../example/data/single-event.dat ||  report_failure cs_delete_self

header 
./run_tests || report_failure run_tests

header
if ../fastjet-config --config | grep "Thread safety" | grep -q "yes"; then
    ./thread_safety_tests || report_failure thread_safety_tests
else
    echo "Thread-safety tests enabled only when thread safety enabled for fastjet"
fi

