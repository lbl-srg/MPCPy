# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the buildings module of mpcpy.

"""

import unittest
from mpcpy import exodata
from mpcpy import systems
from mpcpy import variables
from mpcpy import units
from mpcpy import utility
from testing import TestCaseMPCPy
from matplotlib import pyplot as plt
import os

# Simulation Tests
class EmulationFromFMU(TestCaseMPCPy):
    #%% FMU
    def setUp(self):
        # Set path variable(s)
        MPCPyPath = utility.get_MPCPy_path();
        # Setup building
        self.building_source_file_path = os.path.join(MPCPyPath, 'resources', 'building', \
                                                      'LBNL71T_Emulation_JModelica_v2.fmu');   
        self.zone_names = ['wes', 'hal', 'eas'];
        weather_path = os.path.join(MPCPyPath, 'resources', 'weather', \
                                    'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        internal_path = os.path.join(MPCPyPath, 'resources', 'internal', 'sampleCSV.csv');
        internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                 'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                 'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                 'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                 'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                 'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                 'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                 'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                 'intLat_eas' : ('eas', 'intLat', units.W_m2)};        
        control_path = os.path.join(MPCPyPath, 'resources', 'building', 'ControlCSV_0.csv');
        control_variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                                     'conHeat_hal' : ('conHeat_hal', units.unit1), \
                                     'conHeat_eas' : ('conHeat_eas', units.unit1)};        
        # Measurements
        self.measurements = {};
        self.measurements['wesTdb'] = {'Sample' : variables.Static('wesTdb_sample', 600, units.s)};
        self.measurements['halTdb'] = {'Sample' : variables.Static('halTdb_sample', 1200, units.s)};
        self.measurements['easTdb'] = {'Sample' : variables.Static('easTdb_sample', 1200, units.s)};           
        # Exodata
        self.weather = exodata.WeatherFromEPW(weather_path);
        self.internal = exodata.InternalFromCSV(internal_path, internal_variable_map, tz_name = self.weather.tz_name);
        self.control = exodata.ControlFromCSV(control_path, control_variable_map, tz_name = self.weather.tz_name);
        # Parameters
        self.parameter_data = {};
        self.parameter_data['lat'] = {};
        self.parameter_data['lat']['Value'] = self.weather.lat;
        
    def test_collect_measurements(self):
        start_time = '1/1/2015';
        final_time = '1/4/2015';
        # Collect exodata
        self.weather.collect_data(start_time, final_time);
        self.internal.collect_data(start_time, final_time);
        self.control.collect_data(start_time, final_time);
        # Instantiate building source
        building = systems.EmulationFromFMU(self.measurements, \
                                            fmupath = self.building_source_file_path, \
                                            zone_names = self.zone_names, \
                                            weather_data = self.weather.data, \
                                            internal_data = self.internal.data, \
                                            control_data = self.control.data, \
                                            parameter_data = self.parameter_data, \
                                            tz_name = self.weather.tz_name);
        # Collect measurements
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_display.csv');
        df_test = building.get_base_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_base.csv');  
        
    def test_collect_measurements_dst_start(self):
        # Test simulation through the start of daylight savings time
        start_time = '3/6/2015';
        final_time = '3/10/2015';
        self.weather.collect_data(start_time, final_time);
        self.internal.collect_data(start_time, final_time);
        self.control.collect_data(start_time, final_time);
        # Instantiate building source
        building = systems.EmulationFromFMU(self.measurements, \
                                            fmupath = self.building_source_file_path, \
                                            zone_names = self.zone_names, \
                                            weather_data = self.weather.data, \
                                            internal_data = self.internal.data, \
                                            control_data = self.control.data, \
                                            parameter_data = self.parameter_data, \
                                            tz_name = self.weather.tz_name);
        # Collect measurements
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_dst_start.csv');
        
    def test_collect_measurements_dst_end(self):
        # Test simulation through the end of daylight savings time
        start_time = '10/30/2015';
        final_time = '11/3/2015';
        self.weather.collect_data(start_time, final_time);
        self.internal.collect_data(start_time, final_time);
        self.control.collect_data(start_time, final_time);
        # Instantiate building source
        building = systems.EmulationFromFMU(self.measurements, \
                                            fmupath = self.building_source_file_path, \
                                            zone_names = self.zone_names, \
                                            weather_data = self.weather.data, \
                                            internal_data = self.internal.data, \
                                            control_data = self.control.data, \
                                            parameter_data = self.parameter_data, \
                                            tz_name = self.weather.tz_name);
        # Collect measurements
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_dst_end.csv');

    def plot_measurements(self, name):
        for key in self.building.measurements.keys():
            variable = self.building.measurements[key]['Measured'];
            variable.set_display_unit(units.degC);
            variable.display_data(tz_name = 'America/Chicago').plot(label = key, rot = 90, linewidth = 2.0);
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});        
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.rcParams.update({'font.size': 16});
        plt.savefig(self.MPCPyPath + os.sep + 'unittests' + os.sep + 'resources' + os.sep + name + '.png');
        plt.close();
        
class RealfromCSV(TestCaseMPCPy):
    #%% CSV
    def setUp(self):
        # Set path variable(s)
        MPCPyPath = utility.get_MPCPy_path();
        # Setup building measurement collection from csv
        self.csv_filepath = os.path.join(MPCPyPath, 'resources', 'building', 'OccData.csv');
        # Measurements
        self.measurements = {};
        self.measurements['occupancy'] = {'Sample' : variables.Static('occupancy_sample', 300, units.s)};
        self.measurement_variable_map = {'Total People Count for the whole building (+)' : ('occupancy', units.unit1)};                        
        # Instantiate building measurement source
        self.building = systems.RealFromCSV(self.csv_filepath, \
                                            self.measurements, 
                                            self.measurement_variable_map,
                                            time_header = 'Date');
                                            
    def test_collect_measurements(self):
        # Simulation time
        start_time = '2/1/2013';
        final_time = '2/20/2013 23:55';
        # Get training measurement data
        self.building.collect_measurements(start_time, final_time);
        # Check references
        df_test = self.building.display_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_display.csv');
        df_test = self.building.get_base_measurements('Measured');
        self.check_df_timeseries(df_test, 'collect_measurements_base.csv');
        
#%% Main        
if __name__ == '__main__':
    unittest.main()