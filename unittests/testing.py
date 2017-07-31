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

class TestCaseMPCPy(unittest.TestCase):
    '''General test methods for testing in mpcpy.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    def get_ref_path(self):
        '''Returns the path to the test data reference file.
        
        '''
        
        ref_path = os.path.join(utility.get_MPCPy_path(), 'unittests', 'references', self.__module__.split('.')[-1], self.__class__.__name__);
        
        return ref_path;
        
    def check_df_timeseries(self, df_test, ref_file_name):
        '''Compares timeseries test data to reference data.
        
        Uses pandas testing method ``assert_frame_equal()``.  If the 
        reference data file does not exist, a reference data file is created.
        
        Parameters
        ----------
        df_test : pandas DataFrame
            DataFrame of timeseries data to test
        ref_file_name : string
            Path to csv file containing reference data
        
        '''
        
        # Define reference file
        ref_file_path = os.path.join(self.get_ref_path(), ref_file_name);
        # Check if reference file exists
        try:
            df_ref = pd.read_csv(ref_file_path, index_col=0);
            df_ref.index = pd.to_datetime(df_ref.index);
            df_ref = df_ref.tz_localize('UTC')
            pd.util.testing.assert_frame_equal(df_test, df_ref);
        # If reference file does not exist, create one
        except IOError:
            ref_file_dir = self.get_ref_path();
            if not os.path.exists(ref_file_dir):
                os.makedirs(ref_file_dir);
            df_test.to_csv(ref_file_path);
            
    def check_df_general(self, df_test, ref_file_name):
        '''Compares general test data to reference data.
        
        Uses pandas testing method ``assert_frame_equal()``.   If the 
        reference data file does not exist, a reference data file is created.
        
        Parameters
        ----------    
        df_test : pandas DataFrame
            DataFrame of general data to test
        ref_file_name : string
            Path to csv file containing reference data
        
        '''
        
        # Define reference file
        ref_file_path = os.path.join(self.get_ref_path(), ref_file_name);
        # Check if reference file exists
        try:
            df_ref = pd.read_csv(ref_file_path, index_col=0);
            pd.util.testing.assert_frame_equal(df_test, df_ref, check_dtype=False);
        # If reference file does not exist, create one
        except IOError:
            ref_file_dir = self.get_ref_path();
            if not os.path.exists(ref_file_dir):
                os.makedirs(ref_file_dir);
            df_test.to_csv(ref_file_path);
            
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