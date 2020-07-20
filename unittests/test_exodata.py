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
import datetime
import pytz

#%% Weather Tests
class WeatherFromEPW(TestCaseMPCPy):
    '''Test the collection of weather data from an EPW.
    
    '''
    
    def setUp(self):
        self.epw_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', \
                                         'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.weather = exodata.WeatherFromEPW(self.epw_filepath);
        
    def tearDown(self):
        del self.weather
        
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

    def test_standard_time(self):
        start_time = '1/1/2015';
        final_time = '1/1/2016';
        weather = exodata.WeatherFromEPW(self.epw_filepath, standard_time=True)
        weather.collect_data(start_time, final_time);
        # Check instantiation        
        self.assertAlmostEqual(weather.lat.display_data(), 41.980, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -87.92, places=4);
        self.assertEqual(weather.tz_name, 'utc');
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_standard_time.csv');

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
                             
    def tearDown(self):
        del self.csv_filepath
        del self.geography
        del self.variable_map
                             
    def test_instantiate(self):
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, 
                                         self.geography);
        self.assertEqual(weather.name, 'weather_from_csv');
        self.assertEqual(weather.file_path, self.csv_filepath);
        self.assertAlmostEqual(weather.lat.display_data(), 37.8716, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -122.2727, places=4);
        self.assertEqual(weather.tz_name, 'UTC');

    def test_instantiate_without_geography(self):
        with self.assertRaises(TypeError):
            weather = exodata.WeatherFromCSV(self.csv_filepath,
                                             self.variable_map);

    def test_collect_data_default_time(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time_header = 'DateUTC';
        # Instantiate weather object
        weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                         self.variable_map, \
                                         self.geography, \
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
                                         self.geography, \
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
                                         self.geography, \
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
                                         self.geography, \
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
                             
    def tearDown(self):
        del self.df
        del self.geography
        del self.variable_map
                             
    def test_instantiate(self):
        time = pd.to_datetime(self.df['DateUTC']);
        self.df.set_index(time, inplace=True);
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map,
                                        self.geography);
        self.assertEqual(weather.name, 'weather_from_df');
        self.assertAlmostEqual(weather.lat.display_data(), 37.8716, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -122.2727, places=4);
        self.assertEqual(weather.tz_name, 'UTC');

    def test_instantiate_without_geography(self):
        with self.assertRaises(TypeError):
            weather = exodata.WeatherFromDF(self.df,
                                            self.variable_map)
        
    def test_collect_data_default_time(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time = pd.to_datetime(self.df['DateUTC']);
        self.df.set_index(time, inplace=True); 
        # Instantiate weather object
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        self.geography);
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
                                        self.geography,
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
                                        self.geography,
                                        tz_name = 'America/Los_Angeles');
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_local_time_from_tz_name.csv');

    def test_collect_data_tz_handling(self):
        start_time = '2016-10-19 19:53:00';
        final_time = '2016-10-20 06:53:00';
        time = pd.to_datetime(self.df['DateUTC']);
        self.df.set_index(time, inplace=True);
        # Localize timezone
        self.df = self.df.tz_localize('UTC')
        # Instantiate weather object
        with self.assertRaises(TypeError):
            weather = exodata.WeatherFromDF(self.df, \
                                            self.variable_map, \
                                            self.geography);
        # Remove timezone
        self.df = self.df.tz_convert(None)
        # Instantiate weather object
        weather = exodata.WeatherFromDF(self.df, \
                                        self.variable_map, \
                                        self.geography);
        # Get weather data
        weather.collect_data(start_time, final_time);
        # Collect twice
        weather.collect_data(start_time, final_time);
        # Check reference
        df_test = weather.display_data();
        self.check_df(df_test, 'collect_data_default_time.csv');

class WeatherFromNOAA(TestCaseMPCPy):
    '''Test the collection of weather data from NOAA.
    
    '''
    
    def setUp(self):
        self.geography = [37.8716, -122.2727]
        self.ins_model_name = 'GFS'
        self.weather = exodata.WeatherFromNOAA(self.geography, self.ins_model_name);
        self.start_time_pre = pd.Timestamp(datetime.datetime.now(pytz.timezone(self.weather.tz_name)))
        self.final_time_pre = self.start_time_pre + pd.Timedelta(days=7)
        self.start_time_his = self.start_time_pre - pd.Timedelta(days=7)
        self.final_time_his = self.start_time_pre
                             
    def tearDown(self):
        del self.geography
        del self.ins_model_name
        del self.start_time_his
        del self.final_time_his
        del self.start_time_pre
        del self.final_time_pre

    def valueTest(self, df_test):
        '''The function to test the weather values are reasonable:
        1. Contains the prediction of weaHDifHor, weaHDirNor, weaHGloHor, weaNTot, weaTDryBul, weaWinSpe
        2. The values of predicted weaHDifHor, weaHDirNor, weaHGloHor are in the range of (0,2000)
        3. The values of predicted weaNTot are in the range of (0,100)
        4. The values of predicted weaTDryBul are in the range of (200,350)
        5. The values of predicted weaWinSpe are in the range of (0,20)  
        '''
        # test 1:
        fields = df_test.columns
        self.assertIn('weaHDifHor', fields)
        self.assertIn('weaHDirNor', fields)
        self.assertIn('weaHGloHor', fields)
        self.assertIn('weaNTot', fields)
        self.assertIn('weaTDryBul', fields)
        self.assertIn('weaWinSpe', fields)
        # test 2-5:
        self.assertEqual((df_test[['weaHDifHor','weaHDirNor','weaHGloHor']]<0).sum().sum(),0)
        self.assertEqual((df_test[['weaHDifHor','weaHDirNor','weaHGloHor']]>2000).sum().sum(),0)
        self.assertEqual((df_test['weaNTot']<0).sum(),0)
        self.assertEqual((df_test['weaNTot']>100).sum(),0)
        self.assertEqual((df_test['weaTDryBul']<200).sum(),0)
        self.assertEqual((df_test['weaTDryBul']>350).sum(),0)
        self.assertEqual((df_test['weaWinSpe']<0).sum(),0)
        self.assertEqual((df_test['weaWinSpe']>20).sum(),0)
        
    def test_instantiate(self):
        weather = exodata.WeatherFromNOAA(self.geography, self.ins_model_name);
        self.assertEqual(weather.name, 'weather_from_noaa');
        self.assertEqual(weather.tz_name, 'America/Los_Angeles');
        self.assertAlmostEqual(weather.lat.display_data(), 37.8716, places=4);
        self.assertAlmostEqual(weather.lon.display_data(), -122.2727, places=4);
        
    def test_GFS_collect_historical_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'GFS');
        # Get weather data
        weather.collect_data(self.start_time_his, self.final_time_his);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the length of collected data is at least (24/3)*7-1, because of 3 hours interval
        self.assertGreater(self.df_test.shape[0], 55)
    
    def test_HRRR_collect_historical_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'HRRR');
        # Get weather data
        weather.collect_data(self.start_time_his, self.final_time_his);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the length of collected data is at least 3 days, HRRR method only save 3 days' data
        self.assertGreater(self.df_test.shape[0], 72)
    
    def test_RAP_collect_historical_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'RAP');
        # Get weather data
        weather.collect_data(self.start_time_his, self.final_time_his);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the length of collected data is at least (24/1)*7-1, because of 1 hours interval
        self.assertGreater(self.df_test.shape[0], 167)

    def test_NAM_collect_historical_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'NAM');
        # Get weather data
        weather.collect_data(self.start_time_his, self.final_time_his);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the length of collected data is at least (24/1)*7-1, because of 1 hours interval
        self.assertGreater(self.df_test.shape[0], 167)

    def test_GFS_collect_prediction_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'GFS');
        # Get weather data
        weather.collect_data(self.start_time_pre, self.final_time_pre);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the first prediction is within 3 hours
        self.secToFirstPre = (self.df_test.index[0] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertLess(self.secToFirstPre, 3600*3)
        # Check the prediction is available for at least 5 days
        self.secToLastPre = (self.df_test.index[-1] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertGreater(self.secToLastPre, 3600*24*5)
            
    def test_HRRR_collect_prediction_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'HRRR');
        # Get weather data
        weather.collect_data(self.start_time_pre, self.final_time_pre);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the first prediction is within 1 hours
        self.secToFirstPre = (self.df_test.index[0] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertLess(self.secToFirstPre, 3600*1)
        # Check the prediction is available for at least 15 hours
        self.secToLastPre = (self.df_test.index[-1] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertGreaterEqual(self.secToLastPre, 3600*15)
    
    def test_RAP_collect_prediction_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'RAP');
        # Get weather data
        weather.collect_data(self.start_time_pre, self.final_time_pre);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the first prediction is within 1 hours
        self.secToFirstPre = (self.df_test.index[0] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertLess(self.secToFirstPre, 3600*1)
        # Check the prediction is available for at least 18 hours
        self.secToLastPre = (self.df_test.index[-1] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertGreaterEqual(self.secToLastPre, 3600*18)
    
    def test_NAM_collect_prediction_data(self):
        # Instantiate weather object
        weather = exodata.WeatherFromNOAA(self.geography,'NAM');
        # Get weather data
        weather.collect_data(self.start_time_pre, self.final_time_pre);
        self.df_test = weather.get_base_data()
        # Check the fields and value range
        self.valueTest(self.df_test)
        # Check the first prediction is within 6 hours
        self.secToFirstPre = (self.df_test.index[0] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertLess(self.secToFirstPre, 3600*6)
        # Check the prediction is available for at least 3 days
        self.secToLastPre = (self.df_test.index[-1] - self.start_time_pre.tz_convert('UTC')).total_seconds()
        self.assertGreaterEqual(self.secToLastPre, 3600*24*3)
    
    def test_catch_method_error(self):
        # Instantiate weather object
        with self.assertRaises(NameError):
            weather = exodata.WeatherFromNOAA(self.geography,'test');
        # # Get weather data
        # weather.collect_data(self.start_time_his, self.final_time_his);
        # # Check reference
        # self.df_test = weather.display_data();
        # self.check_df(self.df_test, 'method_error.csv');  

#%% Internal Tests
class InternalFromCSV(TestCaseMPCPy):
    '''Test the collection of internal data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                             'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                             'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                             'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                             'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                             'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                             'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                             'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                             'intLat_eas' : ('eas', 'intLat', units.W_m2)};
        # Instantiate internal object
        self.internal = exodata.InternalFromCSV(csv_filepath, \
                                                variable_map);
                                                
    def tearDown(self):
        del self.internal

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
        
    def tearDown(self):
        del self.internal

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
                                            
    def tearDown(self):
        del self.control

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
        self.variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                        'conHeat_hal' : ('conHeat_hal', units.unit1), \
                        'conHeat_eas' : ('conHeat_eas', units.unit1)};
                        
    def tearDown(self):
        del self.df
        del self.variable_map

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Instantiate control object
        control = exodata.ControlFromDF(self.df, \
                                             self.variable_map); 
        # Get control data
        control.collect_data(start_time, final_time);
        # Check reference
        df_test = control.display_data();
        self.check_df(df_test, 'collect_data.csv');
        
    def test_collect_data_tz_handling(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Localize timezone
        self.df = self.df.tz_localize('UTC')
        # Instantiate weather object
        with self.assertRaises(TypeError):
            control = exodata.ControlFromDF(self.df, \
                                            self.variable_map); 
        # Remove timezone
        self.df = self.df.tz_convert(None)
        # Instantiate weather object
        control = exodata.ControlFromDF(self.df, \
                                        self.variable_map);
        # Get control data
        control.collect_data(start_time, final_time);
        # Collect twice
        control.collect_data(start_time, final_time);
        # Check reference
        df_test = control.display_data();
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
                                                    
    def tearDown(self):
        del self.otherinput

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
        self.variable_map = {'T' : ('Tamb', units.degC)};
        
    def tearDown(self):
        del self.df
        del self.variable_map

    def test_collect_data(self):
        start_time = '1/1/2015 00:00:00';
        final_time = '1/1/2015 06:00:00';
        # Instantiate control object
        otherinput = exodata.OtherInputFromDF(self.df, \
                                                   self.variable_map);
        # Get control data
        otherinput.collect_data(start_time, final_time);
        # Check reference
        df_test = otherinput.display_data();
        self.check_df(df_test, 'collect_data.csv');

    def test_collect_data_tz_handling(self):
        start_time = '1/1/2015 00:00:00';
        final_time = '1/1/2015 06:00:00';
        # Localize timezone
        self.df = self.df.tz_localize('UTC')
        # Instantiate weather object
        with self.assertRaises(TypeError):
            otherinput = exodata.OtherInputFromDF(self.df, \
                                                  self.variable_map); 
        # Remove timezone
        self.df = self.df.tz_convert(None)
        # Instantiate weather object
        otherinput = exodata.OtherInputFromDF(self.df, \
                                              self.variable_map);
        # Get control data
        otherinput.collect_data(start_time, final_time);
        # Collect twice
        otherinput.collect_data(start_time, final_time);
        # Check reference
        df_test = otherinput.display_data();
        self.check_df(df_test, 'collect_data.csv');

#%% Parameter Tests
class ParameterFromCSV(TestCaseMPCPy):
    '''Test the collection of parameter data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        # Instantiate weather object
        self.parameters = exodata.ParameterFromCSV(csv_filepath);
        # Get parameter data
        self.parameters.collect_data()
        
    def tearDown(self):
        del self.parameters

    def test_collect_data(self):
        # Check reference
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'collect_data.csv', timeseries=False);

class ParameterSet(TestCaseMPCPy):
    '''Test setting parameter data.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        # Instantiate weather object
        self.parameters = exodata.ParameterFromCSV(csv_filepath);
        # Get parameter data
        self.parameters.collect_data()
        
    def tearDown(self):
        del self.parameters
        
    def test_set_data_value(self):
        # Set value only
        self.parameters.set_data('adjeas.c_bou', value=20000.0)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_value.csv', timeseries=False);
        
    def test_set_data_free(self):
        # Set free only
        self.parameters.set_data('adjeas.c_bou', free=False)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_free.csv', timeseries=False);
        
    def test_set_data_min(self):
        # Set min only
        self.parameters.set_data('adjeas.c_bou', minimum=10000.0)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_min.csv', timeseries=False);
        
    def test_set_data_max(self):
        # Set max only
        self.parameters.set_data('adjeas.c_bou', maximum=30000.0)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_max.csv', timeseries=False);
        
    def test_set_data_cov(self):
        # Set cov only
        self.parameters.set_data('adjeas.c_bou', covariance=0.1)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_cov.csv', timeseries=False);
        
    def test_set_data_name(self):
        # Set name only
        self.parameters.set_data('adjeas.c_bou', new_name='c_bou')
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_name.csv', timeseries=False);
        
    def test_set_data_all(self):
        # Set all data
        self.parameters.set_data('adjeas.c_bou', 
                                 value=20000.0,
                                 free=False,
                                 minimum=10000.0, 
                                 maximum=30000.0,
                                 covariance=0.1,
                                 new_name='c_bou')
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'set_data_all.csv', timeseries=False);
        
    def test_set_data_keyerror(self):
        # Set cov only
        with self.assertRaises(KeyError): 
            self.parameters.set_data('c_bou', value=20000.0)
            
class ParameterAppend(TestCaseMPCPy):
    '''Test appending parameter data.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        # Instantiate weather object
        self.parameters = exodata.ParameterFromCSV(csv_filepath);
        # Get parameter data
        self.parameters.collect_data()
        
    def tearDown(self):
        del self.parameters
        
    def test_set_data_all(self):
        # Set all data
        self.parameters.append_data('c_bou', 
                                    value=20000.0,
                                    free=False,
                                    minimum=10000.0, 
                                    maximum=30000.0,
                                    covariance=0.1,
                                    unit=units.J_m2K)
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'append_data.csv', timeseries=False);
        
    def test_set_data_keyerror(self):
        # Set cov only
        with self.assertRaises(KeyError): 
            self.parameters.append_data('adjeas.c_bou', 
                                        value=20000.0,
                                        free=False,
                                        minimum=10000.0, 
                                        maximum=30000.0,
                                        covariance=0.1,
                                        unit=units.J_kgK)

class ParameterFromDF(TestCaseMPCPy):
    '''Test the collection of parameter data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv');
        df = pd.read_csv(csv_filepath, index_col = 'Name')
        # Instantiate weather object
        self.parameters = exodata.ParameterFromDF(df);
        
    def tearDown(self):
        del self.parameters

    def test_collect_data(self):
        # Get parameter data
        self.parameters.collect_data();
        # Check reference
        df_test = self.parameters.display_data();
        self.check_df(df_test, 'collect_data.csv', timeseries=False);
        
#%% Estimated State Tests
class EstimatedStateFromCSV(TestCaseMPCPy):
    '''Test the collection of estimated state data from a CSV file.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'EstimatedStates.csv');
        # Instantiate estimated state object
        self.estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        # Get estimated state data
        self.estimated_states.collect_data()
        
    def tearDown(self):
        del self.estimated_states

    def test_collect_data(self):
        # Check reference
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'collect_data.csv', timeseries=False);

class EstimatedStateSet(TestCaseMPCPy):
    '''Test setting estimated state data.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'EstimatedStates.csv');
        # Instantiate estimated state object
        self.estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        # Get estimated state data
        self.estimated_states.collect_data()
        
    def tearDown(self):
        del self.estimated_states
        
    def test_set_data_value(self):
        # Set value only
        self.estimated_states.set_data('heatCapacitor2.T', value=20.0)
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'set_data_value.csv', timeseries=False);
    def test_set_data_parameter(self):
        # Set value only
        self.estimated_states.set_data('heatCapacitor2.T', parameter='T2_o')
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'set_data_parameter.csv', timeseries=False);
        
    def test_set_data_name(self):
        # Set name only
        self.estimated_states.set_data('heatCapacitor2.T', new_name='heaCap2.T')
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'set_data_name.csv', timeseries=False);
        
    def test_set_data_all(self):
        # Set all data
        self.estimated_states.set_data('heatCapacitor2.T', 
                                 value=20.0,
                                 new_name='heaCap2.T',
                                 parameter='T2_o')
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'set_data_all.csv', timeseries=False);
        
    def test_set_data_keyerror(self):
        # Key doesn't exist
        with self.assertRaises(KeyError): 
            self.estimated_states.set_data('heaCap2.T', value=20.0)
            
class EstimatedStateAppend(TestCaseMPCPy):
    '''Test appending estimated state data.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'EstimatedStates.csv');
        # Instantiate estimated state object
        self.estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        # Get estimated state data
        self.estimated_states.collect_data()
        
    def tearDown(self):
        del self.estimated_states
        
    def test_set_data_all(self):
        # Set all data
        self.estimated_states.append_data('heaCap2.T', 
                                    value=20.0,
                                    unit=units.degC, 
                                    parameter='T2o')
        df_test = self.estimated_states.display_data();
        self.check_df(df_test, 'append_data.csv', timeseries=False);
        
    def test_set_data_keyerror(self):
        # Key already exists
        with self.assertRaises(KeyError): 
            self.estimated_states.append_data('heatCapacitor2.T', 
                                        value=20.0,
                                        unit=units.degC,
                                        parameter='T2o')

class EstimatedStateFromDF(TestCaseMPCPy):
    '''Test the collection of estimated state data from a pandas DataFrame object.
    
    '''
    
    def setUp(self):
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'EstimatedStates.csv');
        df = pd.read_csv(csv_filepath, index_col = 'Name')
        # Instantiate estimated state object
        self.estimated_states = exodata.EstimatedStateFromDF(df);
        
    def tearDown(self):
        del self.estimated_states

    def test_collect_data(self):
        # Get estimated state data
        self.estimated_states.collect_data();
        # Check reference
        df_test = self.estimated_states.display_data();
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
                        'conHeat_eas_min' : ('conHeat_eas', 'sGTE', units.unit1, 100), \
                        'conHeat_eas_max' : ('conHeat_eas', 'sLTE', units.unit1, 200)};
        # Instantiate weather object
        self.constraints = exodata.ConstraintFromCSV(csv_filepath, \
                                                     variable_map);
                                                     
    def tearDown(self):
        del self.constraints

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
        self.variable_map = {'wesTdb_min' : ('wesTdb', 'GTE', units.degC), \
                        'wesTdb_max' : ('wesTdb', 'LTE', units.degC), \
                        'easTdb_min' : ('easTdb', 'GTE', units.degC), \
                        'easTdb_max' : ('easTdb', 'LTE', units.degC), \
                        'halTdb_min' : ('halTdb', 'GTE', units.degC), \
                        'halTdb_max' : ('halTdb', 'LTE', units.degC), \
                        'conHeat_wes_min' : ('conHeat_wes', 'GTE', units.unit1), \
                        'conHeat_wes_max' : ('conHeat_wes', 'LTE', units.unit1), \
                        'conHeat_hal_min' : ('conHeat_hal', 'GTE', units.unit1), \
                        'conHeat_hal_max' : ('conHeat_hal', 'LTE', units.unit1), \
                        'conHeat_eas_min' : ('conHeat_eas', 'sGTE', units.unit1, 100), \
                        'conHeat_eas_max' : ('conHeat_eas', 'sLTE', units.unit1, 200)};

    def tearDown(self):
        del self.df
        del self.variable_map

    def test_collect_data(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Instantiate weather object
        constraints = exodata.ConstraintFromDF(self.df, \
                                               self.variable_map);
        # Get constraint data
        constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = constraints.display_data();
        self.check_df(df_test, 'collect_data.csv');

    def test_collect_data_tz_handling(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Localize timezone
        self.df = self.df.tz_localize('UTC')
        # Instantiate weather object
        with self.assertRaises(TypeError):
            constraints = exodata.ConstraintFromDF(self.df, \
                                                   self.variable_map); 
        # Remove timezone
        self.df = self.df.tz_convert(None)
        # Instantiate weather object
        constraints = exodata.ConstraintFromDF(self.df, \
                                               self.variable_map);
        # Get control data
        constraints.collect_data(start_time, final_time);
        # Collect twice
        constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = constraints.display_data();
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
            self.occupancy_model = pickle.load(f);
        # Define state variables and values
        self.state_variable_list = ['wesTdb', 'wesTdb', 'easTdb', 'easTdb', 'halTdb', 'halTdb'];
        self.values_list = [[25,30], [20,15], [25+273.15, 30+273.15], [20+273.15, 15+273.15], [25,30], [20,15]];
        self.constraint_type_list = ['LTE', 'GTE', 'LTE', 'GTE', 'LTE', 'GTE'];
        self.unit_list = [units.degC, units.degC, units.K, units.K, units.degC, units.degC]
        # Simulate occupancy model
        simulate_options = self.occupancy_model.get_simulate_options();
        simulate_options['iter_num'] = 5;
        np.random.seed(1); # start with same seed for random number generation
        self.occupancy_model.simulate(start_time_occupancy, final_time_occupancy);

    def tearDown(self):
        del self.constraints

    def test_collect_data(self):
        start_time = '3/2/2012';
        final_time = '3/4/2012';
        # Instantiate constraint object
        self.constraints = exodata.ConstraintFromOccupancyModel(self.state_variable_list, self.values_list, self.constraint_type_list, self.unit_list, self.occupancy_model);
        # Get constraint data
        self.constraints.collect_data(start_time, final_time);
        # Check reference
        df_test = self.constraints.display_data();
        self.check_df(df_test, 'collect_data.csv');

    def test_collect_data_slack_constraints(self):
        # Reset constraint data
        self.constraint_type_list = ['sLTE', 'GTE', 'LTE', 'GTE', 'LTE', 'GTE'];
        # Instantiate constraint object
        with self.assertRaises(TypeError):
            self.constraints = exodata.ConstraintFromOccupancyModel(self.state_variable_list, self.values_list, self.constraint_type_list, self.unit_list, self.occupancy_model);
        self.constraints = None
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
                                           
    def tearDown(self):
        del self.prices

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
        self.variable_map = {'pi_e' : ('pi_e', units.unit1)};

    def tearDown(self):
        del self.df
        del self.variable_map

    def test_print(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Instantiate weather object
        prices = exodata.PriceFromDF(self.df, \
                                     self.variable_map);
        # Get price data
        prices.collect_data(start_time, final_time);
        # Check reference
        df_test = prices.display_data();
        self.check_df(df_test, 'collect_data.csv');

    def test_collect_data_tz_handling(self):
        start_time = '1/1/2015 13:00:00';
        final_time = '1/2/2015';
        # Localize timezone
        self.df = self.df.tz_localize('UTC')
        # Instantiate weather object
        with self.assertRaises(TypeError):
            prices = exodata.PriceFromDF(self.df, \
                                         self.variable_map); 
        # Remove timezone
        self.df = self.df.tz_convert(None)
        # Instantiate weather object
        prices = exodata.PriceFromDF(self.df, \
                                     self.variable_map);
        # Get control data
        prices.collect_data(start_time, final_time);
        # Collect twice
        prices.collect_data(start_time, final_time);
        # Check reference
        df_test = prices.display_data();
        self.check_df(df_test, 'collect_data.csv');

#%% Source Tests
class Type(TestCaseMPCPy):
    '''Test the general methods of a Type object.
    
    '''
    
    def setUp(self):
        epw_filepath = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.weather = exodata.WeatherFromEPW(epw_filepath);

    def tearDown(self):
        del self.weather

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