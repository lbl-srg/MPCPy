# -*- coding: utf-8 -*-
"""
This module contains base classes for testing in mpcpy.

"""

from abc import ABCMeta
import unittest
from mpcpy import utility
import pandas as pd
import os
import json
import numpy as np
from matplotlib import pyplot as plt

class TestCaseMPCPy(unittest.TestCase):
    '''General test methods for testing in mpcpy.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    def get_unittest_path(self):
        '''Returns the path to the unittest directory.
        
        '''
        
        unittest_path = os.path.join(utility.get_MPCPy_path(), 'unittests');
        
        return unittest_path;
        
    def get_ref_path(self):
        '''Returns the path to the test data reference file.
        
        '''
        
        ref_path = os.path.join(utility.get_MPCPy_path(), 'unittests', 'references', self.__module__.split('.')[-1], self.__class__.__name__);
        
        return ref_path;
        
    def check_df(self, df_test, ref_file_name, timeseries=True):
        '''Compares DataFrame test data to reference data according to tolerance.
        
        Parameters
        ----------
        df_test : pandas DataFrame
            DataFrame of timeseries data to test
        ref_file_name : string
            Path to csv file containing reference data
        timeseries : boolean
            True if the index of df_test is timestamps.
        
        '''
        
        # Define reference file
        self.ref_file_path = os.path.join(self.get_ref_path(), ref_file_name);
        # Check if reference file exists
        try:
            df_ref = pd.read_csv(self.ref_file_path, index_col=0);
            if timeseries:
                df_ref.index = pd.to_datetime(df_ref.index);
                df_ref = df_ref.tz_localize('UTC');
            # Test index
            i_ref = df_ref.index.values;
            i_test = df_test.index.values;
            self._check_index(i_test, i_ref)
            # Test keys
            k_ref = list(df_ref);
            k_test = list(df_test);
            self._check_keys(k_test, k_ref)
            # Test values
            self._check_values(df_test, df_ref)
        # If reference file does not exist, create one
        except IOError:
            ref_file_dir = self.get_ref_path();
            if not os.path.exists(ref_file_dir):
                os.makedirs(ref_file_dir);
            df_test.to_csv(self.ref_file_path);
            
    def check_json(self, json_test, ref_file_name):
        '''Compares json test data to reference data.
        
        Uses method ``assertEqual()``.  If the reference data file does not 
        exist, a reference data file is created.
        
        Parameters
        ----------    
        json_test : dictionary
            Dictionary of data to test
        ref_file_name : string
            Path to csv file containing reference data
        
        '''
        
        # Define reference file
        ref_file_path = os.path.join(self.get_ref_path(), ref_file_name);
        test_file_path = os.path.join(self.get_ref_path(), 'test.txt');
        # Check if reference file exists
        try:
            with open(ref_file_path, 'r') as file_ref:
                json_ref = json.load(file_ref);
            # Convert json_test
            with open(test_file_path, 'w') as file_test:
                json.dump(json_test, file_test);
            with open(test_file_path, 'r') as file_test:
                json_test = json.load(file_test);
            os.remove(test_file_path)
            self.assertEqual(json_test, json_ref);
        # If reference file does not exist, create one
        except IOError:
            ref_file_dir = self.get_ref_path();
            if not os.path.exists(ref_file_dir):
                os.makedirs(ref_file_dir);
            with open(ref_file_path, 'w') as file_ref:
                json.dump(json_test, file_ref, sort_keys=True, indent=4, separators=(',', ': '));
                
    def _check_index(self, i_test, i_ref):
        '''Test the index of the test against the reference.
        
        Parameters
        ----------
        i_test : list-like
            Index of test.
        i_ref : list-like
            Index of reference.
            
        '''
        
        # Test length
        self.assertTrue(len(i_ref)==len(i_test), 'Index test failed beacuse of differing number of values.');
        # Test values
        for i in range(len(i_ref)):
            self.assertTrue(i_ref[i]==i_test[i], 'Index test failed at reference index value {0}.'.format(i_ref[i]));
    
    def _check_keys(self, k_test, k_ref):
        '''Test the keys of the test against the reference.
        
        Parameters
        ----------
        k_test : list-like
            Keys of test.
        k_ref : list-like
            Keys of reference.
            
        '''
        
        # Test length
        self.assertTrue(len(k_ref)==len(k_test), 'Key test failed beacuse of differing number of keys.');
        # Test values
        for i in range(len(k_ref)):
            self.assertTrue(k_ref[i] in k_test, 'Key test failed at reference key value {0}.'.format(k_ref[i]));
    
    def _check_values(self, df_test, df_ref):
        '''Test the values of the test against the reference.
        
        Parameters
        ----------
        df_test : pandas DataFrame
            Data of test.
        df_ref : pandas DataFrame
            Data of reference.

        '''

        # Set tolerance
        tol = 1e-3
        for key in list(df_ref):
            # Get values
            y_ref = df_ref[key].get_values();
            y_test = df_test[key].get_values();
            # Initialize error arrays
            err_abs = np.zeros(len(y_ref))
            err_rel = np.zeros(len(y_ref))
            err_fun = np.zeros(len(y_ref))
            # Calculate errors
            for i in range(len(y_ref)):
                # If non-numeric comparison
                if type(y_ref[i]) is str or type(y_ref[i]) is bool:
                    try:
                        self.assertTrue(y_ref[i] == y_test[i])
                    except AssertionError:
                        self.assertTrue(False, 'Value test failed with {0} error for key {1} at reference index {2}.'.format(type(y_ref[i]), key, df_ref.index.values[i]))
                # If numeric comparison
                else:
                    # Absolute error
                    err_abs[i] = np.absolute(y_test[i] - y_ref[i])
                    # Relative error
                    if (abs(y_ref[i]) > 10 * tol):
                        err_rel[i] = err_abs[i] / abs(y_ref[i])
                    else:
                        err_rel[i] = 0
                    # Total error
                    err_fun[i] = err_abs[i] + err_rel[i]
                # Assess error
                err_max = max(err_fun);
                i_max = np.argmax(err_fun);
                try:
                    self.assertTrue(err_max <= tol)
                except AssertionError:
                    # Plot reference
                    plt.plot(y_ref, '-ob', 
                                    label = 'ref', 
                                    linewidth = 3,
                                    markersize = 8)
                    # Plot test
                    plt.plot(y_test, '-or', 
                                     label = 'test',
                                     linewidth = 1.5,
                                     markersize = 4)
                    # Plot location of max error
                    plt.plot(i_max, y_test[i_max], 'og', 
                                                   label = 'location of max error', 
                                                   markerfacecolor='none',
                                                   markersize = 12.0, 
                                                   markeredgewidth = 3)
                    # Save plot
                    plt.legend()
                    fig_path = self.ref_file_path[:-4]+'_'+key+'.png'
                    plt.savefig(fig_path)
                    # Fail test
                    self.assertTrue(False, 'Value test failed with max error {0} for key {1} and reference index {2}.  Check {3} for plot of all values for key.'.format(err_max, key, df_ref.index.values[i_max], fig_path))