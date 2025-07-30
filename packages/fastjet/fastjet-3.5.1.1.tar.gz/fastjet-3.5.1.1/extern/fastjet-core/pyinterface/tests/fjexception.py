#!/usr/bin/env python

import fastjet as fj

from exceptions import BaseException

p = fj.PseudoJet()

try:
    c = p.constituents()
except fj.Error as e:
    print "Caught fj.Error exception:"
    print "    ", e
    
