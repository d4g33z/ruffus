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




parser = OptionParser(version="%prog 1.0")
parser.add_option("-D", "--debug", dest="debug",
                    action="store_true", default=False,
                    help="Make sure output is correct and clean up.")
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME",
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=1,
                  metavar="jobs",
                  type="int",
                  help="Specifies  the number of jobs (commands) to run simultaneously.")
parser.add_option("-v", "--verbose", dest = "verbose",
                  action="count", default=0,
                  help="Do not echo to shell but only print to log.")
parser.add_option("-d", "--dependency", dest="dependency_file",
                  #default="simple.svg",
                  metavar="FILE",
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT",
                  type="string",
                  default = 'svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), "+
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                    action="store_true", default=False,
                    help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")
parser.add_option("-M", "--minimal_rebuild_mode", dest="minimal_rebuild_mode",
                    action="store_true", default=False,
                    help="Rebuild a minimum of tasks necessary for the target. "
                    "Ignore upstream out of date tasks if intervening tasks are fine.")
parser.add_option("-K", "--no_key_legend_in_graph", dest="no_key_legend_in_graph",
                    action="store_true", default=False,
                    help="Do not print out legend and key for dependency graph.")
parser.add_option("-H", "--draw_graph_horizontally", dest="draw_horizontally",
                    action="store_true", default=False,
                    help="Draw horizontal dependency graph.")

parameters = [
                ]







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

#   Functions


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import time
def test_job_io(infiles, outfiles, extra_params):
    """
    cat input files content to output files
        after writing out job parameters
    """
    # dump parameters
    params = (infiles, outfiles) + extra_params

    if isinstance(infiles, str):
        infiles = [infiles]
    elif infiles is None:
        infiles = []
    if isinstance(outfiles, str):
        outfiles = [outfiles]
    output_text = list()
    for f in infiles:
        with open(f) as ii:
            output_text.append(ii.read())
    output_text = "".join(sorted(output_text))
    output_text += json.dumps(infiles) + " -> " + json.dumps(outfiles) + "\n"
    for f in outfiles:
        with open(f, "w") as ff:
            ff.write(output_text)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#
#   1   ->  2   ->  3   ->
#       ->  4           ->
#                   5   ->    6
#

tempdir = "test_pausing_dir/"
def do_write(file_name, what):
    with open(file_name, "a") as oo:
        oo.write(what)
test_file = tempdir + "task.done"
#
#    task1
#
@files(None, [tempdir + d for d in ('a.1', 'b.1', 'c.1')])
@follows(mkdir(tempdir))
@posttask(lambda: do_write(test_file, "Task 1 Done\n"))
def task1(infiles, outfiles, *extra_params):
    """
    First task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))


#
#    task2
#
@posttask(lambda: do_write(test_file, "Task 2 Done\n"))
@follows(task1)
@transform(tempdir + "*.1", suffix(".1"), ".2")
def task2(infiles, outfiles, *extra_params):
    """
    Second task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))



#
#    task3
#
@transform(task2, regex('(.*).2'), inputs([r"\1.2", tempdir + "a.1"]), r'\1.3')
@posttask(lambda: do_write(test_file, "Task 3 Done\n"))
def task3(infiles, outfiles, *extra_params):
    """
    Third task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))



#
#    task4
#
@transform(tempdir + "*.1", suffix(".1"), ".4")
@follows(task1)
@posttask(lambda: do_write(test_file, "Task 4 Done\n"))
def task4(infiles, outfiles, *extra_params):
    """
    Fourth task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))

#
#    task5
#
@files(None, tempdir + 'a.5')
@follows(mkdir(tempdir))
@posttask(lambda: do_write(test_file, "Task 5 Done\n"))
def task5(infiles, outfiles, *extra_params):
    """
    Fifth task is extra slow
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))

#
#    task6
#
#@files([[[tempdir + d for d in 'a.3', 'b.3', 'c.3', 'a.4', 'b.4', 'c.4', 'a.5'], tempdir + 'final.6']])
@merge([task3, task4, task5], tempdir + "final.6")
@follows(task3, task4, task5, )
@posttask(lambda: do_write(test_file, "Task 6 Done\n"))
def task6(infiles, outfiles, *extra_params):
    """
    final task
    """
    with open(tempdir + "jobs.start",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))
    test_job_io(infiles, outfiles, extra_params)
    with open(tempdir + "jobs.finish",  "a") as oo:
        oo.write('job = %s\n' % json.dumps([infiles, outfiles]))





def check_job_order_correct(filename):
    """
       1   ->  2   ->  3   ->
           ->  4           ->
                       5   ->    6
    """

    precedence_rules = [[1, 2],
                        [2, 3],
                        [1, 4],
                        [5, 6],
                        [3, 6],
                        [4, 6]]

    index_re = re.compile(r'.*\.([0-9])["\]\n]*$')
    job_indices = defaultdict(list)
    with open(filename) as ii:
        for linenum, l in enumerate(ii):
            m = index_re.search(l)
            if not m:
                raise "Non-matching line in [%s]" % filename
            job_indices[int(m.group(1))].append(linenum)

    for job_index in job_indices:
        job_indices[job_index].sort()

    for before, after in precedence_rules:
        if job_indices[before][-1] >= job_indices[after][0]:
            raise "Precedence violated for job %d [line %d] and job %d [line %d] of [%s]"



def check_final_output_correct():
    """
    check if the final output in final.6 is as expected
    """
    expected_output = \
"""        ["DIR/a.1"] -> ["DIR/a.2"]
        ["DIR/a.1"] -> ["DIR/a.4"]
        ["DIR/a.2", "DIR/a.1"] -> ["DIR/a.3"]
        ["DIR/a.3", "DIR/b.3", "DIR/c.3", "DIR/a.4", "DIR/b.4", "DIR/c.4", "DIR/a.5"] -> ["DIR/final.6"]
        ["DIR/b.1"] -> ["DIR/b.2"]
        ["DIR/b.1"] -> ["DIR/b.4"]
        ["DIR/b.2", "DIR/a.1"] -> ["DIR/b.3"]
        ["DIR/c.1"] -> ["DIR/c.2"]
        ["DIR/c.1"] -> ["DIR/c.4"]
        ["DIR/c.2", "DIR/a.1"] -> ["DIR/c.3"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.1", "DIR/b.1", "DIR/c.1"]
        [] -> ["DIR/a.5"]"""
    expected_output = expected_output.replace("        ", "").replace("DIR/", tempdir).split("\n")
    with open(tempdir + "final.6", "r") as ii:
        final_6_contents = sorted([l.rstrip() for l in ii.readlines()])
    if final_6_contents != expected_output:
        for i, (l1, l2) in enumerate(zip(final_6_contents, expected_output)):
            if l1 != l2:
                sys.stderr.write("%d\n  >%s<\n  >%s<\n" % (i, l1, l2))
        raise Exception ("Final.6 output is not as expected\n")



import unittest, shutil, os
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_ruffus (self):
        pipeline_run(multiprocess = 50, verbose = 0)
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")


    def test_newstyle_ruffus (self):
        test_pipeline = Pipeline("test")

        test_pipeline.files(task1,
                            None, 
                            [tempdir + d for d in ('a.1', 'b.1', 'c.1')])\
            .follows(mkdir(tempdir))\
            .posttask(lambda: do_write(test_file, "Task 1 Done\n"))

        test_pipeline.transform(task2, tempdir + "*.1", suffix(".1"), ".2")\
            .posttask(lambda: do_write(test_file, "Task 2 Done\n"))\
            .follows(task1)

        test_pipeline.transform(task3, task2, regex('(.*).2'), inputs([r"\1.2", tempdir + "a.1"]), r'\1.3')\
            .posttask(lambda: do_write(test_file, "Task 3 Done\n"))

        test_pipeline.transform(task_func = task4, 
                                input     = tempdir + "*.1", 
                                filter    = suffix(".1"), 
                                output    = ".4")\
            .follows(task1)\
            .posttask(lambda: do_write(test_file, "Task 4 Done\n"))

        test_pipeline.files(task5, None, tempdir + 'a.5')\
            .follows(mkdir(tempdir))\
            .posttask(lambda: do_write(test_file, "Task 5 Done\n"))

        test_pipeline.merge(task_func = task6,
                            input     = [task3, task4, task5], 
                            output    = tempdir + "final.6")\
            .follows(task3, task4, task5, )\
            .posttask(lambda: do_write(test_file, "Task 6 Done\n"))

        test_pipeline.run(multiprocess = 50, verbose = 0)
        check_final_output_correct()
        check_job_order_correct(tempdir + "jobs.start")
        check_job_order_correct(tempdir + "jobs.finish")

if __name__ == '__main__':
    unittest.main()

