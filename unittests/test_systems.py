# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the buildings module of mpcpy.

"""

import unittest
from mpcpy import exodata
from mpcpy import systems
from mpcpy import variables
from mpcpy import units
from testing import TestCaseMPCPy
from matplotlib import pyplot as plt
import os
import pandas as pd

# Simulation Tests
class EmulationFromFMU(TestCaseMPCPy):
    #%% FMU
    def setUp(self):
        # Setup building
        self.building_source_file_path = os.path.join(self.get_unittest_path(), 'resources', 'building', \
                                                      'LBNL71T_Emulation_JModelica_v2.fmu');   
        self.zone_names = ['wes', 'hal', 'eas'];
        weather_path = os.path.join(self.get_unittest_path(), 'resources', 'weather', \
                                    'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        internal_path = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                 'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                 'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                 'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                 'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                 'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                 'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                 'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                 'intLat_eas' : ('eas', 'intLat', units.W_m2)};        
        control_path = os.path.join(self.get_unittest_path(), 'resources', 'building', 'ControlCSV_0.csv');
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
        
    def tearDown(self):
        del self.measurements
        del self.weather
        del self.internal
        del self.control
        del self.parameter_data
        
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
        self.check_df(df_test, 'collect_measurements_display.csv');
        df_test = building.get_base_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_base.csv');

    def test_collect_measurements_save_parameter_input_data(self):
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
                                            tz_name = self.weather.tz_name,
                                            save_parameter_input_data=True);
        # Collect measurements
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_display.csv');
        df_test = building.get_base_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_base.csv');
        # Check parameter and input data was saved
        df_test = pd.read_csv('mpcpy_simulation_inputs_system.csv', index_col='Time');
        df_test.index = pd.to_datetime(df_test.index).tz_localize('UTC')
        self.check_df(df_test, 'mpcpy_simulation_inputs_system.csv');
        df_test = pd.read_csv('mpcpy_simulation_parameters_system.csv', index_col = 'parameter')
        self.check_df(df_test, 'mpcpy_simulation_parameters_system.csv', timeseries=False);  
        
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
        self.check_df(df_test, 'collect_measurements_dst_start.csv');
        
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
        self.check_df(df_test, 'collect_measurements_dst_end.csv');
        
    def test_collect_measurements_continue(self):
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
        # Collect measurements in daily chunks
        sim_steps = pd.date_range(start_time, final_time, freq=str('1d'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                building.collect_measurements(sim_steps[i], sim_steps[i+1]);
            else:
                building.collect_measurements('continue', sim_steps[i+1]);
            # Check references
            df_test = building.display_measurements('Measured');
            self.check_df(df_test, 'collect_measurements_continue_step{0}.csv'.format(i));
            
    def test_collect_measurements_continue_me_1(self):
        start_time = '1/1/2017';
        final_time = '1/2/2017';
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        moinfo = (mopath, modelpath, {});
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate model
        building = systems.EmulationFromFMU(measurements, \
                                            moinfo = moinfo, \
                                            control_data = controls.data,
                                            version = '1.0',
                                            target = 'me');
        # Simulate model
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Simulated');
        self.check_df(df_test, 'collect_measurements_display_me.csv');
        
        # Simulate model in 4-hour chunks
        sim_steps = pd.date_range(start_time, final_time, freq=str('8H'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                building.collect_measurements(sim_steps[i], sim_steps[i+1]);
            else:
                building.collect_measurements('continue', sim_steps[i+1]);
            # Check references
            df_test = building.display_measurements('Simulated');
            self.check_df(df_test, 'collect_measurements_step_me{0}.csv'.format(i));
    
    def test_collect_measurements_continue_me_2(self):
        start_time = '1/1/2017';
        final_time = '1/2/2017';
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        moinfo = (mopath, modelpath, {});
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate model
        building = systems.EmulationFromFMU(measurements, \
                                            moinfo = moinfo, \
                                            control_data = controls.data,
                                            version = '2.0',
                                            target = 'me');
        # Simulate model
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Simulated');
        self.check_df(df_test, 'collect_measurements_display_me.csv');
        
        # Simulate model in 4-hour chunks
        sim_steps = pd.date_range(start_time, final_time, freq=str('8H'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                building.collect_measurements(sim_steps[i], sim_steps[i+1]);
            else:
                building.collect_measurements('continue', sim_steps[i+1]);
            # Check references
            df_test = building.display_measurements('Simulated');
            self.check_df(df_test, 'collect_measurements_step_me{0}.csv'.format(i));
            
    def test_collect_measurements_continue_cs_1(self):
        start_time = '1/1/2017';
        final_time = '1/2/2017';
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        moinfo = (mopath, modelpath, {});
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate model
        building = systems.EmulationFromFMU(measurements, \
                                            moinfo = moinfo, \
                                            control_data = controls.data,
                                            version = '1.0',
                                            target = 'cs');
        # Simulate model
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Simulated');
        self.check_df(df_test, 'collect_measurements_display_cs.csv');
        
        # Simulate model in 4-hour chunks
        sim_steps = pd.date_range(start_time, final_time, freq=str('8H'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                building.collect_measurements(sim_steps[i], sim_steps[i+1]);
            else:
                building.collect_measurements('continue', sim_steps[i+1]);
            # Check references
            df_test = building.display_measurements('Simulated');
            self.check_df(df_test, 'collect_measurements_step_cs{0}.csv'.format(i));
            
    def test_collect_measurements_continue_cs_2(self):
        start_time = '1/1/2017';
        final_time = '1/2/2017';
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        moinfo = (mopath, modelpath, {});
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate model
        building = systems.EmulationFromFMU(measurements, \
                                            moinfo = moinfo, \
                                            control_data = controls.data,
                                            version = '2.0',
                                            target = 'cs');
        # Simulate model
        building.collect_measurements(start_time, final_time);
        # Check references
        df_test = building.display_measurements('Simulated');
        self.check_df(df_test, 'collect_measurements_display_cs.csv');
        
        # Simulate model in 4-hour chunks
        sim_steps = pd.date_range(start_time, final_time, freq=str('8H'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                building.collect_measurements(sim_steps[i], sim_steps[i+1]);
            else:
                building.collect_measurements('continue', sim_steps[i+1]);
            # Check references
            df_test = building.display_measurements('Simulated');
            self.check_df(df_test, 'collect_measurements_step_cs{0}.csv'.format(i));
            

            
    def plot_measurements(self, name):
        for key in self.building.measurements.keys():
            variable = self.building.measurements[key]['Measured'];
            variable.set_display_unit(units.degC);
            variable.display_data(tz_name = 'America/Chicago').plot(label = key, rot = 90, linewidth = 2.0);
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});        
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.rcParams.update({'font.size': 16});
        plt.savefig(os.path.join(self.get_unittest_path(), 'outputs', name + '.png'));
        plt.close();
        
class RealfromCSV(TestCaseMPCPy):
    #%% CSV
    def setUp(self):
        # Setup building measurement collection from csv
        self.csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'building', 'OccData.csv');
        # Measurements
        self.measurements = {};
        self.measurements['occupancy'] = {'Sample' : variables.Static('occupancy_sample', 300, units.s)};
        self.measurement_variable_map = {'Total People Count for the whole building (+)' : ('occupancy', units.unit1)};                        
        # Instantiate building measurement source
        self.building = systems.RealFromCSV(self.csv_filepath, \
                                            self.measurements, 
                                            self.measurement_variable_map,
                                            time_header = 'Date');
                                            
    def tearDown(self):
        del self.measurements
        del self.building
                                            
    def test_collect_measurements(self):
        # Simulation time
        start_time = '2/1/2013';
        final_time = '2/20/2013 23:55';
        # Get training measurement data
        self.building.collect_measurements(start_time, final_time);
        # Check references
        df_test = self.building.display_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_display.csv');
        df_test = self.building.get_base_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_base.csv');
        
class RealfromDF(TestCaseMPCPy):
    #%% DF
    def setUp(self):
        # Setup building measurement collection from df
        self.df = pd.read_csv(os.path.join(self.get_unittest_path(), 'resources', 'building', 'OccData.csv'));
        time = pd.to_datetime(self.df['Date']);
        self.df.set_index(time, inplace=True);         
        # Measurements
        self.measurements = {};
        self.measurements['occupancy'] = {'Sample' : variables.Static('occupancy_sample', 300, units.s)};
        self.measurement_variable_map = {'Total People Count for the whole building (+)' : ('occupancy', units.unit1)};                        
        # Instantiate building measurement source
        self.building = systems.RealFromDF(self.df,
                                           self.measurements, 
                                           self.measurement_variable_map);
                                           
    def tearDown(self):
        del self.measurements
        del self.building
                                            
    def test_collect_measurements(self):
        # Simulation time
        start_time = '2/1/2013';
        final_time = '2/20/2013 23:55';
        # Get training measurement data
        self.building.collect_measurements(start_time, final_time);
        # Check references
        df_test = self.building.display_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_display.csv');
        df_test = self.building.get_base_measurements('Measured');
        self.check_df(df_test, 'collect_measurements_base.csv');
        
#%% Main        
if __name__ == '__main__':
    unittest.main()