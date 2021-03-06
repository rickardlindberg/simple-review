#!/usr/bin/env python

import glob
import os
import sys
import unittest

ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, "libs"))

suite = unittest.TestSuite()

for path in glob.glob("**/test_*.py"):
    if len(sys.argv[1:]) == 0 or path == sys.argv[1]:
        module_name = path.replace("/", ".")[:-3]
        __import__(module_name)
        module = sys.modules[module_name]
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))

if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
