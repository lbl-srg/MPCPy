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
from matplotlib import pyplot as plt
import pickle
import os

#%%
class SimpleRC(unittest.TestCase):
    '''Test simple model simulate and optimization functions.'''
    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        self.MPCPyPath = utility.get_MPCPy_path();
        # Set model paths
        mopath = self.MPCPyPath+'/resources/model/Simple.mo';
        modelpath = 'Simple.RC';
        # Gather inputs
        input_csv_filepath = self.MPCPyPath+'/resources/model/SimpleRC_Input.csv';
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        self.other_input = exodata.OtherInputFromCSV(input_csv_filepath, variable_map);
        self.other_input.collect_data(self.start_time, self.final_time);
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     other_inputs = self.other_input.data);
    def test_simulate(self):
        self.model.simulate(self.start_time, self.final_time);
        plt.close('all')
        self.model.measurements['T_db']['Simulated'].display_data().plot();
        quantity = self.model.measurements['T_db']['Simulated'].quantity_name;
        unit_name = self.model.measurements['T_db']['Simulated'].display_unit.name;
        plt.ylabel(quantity + ' [' + unit_name + ']');
        plt.savefig(self.MPCPyPath+'/unittests/resources/model_simplerc_simulation' + '.png');
        plt.close();

#%%    
class Estimate_Jmo(unittest.TestCase):
    '''Test the parameter estimation of a model using JModelica.'''
    def setUp(self):
        self.MPCPyPath = utility.get_MPCPy_path();
        ## Setup building fmu emulation
        self.building_source_file_path = self.MPCPyPath + '/resources/building/Examples_LBNL71T_Emulation_WithHeaters_ME2.fmu';
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
                                                 
    def test_simulate(self):
        '''Test the simulation of the model.'''
        plt.close('all');       
        # Simulation time
        self.start_time = '1/1/2015';
        self.final_time = '1/4/2015';        
        
        ## Get emulation data
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
        # Simulate model with current guess of coefficients
        self.model.simulate(self.start_time, self.final_time);
        # Compare model simulation with building emulation
        i = 1;
        for key in ['wesTdb', 'easTdb', 'halTdb', 'Ptot']:
            plt.figure(i)
            data_emulation = self.building.measurements[key]['Measured'].display_data();
            data_model = self.model.measurements[key]['Simulated'].display_data();
            quantity = self.building.measurements[key]['Measured'].quantity_name;
            unit_name = self.building.measurements[key]['Measured'].display_unit.name;
            plt.plot(data_emulation);
            plt.plot(data_model);
            plt.title(key);
            plt.ylabel(quantity + ' [' + unit_name + ']');
            i = i + 1;
            plt.savefig(self.MPCPyPath+'/unittests/resources/model_simulation_' + key + '.png');
            plt.close();
        
    def test_estimate(self):
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

        ## Get emulation data
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
        self.parameters.data = self.model.parameter_data;
        self.parameters.display_data().to_csv(self.MPCPyPath+'/unittests/resources/model_parameters_est.txt')        
        # Validate on validation data
        self.building.collect_measurements(self.start_time_validation, self.final_time_validation);
        self.model.measurements = self.building.measurements;
        self.model.validate(self.start_time_validation, self.final_time_validation, self.MPCPyPath+'/unittests/resources/model_validation');
        # Save coefficients
        self.parameters.data = self.model.parameter_data;
        self.parameters.display_data().to_csv(self.MPCPyPath+'/unittests/resources/model_parameters.txt')
        # Save RMSE
        with open(self.MPCPyPath+'/unittests/resources/model_RMSE.txt', 'w') as f:
            for key in self.model.RMSE.keys():
                f.write(str(key) + ',' + str(self.model.RMSE[key].display_data()) + ',' + self.model.RMSE[key].display_unit.name);
                f.write('\n');
         
#%% Occupancy tests
class Queueing(unittest.TestCase):
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
        self.occupancy.estimate(self.start_time, self.final_time);
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'w') as f:
            pickle.dump(self.occupancy, f);
            
    def test_simulate(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';
        # Load occupancy model
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy = pickle.load(f);
        # Simulate occupancy model
        self.occupancy.simulate(self.start_time, self.final_time);

    def test_validate(self):
        '''Test occupancy prediction comparison with measured data.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';           
        # Load occupancy model
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy = pickle.load(f);
        # Collect validation measurements
        self.building.collect_measurements(self.start_time, self.final_time);             
        # Set valiation measurements in occupancy model        
        self.occupancy.measurements = self.building.measurements;
        # Validate occupancy model with simulation options
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        self.occupancy.set_simulate_options(simulate_options);
        self.occupancy.validate(self.start_time, self.final_time, self.MPCPyPath+'/unittests/resources/occupancy_model_validate');
        
    def test_generate_load(self):
        '''Test generation of occupancy load data using occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy = pickle.load(f);        
        # Simulate occupancy model
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;            
        self.occupancy.simulate(self.start_time, self.final_time);
        load = self.occupancy.generate_load(100);
        load.plot();
        plt.ylabel('Internal Load [W]');
        plt.xlabel('Time');
        plt.savefig(self.MPCPyPath+'/unittests/resources/occupancy_model_load.png');
        plt.close();
        
    def test_generate_constraint(self):
        '''Test generation of occupancy constraint data using occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy = pickle.load(f);        
        # Simulate occupancy model
        simulate_options = self.occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;               
        self.occupancy.simulate(self.start_time, self.final_time);
        constraint = self.occupancy.generate_constraint(20, 25);
        constraint.plot();
        plt.ylim([15,30]);
        plt.ylabel('Temperature [degC]');
        plt.xlabel('Time');
        plt.savefig(self.MPCPyPath+'/unittests/resources/occupancy_model_constraint.png');
        plt.close();
        
    def test_error_points_per_day(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';        
        # Load occupancy model
        with open(self.MPCPyPath+'/unittests/resources/occupancy_model_estimated.txt', 'r') as f:
            self.occupancy = pickle.load(f);
        # Change occupant measurements to not be whole number in points per day
        self.occupancy.measurements['occupancy']['Sample'] = variables.Static('occupancy_sample', 299, units.s);
        # Estimate occupancy model parameters and expect error
        with self.assertRaises(ValueError):
            self.occupancy.estimate(self.start_time, self.final_time);
                                                    
    
if __name__ == '__main__':
    unittest.main()