#!/usr/bin/env python
"""Simple example to illustrate how to handle fastjet::Error
exceptions. 

Arguably, the greatest benefit of these exceptions is that the
interpreter recovers from mistakes made in interactive mode; best seen
trying the following in interactive mode:

import fastjet as fj
jd = fj.JetDefinition(fj.antikt_algorithm, 1e4)

For this script to work, make sure that the installation location for
the fastjet python module (cf. fastjet-config --pythonpath) is
included in your PYTHONPATH environment variable.

"""
from __future__ import print_function

import fastjet as fj
#import gzip

def main():

    trial_R_values = [0.1, 1.0, 10.0, 10000.0]

    for R in trial_R_values:
        try:
            jet_def = fj.JetDefinition(fj.antikt_algorithm, R)
            print("successfully created jet definition:",jet_def)
        except fj.Error:
            print("failed to create jet definition with R =", R)
            
if __name__ == '__main__':
    main()
