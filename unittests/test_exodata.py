# -*- coding: utf-8 -*-
"""
test_exodata.py
by David Blum

This module contains the classes for testing the exodata of mpcpy.
"""
from abc import ABCMeta
import unittest
from mpcpy import exodata
from mpcpy import utility
from mpcpy import units
from mpcpy import variables
from matplotlib import pyplot as plt
import pandas as pd
import pickle
import copy

#%% General Test Methods
class TestExodata(unittest.TestCase):
    '''General test methods for testing exodata objects.'''
    __metaclass__ = ABCMeta;
    def print_data(self, obj):
        df = obj.display_data();
        print(df)
        df = obj.get_base_data();
        print(df)

#%% Weather Tests
class Weather_epw(TestExodata):
    '''Test the collection of weather data from an EPW.'''
    def setUp(self):
        self.start_time = '1/1/2015'; # No leap years!
        self.final_time = '1/1/2016'; # No leap years!
        self.test_varnames = ['weaPAtm', 'weaTDewPoi', 'weaTDryBul', 'weaRelHum', \
                              'weaNOpa', 'weaCelHei', 'weaNTot', 'weaWinSpe', 'weaWinDir', \
                              'weaHHorIR', 'weaHDirNor', 'weaHGloHor', 'weaHDifHor', \
                              'weaIAveHor', 'weaIDirNor', 'weaIDifHor', 'weaZLum', \
                              'weaHDifHor', 'weaTBlaSky', 'weaTWetBul', 'weaSolZen', \
                              'weaCloTim', 'weaSolTim'];
        # Instantiate weather object
        self.epw_filepath = utility.getMPCPyPath()+'/resources/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw';
        self.weather = exodata.WeatherFromEPW(self.epw_filepath);
        # Get weather data
        self.weather.collect_data(self.start_time, self.final_time);
        self.initial_ref = utility.getMPCPyPath() + '/unittests/resources/exodata_epw_dymola_out.csv';
        self.test_ref = utility.getMPCPyPath() + '/unittests/resources/exodata_epw_ref_out.csv';

    def test_values(self):
        '''Compare the values of collected weather data to a reference.'''
        try:
            # Try reading reference values from established test base
            df_ref = pd.read_csv(self.test_ref);
            df_ref.index = pd.to_datetime(df_ref['Time'].get_values());
            df_ref = df_ref.tz_localize('UTC');
            for key in self.weather.data.keys():
                if key in self.test_varnames and key in list(df_ref.columns.values):
                    var = self.weather.data[key];
                    test_data = var.get_base_data();
                    ref_data = df_ref[key];
                    if var.variability == 'Timeseries':
                        data_range = (ref_data.max()-ref_data.min());
                        if data_range == 0:
                            rerror = test_data-ref_data;
                        else:
                            rerror = (test_data-ref_data)/data_range;
                        rerror_gt = rerror>0.01;
                        self.assertFalse(rerror_gt.any(), 'Relative error of {} found in variable {}.'.format(rerror, key));

        except IOError:
            # Read data from initial reference source
            df_dymola = pd.read_csv(self.initial_ref, index_col = 'Time');
            time_dymola = df_dymola.index.values;
            # Turn data in dataframe
            df_wea = self.weather.get_base_data();
            df_wea = self.weather.add_simtime_column(df_wea);
            # Plot values
            i = 1;
            for key in self.weather.data.keys():
                if key in self.test_varnames and key in list(df_dymola.columns.values):
                    data = df_wea[key].get_values();
                    time_data = df_wea['SimTime'].get_values();
                    plt.figure(i);
                    plt.plot(time_data, data, '-', label = key+'_mpcpy');
                    plt.plot(time_dymola, df_dymola.loc[:,key], '--', label = key+'_dymola');
                    plt.title(key);
                    plt.legend();
                    i = i + 1;
            df_wea.to_csv(self.test_ref, index_label = 'Time');
            plt.show();

class Weather_csv(TestExodata):
    '''Test the collection of weather data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/weather/BerkeleyCSV.csv';
        self.start_time = '2016-10-19 19:53:00';
        self.final_time = '2016-10-20 06:53:00';
        self.geography = [37.8716, -122.2727];
        self.time_header = 'DateUTC';
        self.variable_map = {'TemperatureF' : ('weaTDryBul', units.degF), \
                             'Dew PointF' : ('weaTDewPoi', units.degF), \
                             'Humidity' : ('weaRelHum', units.percent), \
                             'Sea Level PressureIn' : ('weaPAtm', units.inHg), \
                             'WindDirDegrees' : ('weaWinDir', units.deg), \
                             'Wind SpeedMPH' : ('weaWinSpe', units.mph)};
        self.clean_data = {'Wind SpeedMPH' : {'cleaning_type' : variables.Timeseries.cleaning_replace, \
                                              'cleaning_args' : ('Calm', 0)}};

    def test_default_time(self):
        # Instantiate weather object
        self.weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                              self.variable_map, \
                                              geography = self.geography, \
                                              time_header = self.time_header, \
                                              clean_data = self.clean_data);
        # Get weather data
        self.weather.collect_data(self.start_time, self.final_time);
        self.print_data(self.weather);

    def test_local_time_from_geography(self):
        print('local time from geography')
        self.time_header = 'TimePDT';
        self.start_time = '12:53:00 PM';
        self.final_time = '11:53:00 PM';
        # Instantiate weather object
        self.weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                              self.variable_map, \
                                              geography = self.geography, \
                                              time_header = self.time_header, \
                                              clean_data = self.clean_data,
                                              tz_name = 'from_geography');
        # Get weather data
        self.weather.collect_data(self.start_time, self.final_time);
        self.print_data(self.weather);

    def test_local_time_from_tz_name(self):
        print('local time from tz_name')
        self.time_header = 'TimePDT';
        self.start_time = '12:53:00 PM';
        self.final_time = '11:53:00 PM';
        # Instantiate weather object
        self.weather = exodata.WeatherFromCSV(self.csv_filepath, \
                                              self.variable_map, \
                                              geography = self.geography, \
                                              time_header = self.time_header, \
                                              clean_data = self.clean_data,
                                              tz_name = 'America/Los_Angeles');
        # Get weather data
        self.weather.collect_data(self.start_time, self.final_time);
        self.print_data(self.weather);

#%% Internal Tests
class Internal_csv(TestExodata):
    '''Test the collection of internal data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/internal/sampleCSV.csv';
        self.start_time = '2015-1-1';
        self.final_time = '2015-1-2';
        self.variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                             'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                             'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                             'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                             'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                             'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                             'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                             'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                             'intLat_eas' : ('eas', 'intLat', units.W_m2)};
        # Instantiate weather object
        self.internal = exodata.InternalFromCSV(self.csv_filepath, \
                                                self.variable_map);
        # Get internal data
        self.internal.collect_data(self.start_time, self.final_time);

    def test_print(self):
        self.print_data(self.internal);

class Internal_occupancy(TestExodata):
    '''Test the collection of internal data from an occupancy model.'''
    def setUp(self):
        # Time
        self.start_time_occupancy = '4/1/2013';
        self.final_time_occupancy = '4/7/2013 23:55:00';
        self.start_time_internal = '4/2/2013';
        self.final_time_internal = '4/4/2013';
        # Load occupancy models
        with open(utility.getMPCPyPath()+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy_model = pickle.load(f);
        # Define zones and loads
        self.zone_list = ['wes', 'hal', 'eas'];
        self.load_list = [[0.4,0.4,0.2], [0.4,0.4,0.2], [0.4,0.4,0.2]];
        # Simulate occupancy models for each zone
        self.occupancy_model_list = [];
        for zone in self.zone_list:
            simulate_options = self.occupancy_model.get_simulate_options();
            simulate_options['iter_num'] = 5;
            self.occupancy_model.simulate(self.start_time_occupancy, self.final_time_occupancy)
            self.occupancy_model_list.append(copy.deepcopy(self.occupancy_model));
        # Instantiate internal object
        self.internal = exodata.InternalFromOccupancyModel(self.zone_list, self.load_list, units.W_m2, self.occupancy_model_list);
        # Get internal data
        self.internal.collect_data(self.start_time_internal, self.final_time_internal);

    def test_print(self):
        self.print_data(self.internal);

#%% Control Tests
class Control_csv(TestExodata):
    '''Test the collection of control data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/building/ControlCSV_0.csv';
        self.start_time = '1/1/2015 13:00:00';
        self.final_time = '1/2/2015';
        self.variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                             'conHeat_hal' : ('conHeat_hal', units.unit1), \
                             'conHeat_eas' : ('conHeat_eas', units.unit1)};
        # Instantiate control object
        self.control = exodata.ControlFromCSV(self.csv_filepath, \
                                              self.variable_map);
        # Get control data
        self.control.collect_data(self.start_time, self.final_time);  

    def test_print(self):
        self.print_data(self.control);

#%% Other Input Tests
class OtherInput_csv(TestExodata):
    '''Test the collection of other input data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/weather/Tamb.csv';
        self.start_time = '1/1/2015 00:00:00';
        self.final_time = '1/1/2015 02:00:00';
        self.variable_map = {'T' : ('Tamb', units.degC)};
        # Instantiate other input object
        self.otherinput = exodata.OtherInputFromCSV(self.csv_filepath, \
                                                    self.variable_map);
        # Get other input data
        self.otherinput.collect_data(self.start_time, self.final_time);

    def test_print(self):
        self.print_data(self.otherinput);

#%% Parameter Tests
class Parameters_csv(TestExodata):
    '''Test the collection of parameter data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/model/LBNL71T_Parameters.csv';
        # Instantiate weather object
        self.parameters = exodata.ParameterFromCSV(self.csv_filepath);
        # Get coefficient data
        self.parameters.collect_data();
        print('PARAMETERS %%%%%%%%%%%%%%%%%%%\n',self.parameters.data)

    def test_print(self):
        self.print_data(self.parameters);

#%% Constraint Tests
class Constraint_csv(TestExodata):
    '''Test the collection of constraint data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/optimization/sampleConstraintCSV_Setback.csv';
        self.start_time = '1/1/2015 13:00:00';
        self.final_time = '1/2/2015';
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
                             'conHeat_eas_min' : ('conHeat_eas', 'GTE', units.unit1), \
                             'conHeat_eas_max' : ('conHeat_eas', 'LTE', units.unit1)};
        # Instantiate weather object
        self.constraints = exodata.ConstraintFromCSV(self.csv_filepath, \
                                                     self.variable_map);
        # Get constraint data
        self.constraints.collect_data(self.start_time, self.final_time);

    def test_print(self):
        self.print_data(self.constraints);

class Constraint_occupancy(TestExodata):
    '''Test the collection of constraint data from an occupancy model.'''
    def setUp(self):
        # Time
        self.start_time_occupancy = '3/1/2012';
        self.final_time_occupancy = '3/7/2012 23:55:00';
        self.start_time_internal = '3/2/2012';
        self.final_time_internal = '3/4/2012';
        # Load occupancy models
        with open(utility.getMPCPyPath()+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy_model = pickle.load(f);
        # Define state variables and values
        self.state_variable_list = ['wesTdb', 'wesTdb', 'easTdb', 'easTdb', 'halTdb', 'halTdb'];
        self.values_list = [[25,30], [20,15], [25+273.15, 30+273.15], [20+273.15, 15+273.15], [25,30], [20,15]];
        self.constraint_type_list = ['LTE', 'GTE', 'LTE', 'GTE', 'LTE', 'GTE'];
        self.unit_list = [units.degC, units.degC, units.K, units.K, units.degC, units.degC]
        # Simulate occupancy model
        simulate_options = self.occupancy_model.get_simulate_options();
        simulate_options['iter_num'] = 5;
        self.occupancy_model.simulate(self.start_time_occupancy, self.final_time_occupancy);
        # Instantiate constraint object
        self.constraints = exodata.ConstraintFromOccupancyModel(self.state_variable_list, self.values_list, self.constraint_type_list, self.unit_list, self.occupancy_model);
        # Get internal data
        self.constraints.collect_data(self.start_time_internal, self.final_time_internal);

    def test_print(self):
        self.print_data(self.constraints);

#%% Prices Tests
class Price_csv(TestExodata):
    '''Test the collection of control data from a CSV file.'''
    def setUp(self):
        self.csv_filepath = utility.getMPCPyPath()+'/resources/optimization/PriceCSV.csv';
        self.start_time = '1/1/2015 13:00:00';
        self.final_time = '1/2/2015';
        self.variable_map = {'pi_e' : ('pi_e', units.unit1)};
        # Instantiate weather object
        self.prices = exodata.PriceFromCSV(self.csv_filepath, \
                                           self.variable_map);
        # Get weather data
        self.prices.collect_data(self.start_time, self.final_time);  

    def test_print(self):
        self.print_data(self.prices);

#%% Source Tests
class Source(unittest.TestCase):
    '''Test the general methods of a Source object.'''
    def setUp(self):
        self.epw_filepath = utility.getMPCPyPath()+'/resources/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw';
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