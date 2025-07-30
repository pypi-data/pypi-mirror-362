#!/usr/bin/env python
"""
Script to check whether we have a memory leak when accessing the "str" element
from a SelectorPython object
"""

import fastjet as fj
def fn(p): return True

sel = fj.SelectorPython(fn)
for i in range(0,int(1e7)): r = str(sel)

