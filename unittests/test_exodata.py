# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the exodata of mpcpy.

"""

from mpcpy import exodata
from mpcpy import utility
from mpcpy import units
from mpcpy import variables
from testing import TestCaseMPCPy
import unittest
import numpy as np
import pickle
import copy
import os
import pandas as pd

#%% Weather Tests
class WeatherFromEPW(TestCaseMPCPy):
    '''Test the collection of weather data from an EPW.
    
    '''
    
    def setUp(self):
        self.epw_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', \
                                         'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.weather = exodata.WeatherFromEPW(self.epw_filepath);
        
    def test_instantiate(self):
        self.assertEqual(self.weather.name, 'weather_from_epw');
        self.assertEqual(self.weather.file_path, self.epw_filepath);
        self.assertAlmostEqual(self.weather.lat.display_data(), 41.980, places=4);
        self.assertAlmostEqual(self.weather.lon.display_data(), -87.92, places=4);
        self.assertEqual(self.weather.tz_name, 'America/Chicago');
        
    def test_collect_data(self):
        start_time = '1/1/2015';
        final_time = '1/1/2016';
        self.weather.collect_data(start_time, final_time);
        # Check reference
        df_test = self.weather.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
    def test_collect_data_partial(self):
        start_time = '10/2/2015 06:00:00';
        final_time = '11/13/2015 16:00:00';
        self.weather.collect_data(start_time, final_time);
        # Check references
        df_test = self.weather.display_data();
        self.check_df(df_test, 'collect_data_partial_display.csv');
        df_test = self.weather.get_base_data();
        self.check_df(df_test, 'collect_data_partial_base.csv');

class WeatherFromCSV(TestCaseMPCPy):
    '''Test the collection of weather data from a CSV file.
    
    '''
    
    def setUp(self):
        self.csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'BerkeleyCSV.csv');
        self.geography = [37.8716, -122.2727];
        self.variable_map = {'TemperatureF' : ('weaTDryBul', units.degF), \
                             'Dew PointF' : ('weaTDewPoi', units.degF), \
                             'Humidity' : ('weaRelHum', units.percent), \
                             'Sea Level PressureIn' : ('weaPAtm', units.inHg), \
                             'WindDirDegrees' : ('weaWinDir', units.deg)};
                             
    def test_instantiate(self):
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, 
                                         geography = self.geography);
        self.assertEqual(weather.name, 'weather_from_csv');
        self.assertEqual(weather.file_path, self.csv_filepath);
        self.assertAlmostEqual(weather.lat.display_data(), 37.8716, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -122.2727, places=4);
        self.assertEqual(weather.tz_name, 'UTC');
        
    def test_collect_data_default_time(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time_header = 'DateUTC';
        # Instantiate weather object
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, \
                                         geography = self.geography, \
                                         time_header = time_header);
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_default_time.csv');

    def test_collect_data_local_time_from_geography(self):
        start_time = '10/19/2016 12:53:00 PM';
        final_time = '10/19/2016 11:53:00 PM';
        time_header = 'TimePDT';
        # Instantiate weather object
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, \
                                         geography = self.geography, \
                                         time_header = time_header, \
                                         tz_name = 'from_geography');
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_local_time_from_geography.csv');

    def test_collect_data_local_time_from_tz_name(self):
        start_time = '10/19/2016 12:53:00 PM';
        final_time = '10/19/2016 11:53:00 PM';
        time_header = 'TimePDT';
        # Instantiate weather object
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, \
                                         geography = self.geography, \
                                         time_header = time_header, \
                                         tz_name = 'America/Los_Angeles');
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_local_time_from_tz_name.csv');

    def test_collect_data_clean_data(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time_header = 'DateUTC';
        variable_map = {'TemperatureF' : ('weaTDryBul', units.degF), \
                        'Dew PointF' : ('weaTDewPoi', units.degF), \
                        'Humidity' : ('weaRelHum', units.percent), \
                        'Sea Level PressureIn' : ('weaPAtm', units.inHg), \
                        'WindDirDegrees' : ('weaWinDir', units.deg), \
                        'Wind SpeedMPH' : ('weaWinSpe', units.mph)};
        clean_data = {'Wind SpeedMPH' : {'cleaning_type' : variables.Timeseries.cleaning_replace, \
                                         'cleaning_args' : ('Calm', 0)}};        
        # Instantiate weather object
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         variable_map, \
                                         geography = self.geography, \
                                         time_header = time_header, 
                                         clean_data = clean_data);
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_clean_data.csv');

class WeatherFromDF(TestCaseMPCPy):
    '''Test the collection of weather data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'weather', 'BerkeleyCSV.csv'));     
        self.geography = [37.8716, -122.2727];
        self.variable_map = {'TemperatureF' : ('weaTDryBul', units.degF), \
                             'Dew PointF' : ('weaTDewPoi', units.degF), \
                             'Humidity' : ('weaRelHum', units.percent), \
                             'Sea Level PressureIn' : ('weaPAtm', units.inHg), \
                             'WindDirDegrees' : ('weaWinDir', units.deg)};
                             
    def test_instantiate(self):
        time = pd.to_datetime(self.df['DateUTC']);
        self.df.set_index(time, inplace=True);
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        geography = self.geography);
        self.assertEqual(weather.name, 'weather_from_df');
        self.assertAlmostEqual(weather.lat.display_data(), 37.8716, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -122.2727, places=4);
        self.assertEqual(weather.tz_name, 'UTC');
        
    def test_collect_data_default_time(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time = pd.to_datetime(self.df['DateUTC']);
        self.df.set_index(time, inplace=True); 
        # Instantiate weather object
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        geography = self.geography);
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_default_time.csv');
        
    def test_collect_data_local_time_from_geography(self):
        start_time = '10/19/2016 12:53:00 PM';
        final_time = '10/19/2016 11:53:00 PM';
        time = pd.to_datetime(self.df['TimePDT']);
        self.df.set_index(time, inplace=True); 
        # Instantiate weather object
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        geography = self.geography,
                                        tz_name = 'from_geography');
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_local_time_from_geography.csv');

    def test_collect_data_local_time_from_tz_name(self):
        start_time = '10/19/2016 12:53:00 PM';
        final_time = '10/19/2016 11:53:00 PM';
        time = pd.to_datetime(self.df['TimePDT']);
        self.df.set_index(time, inplace=True); 
        # Instantiate weather object
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        geography = self.geography,
                                        tz_name = 'America/Los_Angeles');
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_local_time_from_tz_name.csv');
        
class Weather_ghi_to_poa(TestCaseMPCPy):
    '''Test the estimation of poa irradiance from ghi measurements.
    
    '''
    
    def test_ghi_to_poa(self):
        # Instantiate weather object
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'WeatherUndergroundHistory.csv');
        geography = [37.8716, -122.2727];
        variable_map = {'solar_radiation_set_1' : ('weaHGloHor', units.W_m2)};
        
        weather = exodata.WeatherFromCSV(csv_filepath,
                                         variable_map, 
                                         geography = geography,
                                         tz_name = 'utc');
        # Collect data
        weather.collect_data('2017-09-18 00:00:00','2017-09-21 00:00:00' )
        # Add POA irradiance for walls with cardinal orientations
        til = 90
        azis = [0,90,180,270]
        for azi in azis:
            weather.add_poa_from_ghi(til, azi, poa_var='weaHPoa_{0}'.format(azi))
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'ghi_to_poa.csv'.format(azi));
        
#%% Internal Tests
class InternalFromCSV(TestCaseMPCPy):
    '''Test the collection of internal data from a CSV file.
    
    '''
    
    def setUp(self):
        self.csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        self.variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                             'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                             'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                             'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                             'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                             'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                             'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                             'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                             'intLat_eas' : ('eas', 'intLat', units.W_m2)};
        # Instantiate internal object
        self.internal = exodata.InternalFromCSV(self.csv_filepath, \
                                                self.variable_map);

    def test_collect_data(self):
        start_time = '1/2/2015';
        final_time = '1/3/2015';
        # Get internal data
        self.internal.collect_data(start_time, final_time);
        # Check reference
        df_test = self.internal.display_data();
        self.check_df(df_test, 'collect_data.csv');

class InternalFromOccupancyModel(TestCaseMPCPy):
    '''Test the collection of internal data from an occupancy model.
    
    '''
    
    def setUp(self):
        # Time
        start_time_occupancy = '4/1/2013';
        final_time_occupancy = '4/7/2013 23:55:00';
        # Load occupancy models
        with open(os.path.join(utility.get_MPCPy_path(), 'unittests', 'references', \
                               'test_models', 'OccupancyFromQueueing', \
                               'occupancy_model_estimated.txt'), 'r') as f:
            occupancy_model = pickle.load(f);
        # Define zones and loads
        zone_list = ['wes', 'hal', 'eas'];
        load_list = [[0.4,0.4,0.2], [0.4,0.4,0.2], [0.4,0.4,0.2]];
        # Simulate occupancy models for each zone
        occupancy_model_list = [];
        np.random.seed(1); # start with same seed for random number generation
        for zone in zone_list:
            simulate_options = occupancy_model.get_simulate_options();
            simulate_options['iter_num'] = 5;
            occupancy_model.simulate(start_time_occupancy, final_time_occupancy)
            occupancy_model_list.append(copy.deepcopy(occupancy_model));
        # Instantiate internal object
        self.internal = exodata.InternalFromOccupancyModel(zone_list, load_list, units.W_m2, occupancy_model_list);

    def test_collect_data(self):
        start_time = '4/2/2013';
        final_time = '4/4/2013';
        # Get internal data
        self.internal.collect_data(start_time, final_time);
        # Check reference
        df_test = self.internal.display_data();
        self.check_df(df_test, 'collect_data.csv');

#%% Control Tests
class ControlFromCSV(TestCaseMPCPy):
    '''Test the collection of control data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'building', 'ControlCSV_0.csv');
        variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                        'conHeat_hal' : ('conHeat_hal', units.unit1), \
                        'conHeat_eas' : ('conHeat_eas', units.unit1)};
        # Instantiate control object
        self.control = exodata.ControlFromCSV(csv_filepath, \
                                              variable_map); 

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get control data
        self.control.collect_data(start_time, final_time);
        # Check reference
        df_test = self.control.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
class ControlFromDF(TestCaseMPCPy):
    '''Test the collection of control data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'building', 'ControlCSV_0.csv'));
        time = pd.to_datetime(self.df['Time']);
        self.df.set_index(time, inplace=True);
        variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                        'conHeat_hal' : ('conHeat_hal', units.unit1), \
                        'conHeat_eas' : ('conHeat_eas', units.unit1)};
        # Instantiate control object
        self.control = exodata.ControlFromDF(self.df, \
                                              variable_map); 

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get control data
        self.control.collect_data(start_time, final_time);
        # Check reference
        df_test = self.control.display_data();
        self.check_df(df_test, 'collect_data.csv');

#%% Other Input Tests
class OtherInputFromCSV(TestCaseMPCPy):
    '''Test the collection of other input data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'Tamb.csv');
        variable_map = {'T' : ('Tamb', units.degC)};
        # Instantiate other input object
        self.otherinput = exodata.OtherInputFromCSV(csv_filepath, \
                                                    variable_map);

    def test_collect_data(self):
        start_time = '1/1/2015 00:00:00';
        final_time = '1/1/2015 06:00:00';
        # Get other input data
        self.otherinput.collect_data(start_time, final_time);
        # Check reference
        df_test = self.otherinput.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
class OtherInputFromDF(TestCaseMPCPy):
    '''Test the collection of other input data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'weather', 'Tamb.csv'));
        time = pd.to_datetime(self.df['Time']);
        self.df.set_index(time, inplace=True);
        variable_map = {'T' : ('Tamb', units.degC)};
        # Instantiate control object
        self.otherinput = exodata.OtherInputFromDF(self.df, \
                                                   variable_map); 

    def test_collect_data(self):
        start_time = '1/1/2015 00:00:00';
        final_time = '1/1/2015 06:00:00';
        # Get control data
        self.otherinput.collect_data(start_time, final_time);
        # Check reference
        df_test = self.otherinput.display_data();
        self.check_df(df_test, 'collect_data.csv');

#%% Parameter Tests
class ParameterFromCSV(TestCaseMPCPy):
    '''Test the collection of parameter data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        # Instantiate weather object
        self.parameters = exodata.ParameterFromCSV(csv_filepath);

    def test_collect_data(self):
        # Get parameter data
        self.parameters.collect_data();
        # Check reference
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'collect_data.csv', timeseries=False);
        
class ParameterFromDF(TestCaseMPCPy):
    '''Test the collection of parameter data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        df = pd.read_csv(csv_filepath, index_col = 'Name')
        # Instantiate weather object
        self.parameters = exodata.ParameterFromDF(df);

    def test_collect_data(self):
        # Get parameter data
        self.parameters.collect_data();
        # Check reference
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'collect_data.csv', timeseries=False);

#%% Constraint Tests
class ConstraintFromCSV(TestCaseMPCPy):
    '''Test the collection of constraint data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'sampleConstraintCSV_Setback.csv');
        variable_map = {'wesTdb_min' : ('wesTdb', 'GTE', units.degC), \
                        'wesTdb_max' : ('wesTdb', 'LTE', units.degC), \
                        'easTdb_min' : ('easTdb', 'GTE', units.degC), \
                        'easTdb_max' : ('easTdb', 'LTE', units.degC), \
                        'halTdb_min' : ('halTdb', 'GTE', units.degC), \
                        'halTdb_max' : ('halTdb', 'LTE', units.degC), \
                        'conHeat_wes_min' : ('conHeat_wes', 'GTE', units.unit1), \
                        'conHeat_wes_max' : ('conHeat_wes', 'LTE', units.unit1), \
                        'conHeat_hal_min' : ('conHeat_hal', 'GTE', units.unit1), \
                        'conHeat_hal_max' : ('conHeat_hal', 'LTE', units.unit1), \
                        'conHeat_eas_min' : ('conHeat_eas', 'GTE', units.unit1), \
                        'conHeat_eas_max' : ('conHeat_eas', 'LTE', units.unit1)};
        # Instantiate weather object
        self.constraints = exodata.ConstraintFromCSV(csv_filepath, \
                                                     variable_map);

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get constraint data
        self.constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = self.constraints.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
class ConstraintFromDF(TestCaseMPCPy):
    '''Test the collection of constraint data from a df.
    
    '''
    
    def setUp(self):
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'sampleConstraintCSV_Setback.csv'));
        time = pd.to_datetime(self.df['Time']);
        self.df.set_index(time, inplace=True);
        variable_map = {'wesTdb_min' : ('wesTdb', 'GTE', units.degC), \
                        'wesTdb_max' : ('wesTdb', 'LTE', units.degC), \
                        'easTdb_min' : ('easTdb', 'GTE', units.degC), \
                        'easTdb_max' : ('easTdb', 'LTE', units.degC), \
                        'halTdb_min' : ('halTdb', 'GTE', units.degC), \
                        'halTdb_max' : ('halTdb', 'LTE', units.degC), \
                        'conHeat_wes_min' : ('conHeat_wes', 'GTE', units.unit1), \
                        'conHeat_wes_max' : ('conHeat_wes', 'LTE', units.unit1), \
                        'conHeat_hal_min' : ('conHeat_hal', 'GTE', units.unit1), \
                        'conHeat_hal_max' : ('conHeat_hal', 'LTE', units.unit1), \
                        'conHeat_eas_min' : ('conHeat_eas', 'GTE', units.unit1), \
                        'conHeat_eas_max' : ('conHeat_eas', 'LTE', units.unit1)};
        # Instantiate weather object
        self.constraints = exodata.ConstraintFromDF(self.df, \
                                                    variable_map);

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get constraint data
        self.constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = self.constraints.display_data();
        self.check_df(df_test, 'collect_data.csv'); 

class ConstraintFromOccupancyModel(TestCaseMPCPy):
    '''Test the collection of constraint data from an occupancy model.
    
    '''
    
    def setUp(self):
        # Time
        start_time_occupancy = '3/1/2012';
        final_time_occupancy = '3/7/2012 23:55:00';
        # Load occupancy models
        with open(os.path.join(self.get_unittest_path(), 'references', 'test_models',\
                               'OccupancyFromQueueing', 'occupancy_model_estimated.txt'), 'r') as f:
            occupancy_model = pickle.load(f);
        # Define state variables and values
        state_variable_list = ['wesTdb', 'wesTdb', 'easTdb', 'easTdb', 'halTdb', 'halTdb'];
        values_list = [[25,30], [20,15], [25+273.15, 30+273.15], [20+273.15, 15+273.15], [25,30], [20,15]];
        constraint_type_list = ['LTE', 'GTE', 'LTE', 'GTE', 'LTE', 'GTE'];
        unit_list = [units.degC, units.degC, units.K, units.K, units.degC, units.degC]
        # Simulate occupancy model
        simulate_options = occupancy_model.get_simulate_options();
        simulate_options['iter_num'] = 5;
        np.random.seed(1); # start with same seed for random number generation
        occupancy_model.simulate(start_time_occupancy, final_time_occupancy);
        # Instantiate constraint object
        self.constraints = exodata.ConstraintFromOccupancyModel(state_variable_list, values_list, constraint_type_list, unit_list, occupancy_model);

    def test_collect_data(self):
        start_time = '3/2/2012';
        final_time = '3/4/2012';
        # Get constraint data
        self.constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = self.constraints.display_data();
        self.check_df(df_test, 'collect_data.csv');         

#%% Prices Tests
class PriceFromCSV(TestCaseMPCPy):
    '''Test the collection of control data from a CSV file.

    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'PriceCSV.csv');
        variable_map = {'pi_e' : ('pi_e', units.unit1)};
        # Instantiate weather object
        self.prices = exodata.PriceFromCSV(csv_filepath, \
                                           variable_map);

    def test_print(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get price data
        self.prices.collect_data(start_time, final_time);
        # Check reference
        df_test = self.prices.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
class PriceFromDF(TestCaseMPCPy):
    '''Test the collection of price data from a df.

    '''
    
    def setUp(self):
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'PriceCSV.csv'));
        time = pd.to_datetime(self.df['Time']);
        self.df.set_index(time, inplace=True);
        variable_map = {'pi_e' : ('pi_e', units.unit1)};
        # Instantiate weather object
        self.prices = exodata.PriceFromDF(self.df, \
                                          variable_map);

    def test_print(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Get price data
        self.prices.collect_data(start_time, final_time);
        # Check reference
        df_test = self.prices.display_data();
        self.check_df(df_test, 'collect_data.csv');  

#%% Source Tests
class Type(TestCaseMPCPy):
    '''Test the general methods of a Type object.
    
    '''
    
    def setUp(self):
        self.epw_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.weather = exodata.WeatherFromEPW(self.epw_filepath);
    def test_set_time_interval(self):
        '''Test this method sets the time metrics properly in the exodata source.'''
        # Set start and final time
        start_time = '1/2/2016';
        final_time = '1/4/2016';
        # Set known time metrics
        elapsed_seconds = 86400*2;
        year_start_seconds = 86400;
        year_final_seconds = 86400*3;
        # Set start and final time in exodata source
        self.weather._set_time_interval(start_time, final_time);
        # Check time metrics are correct         
        self.assertAlmostEqual(elapsed_seconds, self.weather.elapsed_seconds, places=3);
        self.assertAlmostEqual(year_start_seconds, self.weather.year_start_seconds, places=3);
        self.assertAlmostEqual(year_final_seconds, self.weather.year_final_seconds, places=3);

#%% Main
if __name__ == '__main__':
    unittest.main()