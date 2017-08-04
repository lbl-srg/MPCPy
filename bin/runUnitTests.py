# -*- coding: utf-8 -*-
"""
Run the unit tests for mpcpy.

"""
import unittest
import doctest
import argparse
import inspect
import importlib
import tempfile
import os
import shutil
import sys
from mpcpy import utility
from doc.userGuide.tutorial import introductory


def check_result(results):
    sys.stdout = sys.__stdout__
    if result.errors or result.failures:
        print('{0} errors and {1} failures found in tests.  Please consult outputs/log for more info.'.format(len(result.errors), len(result.failures)));
    else:
        print('All tests successful.')
    
# Change working directory to temporary
cwd = os.getcwd(); 
tempdir = tempfile.mkdtemp();
os.chdir(tempdir);

# Configure the argument parser
parser = argparse.ArgumentParser(description='Run the unit tests for mpcpy.');
unit_test_group = parser.add_argument_group("arguments to run unit tests");
unit_test_group.add_argument('-s', '--specify_test', \
                             metavar='module.class', \
                             help='test only the module and class specified');
args = parser.parse_args();
               
# Define test modules and classes, if any
modules = [];
classes = [];
if args.specify_test:
    modules.append(args.specify_test.split('.')[0]);
    try:
        classes.append(args.specify_test.split('.')[1]);
    except IndexError:
        classes = [];
else:                        
    modules += ['test_utility', \
                'test_variables', \
                'test_units', \
                'test_exodata', \
                'test_systems', \
                'test_models', \
                'test_optimization', \
                'test_tutorial'];
    classes = [];

# Load Tests
print('Loading tests...'); 
suite = unittest.TestSuite();
for module in modules:
    if module != 'test_tutorial':
        module_name = 'unittests.' + module;
        test_module = importlib.import_module(module_name);
        # Find all test classes in module, select if test class is specified
        module_classes = [];
        if not classes:
            for name, obj in inspect.getmembers(test_module):       
                if inspect.isclass(obj):
                    module_classes.append(obj);             
        else:
            for name, obj in inspect.getmembers(test_module):       
                if inspect.isclass(obj) and name in classes:
                    module_classes.append(obj);        
        # Add test classes to suite
        for obj in module_classes:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(obj));

# Report number of tests found
n_tests = suite.countTestCases();
print('{} unit tests found.'.format(n_tests));
if n_tests:
    # Run test suite
    print('Running unit tests...');
    # Configure the log
    logpath = os.path.join(utility.get_MPCPy_path(), 'unittests', 'outputs', 'unittests.log')
    sys.stdout = open(logpath, 'w')
    result = unittest.TextTestRunner(verbosity = 1, stream=sys.stdout).run(suite);
   
    check_result(result)
   
# Delete temporary directory and change working directory back to original
shutil.rmtree(tempdir, ignore_errors=True)
os.chdir(cwd);

# Run tutorial doctest
#---------------------

if 'test_tutorial' in modules:
    print('\n\nRunning tutorial doctests...')
    sys.stdout = open(logpath, 'w')
    doctest.ELLIPSIS_MARKER = '-etc-'
    os.chdir(os.path.dirname(introductory.__file__))
    suite_tut = unittest.TestSuite();
    suite_tut.addTests(doctest.DocTestSuite(introductory))
    result = unittest.TextTestRunner(verbosity = 1, stream=sys.stdout).run(suite_tut);
    
    check_result(result)
