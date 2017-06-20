# -*- coding: utf-8 -*-
"""
This module contains the classes for testing in mpcpy.

"""

from abc import ABCMeta
import unittest
from mpcpy import utility
import pandas as pd
import os

class TestCaseMPCPy(unittest.TestCase):
    '''General test methods for testing in mpcpy.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    def get_ref_path(self):
        ref_path = utility.get_MPCPy_path() + '/unittests/references/' + self.__module__.split('.')[-1] + '/' + self.__class__.__name__;
        
        return ref_path;
        
    def check_df_timeseries(self, df_test, ref_file_name):
        # Define reference file
        ref_file_path = self.get_ref_path() + '/' + ref_file_name;
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
        # Define reference file
        ref_file_path = self.get_ref_path() + '/' + ref_file_name;
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