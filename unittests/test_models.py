# -*- coding: utf-8 -*-
"""
test_models.py
by David Blum

This module contains the classes for testing the model module of mpcpy.
"""
import unittest
from mpcpy import models
from mpcpy import exodata
from mpcpy import utility
from mpcpy import systems
from mpcpy import units
from mpcpy import variables
from testing import TestCaseMPCPy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pickle
import os

#%%
class SimpleRC(TestCaseMPCPy):
    '''Test simple model simulate.
    
    '''

    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        MPCPyPath = utility.get_MPCPy_path();
        # Set model paths
        mopath = MPCPyPath+'/resources/model/Simple.mo';
        modelpath = 'Simple.RC';
        # Gather control inputs
        control_csv_filepath = MPCPyPath+'/resources/model/SimpleRC_Input.csv';
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(self.start_time, self.final_time);
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     control_data = controls.data);
    def test_simulate(self):
        # Simulate model
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_display.csv');
        df_test = self.model.get_base_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_base.csv');

#%%    
class EstimateFromJModelica(TestCaseMPCPy):
    '''Test the parameter estimation of a model using JModelica.
    
    '''
    
    def setUp(self):
        self.MPCPyPath = utility.get_MPCPy_path();
        ## Setup building fmu emulation
        self.building_source_file_path = self.MPCPyPath + '/resources/building/LBNL71T_Emulation_JModelica_v2.fmu';
        self.zone_names = ['wes', 'hal', 'eas'];
        self.weather_path = self.MPCPyPath + '/resources/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw';
        self.internal_path = self.MPCPyPath + '/resources/internal/sampleCSV.csv';
        self.internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                      'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                      'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                      'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                      'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                      'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                      'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                      'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                      'intLat_eas' : ('eas', 'intLat', units.W_m2)};        
        self.control_path = self.MPCPyPath + '/resources/building/ControlCSV_0.csv';
        self.control_variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                                     'conHeat_hal' : ('conHeat_hal', units.unit1), \
                                     'conHeat_eas' : ('conHeat_eas', units.unit1)};        
        # Measurements
        self.measurements = {};
        self.measurements['wesTdb'] = {'Sample' : variables.Static('wesTdb_sample', 1800, units.s)};
        self.measurements['halTdb'] = {'Sample' : variables.Static('halTdb_sample', 1800, units.s)};
        self.measurements['easTdb'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['wesPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['halPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};     
        self.measurements['easPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['Ptot'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        ## Setup model
        self.mopath = self.MPCPyPath + '/resources/model/LBNL71T_MPC.mo';
        self.modelpath = 'LBNL71T_MPC.MPC';
        self.libraries = os.environ.get('MODELICAPATH');
        self.estimate_method = models.JModelica; 
        self.validation_method = models.RMSE;
        # Instantiate exo data sources
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);   
        # Parameters        
        self.parameters = exodata.ParameterFromCSV(self.MPCPyPath + '/resources/model/LBNL71T_Parameters.csv');
        self.parameters.collect_data();
        self.parameters.data['lat'] = {};
        self.parameters.data['lat']['Value'] = self.weather.lat;    
        # Instantiate building
        self.building = systems.EmulationFromFMU(self.measurements, \
                                                 fmupath = self.building_source_file_path, \
                                                 zone_names = self.zone_names, \
                                                 parameter_data = self.parameters.data);
                                                 
    def test_simulate_initial_parameters(self):
        '''Test the simulation of the model.'''
        plt.close('all');       
        # Simulation time
        self.start_time = '1/1/2015';
        self.final_time = '1/4/2015';
        # Exodata
        self.weather.collect_data(self.start_time, self.final_time);
        self.internal.collect_data(self.start_time, self.final_time);
        self.control.collect_data(self.start_time, self.final_time);       
        # Collect emulation measurements for comparison
        self.building.weather_data = self.weather.data;
        self.building.internal_data = self.internal.data;
        self.building.control_data = self.control.data;
        self.building.tz_name = self.weather.tz_name;
        self.building.collect_measurements(self.start_time, self.final_time);
        # Instantiate model
        self.model = models.Modelica(self.estimate_method, \
                                     self.validation_method, \
                                     self.building.measurements, \
                                     moinfo = (self.mopath, self.modelpath, self.libraries), \
                                     zone_names = self.zone_names, \
                                     weather_data = self.weather.data, \
                                     internal_data = self.internal.data, \
                                     control_data = self.control.data, \
                                     parameter_data = self.parameters.data, \
                                     tz_name = self.weather.tz_name);                    
        # Simulate model with current guess of parameters
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_initial_parameters.csv');
        
    def test_estimate_and_validate(self):
        '''Test the estimation of a model's coefficients based on measured data.'''
        plt.close('all');
        # Exogenous collection time
        self.start_time_exodata = '1/1/2015';
        self.final_time_exodata = '1/30/2015';    
        # Emulation time
        self.start_time_emulation = '1/1/2015';
        self.final_time_emulation = '1/4/2015';
        # Estimation time
        self.start_time_estimation = '1/1/2015';
        self.final_time_estimation = '1/4/2015';
        # Validation time
        self.start_time_validation = '1/4/2015';
        self.final_time_validation = '1/5/2015';
        # Measurement variables for estimate
        self.measurement_variable_list = ['wesTdb', 'easTdb', 'halTdb'];
        # Exodata
        self.weather.collect_data(self.start_time_exodata, self.final_time_exodata);
        self.internal.collect_data(self.start_time_exodata, self.final_time_exodata);
        self.control.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Set exodata to building emulation
        self.building.weather_data = self.weather.data;
        self.building.internal_data = self.internal.data;
        self.building.control_data = self.control.data;
        self.building.tz_name = self.weather.tz_name;       
        # Collect measurement data
        self.building.collect_measurements(self.start_time_emulation, self.final_time_emulation);
        
        # Instantiate model
        self.model = models.Modelica(self.estimate_method, \
                                     self.validation_method, \
                                     self.building.measurements, \
                                     moinfo = (self.mopath, self.modelpath, self.libraries), \
                                     zone_names = self.zone_names, \
                                     weather_data = self.weather.data, \
                                     internal_data = self.internal.data, \
                                     control_data = self.control.data, \
                                     parameter_data = self.parameters.data, \
                                     tz_name = self.weather.tz_name);                 
        # Estimate model based on emulated data
        self.model.estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_estimated_parameters.csv');
        # Validate on validation data
        self.building.collect_measurements(self.start_time_validation, self.final_time_validation);
        self.model.measurements = self.building.measurements;
        self.model.validate(self.start_time_validation, self.final_time_validation, self.MPCPyPath+'/unittests/resources/model_validation');
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df_general(df_test, 'validate_RMSE.csv');
         
#%% Occupancy tests
class OccupancyFromQueueing(TestCaseMPCPy):
    '''Test the occupancy model using a queueing approach.
    
    '''
    
    def setUp(self):
        # Set path variable(s)
        self.MPCPyPath = utility.get_MPCPy_path();
        # Setup building measurement collection from csv
        self.csv_filepath = self.MPCPyPath+'/resources/building/OccData.csv';   
        # Measurements
        self.measurements = {};
        self.measurements['occupancy'] = {'Sample' : variables.Static('occupancy_sample', 300, units.s)};
        self.measurement_variable_map = {'Total People Count for the whole building (+)' : ('occupancy', units.unit1)};                        
        # Instantiate building measurement source
        self.building = systems.RealFromCSV(self.csv_filepath, \
                                            self.measurements, 
                                            self.measurement_variable_map,
                                            time_header = 'Date');
        # Where to save ref occupancy model
        self.occupancy_model_file = self.get_ref_path()+'/occupancy_model_estimated.txt';
        
        
    def test_estimate(self):
        '''Test the estimation method.'''
        plt.close('all');
        # Time
        self.start_time = '2/1/2013';
        self.final_time = '7/24/2013 23:59';
        # Collect measurements
        self.building.collect_measurements(self.start_time, self.final_time);
        # Instantiate occupancy model
        self.occupancy = models.Occupancy(models.QueueModel, self.building.measurements);
        # Estimate occupancy model parameters
        np.random.seed(1);
        self.occupancy.estimate(self.start_time, self.final_time);
        try:
            with open(self.occupancy_model_file, 'r') as f:
                self.occupancy = pickle.load(f);
        except IOError:
            os.makedirs(self.get_ref_path());
            with open(self.occupancy_model_file, 'w') as f:
                pickle.dump(self.occupancy, f);
            
    def test_simulate(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            self.occupancy = pickle.load(f);
        # Simulate occupancy model
        np.random.seed(1);
        self.occupancy.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.occupancy.display_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_display.csv');
        df_test = self.occupancy.get_base_measurements('Simulated');
        self.check_df_timeseries(df_test, 'simulate_base.csv');

    def test_validate(self):
        '''Test occupancy prediction comparison with measured data.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';           
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            self.occupancy = pickle.load(f);
        # Collect validation measurements
        self.building.collect_measurements(self.start_time, self.final_time);             
        # Set valiation measurements in occupancy model        
        self.occupancy.measurements = self.building.measurements;
        # Validate occupancy model with simulation options
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        self.occupancy.set_simulate_options(simulate_options);
        np.random.seed(1);
        self.occupancy.validate(self.start_time, self.final_time, self.MPCPyPath+'/unittests/resources/occupancy_model_validate');
        # Check references
        RMSE = {};
        for key in self.occupancy.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.occupancy.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df_general(df_test, 'validate_RMSE.csv');        
        
    def test_get_load(self):
        '''Test generation of occupancy load data using occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            self.occupancy = pickle.load(f);        
        # Simulate occupancy model
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;  
        np.random.seed(1);
        self.occupancy.simulate(self.start_time, self.final_time);
        load = self.occupancy.get_load(100);
        # Check references
        df_test = load.to_frame(name='load');
        df_test.index.name = 'Time';
        self.check_df_timeseries(df_test, 'get_load.csv');
        
    def test_get_constraint(self):
        '''Test generation of occupancy constraint data using occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            self.occupancy = pickle.load(f);        
        # Simulate occupancy model
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        np.random.seed(1);         
        self.occupancy.simulate(self.start_time, self.final_time);
        constraint = self.occupancy.get_constraint(20, 25);
        # Check references
        df_test = constraint.to_frame(name='constraint');
        df_test.index.name = 'Time';
        self.check_df_timeseries(df_test, 'get_constraint.csv');
        
    def test_error_points_per_day(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            self.occupancy = pickle.load(f);
        # Change occupant measurements to not be whole number in points per day
        self.occupancy.measurements['occupancy']['Sample'] = variables.Static('occupancy_sample', 299, units.s);
        # Estimate occupancy model parameters and expect error
        with self.assertRaises(ValueError):
            np.random.seed(1);
            self.occupancy.estimate(self.start_time, self.final_time);
                                                    
    
if __name__ == '__main__':
    unittest.main()