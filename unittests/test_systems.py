# -*- coding: utf-8 -*-
"""
test_systems.py
by David Blum

This module contains the classes for testing the buildings module of mpcpy.
"""

import unittest
from mpcpy import exodata
from mpcpy import systems
from mpcpy import variables
from mpcpy import units
from mpcpy import utility
from matplotlib import pyplot as plt
import os

# Simulation Tests
class EmulationfromFMU(unittest.TestCase):
    #%% FMU
    def setUp(self):
        # Set path variable(s)
        self.MPCPyPath = utility.get_MPCPy_path();
        # Simulation time
        self.start_time = '1/1/2015';
        self.final_time = '1/4/2015';
        # Setup building fmu emulation
        # Setup Building
        self.building_source_file_path = self.MPCPyPath + os.sep + 'resources' + os.sep + 'building' + os.sep + 'LBNL71T_Emulation_JModelica_v2.fmu';   
        self.zone_names = ['wes', 'hal', 'eas'];
        self.weather_path = self.MPCPyPath + os.sep + 'resources' + os.sep + 'weather' + os.sep + 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw';
        self.internal_path = self.MPCPyPath + os.sep + 'resources' + os.sep + 'internal' + os.sep + 'sampleCSV.csv';
        self.internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                      'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                      'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                      'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                      'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                      'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                      'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                      'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                      'intLat_eas' : ('eas', 'intLat', units.W_m2)};        
        self.control_path = self.MPCPyPath + os.sep + 'resources' + os.sep + 'building' + os.sep + 'ControlCSV_0.csv';
        self.control_variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                                     'conHeat_hal' : ('conHeat_hal', units.unit1), \
                                     'conHeat_eas' : ('conHeat_eas', units.unit1)};        
        # Measurements
        self.measurements = {};
        self.measurements['wesTdb'] = {'Sample' : variables.Static('wesTdb_sample', 600, units.s)};
        self.measurements['halTdb'] = {'Sample' : variables.Static('halTdb_sample', 1200, units.s)};
        self.measurements['easTdb'] = {'Sample' : variables.Static('easTdb_sample', 1200, units.s)};           
        # Exodata
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.weather.collect_data(self.start_time, self.final_time);
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.internal.collect_data(self.start_time, self.final_time);
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);
        self.control.collect_data(self.start_time, self.final_time); 
        # Parameters
        self.parameter_data = {};
        self.parameter_data['lat'] = {};
        self.parameter_data['lat']['Value'] = self.weather.lat;
        
        # Instantiate building source
        self.building = systems.EmulationFromFMU(self.measurements, \
                                                 fmupath = self.building_source_file_path, \
                                                 zone_names = self.zone_names, \
                                                 weather_data = self.weather.data, \
                                                 internal_data = self.internal.data, \
                                                 control_data = self.control.data, \
                                                 parameter_data = self.parameter_data, \
                                                 tz_name = self.weather.tz_name);
        
    def test_simulation(self):
        # Get training measurement data
        self.building.collect_measurements(self.start_time, self.final_time);
        plt.figure(1);
        self.plot_measurements('buildings_simulation');
        
    def test_dst_start(self):
        # Test simulation through the start of daylight savings time
        self.start_time = '3/6/2015';
        self.final_time = '3/10/2015';
        self.weather.collect_data(self.start_time, self.final_time);
        self.internal.collect_data(self.start_time, self.final_time);
        self.building.collect_measurements(self.start_time, self.final_time);
        self.control.collect_data(self.start_time, self.final_time); 
        plt.figure(1);
        self.plot_measurements('buildings_dst_start');
        
    def test_dst_end(self):
        # Test simulation through the end of daylight savings time
        self.start_time = '10/30/2015';
        self.final_time = '11/3/2015';
        self.weather.collect_data(self.start_time, self.final_time);
        self.internal.collect_data(self.start_time, self.final_time);
        self.control.collect_data(self.start_time, self.final_time); 
        self.building.collect_measurements(self.start_time, self.final_time);
        plt.figure(1);
        self.plot_measurements('buildings_dst_end');

    def plot_measurements(self, name):
        for key in self.building.measurements.keys():
            variable = self.building.measurements[key]['Measured'];
            variable.set_display_unit(units.degC);
            variable.display_data(tz_name = 'America/Chicago').plot(label = key, rot = 90, linewidth = 2.0);
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});        
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.rcParams.update({'font.size': 16});
        plt.savefig(self.MPCPyPath+os.sep + 'unittests' + os.sep + 'resources' + os.sep + name + '.png');
        plt.close();        
        
class RealfromCSV(unittest.TestCase):
    #%% CSV
    def setUp(self):
        # Set path variable(s)
        self.MPCPyPath = utility.get_MPCPy_path();
        # Simulation time
        self.start_time = '2/1/2013';
        self.final_time = '2/20/2013 23:55';
        # Setup building measurement collection from csv
        self.csv_filepath = self.MPCPyPath+os.sep + 'resources' + os.sep + 'building' + os.sep + 'OccData.csv';   
        # Measurements
        self.measurements = {};
        self.measurements['occupancy'] = {'Sample' : variables.Static('occupancy_sample', 300, units.s)};
        self.measurement_variable_map = {'Total People Count for the whole building (+)' : ('occupancy', units.unit1)};                        
        # Instantiate building measurement source
        self.building = systems.RealFromCSV(self.csv_filepath, \
                                            self.measurements, 
                                            self.measurement_variable_map,
                                            time_header = 'Date');
                                            
    def test_collection(self):
        # Get training measurement data
        self.building.collect_measurements(self.start_time, self.final_time);
        self.measurements['occupancy']['Measured'].display_data().plot();
        plt.ylabel('Number of People');
        plt.savefig(self.MPCPyPath+os.sep + 'unittests' + os.sep + 'resources' + os.sep + 'occupancy_collected.png');
        self.assertEqual(self.measurements['occupancy']['Sample'].display_data(), 300);
        
#%% Main        
if __name__ == '__main__':
    unittest.main()