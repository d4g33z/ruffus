#!/usr/bin/env python
from __future__ import print_function
"""

    test_pausing.py

        test time.sleep keeping input files and output file times correct

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
try:
    import StringIO as io
except:
    import io as io
import re

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__









#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import re
import operator
import sys,os
from collections import defaultdict
import random

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888






#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
a = []

#
#    task1
#
@files(a)
def task1():
    """
    First task
    """
    print("Task1", file=sys.stderr)


import unittest

class t_save_to_str_logger:
    """
    Everything to stderr
    """
    def __init__ (self):
        self.info_str = ""
        self.warning_str = ""
        self.debug_str = ""
    def info (self, message):
        self.info_str += message
    def warning (self, message):
        self.warning_str += message
    def debug (self, message):
        self.debug_str += message

class Test_task(unittest.TestCase):

    def test_task (self):

        save_to_str_logger = t_save_to_str_logger()
        pipeline_run(multiprocess = 10,
                            logger = save_to_str_logger,
                            verbose = 1)
        self.assertTrue("@files() was empty" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)


    def test_newstyle_task (self):
        test_pipeline = Pipeline("test")
        test_pipeline.files(task1, a)

        save_to_str_logger = t_save_to_str_logger()
        test_pipeline.run(multiprocess = 10,
                            logger = save_to_str_logger,
                            verbose = 1)
        self.assertTrue("@files() was empty" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)

#
#   Necessary to protect the "entry point" of the program under windows.
#       see: http://docs.python.org/library/multiprocessing.html#multiprocessing-programming
#
if __name__ == '__main__':
        unittest.main()

