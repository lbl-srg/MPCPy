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
from mpcpy import utility
from doc.userGuide.tutorial import introductory


def check_result(result, name):
    '''Check and report results of testing.
    
    Parameters
    ----------
    result : unittest.TextTestRunner result
        The results of the test.  
        result.errors and results.failures are lists.
    name : string
        Type of test: unit or tutorial
    
    '''
    
    if result:
        if result.errors or result.failures:
            print('{0} errors and {1} failures found in '.format(len(result.errors), len(result.failures)) + name + ' tests.  Please consult terminal output for more info.');
        else:
            print(name + ' tests OK.')
    else:
        print(name + ' tests not run.')
    
    return None


# Main program
# ============

# Setup
# -----
# Change working directory to temporary
cwd = os.getcwd(); 
tempdir = tempfile.mkdtemp();
os.chdir(tempdir);
# Configure the log
logpath = os.path.join(utility.get_MPCPy_path(), 'unittests', 'outputs', 'unittests.log')
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

# Unit tests
# ----------
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
print('\n{} unit tests found.'.format(n_tests));
if n_tests:
    # Run test suite
    print('\nRunning unit tests...');
    result1 = unittest.TextTestRunner(verbosity = 1).run(suite);
else:
    result1 = None;
# Delete temporary directory and change working directory back to original
shutil.rmtree(tempdir, ignore_errors=True)
os.chdir(cwd);

# Tutorial tests
#---------------
if 'test_tutorial' in modules:
    # Collect tests
    suite_tut = unittest.TestSuite();
    suite_tut.addTests(doctest.DocTestSuite(introductory))
    # Report number of tests found
    n_tests = suite_tut.countTestCases();
    print('\n{} tutorials found.'.format(n_tests)); 
    # Run tests
    print('\nRunning tutorial doctests...')  
    doctest.ELLIPSIS_MARKER = '-etc-'
    os.chdir(os.path.dirname(introductory.__file__))
    result2 = unittest.TextTestRunner(verbosity = 1).run(suite_tut);
    os.chdir(cwd);
else:
    result2 = None;

# Check and report results
#-------------------------
print('\nResults\n-------')
check_result(result1, 'Unit')
check_result(result2, 'Tutorial')