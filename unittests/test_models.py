# -*- coding: utf-8 -*-
"""
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
    '''Test simple model simulate and estimate.

    '''

    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        
    def tearDown(self):
        del self.start_time
        del self.final_time
        del self.measurements

    def test_simulate(self):
        '''Test simulation of a model.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(self.start_time, self.final_time);
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     control_data = controls.data);
        # Simulate model
        model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_display.csv');
        df_test = model.get_base_measurements('Simulated');
        self.check_df(df_test, 'simulate_base.csv');
        
    def test_simulate_with_save_parameter_input_data(self):
        '''Test simulation of a model.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(self.start_time, self.final_time);
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     control_data = controls.data,
                                     save_parameter_input_data=True);
        # Simulate model
        model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_display.csv');
        df_test = model.get_base_measurements('Simulated');
        self.check_df(df_test, 'simulate_base.csv');

    def test_estimate_one_par(self):
        '''Test the estimation of one parameter of a model.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';
        # Instantiate system
        system = systems.EmulationFromFMU(self.measurements, \
                                               moinfo = (mopath, modelpath, {}));
        system.collect_measurements(self.start_time, self.final_time);
        # Define parameters
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_Value', 55000, units.J_K);
        parameter_data['heatCapacitor.C']['Minimum'] = variables.Static('C_Min', 10000, units.J_K);
        parameter_data['heatCapacitor.C']['Maximum'] = variables.Static('C_Max', 1000000, units.J_K);
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_Free', True, units.boolean);
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     parameter_data = parameter_data);
        # Estimate models
        model.parameter_estimate(self.start_time, self.final_time, ['T_db'])
        # Check references
        data = [model.parameter_data['heatCapacitor.C']['Value'].display_data()]
        index = ['heatCapacitor.C']
        df_test = pd.DataFrame(data=data, index=index, columns=['Value'])
        self.check_df(df_test, 'estimate_one_par.csv', timeseries=False)

    def test_estimate_two_par(self):
        '''Test the estimation of two parameters of a model.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';
        # Instantiate system
        system = systems.EmulationFromFMU(self.measurements, \
                                               moinfo = (mopath, modelpath, {}));
        system.collect_measurements(self.start_time, self.final_time);
        # Define parameters
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_Value', 55000, units.J_K);
        parameter_data['heatCapacitor.C']['Minimum'] = variables.Static('C_Min', 10000, units.J_K);
        parameter_data['heatCapacitor.C']['Maximum'] = variables.Static('C_Max', 1000000, units.J_K);
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_Free', True, units.boolean);
        parameter_data['thermalResistor.R'] = {};
        parameter_data['thermalResistor.R']['Value'] = variables.Static('R_Value', 0.02, units.K_W);
        parameter_data['thermalResistor.R']['Minimum'] = variables.Static('R_Min', 0.001, units.K_W);
        parameter_data['thermalResistor.R']['Maximum'] = variables.Static('R_Max', 0.1, units.K_W);
        parameter_data['thermalResistor.R']['Free'] = variables.Static('R_Free', True, units.boolean);
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     parameter_data = parameter_data);
        # Estimate models
        model.parameter_estimate(self.start_time, self.final_time, ['T_db'])
        # Check references
        data = [model.parameter_data['heatCapacitor.C']['Value'].display_data(),
                model.parameter_data['thermalResistor.R']['Value'].display_data(),]
        index = ['heatCapacitor.C', 'thermalResistor.R']
        df_test = pd.DataFrame(data=data, index=index, columns=['Value'])
        self.check_df(df_test, 'estimate_two_par.csv', timeseries=False)

    def test_simulate_continue(self):
        '''Test simulation of a model in steps.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(self.start_time, self.final_time);
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}), \
                                     control_data = controls.data);
        # Simulate model
        model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_display.csv');

        # Simulate model in 4-hour chunks
        sim_steps = pd.date_range(self.start_time, self.final_time, freq=str('8H'))
        for i in range(len(sim_steps)-1):
            if i == 0:
                model.simulate(sim_steps[i], sim_steps[i+1]);
            else:
                model.simulate('continue', sim_steps[i+1]);
            # Check references
            df_test = model.display_measurements('Simulated');
            self.check_df(df_test, 'simulate_step{0}.csv'.format(i));

    def test_simulate_noinputs(self):
        '''Test simulation of a model with no external inputs.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = (mopath, modelpath, {}));
        # Simulate model
        model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_noinputs.csv');

    def test_estimate_error_nofreeparameters(self):
        '''Test error raised if no free parameters passed.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';
        # Instantiate model
        model_no_params = models.Modelica(models.JModelicaParameter, \
                                               models.RMSE, \
                                               self.measurements, \
                                               moinfo = (mopath, modelpath, {}));
        # Check error raised with no parameters
        with self.assertRaises(ValueError):
            model_no_params.parameter_estimate(self.start_time, self.final_time, []);
        # Set parameters
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_Value', 55000, units.J_K);
        parameter_data['heatCapacitor.C']['Minimum'] = variables.Static('C_Min', 10000, units.J_K);
        parameter_data['heatCapacitor.C']['Maximum'] = variables.Static('C_Max', 100000, units.J_K);
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_Free', False, units.boolean);
        # Instantiate model
        model_no_free = models.Modelica(models.JModelicaParameter, \
                                               models.RMSE, \
                                               self.measurements, \
                                               moinfo = (mopath, modelpath, {}), \
                                               parameter_data = parameter_data);
        # Check error raised with no free parameters
        with self.assertRaises(ValueError):
            model_no_params.parameter_estimate(self.start_time, self.final_time, []);

    def test_estimate_error_nomeasurements(self):
        '''Test error raised if measurement_variable_list not in measurements dictionary.'''
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';
        # Set parameters
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_Value', 55000, units.J_K);
        parameter_data['heatCapacitor.C']['Minimum'] = variables.Static('C_Min', 10000, units.J_K);
        parameter_data['heatCapacitor.C']['Maximum'] = variables.Static('C_Max', 100000, units.J_K);
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_Free', True, units.boolean);
        # Instantiate model
        model_no_meas = models.Modelica(models.JModelicaParameter, \
                                               models.RMSE, \
                                               self.measurements, \
                                               moinfo = (mopath, modelpath, {}), \
                                               parameter_data = parameter_data);
        # Check error raised with no free parameters
        with self.assertRaises(ValueError):
            model_no_meas.parameter_estimate(self.start_time, self.final_time, ['wrong_meas']);
            
    def test_instantiate_error_incompatible_estimation(self):
        '''Test error raised if estimation method is incompatible with model.'''
        # Set model path
        fmupath = os.path.join(self.get_unittest_path(), 'resources', 'building', 'LBNL71T_Emulation_JModelica_v1.fmu');
        with self.assertRaises(ValueError):
            model = models.Modelica(models.JModelicaParameter, models.RMSE, {}, fmupath=fmupath);


#%%
class EstimateFromJModelicaRealCSV(TestCaseMPCPy):
    '''Test parameter estimation of a model using JModelica from real csv data.

    '''

    def setUp(self):
        ## Setup building fmu emulation
        self.building_source_file_path_est = os.path.join(self.get_unittest_path(), 'resources', 'building', 'RealMeasurements_est.csv');
        self.building_source_file_path_val = os.path.join(self.get_unittest_path(), 'resources', 'building', 'RealMeasurements_val.csv');
        self.building_source_file_path_val_missing = os.path.join(self.get_unittest_path(), 'resources', 'building', 'RealMeasurements_val_missing.csv');
        self.zone_names = ['wes', 'hal', 'eas'];
        self.weather_path = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.internal_path = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        self.internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                      'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                      'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                      'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                      'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                      'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                      'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                      'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                      'intLat_eas' : ('eas', 'intLat', units.W_m2)};
        self.control_path = os.path.join(self.get_unittest_path(), 'resources', 'building', 'ControlCSV_0.csv');
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
        self.measurement_variable_map = {'wesTdb_mea' : ('wesTdb', units.K),
                                         'halTdb_mea' : ('halTdb', units.K),
                                         'easTdb_mea' : ('easTdb', units.K),
                                         'wesPhvac_mea' : ('wesPhvac', units.W),
                                         'halPhvac_mea' : ('halPhvac', units.W),
                                         'easPhvac_mea' : ('easPhvac', units.W),
                                         'Ptot_mea' : ('Ptot', units.W)}
        ## Setup model
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_MPC.mo');
        self.modelpath = 'LBNL71T_MPC.MPC';
        self.libraries = os.environ.get('MODELICAPATH');
        self.estimate_method = models.JModelicaParameter;
        self.validation_method = models.RMSE;
        # Instantiate exo data sources
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);
        # Parameters
        self.parameters = exodata.ParameterFromCSV(os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv'));
        self.parameters.collect_data();
        self.parameters.data['lat'] = {};
        self.parameters.data['lat']['Value'] = self.weather.lat;
        # Instantiate test building
        self.building_est = systems.RealFromCSV(self.building_source_file_path_est,
                                            self.measurements,
                                            self.measurement_variable_map,
                                            tz_name = self.weather.tz_name);
        # Exogenous collection time
        self.start_time_exodata = '1/1/2015';
        self.final_time_exodata = '1/30/2015';
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
        # Collect measurement data
        self.building_est.collect_measurements(self.start_time_estimation, self.final_time_estimation);
        # Instantiate model
        self.model = models.Modelica(self.estimate_method, \
                                     self.validation_method, \
                                     self.building_est.measurements, \
                                     moinfo = (self.mopath, self.modelpath, self.libraries), \
                                     zone_names = self.zone_names, \
                                     weather_data = self.weather.data, \
                                     internal_data = self.internal.data, \
                                     control_data = self.control.data, \
                                     parameter_data = self.parameters.data, \
                                     tz_name = self.weather.tz_name);
        # Simulate model with initial guess
        self.model.simulate(self.start_time_estimation, self.final_time_estimation)
        
    def tearDown(self):
        del self.model
        del self.building_est
        del self.weather
        del self.internal
        del self.control
        del self.parameters
        del self.measurements

    def test_estimate_and_validate(self):
        '''Test the estimation of a model's coefficients based on measured data.'''
        plt.close('all');
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_initial_parameters.csv');
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list);
        # Finish test
        self._finish_estimate_validate('')

    def test_estimate_and_validate_missing_measurements(self):
        '''Test the estimation of a model's coefficients based on measured data.

        Some of the validation measurement data is missing.

        '''

        plt.close('all');
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_initial_parameters.csv');
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list);
        # Validate model based on estimation data
        self.model.validate(self.start_time_estimation, self.final_time_estimation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_estimation_csv'), plot=0)
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'estimate_RMSE.csv', timeseries=False);
        # Instantiate validate building
        building_val = systems.RealFromCSV(self.building_source_file_path_val_missing,
                                            self.measurements,
                                            self.measurement_variable_map,
                                            tz_name = self.weather.tz_name);
        # Validate on validation data
        building_val.collect_measurements(self.start_time_validation, self.final_time_validation);
        self.model.measurements = building_val.measurements;
        self.model.validate(self.start_time_validation, self.final_time_validation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_validation_csv'), plot=0);
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'validate_RMSE_missing.csv', timeseries=False);

    def test_estimate_and_validate_global_start_init(self):
        '''Test the estimation of a model's coefficients based on measured data using global start and user-defined initial value.'''
        plt.close('all');
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list, global_start=7, seed=0, use_initial_values=True);
        # Finish test
        self._finish_estimate_validate('_global_start_winit')
        
    def test_estimate_and_validate_global_start_woinit(self):
        '''Test the estimation of a model's coefficients based on measured data using global start and no user-defined initial value.'''
        plt.close('all');
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list, global_start=7, seed=0, use_initial_values=False);
        # Finish test
        self._finish_estimate_validate('_global_start_woinit')
        
    def test_estimate_and_validate_global_start_maxexceeded(self):
        '''Test the estimation of a model's coefficients based on measured data using global start and maximum cpu time and iterations.'''
        plt.close('all');
        # Set maximum cpu time for JModelica
        opt_options = self.model._parameter_estimate_method.opt_problem.get_optimization_options();
        opt_options['IPOPT_options']['max_cpu_time'] = 60;
        opt_options['IPOPT_options']['max_iter'] = 100;
        self.model._parameter_estimate_method.opt_problem.set_optimization_options(opt_options);
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list, global_start=7, seed=0, use_initial_values=True);
        # Finish test
        self._finish_estimate_validate('_global_start_maxexceeded')
        
    def _finish_estimate_validate(self,tag):
        '''Internal method for finishing the estimate and valudate tests.'''
        # Validate model based on estimation data
        self.model.validate(self.start_time_estimation, self.final_time_estimation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_estimation_csv'), plot=0)
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'estimate_RMSE{0}.csv'.format(tag), timeseries=False);
        # All estimates if global estimate
        try:
            glo_est_data_test = self.model.get_global_estimate_data()
            self.check_json(glo_est_data_test, 'estimate_gloest{0}.txt'.format(tag));
        except:
            pass
        # Instantiate validate building
        self.building_val = systems.RealFromCSV(self.building_source_file_path_val,
                                            self.measurements, 
                                            self.measurement_variable_map, 
                                            tz_name = self.weather.tz_name);
        # Validate on validation data
        self.building_val.collect_measurements(self.start_time_validation, self.final_time_validation);
        self.model.measurements = self.building_val.measurements;
        self.model.validate(self.start_time_validation, self.final_time_validation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_validation_csv'), plot=0);
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'validate_RMSE{0}.csv'.format(tag), timeseries=False);

class EstimateFromJModelicaEmulationFMU(TestCaseMPCPy):
    '''Test emulation-based parameter estimation of a model using JModelica.

    '''

    def setUp(self):
        ## Setup building fmu emulation
        self.building_source_file_path = os.path.join(self.get_unittest_path(), 'resources', 'building', 'LBNL71T_Emulation_JModelica_v2.fmu');
        self.zone_names = ['wes', 'hal', 'eas'];
        self.weather_path = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.internal_path = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        self.internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                      'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                      'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                      'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                      'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                      'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                      'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                      'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                      'intLat_eas' : ('eas', 'intLat', units.W_m2)};
        self.control_path = os.path.join(self.get_unittest_path(), 'resources', 'building', 'ControlCSV_0.csv');
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
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_MPC.mo');
        self.modelpath = 'LBNL71T_MPC.MPC';
        self.libraries = os.environ.get('MODELICAPATH');
        self.estimate_method = models.JModelicaParameter;
        self.validation_method = models.RMSE;
        # Instantiate exo data sources
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);
        # Parameters
        self.parameters = exodata.ParameterFromCSV(os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_Parameters.csv'));
        self.parameters.collect_data();
        self.parameters.data['lat'] = {};
        self.parameters.data['lat']['Value'] = self.weather.lat;
        # Instantiate building
        building_parameters_data = {};
        building_parameters_data['lat'] = {};
        building_parameters_data['lat']['Value'] = self.weather.lat;
        self.building = systems.EmulationFromFMU(self.measurements, \
                                                 fmupath = self.building_source_file_path, \
                                                 zone_names = self.zone_names, \
                                                 parameter_data = building_parameters_data);
                                                 
    def tearDown(self):
        del self.building
        del self.weather
        del self.internal
        del self.control
        del self.parameters
        del self.measurements

    def test_estimate_and_validate(self):
        '''Test the estimation of a model's coefficients based on measured data.'''
        plt.close('all');
        # Exogenous collection time
        self.start_time_exodata = '1/1/2015';
        self.final_time_exodata = '1/30/2015';
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
        self.building.collect_measurements(self.start_time_estimation, self.final_time_estimation);
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
                                     tz_name = self.weather.tz_name,
                                     save_parameter_input_data=True);
        # Simulate model with initial guess
        self.model.simulate(self.start_time_estimation, self.final_time_estimation)
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_initial_parameters.csv');
        # Check parameter and input data were saved
        df_test = pd.read_csv('mpcpy_simulation_inputs_model.csv', index_col='Time');
        df_test.index = pd.to_datetime(df_test.index).tz_localize('UTC')
        self.check_df(df_test, 'mpcpy_simulation_inputs_model.csv');
        df_test = pd.read_csv('mpcpy_simulation_parameters_model.csv', index_col='parameter');
        self.check_df(df_test, 'mpcpy_simulation_parameters_model.csv', timeseries=False);   
        # Estimate model based on emulated data
        self.model.parameter_estimate(self.start_time_estimation, self.final_time_estimation, self.measurement_variable_list);
        # Validate model based on estimation data
        self.model.validate(self.start_time_estimation, self.final_time_estimation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_estimation'), plot=0)
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'estimate_RMSE.csv', timeseries=False);
        # Validate on validation data
        self.building.collect_measurements(self.start_time_validation, self.final_time_validation);
        self.model.measurements = self.building.measurements;
        self.model.validate(self.start_time_validation, self.final_time_validation, \
                            os.path.join(self.get_unittest_path(), 'outputs', 'model_validation'), plot=0);
        # Check references
        RMSE = {};
        for key in self.model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = self.model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'validate_RMSE.csv', timeseries=False);

    def test_estimate_error_continue(self):
        '''Test that an error is thrown for estimation start_time of continue.

        '''

        plt.close('all');
        # Exogenous collection time
        start_time_exodata = '1/1/2015';
        final_time_exodata = '1/30/2015';
        # Estimation time
        start_time_estimation = 'continue';
        final_time_estimation = '1/4/2015';
        # Measurement variables for estimate
        self.measurement_variable_list = ['wesTdb', 'easTdb', 'halTdb'];
        # Exodata
        self.weather.collect_data(start_time_exodata, final_time_exodata);
        self.internal.collect_data(start_time_exodata, final_time_exodata);
        self.control.collect_data(start_time_exodata, final_time_exodata);
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
        # Error when estimate model
        with self.assertRaises(ValueError):
            self.model.parameter_estimate(start_time_estimation, final_time_estimation, self.measurement_variable_list);

#%%
class EstimateFromUKF(TestCaseMPCPy):
    '''Test the parameter estimation of a model using UKF.

    '''

    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/10/2017';
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_nostart';
        self.moinfo = (mopath, modelpath, {})
        # Gather parameters
        parameter_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Parameters.csv');
        self.parameters = exodata.ParameterFromCSV(parameter_csv_filepath);
        self.parameters.collect_data();
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        self.controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        self.controls.collect_data(self.start_time, self.final_time);
        # Instantiate system
        self.system = systems.EmulationFromFMU(self.measurements, \
                                               moinfo = self.moinfo, \
                                               control_data = self.controls.data);
        # Get measurements
        self.system.collect_measurements(self.start_time, self.final_time);
        
    def tearDown(self):
        del self.system
        del self.controls
        del self.parameters
        del self.measurements

    def _test_estimate_and_validate(self, fmu_ver):
        '''Test the estimation of a model's coefficients based on measured data.'''
        # Instantiate model
        model = models.Modelica(models.UKFParameter, \
                                     models.RMSE, \
                                     self.system.measurements, \
                                     moinfo = self.moinfo, \
                                     parameter_data = self.parameters.data, \
                                     control_data = self.controls.data, \
                                     version = fmu_ver);
        # Estimate
        model.parameter_estimate(self.start_time, self.final_time, ['T_db']);
        # Validate
        model.validate(self.start_time, self.final_time, 'validate', plot = 0);
        # Check references
        RMSE = {};
        for key in model.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = model.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'validate_RMSE.csv', timeseries=False);
        
    def test_estimate_and_validate_10(self):
        self._test_estimate_and_validate(fmu_ver = '1.0')
        
    def test_estimate_and_validate_20(self):
        self._test_estimate_and_validate(fmu_ver = '2.0')

class StateEstimateFromUKF(TestCaseMPCPy):
    '''Test the state estimation of a model using UKF.

    '''

    def _test_simple_estimate(self, fmu_ver):
        '''Test state estimation on a simple two-state model.
        
        '''
        
        start_time = '1/1/2017';
        final_time = '1/1/2017 12:00:00';
        plot = False
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        measurements['heatCapacitor2.T'] = {'Sample' : variables.Static('T_flo_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.R2C2';
        moinfo = (mopath, modelpath, {})
        # Gather state data
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleEstimatedStates.csv');
        # Instantiate estimated state object
        estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        estimated_states.collect_data()
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate system
        system = systems.EmulationFromFMU(measurements, \
                                          moinfo = moinfo, \
                                          control_data = controls.data);
        # Get measurements
        system.collect_measurements(start_time, final_time);
        
        # Instantiate model
        model = models.Modelica(models.UKFParameter, \
                                     models.RMSE, \
                                     system.measurements, \
                                     models.UKFState, \
                                     moinfo = moinfo, \
                                     estimated_state_data = estimated_states.data, \
                                     control_data = controls.data, \
                                     version = fmu_ver);
        # Estimate
        model.state_estimate(start_time, final_time, ['T_db']);
        # Check references
        df_test = system.display_measurements('Measured')
        est = [x[0] for x in model._state_estimate_method.res_est[1]]
        df_test['heatCapacitor2.T_est'] = est
        self.check_df(df_test, 'estimate_and_validate.csv');
        if plot:
            plt.figure(1)
            plt.plot(df_test['T_db'], '-', label='T_db_meas')
            plt.plot(df_test['heatCapacitor2.T'], '-', label='T_flo_meas')
            plt.plot(df_test['heatCapacitor2.T_est'], 'o', label = 'T_flo_est')
            plt.legend()
            plt.show()
            
    def test_simple_estimate_10(self):
        self._test_simple_estimate(fmu_ver='1.0')
        
    def test_simple_estimate_20(self):
        self._test_simple_estimate(fmu_ver='2.0')
            
    def test_estimationpy_example(self):
        '''Validate state estimation with example from estimationpy package.
        
        The example is the FirstOrder example, and is adapted from
        estimationpy/examples/first_order/run_ukf.py
        
        '''
        
        start_time = '1/1/2017 00:00:00'
        final_time = '1/1/2017 00:00:30'
        plot= False
        # Get estimationpy directory
        ep_dir = self.get_estimationpy_dir()
        # Copy and format data
        csv_file_path = os.path.join(ep_dir, 'estimationpy', 'modelica','FmuExamples','Resources', 'data', 'NoisySimulationData_FirstOrder.csv')
        csv_file_path_new = self.create_mpcpy_csv(csv_file_path)
        # Set measurements
        measurements = {};
        measurements['y'] = {'Sample' : variables.Static('y_sample', 30, units.s)};
        measurements['x'] = {'Sample' : variables.Static('x_sample', 30, units.s)};
        vm_measurements = {'system.y': ('y', units.unit1),
                           'system.x': ('x', units.unit1)}
        # Gather control inputs
        vm_control = {'system.u' : ('u', units.unit1)};
        controls = exodata.ControlFromCSV(csv_file_path_new, vm_control);
        controls.collect_data(start_time, final_time);
        # Instantiate system
        system = systems.RealFromCSV(csv_file_path_new, measurements, vm_measurements)
        # Get measurements
        system.collect_measurements(start_time, final_time);
        # Set model paths
        mopath = os.path.join(ep_dir, 'estimationpy', 'modelica','FmuExamples', 'package.mo')
        modelpath = 'FmuExamples.FirstOrder';
        moinfo = (mopath, modelpath, {})
        # Gather state data
        estimated_state_data = {'x':{'Value':variables.Static('x_init', 1.5, units.unit1)}}    
        # Gather parameter data
        parameter_data = {};
        parameter_data['a'] = {};
        parameter_data['a']['Value'] = variables.Static('a_value', -0.90717055, units.unit1);
        parameter_data['b'] = {};
        parameter_data['b']['Value'] = variables.Static('b_value', 2.28096907, units.unit1);
        parameter_data['c'] = {};
        parameter_data['c']['Value'] = variables.Static('c_value', 3.01419707, units.unit1);
        parameter_data['d'] = {};
        parameter_data['d']['Value'] = variables.Static('d_value', 0.06112703, units.unit1);
        # Instantiate model
        model = models.Modelica(models.UKFParameter, 
                                models.RMSE,
                                measurements,
                                models.UKFState,
                                moinfo = moinfo,
                                estimated_state_data = estimated_state_data,
                                parameter_data = parameter_data,
                                control_data = controls.data)
        # Estimate
        model.state_estimate(start_time, final_time, ['y']);
        # Check references
        df_test = system.display_measurements('Measured')
        x_est = np.array([x[0] for x in model._state_estimate_method.res_est[1]])
        y_est = np.array([x[0] for x in model._state_estimate_method.res_est[3]])
        df_test['x_est'] = x_est
        df_test['y_est'] = y_est
        df_test['x+'] = x_est+np.array(model._state_estimate_method.res_est[2])[:,0,0]
        df_test['x-'] = x_est-np.array(model._state_estimate_method.res_est[2])[:,0,0]
        self.check_df(df_test, 'estimationpy_example.csv');
        if plot:
            plt.figure(1)
            plt.plot(df_test['x_est'], 'o', label='x_est')
            plt.plot(df_test['y_est'], 'o', label='y_est')
            plt.plot(df_test['x+'], '-b')
            plt.plot(df_test['x-'], '-b')
            plt.legend()
            plt.show()
        os.remove(csv_file_path_new)
        
    def test_instantiate_error_incompatible_estimation(self):
        '''Check that the correct FMU model is supplied for UKF state estimation'''

        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.R2C2';
        moinfo = (mopath, modelpath, {})
        with self.assertRaises(ValueError):
            model = models.Modelica(models.UKFParameter, \
                                         models.RMSE, \
                                         {}, \
                                         models.UKFState, \
                                         moinfo = moinfo, \
                                         target = 'cs');        
            
    def get_estimationpy_dir(self):
        '''Return the path of estimationpy on the PYTHONPATH'''
        
        ep_dir = None
        for path in os.environ['PYTHONPATH'].split(os.pathsep):
            if 'EstimationPy' in path:
                ep_dir = path
                break
        if ep_dir is None:
            raise ValueError('Directory for EstimationPy not found on PYTHONPATH')
            
        return ep_dir
        
    def create_mpcpy_csv(self, path):
        '''Converts the example data found in estimationpy to mpcpy format'''
        
        csv_file_path_new = 'ep_input_data.csv'
        df = pd.read_csv(path)
        df.index = pd.to_datetime(pd.to_timedelta(df['time'], unit='s')+pd.to_datetime('1/1/2017'))
        del(df['time'])
        df.index.name = 'Time'
        df.to_csv(csv_file_path_new)
        
        return csv_file_path_new
        
class StateEstimateFromJModelica(TestCaseMPCPy):
    '''Test the state estimation of a model using JModelica.

    '''

    def test_simple_estimate(self):
        '''Test state estimation on a simple two-state model.
        
        '''
        
        start_time = '1/1/2017';
        final_time = '1/1/2017 12:00:00';
        plot = False
        # Set measurements
        measurements = {};
        measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        measurements['heatCapacitor2.T'] = {'Sample' : variables.Static('T_flo_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.R2C2';
        moinfo = (mopath, modelpath, {})
        # Define parameters
        parameter = {};
        parameter['T2o'] = {};
        parameter['T2o']['Value'] = 295
        parameter['T2o']['Minimum'] = 273.15
        parameter['T2o']['Maximum'] = 350
        parameter['T2o']['Free'] = False
        parameter['T2o']['Unit'] = 'K'
        parameter['To'] = {};
        parameter['To']['Value'] = 295
        parameter['To']['Minimum'] = 273.15
        parameter['To']['Maximum'] = 350
        parameter['To']['Free'] = False
        parameter['To']['Unit'] = 'K'
        df_parameter = pd.DataFrame(parameter).transpose()
        parameters = exodata.ParameterFromDF(df_parameter)
        parameters.collect_data()
        # Gather state data
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleEstimatedStates.csv');
        # Instantiate estimated state object
        estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        estimated_states.collect_data()
        # Gather control inputs
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        controls = exodata.ControlFromCSV(control_csv_filepath, variable_map);
        controls.collect_data(start_time, final_time);
        # Instantiate system
        system = systems.EmulationFromFMU(measurements, \
                                          moinfo = moinfo, \
                                          control_data = controls.data);
        # Get measurements
        system.collect_measurements(start_time, final_time);
        
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     system.measurements, \
                                     models.JModelicaState, \
                                     moinfo = moinfo, \
                                     parameter_data = parameters.data, \
                                     estimated_state_data = estimated_states.data, \
                                     control_data = controls.data);
        # Simulate initial guess
        model.simulate(start_time, final_time)
        df_init = model.display_measurements('Simulated')
        # Estimate
        model.state_estimate(start_time, final_time, ['T_db']);
        # Simulate with updated initial value
        model.simulate(start_time, final_time)
        # Check references
        df_test = system.display_measurements('Measured')
        est_value = estimated_states.display_data().loc['heatCapacitor2.T','Value']
        est = model.display_measurements('Simulated')['heatCapacitor2.T']
        df_test['heatCapacitor2.T_est_init'] = df_init['heatCapacitor2.T']
        df_test['heatCapacitor2.T_est_value'] = est_value
        df_test['heatCapacitor2.T_est'] = est
        self.check_df(df_test, 'estimate_and_validate.csv');
        # Check parameters
        df_test_pars = parameters.display_data()
        self.check_df(df_test_pars, 'model_parameters_estimated.csv', timeseries=False);
        # Plot
        if plot:
            plt.figure(1)
            plt.plot(df_test['T_db'], '-', label='T_db_meas')
            plt.plot(df_test['heatCapacitor2.T'], '-', label='T_flo_meas')
            plt.plot(df_test['heatCapacitor2.T_est_init'], '--', label = 'T_flo_est_init')
            plt.plot(df_test['heatCapacitor2.T_est'], '--', label = 'T_flo_est')
            plt.plot(df_test['heatCapacitor2.T_est_value'].index[-1], est_value, 'o', label = 'T_flo_est_value')
            plt.legend()
            plt.show()
            
    def test_replace_parameters(self):
        '''Test the functions that replace the parameters for state estimation.
        
        '''

        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.R2C2';
        moinfo = (mopath, modelpath, {})
        # Define parameters
        parameter = {};
        parameter['T2o'] = {};
        parameter['T2o']['Value'] = 295
        parameter['T2o']['Minimum'] = 273.15
        parameter['T2o']['Maximum'] = 350
        parameter['T2o']['Free'] = False
        parameter['T2o']['Unit'] = 'K'
        parameter['T2o']['Covariance'] = 1
        parameter['To'] = {};
        parameter['To']['Value'] = 295
        parameter['To']['Minimum'] = 273.15
        parameter['To']['Maximum'] = 350
        parameter['To']['Free'] = True
        parameter['To']['Unit'] = 'K'
        parameter['To']['Covariance'] = 2
        df_parameter = pd.DataFrame(parameter).transpose()
        parameters = exodata.ParameterFromDF(df_parameter)
        parameters.collect_data()
        # Gather state data
        csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleEstimatedStates.csv');
        # Instantiate estimated state object
        estimated_states = exodata.EstimatedStateFromCSV(csv_filepath);
        estimated_states.collect_data()            
        # Instantiate model
        model = models.Modelica(models.JModelicaParameter, \
                                     models.RMSE, \
                                     {}, \
                                     models.JModelicaState, \
                                     moinfo = moinfo, \
                                     parameter_data = parameters.data, \
                                     estimated_state_data = estimated_states.data);
        # Check original parameters
        df_test_pars = parameters.display_data()
        self.check_df(df_test_pars, 'model_parameters_check.csv', timeseries=False);
        # Replace parameters and check
        model._state_estimate_method._replace_parameter_data(model)
        df_test_pars = parameters.display_data()
        self.check_df(df_test_pars, 'model_parameters_replaced_check.csv', timeseries=False);
        # Restore parameters and check with original
        model._state_estimate_method._restore_parameter_data(model)
        df_test_pars = parameters.display_data()
        self.check_df(df_test_pars, 'model_parameters_check.csv', timeseries=False);
        

#%% Occupancy tests
class OccupancyFromQueueing(TestCaseMPCPy):
    '''Test the occupancy model using a queueing approach.

    '''

    def setUp(self):
        # Testing time
        self.start_time = '3/8/2013';
        self.final_time = '3/15/2013 23:59';
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
        # Where to save ref occupancy model
        self.occupancy_model_file = self.get_ref_path() + os.sep +'occupancy_model_estimated.txt';

    def tearDown(self):
        del self.building
        del self.measurements

    def test_estimate(self):
        '''Test the estimation method.'''
        plt.close('all');
        # Training Time
        start_time = '2/1/2013';
        final_time = '7/24/2013 23:59';
        # Collect measurements
        self.building.collect_measurements(start_time, final_time);
        # Instantiate occupancy model
        occupancy = models.Occupancy(models.QueueModel, self.building.measurements);
        # Estimate occupancy model parameters
        np.random.seed(1);
        occupancy.estimate(start_time, final_time);
        try:
            with open(self.occupancy_model_file, 'r') as f:
                occupancy = pickle.load(f);
        except IOError:
            try:
                os.makedirs(self.get_ref_path());
            except OSError:
                pass;
            with open(self.occupancy_model_file, 'w') as f:
                pickle.dump(occupancy, f);

    def test_simulate(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            occupancy = pickle.load(f);
        # Simulate occupancy model
        np.random.seed(1);
        occupancy.simulate(self.start_time, self.final_time);
        # Check references
        df_test = occupancy.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_display.csv');
        df_test = occupancy.get_base_measurements('Simulated');
        self.check_df(df_test, 'simulate_base.csv');

    def test_validate(self):
        '''Test occupancy prediction comparison with measured data.'''
        plt.close('all');
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            occupancy = pickle.load(f);
        # Collect validation measurements
        self.building.collect_measurements(self.start_time, self.final_time);
        # Set valiation measurements in occupancy model
        occupancy.measurements = self.building.measurements;
        # Validate occupancy model with simulation options
        simulate_options = occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        occupancy.set_simulate_options(simulate_options);
        np.random.seed(1);
        occupancy.validate(self.start_time, self.final_time, \
                                os.path.join(self.get_unittest_path(), 'outputs', \
                                             'occupancy_model_validate'));
        # Check references
        RMSE = {};
        for key in occupancy.RMSE.keys():
            RMSE[key] = {};
            RMSE[key]['Value'] = occupancy.RMSE[key].display_data();
        df_test = pd.DataFrame(data = RMSE);
        self.check_df(df_test, 'validate_RMSE.csv', timeseries=False);

    def test_get_load(self):
        '''Test generation of occupancy load data using occupancy prediction.'''
        plt.close('all');
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            occupancy = pickle.load(f);
        # Simulate occupancy model
        simulate_options = occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        np.random.seed(1);
        occupancy.simulate(self.start_time, self.final_time);
        load = occupancy.get_load(100);
        # Check references
        df_test = load.to_frame(name='load');
        df_test.index.name = 'Time';
        self.check_df(df_test, 'get_load.csv');

    def test_get_constraint(self):
        '''Test generation of occupancy constraint data using occupancy prediction.'''
        plt.close('all');
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            occupancy = pickle.load(f);
        # Simulate occupancy model
        simulate_options = occupancy.get_simulate_options();
        simulate_options['iter_num'] = 5;
        np.random.seed(1);
        occupancy.simulate(self.start_time, self.final_time);
        constraint = occupancy.get_constraint(20, 25);
        # Check references
        df_test = constraint.to_frame(name='constraint');
        df_test.index.name = 'Time';
        self.check_df(df_test, 'get_constraint.csv');

    def test_error_points_per_day(self):
        '''Test occupancy prediction.'''
        plt.close('all');
        # Time
        self.start_time = '3/1/2013';
        self.final_time = '3/7/2013 23:59';
        # Load occupancy model
        with open(self.occupancy_model_file, 'r') as f:
            occupancy = pickle.load(f);
        # Change occupant measurements to not be whole number in points per day
        occupancy.measurements['occupancy']['Sample'] = variables.Static('occupancy_sample', 299, units.s);
        # Estimate occupancy model parameters and expect error
        with self.assertRaises(ValueError):
            np.random.seed(1);
            occupancy.estimate(self.start_time, self.final_time);

if __name__ == '__main__':
    unittest.main()
