# -*- coding: utf-8 -*-
"""
Run the unit tests for mpcpy.

by David Blum
"""
import unittest
import argparse
import inspect
import importlib
import tempfile
import os
import shutil

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
                'test_optimization'];
    classes = [];

# Load Tests
print('Loading tests...'); 
suite = unittest.TestSuite();
for module in modules:
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
print('{} tests found.'.format(suite.countTestCases()));
# Run test suite
print('Running tests...'); 
unittest.TextTestRunner(verbosity = 1).run(suite);

# Delete temporary directory and change working directory back to original
shutil.rmtree(tempdir, ignore_errors=True)
os.chdir(cwd);
