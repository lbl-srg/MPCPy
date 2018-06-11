# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the variables of mpcpy.

"""

import unittest
from mpcpy import variables
from mpcpy import units
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


class Static(unittest.TestCase):
    '''Tests for Static class.
    
    '''   
    
    def setUp(self):
        '''Instantiate static variable.'''
        self.var = variables.Static('var1', 20, units.degC);
    def test_instantiation(self):
        '''Test Instantiation.'''
        self.assertEqual(self.var.name, 'var1');
        self.assertEqual(self.var.variability, 'Static');
        self.assertEqual(self.var.quantity_name, 'Temperature');
        self.assertIs(self.var.get_display_unit(), units.degC);
        self.assertEqual(self.var.get_display_unit_name(), 'degC');
        self.assertEqual(self.var.get_base_unit_name(), 'K');
        
    def test_data(self):
        '''Test difference between data (base unit) and display data (display unit).'''
        self.assertAlmostEqual(self.var.get_base_data(), 20+273.15, places = 3);
        self.assertAlmostEqual(self.var.display_data(), 20, places = 3);
    def test_set_display_unit(self):
        '''Test setting the display unit.'''
        self.var.set_display_unit(units.degF);
        self.assertAlmostEqual(self.var.get_base_data(), 20+273.15, places = 3);
        self.assertAlmostEqual(self.var.display_data(), 68, places = 3);
    def test_set_data(self):
        '''Test setting the data.'''
        self.var.set_display_unit(units.degF);
        self.var.set_data(72);
        self.assertAlmostEqual(self.var.get_base_data(), 295.372, places = 3);
        self.assertAlmostEqual(self.var.display_data(), 72, places = 3);
        self.var.set_display_unit(units.degC);
        self.assertAlmostEqual(self.var.get_base_data(), 295.372, places = 3);
        self.assertAlmostEqual(self.var.display_data(), 22.222, places = 3);
    def test_set_data_list(self):
        '''Test setting data that is an array.'''
        x_list = [1,2,3,4.5];
        self.var_list = variables.Static('var_list', x_list, units.degC);
        i = 0;
        for x in x_list:
            self.assertEqual(self.var_list.display_data()[i], x);  
            i = i + 1;
    def test_set_data_array(self):
        '''Test setting data that is an array.'''
        x_array = np.array([1,2,3,4.5]);
        self.var_array = variables.Static('var_array', x_array, units.degC);
        i = 0;
        for x in x_array:
            self.assertEqual(self.var_array.display_data()[i], x);
            i = i + 1;
            
    def test_set_data_string(self):
        '''Test setting data that is a string returns as TypeError.'''
        data = '25.0';
        with self.assertRaises(TypeError):
            var = variables.Static('var_data', data, units.degC);
        
class Timeseries(unittest.TestCase):
    '''Tests for Timeseries class.
    
    '''
    
    def setUp(self):
        '''Instantiate timeseries variable.'''
        self.dataC = np.array([20,21,22,23,24,25]);
        self.dataF = np.array([72,73,74,75,76,77]);
        self.start = pd.datetime(2016, 1, 1, 0);
        self.end   = pd.datetime(2016, 1, 1, 5); 
        self.time  = pd.date_range(self.start, self.end, freq='H');
        self.dataC_pd = pd.Series(data = self.dataC, index = self.time);
        self.dataF_pd = pd.Series(data = self.dataF, index = self.time);  
        self.var = variables.Timeseries('var1', self.dataC_pd, units.degC);        
    def test_instantiation(self):        
        '''Test Instantiation.'''
        self.assertEqual(self.var.name, 'var1');
        self.assertEqual(self.var.variability, 'Timeseries');
        self.assertEqual(self.var.quantity_name, 'Temperature');
        self.assertIs(self.var.get_display_unit(), units.degC);
        self.assertEqual(self.var.get_display_unit_name(), 'degC');
    def test_data(self):
        '''Test difference between data (base unit) and display data (display unit).'''
        for i in range(len(self.dataC)):
            self.assertAlmostEqual(self.var.get_base_data().get_values()[i], self.dataC[i]+273.15, places = 3);
            self.assertAlmostEqual(self.var.display_data().get_values()[i], self.dataC[i], places = 3);
    def test_set_display_unit(self):
        '''Test setting the display unit.'''
        self.var.set_display_unit(units.K);
        for i in range(len(self.dataC)):
            self.assertAlmostEqual(self.var.get_base_data().get_values()[i], self.dataC[i]+273.15, places = 3);
            self.assertAlmostEqual(self.var.display_data().get_values()[i], self.dataC[i]+273.15, places = 3);
    def test_set_data(self):            
        '''Test setting the data.'''
        self.var.set_display_unit(units.degF);            
        self.var.set_data(self.dataF_pd);
        for i in range(len(self.dataF)):
            self.assertAlmostEqual(self.var.get_base_data().get_values()[i], np.array([295.372,295.928,296.483,297.039,297.594,298.150])[i], places = 3);
            self.assertAlmostEqual(self.var.display_data().get_values()[i], self.dataF[i], places = 3);
    def test_set_name(self):
        '''Test setting the name.'''
        self.var.name = 'var2';
        self.assertEqual(self.var.name, 'var2');
    def test_display_time_zone(self):
        '''Test that the default time zone is UTC.'''
        # Time zone by tz_name
        self.var = variables.Timeseries('var1', self.dataC_pd, units.degC);
        for i in range(len(self.dataC)):
            self.assertEqual(self.var.get_base_data().index[i], self.time[i].tz_localize('UTC'));
            self.assertEqual(self.var.display_data().index[i], self.time[i].tz_localize('UTC'));
        self.var = variables.Timeseries('var1', self.dataC_pd, units.degC, tz_name = 'America/Los_Angeles');
        for i in range(len(self.dataC)):
            self.assertEqual(self.var.get_base_data().index[i], self.time[i].tz_localize('UTC')+relativedelta(hours = 8));
            self.assertEqual(self.var.display_data().index[i], self.time[i].tz_localize('UTC')+relativedelta(hours = 8));  
        # Time zone by geography
        self.var = variables.Timeseries('var1', self.dataC_pd, units.degC, geography = [41.8781, -87.6298]);
        for i in range(len(self.dataC)):
            self.assertEqual(self.var.get_base_data().index[i], self.time[i].tz_localize('UTC')+relativedelta(hours = 6));
            self.assertEqual(self.var.display_data().index[i], self.time[i].tz_localize('UTC')+relativedelta(hours = 6));         
        
        
class Operations_Static(unittest.TestCase):
    '''Tests for static addition and subtraction.
    
    '''
    
    def setUp(self):
        '''Instantiate static variables.'''
        self.a = variables.Static('a', 5, units.degC)
        self.b = variables.Static('b', 10, units.degC)
    def test_add(self):
        '''Add static variables.'''
        self.c = self.a + self.b;
        self.assertEqual('ab', self.c.name);
        self.assertIs(self.c.get_display_unit(), units.degC);
        self.assertEqual(self.c.display_data(), 15);
    def test_subtract(self):        
        '''Subtract static variables.'''
        self.d = self.a - self.b;
        self.assertEqual('ab', self.d.name);
        self.assertIs(self.d.get_display_unit(), units.degC);
        self.assertEqual(self.d.display_data(), -5);
        
class Operations_Timeseries(unittest.TestCase):
    '''Tests for timeseries addition and subtraction.
    
    '''
    
    def setUp(self):   
        '''Instantiate timeseries variables.'''
        self.dataC = np.array([20,21,22,23,24,25]);
        self.start = pd.datetime(2016, 1, 1, 0);
        self.end   = pd.datetime(2016, 1, 1, 5); 
        self.time  = pd.date_range(self.start, self.end, freq='H');
        self.dataC_pd = pd.Series(data = self.dataC, index = self.time);
        self.e = variables.Timeseries('e', self.dataC_pd, units.degC);
    def test_add_static(self):
        '''Add static and timeseries variables.'''   
        self.a = variables.Static('a', 5, units.degC)         
        self.f = self.a + self.e;
        self.assertEqual('ae', self.f.name);
        self.assertIs(self.f.get_display_unit(), units.degC);
        for i in range(len(self.dataC)):
            self.assertEqual(self.f.display_data().get_values()[i], 5 + self.dataC[i]);
    def test_add_timeseries(self):            
        '''Add timeseries variables.'''             
        self.g = self.e + self.e;
        self.assertEqual('ee', self.g.name);
        self.assertIs(self.g.get_display_unit(), units.degC);
        for i in range(len(self.dataC)):
            self.assertEqual(self.g.display_data().get_values()[i], 2*self.dataC[i]);
            
class Cleaning(unittest.TestCase):
    '''Tests for cleaning methods.
    
    '''
    
    def setUp(self):
        '''Create test data.'''
        self.time = pd.date_range('9/1/2015 00:00:00', '9/1/2015 03:00:00', freq = 'H');
        self.ts_calm = pd.Series(data = np.array([2,4,'calm',8]), index = self.time);
    def test_replace(self):
        '''Replace 'calm' with 0.5 mph in timeseries variable.'''
        self.var = variables.Timeseries('var', self.ts_calm, units.mph, \
                                        cleaning_type = variables.Timeseries.cleaning_replace,
                                        cleaning_args = ('calm',0.5));
        self.assertAlmostEqual(self.var.get_base_data().get_values()[2], 0.22352, places = 3);
        self.assertAlmostEqual(self.var.display_data().get_values()[2], 0.5, places = 3);

if __name__ == '__main__':
    unittest.main()