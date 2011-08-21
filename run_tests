#!/usr/bin/env python
import sys
import unittest
suite = unittest.defaultTestLoader.discover(".")
res = unittest.TextTestRunner(verbosity=1).run(suite)
if res.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
