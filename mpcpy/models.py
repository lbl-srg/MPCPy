# -*- coding: utf-8 -*-
"""
``models`` classes are models that are used for performance prediction in MPC.
This includes models for physical systems (e.g. thermal envelopes, HVAC 
equipment, facade elements) and occupants at the component level or at an 
aggregated level (e.g. zone, building, campus).

========
Modelica
========

``Modelica`` model objects utilize models represented in Modelica or by an FMU.

Classes
=======

.. autoclass:: mpcpy.models.Modelica
    :members: parameter_estimate, state_estimate, validate, simulate, set_parameter_estimate_method, 
              set_state_estimate_method, set_validate_method, display_measurements, 
              get_base_measurements

Parameter Estimate Methods
==========================

.. autoclass:: mpcpy.models.JModelicaParameter

.. autoclass:: mpcpy.models.UKFParameter

State Estimate Methods
======================

.. autoclass:: mpcpy.models.JModelicaState

.. autoclass:: mpcpy.models.UKFState

Validate Methods
================

.. autoclass:: mpcpy.models.RMSE

=========
Occupancy
=========

``Occupancy`` models consider when occupants arrive and depart a space 
or building as well as how many occupants are present at a particular time.

Classes
=======

.. autoclass:: mpcpy.models.Occupancy
    :members: estimate, validate, simulate, get_load, get_constraint, 
              get_estimate_options, set_occupancy_method, get_simulate_options,
              set_estimate_options, set_simulate_options, display_measurements, 
              get_base_measurements

Occupancy Methods
=================

.. autoclass:: mpcpy.models.QueueModel

"""

from abc import ABCMeta, abstractmethod
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv
import logging
import pdb
from datetime import timedelta
from mpcpy import units
from mpcpy import variables
from mpcpy import utility
from mpcpy import optimization
from occupant.occupancy.queueing.adaptive_breakpoint_placement import adaptive_breakpoint_placement
from occupant.occupancy.queueing.simulate_queue import simulate_queue
from occupant.occupancy.queueing.unique_last import unique_last
from occupant.occupancy.queueing.interp1 import interp1
from occupant.occupancy.queueing.parameter_inference_given_segments import parameter_inference_given_segment
from estimationpy.fmu_utils import model as ukf_model
from estimationpy.ukf.ukf_fmu import UkfFmu
from estimationpy.fmu_utils import estimationpy_logging
import pyDOE as doe
import copy
import os

#%% Model Class
class _Model(utility._mpcpyPandas, utility._Measurements):
    '''Base class for representing a model for MPC.
    
    '''

    __metaclass__ = ABCMeta;

    @abstractmethod
    def parameter_estimate(self):
        '''Estimate parameters of the model using the measurement and 
        parameter_data dictionary attributes.

        Yields
        ------
        Updates the ``'Value'`` key for each estimated parameter in the 
        parameter_data attribute.

        '''

        pass;

    @abstractmethod
    def state_estimate(self):
        '''Estimate states of the model using measurements dictionary attributes.

        Yields
        ------
        Updates the ``'Value'`` key for each estimated state in the 
        state_data attribute.

        '''

        pass;
        
    @abstractmethod        
    def validate(self):
        '''Validate parameters of the model using the measurement and 
        parameter_data dictionary attributes.

        '''

        pass;

    @abstractmethod        
    def simulate(self):
        '''Simulate the model using any given exodata inputs.

        Yields
        ------
        Updates the ``'Simulated'`` key for each measured variable in the 
        measurements dictionary attribute.

        '''

        pass;

#%% Parameter Method Interface
class _ParameterEstimate(utility._mpcpyPandas):
    '''Interface for a model parameter estimation method.
    
    '''
    
    __metaclass__ = ABCMeta;   
    
    @abstractmethod
    def _estimate():
        '''Estimation method-specific call to perform the parameter estimation.
        
        Parameters
        ----------
        Model : mpcpy.Models._Model object
            The model on which the parameter estimation is performed.  Please
            see documentation on the _Model class for info about attributes.
        
        Yields
        ------
        parameter_data : dictionary
            Updates the ``'Value'`` key for each estimated parameter in the 
            parameter_data attribute of the Model.
            
        '''
                
        pass;
        
#%% State Estimate Method Interface
class _StateEstimate(utility._mpcpyPandas):
    '''Interface for a model state estimation method.
    
    '''
    
    __metaclass__ = ABCMeta;   
    
    @abstractmethod
    def _estimate():
        '''Estimation method-specific call to perform the state estimation.
        
        Parameters
        ----------
        Model : mpcpy.Models._Model object
            The model on which the state estimation is performed.  Please
            see documentation on the _Model class for info about attributes.
        
        Yields
        ------
        estimated_state_data : dictionary
            Updates the ``'Value'`` key for each estimated states in the 
            estimated_state_data attribute of the Model.
            
        '''
                
        pass;
        
#%% ValidateMethod Interface
class _Validate(utility._mpcpyPandas):
    '''Interface for a model validation method.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    @abstractmethod
    def _validate():
        pass;
        
    def _plot_simple(self,Model,validate_filename):
        '''Plot the estimated estimated and measured data.
        
        '''
        
        self.plot = {};
        for key in Model.measurements.keys():
            plt.close('all');
            measurement = Model.measurements[key]['Measured'];
            measurement.set_display_unit(measurement.get_base_unit());
            estimated_measurement = Model.measurements[key]['Simulated'];
            estimated_measurement.set_display_unit(estimated_measurement.get_base_unit());
            measurement.display_data(tz_name = Model.tz_name)[Model.start_time:Model.final_time].plot( \
                   label = key+'_measured', linewidth = 2.0, linestyle = '-', rot = 90);
            estimated_measurement.display_data()[Model.start_time:Model.final_time].plot( \
                   label = key+'_estimated', linewidth = 2.0, linestyle = '--', rot = 90);
            plt.xlabel('Time (hr)');
            yname = measurement.quantity_name;
            yunit = measurement.get_display_unit_name();
            plt.ylabel(yname + ' [' + yunit + ']');
            plt.rcParams.update({'font.size': 16});
            plt.legend();
            plt.savefig(validate_filename + '_' + key + '.png');

#%% OccupancyModelMethod Interface
class _OccupancyMethod(utility._mpcpyPandas):
    '''Interface for an occupancy model.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    @abstractmethod
    def _estimate():
        pass;
    @abstractmethod
    def _validate():
        pass;
    @abstractmethod
    def _simulate():
        pass            
             
#%% Parameter Estimate Method Interface Implementations
class JModelicaParameter(_ParameterEstimate):
    '''Parameter Estimation method using JModelica optimization.
    
    This estimation method sets up a parameter estimation problem to be solved
    using JModelica_.
    
    .. _JModelica: http://jmodelica.org/

    '''

    def __init__(self, Model):
        '''Constructor of JModelica estimation method.

        '''

        self.name = 'Jmo';        
        self.opt_problem = optimization.Optimization(Model, optimization._ParameterEstimate, optimization.JModelica, {});
        
    def _estimate(self, Model):
        '''Perform estimation using JModelica optimization.

        '''

        self.opt_problem.optimize(Model.start_time, Model.final_time, measurement_variable_list = Model.measurement_variable_list);
        

class UKFParameter(_ParameterEstimate, utility._FMU):
    '''Parameter estimation method using the Unscented Kalman Filter.
    
    This estimation method uses the UKF implementation EstimationPy_.
    
    .. _EstimationPy: https://github.com/lbl-srg/EstimationPy

    '''

    def __init__(self, Model):
        '''Constructor of UKF estimation method.
        
        '''

        self.name = 'UKF';
        self.fmu_version = Model.fmu_version;
        # Instantiate UKF model
        self.model = ukf_model.Model(Model.fmupath);
        
    def _estimate(self, Model, style='parameter'):
        '''Perform UKF estimation.

        '''

        estimationpy_logging.configure_logger(log_level = logging.DEBUG, log_level_console = logging.INFO, log_level_file = logging.DEBUG)
        # Write the inputs, measurements, and parameters to csv
        self._writeukfcsv(Model);
        # Select inputs
        for key in Model.input_names:
            inputvar = self.model.get_input_by_name(key);
            inputvar.get_csv_reader().open_csv(self.csv_path);
            inputvar.get_csv_reader().set_selected_column(key);    
        # Select outputs
        for key in Model.measurement_variable_list:
            outputvar = self.model.get_output_by_name(key);
            outputvar.get_csv_reader().open_csv(self.csv_path);
            outputvar.get_csv_reader().set_selected_column(key);        
            outputvar.set_measured_output()
            outputvar.set_covariance(0.5);
        # Select the parameters to be identified
        i = 0;
        for key in Model.parameter_data.keys():
            if Model.parameter_data[key]['Free'].get_base_data():
                self.model.add_parameter(self.model.get_variable_object(key));
                par = self.model.get_parameters()[i];
                par.set_initial_value(Model.parameter_data[key]['Value'].get_base_data());
                par.set_covariance(Model.parameter_data[key]['Covariance'].get_base_data());
                par.set_min_value(Model.parameter_data[key]['Minimum'].get_base_data());
                par.set_max_value(Model.parameter_data[key]['Maximum'].get_base_data());
                par.set_constraint_low(True);
                par.set_constraint_high(True);
                i = i + 1;
        # Initialize the model for the simulation
        self.model.initialize_simulator();
        # Set model parameters
        for name in Model.parameter_data.keys():
            self.model.set_real(self.model.get_variable_object(name),Model.parameter_data[name]['Value'].get_base_data());
        # Instantiate the UKF for the FMU
        ukf_FMU = UkfFmu(self.model);
        # Start filter
        t0 = pd.to_datetime(0, unit = "s", utc = True);
        t1 = pd.to_datetime(Model.elapsed_seconds, unit = "s", utc = True);
        self.res_est = ukf_FMU.filter(start = t0, stop = t1);
        # Update parameter results
        self._get_parameter_results(Model);
        
    def _writeukfcsv(self, Model):
        '''Write the UKF csv file.

        '''

        # Collect additional inputs for csv file     
        self._additional_inputs = {};
        # Measurements
        for key_mea in Model.measurement_variable_list:
            variable = Model.measurements[key_mea];
            self._additional_inputs[key_mea] = {};
            self._additional_inputs[key_mea] = variable['Measured'];
        # Parameters
        free_parameters = [];
        for key_par in Model.parameter_data.keys():
            variable = Model.parameter_data[key_par];
            if variable['Free'].get_base_data():
                free_parameters.append(key_par)
                time = self._additional_inputs[key_mea].get_base_data().index.values;
                data = variable['Value'].get_base_data()*np.ones(len(time));
                unit = variable['Value'].get_base_unit();
                ts = pd.Series(index = time, data = data)
                self._additional_inputs[key_par] = variables.Timeseries(key_par+'_ukf', ts, unit);
                
        # Create mpcpy ts list
        self._input_mpcpy_ts_list = [];
        # Weather
        for key in Model.weather_data.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.weather_data[key]);
        # Internal
        for zone in Model.internal_data.keys():
            for intLoad in ['intCon', 'intRad', 'intLat']:
                if intLoad+'_'+zone in Model.input_names:
                    self._input_mpcpy_ts_list.append(Model.internal_data[zone][intLoad]);
        # Controls
        for key in Model.control_data.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.control_data[key]);                     
        # Other inputs                   
        for key in Model.other_inputs.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.other_inputs[key]);
        # Add measurements and parameters
        for key in self._additional_inputs.keys():
            self._input_mpcpy_ts_list.append(self._additional_inputs[key]);
            
        # Create input object to write to csv
        # Set timing
        self.start_time_utc = Model.start_time_utc;
        self.final_time_utc = Model.final_time_utc;   
        self._global_start_time_utc = Model._global_start_time_utc
        self.elapsed_seconds = Model.elapsed_seconds;  
        self.total_elapsed_seconds = Model.total_elapsed_seconds;
        self._create_input_object_from_input_mpcpy_ts_list(self._input_mpcpy_ts_list)
        # Write to csv
        self.csv_path = 'ukf.csv';                                               
        with open(self.csv_path, 'wb') as f:
            ukfwriter = csv.writer(f);
            ukfwriter.writerow(['time'] + list(self._input_object[0]));
            for i in range(len(self._input_object[1][:,0])):
                ukfwriter.writerow(self._input_object[1][i]);

    def _get_parameter_results(self, Model):
        '''Update the parameter data dictionary in the model with ukf results.
        
        '''
        
        i = 0;
        for key in Model.parameter_data.keys():
            if Model.parameter_data[key]['Free'].get_base_data():
                fmu_variable_units = Model._get_fmu_variable_units();
                unit = self._get_unit_class_from_fmu_variable_units(key, fmu_variable_units);
                if not unit:
                    unit = units.unit1;
                data = self.res_est[1][-1][i];
                Model.parameter_data[key]['Value'].set_display_unit(unit);
                Model.parameter_data[key]['Value'].set_data(data);
                i = i + 1;

class JModelicaState(_ParameterEstimate):
    '''State Estimation method using JModelica optimization.
    
    This estimation method sets up a simple moving horizon state estimation problem 
    to be solved using JModelica_.  The method uses a parameter estimation with
    altered parameter data to estimate only initial states.  Given a time
    period of observed state data, the method sets up and solves an optimization
    problem to find the optimal values of the estimated states at the initial
    time of the time period that minimizes the error between the measured
    observed states and modeled observed states.  Then, the final value of
    the estimated states are taken as the current state estimates.
    
    .. _JModelica: http://jmodelica.org/

    '''

    def __init__(self, Model):
        '''Constructor of JModelica estimation method.

        '''

        self.name = 'Jmo';       
        # Replace parameter data for state estimation
        self._replace_parameter_data(Model)
        # Instantiate state estimation optimization problem
        self.opt_problem = optimization.Optimization(Model, optimization._ParameterEstimate, optimization.JModelica, {});
        # Restore original parameter data
        self._restore_parameter_data(Model)
        
    def _estimate(self, Model):
        '''Perform estimation using JModelica optimization.

        '''

        # Replace parameter data for state estimation
        self._replace_parameter_data(Model)
        # Solve problem, which updates parameter estimates
        self.opt_problem.optimize(Model.start_time, Model.final_time, measurement_variable_list = Model.measurement_variable_list);
        # Update estimated state data with updated parameter estimates
        self._get_state_results(Model)
        # Restore original parameter data
        self._restore_parameter_data(Model)
                
    def _replace_parameter_data(self, Model):
        '''Replaces the parameter_data in the Model for state estimation.
        
        '''
        
        # Find all parameters that are state initializers
        pars_state = []
        for key in Model.estimated_state_data.keys():
            pars_state.append(Model.estimated_state_data[key]['Parameter'])
        # Set parameters of state initialization to free, all others not free
        # Keep track of which parameters were changed so that can change back
        self.__change_false_to_true = []
        self.__change_true_to_false = []
        for key in Model.parameter_data.keys():
            if key in pars_state:
                if not Model.parameter_data[key]['Free'].display_data():    
                    Model.parameter_data[key]['Free'].set_data(True)
                    self.__change_false_to_true.append(key)
            else:
                if Model.parameter_data[key]['Free'].display_data():
                    Model.parameter_data[key]['Free'].set_data(False)
                    self.__change_true_to_false.append(key)
                
    def _restore_parameter_data(self, Model):
        '''Restores the parameter_data in the Model for state estimation.
        
        '''
        
        # Change back to how parameters were originally defined
        for key in Model.parameter_data.keys():
            if key in self.__change_false_to_true:
                Model.parameter_data[key]['Free'].set_data(False)
            if key in self.__change_true_to_false:
                Model.parameter_data[key]['Free'].set_data(True)

    def _get_state_results(self, Model):
        '''Update the state data dictionary in the model with ukf results.
        
        '''
        
        i = 0;
        for key in Model.estimated_state_data.keys():
            fmu_variable_units = Model._get_fmu_variable_units();
            unit = Model._get_unit_class_from_fmu_variable_units(key, fmu_variable_units);
            if not unit:
                unit = units.unit1;
            data = self.opt_problem._package_type.res_opt['mpc_model.' + key][-1];
            Model.estimated_state_data[key]['Value'].set_display_unit(unit);
            Model.estimated_state_data[key]['Value'].set_data(data);
            i = i + 1;        

class UKFState(_StateEstimate, utility._FMU):
    '''State estimation method using the Unscented Kalman Filter.
    
    This estimation method uses the UKF implementation EstimationPy_.
    
    .. _EstimationPy: https://github.com/lbl-srg/EstimationPy

    '''

    def __init__(self, Model):
        '''Constructor of UKF estimation method.
        
        '''

        self.name = 'UKF';
        # Get fmu path name            
        fmupath = Model.fmupath
        # Instantiate UKF model
        self.model = ukf_model.Model(fmupath);
        
    def _estimate(self, Model):
        '''Perform UKF estimation.

        '''

        estimationpy_logging.configure_logger(log_level = logging.INFO, log_level_console = logging.INFO, log_level_file = logging.INFO)
        # Write the inputs, measurements, and parameters to csv
        self._writeukfcsv(Model);
        # Select inputs
        for key in Model.input_names:
            inputvar = self.model.get_input_by_name(key);
            inputvar.get_csv_reader().open_csv(self.csv_path);
            inputvar.get_csv_reader().set_selected_column(key);    
        # Select outputs
        for key in Model.measurement_variable_list:
            outputvar = self.model.get_output_by_name(key);
            outputvar.get_csv_reader().open_csv(self.csv_path);
            outputvar.get_csv_reader().set_selected_column(key);        
            outputvar.set_measured_output()
            outputvar.set_covariance(0.5);
        # Select the states to be estimated
        i = 0;
        for key in Model.estimated_state_data.keys():
            self.model.add_variable(self.model.get_variable_object(key));
            var = self.model.get_variables()[i];
            var.set_initial_value(Model.estimated_state_data[key]['Value'].get_base_data());
            i = i + 1;
        # Initialize the model for the simulation
        self.model.initialize_simulator();
        # Set model parameters
        for name in Model.parameter_data.keys():
            self.model.set_real(self.model.get_variable_object(name),Model.parameter_data[name]['Value'].get_base_data());
        # Instantiate the UKF for the FMU
        ukf_FMU = UkfFmu(self.model);
        # Start filter
        t0 = pd.to_datetime(0, unit = "s", utc = True);
        t1 = pd.to_datetime(Model.elapsed_seconds, unit = "s", utc = True);
        self.res_est = ukf_FMU.filter(start = t0, stop = t1);
        # Update parameter results
        self._get_state_results(Model);
        
    def _writeukfcsv(self, Model):
        '''Write the UKF csv file.

        '''

        # Collect additional inputs for csv file     
        self._additional_inputs = {};
        # Measurements
        for key_mea in Model.measurement_variable_list:
            variable = Model.measurements[key_mea];
            self._additional_inputs[key_mea] = {};
            self._additional_inputs[key_mea] = variable['Measured'];
        # Parameters
        free_parameters = [];
        for key_par in Model.parameter_data.keys():
            variable = Model.parameter_data[key_par];
            if variable['Free'].get_base_data():
                free_parameters.append(key_par)
                time = self._additional_inputs[key_mea].get_base_data().index.values;
                data = variable['Value'].get_base_data()*np.ones(len(time));
                unit = variable['Value'].get_base_unit();
                ts = pd.Series(index = time, data = data)
                self._additional_inputs[key_par] = variables.Timeseries(key_par+'_ukf', ts, unit);
                
        # Create mpcpy ts list
        self._input_mpcpy_ts_list = [];
        # Weather
        for key in Model.weather_data.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.weather_data[key]);
        # Internal
        for zone in Model.internal_data.keys():
            for intLoad in ['intCon', 'intRad', 'intLat']:
                if intLoad+'_'+zone in Model.input_names:
                    self._input_mpcpy_ts_list.append(Model.internal_data[zone][intLoad]);
        # Controls
        for key in Model.control_data.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.control_data[key]);                     
        # Other inputs                   
        for key in Model.other_inputs.keys():
            if key in Model.input_names:
                self._input_mpcpy_ts_list.append(Model.other_inputs[key]);
        # Add measurements and parameters
        for key in self._additional_inputs.keys():
            self._input_mpcpy_ts_list.append(self._additional_inputs[key]);
            
        # Create input object to write to csv
        # Set timing
        self.start_time_utc = Model.start_time_utc;
        self.final_time_utc = Model.final_time_utc;   
        self._global_start_time_utc = Model._global_start_time_utc
        self.elapsed_seconds = Model.elapsed_seconds;  
        self.total_elapsed_seconds = Model.total_elapsed_seconds;
        self._create_input_object_from_input_mpcpy_ts_list(self._input_mpcpy_ts_list)
        # Write to csv
        self.csv_path = 'ukf.csv';                                               
        with open(self.csv_path, 'wb') as f:
            ukfwriter = csv.writer(f);
            ukfwriter.writerow(['time'] + list(self._input_object[0]));
            for i in range(len(self._input_object[1][:,0])):
                ukfwriter.writerow(self._input_object[1][i]);

    def _get_state_results(self, Model):
        '''Update the state data dictionary in the model with ukf results.
        
        '''
        
        i = 0;
        for key in Model.estimated_state_data.keys():
            fmu_variable_units = Model._get_fmu_variable_units();
            unit = self._get_unit_class_from_fmu_variable_units(key, fmu_variable_units);
            if not unit:
                unit = units.unit1;
            data = self.res_est[1][-1][i];
            Model.estimated_state_data[key]['Value'].set_display_unit(unit);
            Model.estimated_state_data[key]['Value'].set_data(data);
            i = i + 1;
       
#%% Validate Method Interfaces
class RMSE(_Validate):
    '''Validation method that computes the RMSE between estimated and measured data.
    
    Only modeled values with measurements corresponding to the same time
    are considered in the calculation of RMSE.  If a measurement is 
    detected as missing, a warning is printed.
    
    Yields
    ------
    RMSE : dictionary
        {"Measurement Name" : mpcpy.Variables.Static}.
        Attribute of the model object that contains the RMSE for each 
        measurement variable used to perform the validation in base units.
    
    '''

    def __init__(self, Model):
        '''Constructor of the RMSE validation method class
        
        '''

        pass;

    def _validate(self, Model, validate_filename, plot = 1):
        '''Perform the validation.
        
        '''

        Model.RMSE = {};
        for key in Model.measurements.keys():
            data = Model.measurements[key]['Measured'].get_base_data().loc[Model.start_time_utc:Model.final_time_utc];
            data_est = Model.measurements[key]['Simulated'].get_base_data().loc[Model.start_time_utc:Model.final_time_utc];
            summed = 0;
            length = 0;
            for i in range(len(data_est)):
                t = data_est.index.values[i]
                try:
                    diff = (data_est.loc[t] - data.loc[t])**2
                    summed = summed + diff;
                    length = length + 1;
                except KeyError:
                    print('WARNING: Time {0} missing in measured data.  Model value at time is {1}.'.format(t,data_est.loc[t]));
            RMSE = np.sqrt(summed/length);
            unit_class = Model.measurements[key]['Measured'].get_base_unit();
            Model.RMSE[key] = variables.Static('RMSE_'+key, RMSE, unit_class);
        if plot == 1:
            self._plot_simple(Model, validate_filename);
            
#%% OccupanctPresence Model Types
class QueueModel(_OccupancyMethod):
    '''Occupancy presence prediction based on a queueing approach.

    Based on Jia, R. and C. Spanos (2017). "Occupancy modelling in shared 
    spaces of buildings: a queueing approach." Journal of Building Performance 
    Simulation, 10(4), 406-421.
    
    See ``occupant.occupancy.queueing`` for more information.
    
    Attributes
    ----------
    estimate_options : dictionary
        Specifies options for model estimation with the following keys:
        -res : defines the resolution of grid search for the optimal breakpoint placement 
        -margin : specifies the minimum distance between two adjacent breakpoints
        -n_max : defines the upper limit of the number of breakpoints returned by the algorithm
    simulate_options : dictionary
        Specifies options for model simulation.  
        -iter_num : defines the number of iterations for monte-carlo simulation.

    '''

    def __init__(self):
        '''Constructor of an occupancy model object using a queueing approach.

        '''

        # Initialize options
        self.estimate_options = {};
        self.estimate_options['res'] = 3;
        self.estimate_options['margin'] = 3;
        self.estimate_options['n_max'] = 24;
        self.simulate_options = {};
        self.simulate_options['iter_num'] = 100;
        
    def _estimate(self, Model):
        '''Use measured occupancy data to estimate the queue model parameters.

        '''

        # Set estimation options
        res = self.estimate_options['res'];
        margin = self.estimate_options['margin'];
        n_max = self.estimate_options['n_max'];
        # Initialize variables
        Model.parameters_data['lam'] = {};
        Model.parameters_data['mu'] = {};
        self.seg_point = [];
        self.empty_time = [];
        # Estimate a queue model for each day of the week using training data
        for day in range(7):
            # Format training data
            self._format_training_data(Model, day);
            # Find breakpoints - segment the day into some homogeneous pieces
            self.seg_point.append(adaptive_breakpoint_placement(self.data_train,res=res,margin=margin,n_max=n_max));
            # Learn the arrival and departure rates for each segment
            self.seg_point[day] = np.sort(self.seg_point[day])
            val_size = self.data_train.shape[0];
            seg_num = len(self.seg_point[day])+1;
            lam_all = np.empty((seg_num,val_size));
            mu_all = np.empty((seg_num,val_size));
            presence = np.where(np.mean(self.data_train,axis=0)!=0);
            self.empty_time.append(presence[0][-1]+1);
            for i in range(val_size):
                x = self.data_train[i,:];
                [lam_temp, mu_temp] = parameter_inference_given_segment(x, self.seg_point[day],self.empty_time[day]);
                lam_all[:,i] = lam_temp;
                mu_all[:,i] = mu_temp;
            self.lam = np.mean(lam_all,axis = 1);
            self.mu = np.mean(mu_all,axis = 1);
            # Store estimated model parameters
            Model.parameters_data['lam'][day] = {};
            Model.parameters_data['lam'][day]['Free'] = variables.Static('lam_'+str(day)+'_free', True, units.boolean);
            Model.parameters_data['lam'][day]['Value'] = variables.Static('lam_'+str(day)+'_value', self.lam, units.unit1);
            Model.parameters_data['mu'][day] = {};
            Model.parameters_data['mu'][day]['Free'] = variables.Static('mu_'+str(day)+'_free', True, units.boolean);
            Model.parameters_data['mu'][day]['Value'] = variables.Static('mu_'+str(day)+'_value', self.mu, units.unit1);
        
    def _validate(self, Model, plot):
        '''Compare occupancy predictions to measurements.

        '''

        # Load prediction and measurement data
        prediction = Model.measurements[self.occ_key]['Simulated'].display_data();
        std = Model.measurements[self.occ_key]['SimulatedError'].display_data();
        measurements = Model.measurements[self.occ_key]['Measured'].display_data()[Model.start_time:Model.final_time];
        prediction_pstd = prediction+std;
        prediction_mstd = prediction-std;
        prediction_mstd = (prediction_mstd>=0)*prediction_mstd;
        
        Model.RMSE = {};
        for key in Model.measurements.keys():
            data = Model.measurements[key]['Measured'].get_base_data()[Model.start_time:Model.final_time];
            data_est = Model.measurements[key]['Simulated'].get_base_data()[Model.start_time:Model.final_time];
            RMSE = np.sqrt(sum((data_est-data)**2)/len(data));
            unit_class = Model.measurements[key]['Measured'].get_base_unit();
            Model.RMSE[key] = variables.Static('RMSE_'+key, RMSE, unit_class);
        if plot == 1:
            # Plot data to compare
            measurements.plot(label = 'measured', color = 'k', alpha = 0.5);
            prediction.plot(label='prediction', color = 'r', alpha = 0.5);
            plt.fill_between(prediction.index, prediction_pstd, prediction_mstd, color = 'r', alpha = 0.5);     
            plt.legend();
            plt.savefig(Model.validate_filename+'.png')        
        
    def _simulate(self, Model):
        '''Use Monte Carlo simulation to predict an occupancy timeseries.

        '''

        # Set the number of simulations for the Monte Carlo 
        iter_num = self.simulate_options['iter_num'];
        # Initialize variables 
        ts_pred = pd.Series();
        ts_std = pd.Series();
        d = 0;
        # Get weekdays of simulation time period
        date_range = pd.date_range(Model.start_time, Model.final_time, freq = 'D');
        # Monte Carlo simulate each day of the simulation time period
        for day in date_range.weekday:
            seg_point_added = np.concatenate((np.array([0]),self.seg_point[day], np.array([self.points_per_day])))
            lam_vec = np.empty((self.points_per_day,))
            lam_vec[:] = np.NAN
            mu_vec = np.empty((self.points_per_day,))
            mu_vec[:] = np.NAN
            jmptimes_mc = [None]*iter_num # create an empty list of size iter_num
            syssize_mc = np.empty((self.points_per_day,iter_num))
            syssize_mc[:] = np.NAN
            time_int = np.arange(self.points_per_day)
            nstart = 0
            for i in range(len(seg_point_added)-1):
                lam = Model.parameters_data['lam'][day]['Value'].get_base_data()[i];
                mu = Model.parameters_data['mu'][day]['Value'].get_base_data()[i];
                lam_vec[seg_point_added[i]:seg_point_added[i+1]] = lam;
                mu_vec[seg_point_added[i]:seg_point_added[i+1]] = mu;
            for iter_idx in range(iter_num):
                jmptimes, syssize = simulate_queue(self.points_per_day, lam_vec, mu_vec, nstart, self.empty_time[day])
                if syssize is None:
                    jmptimes_mc[iter_idx] = None
                    syssize_mc[:, iter_idx] = np.zeros((self.points_per_day,))
                    continue
                if np.any(syssize <0):
                    pdb.set_trace()
                    raise ValueError('negative syssize')
                if jmptimes is None:
                    jmptimes_mc[iter_idx] = 0
                    syssize_mc[:, iter_idx] = 0
                else:
                    # round jmptimes to the nearest integer
                    jmptimes_d, ia = unique_last(np.round(jmptimes))
                    syssize_d = syssize[ia]
                    if jmptimes_d[0] != 0:
                        jmptimes_int = np.insert(jmptimes_d, 0, 0)
                        syssize_int = np.insert(syssize_d, 0, 0)
                    else:
                        jmptimes_int = jmptimes_d
                        syssize_int = syssize_d
                    vq = interp1(jmptimes_int, syssize_int, time_int)
                    jmptimes_mc[iter_idx] = jmptimes_d
                    syssize_mc[:, iter_idx] = vq
            prediction = np.mean(syssize_mc, axis=1);
            std = np.std(syssize_mc, axis=1);
            # Convert current prediction to pandas timeseries
            start_time = pd.datetime(Model.start_time.year,Model.start_time.month, Model.start_time.day)+timedelta(days=d);
            final_time = start_time+timedelta(days=1)-timedelta(seconds = Model.measurements[self.occ_key]['Sample'].get_base_data());
            freq = str(int(Model.measurements[self.occ_key]['Sample'].get_base_data()))+'s';
            index = pd.date_range(start_time, final_time, freq = freq);
            ts_pred_new = pd.Series(data = prediction, index = index);
            ts_std_new = pd.Series(data = std, index = index);
            # Join current day's prediction to past predictions
            ts_pred = pd.concat((ts_pred, ts_pred_new), axis = 0);
            ts_std = pd.concat((ts_std, ts_std_new), axis = 0);
            # Increment the day counter
            d = d + 1;
        # Store simulation results in Model measurement dictionary
        unit = Model.measurements[self.occ_key]['Measured'].get_base_unit();
        Model.measurements[self.occ_key]['Simulated'] = variables.Timeseries('prediction', ts_pred, unit);
        Model.measurements[self.occ_key]['SimulatedError'] = variables.Timeseries('prediction', ts_std, unit);
        
    def _format_training_data(self, Model, day):
        '''Format the training data for use in parameter estimation.

        '''

        # Set the occupancy measurement key
        self.occ_key = Model.measurements.keys()[0];
        # Get the training data from measurements
        self.df_data_train = Model.measurements[self.occ_key]['Measured'].get_base_data()[Model.start_time:Model.final_time].to_frame(name='occ');        
        # Specify the weekday number of each measurement point
        self.df_data_train['day'] = pd.Series(self.df_data_train.index.weekday, index=self.df_data_train.index);
        # Calculate the number of measurement points in a full day
        self.points_per_day = 3600*24.0/Model.measurements[self.occ_key]['Sample'].get_base_data();
        # Check that points_per_day is whole number and convert to integer
        if self.points_per_day.is_integer():
            self.points_per_day = int(self.points_per_day);
        else:
            raise ValueError('Points per day of {} is not a whole number. Check occupancy measurement sampling rate.'.format(self.points_per_day));      
        # Isolate the measurement data for the day of interest
        df_interest = self.df_data_train[self.df_data_train['day'] == day];
        # Format isolated data for use in parameter estimation procedure
        self.data_train = df_interest['occ'].as_matrix();
        self.data_train = self.data_train.reshape((self.data_train.size/self.points_per_day, self.points_per_day));
    
#%% Model Implementations
class Modelica(_Model, utility._FMU, utility._Building):
    '''Class for models of physical systems represented by Modelica or an FMU.

    Parameters
    ----------
    parameter_estimate_method : parameter estimation method class from mpcpy.models
        Method for performing the parameter estimation.
    validate_method : validation method class from mpcpy.models
        Method for performing the parameter validation.
    measurements : dictionary
        Measurement variables for the model.  Same as the measurements 
        attribute from a ``systems`` class.  See documentation for ``systems`` 
        for more information.
    state_estimate_method : state estimation method class from mpcpy.models, optional
        Method for performing the state estimation.
        Default is models.UKFState
    moinfo : tuple or list
        Modelica information for the model.  See documentation for 
        ``systems.EmulationFromFMU`` for more information.
    zone_names : list, optional
        List of zone name strings.
    weather_data : dictionary, optional
        ``exodata`` weather object data attribute.
    internal_data : dictionary, optional
        ``exodata`` internal object data attribute.
    control_data : dictionary, optional
        ``exodata`` control object data attribute.    
    other_inputs : dictionary, optional
        ``exodata`` other inputs object data attribute.    
    parameter_data : dictionary, optional
        ``exodata`` parameter object data attribute.
    estimated_state_data : dictionary, optional
        ``exodata`` estimated state object data attribute.
    tz_name : string, optional
        Name of timezone according to the package ``tzwhere``.  If 
        ``'from_geography'``, then geography kwarg is required.
    geography : list or tuple, optional
        List or tuple with (latitude, longitude) in degrees.   
    save_parameter_input_data: boolean
        True to output the parameter and input data set for simulations and optimizations
        Saved files are:
        "mpcpy_simulation_parameters_model.csv"
        "mpcpy_simulation_inputs_model.csv"
        "mpcpy_simulation_parameters_optimization_initial.csv"
        "mpcpy_simulation_inputs_optimization_initial.csv"
        "mpcpy_optimization_parameters.csv"
        "mpcpy_optimization_inputs.csv"
        Times will be in UTC.
        Default is False.

    Attributes
    ----------
    measurements : dictionary
        ``systems`` measurement object attribute.
    fmu : pyfmi fmu object
        FMU respresenting the emulated system.
    fmupath : string
        Path to the FMU file.
    lat : numeric
        Latitude in degrees.  For timezone.
    lon : numeric
        Longitude in degrees.  For timezone.
    tz_name : string
        Timezone name.

    '''
    
    def __init__(self, parameter_estimate_method, validate_method, measurements, state_estimate_method=None, save_parameter_input_data=False, **kwargs):
        '''Constructor of a modelica or FMU model object.
        
        '''
        
        self.name = 'modelica';    
        self.measurements = measurements;
        self._kwargs = kwargs
        self._create_fmu(kwargs);
        self.input_names = self._get_input_names();                                       
        self._parse_building_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        self._save_parameter_input_data = save_parameter_input_data
        self._save_parameter_input_filename = 'model'
        if 'estimated_state_data' in kwargs:
            self.estimated_state_data = kwargs['estimated_state_data'];
        else:
            self.estimated_state_data = {};
        # Check parameter estimation method compatible with model
        if parameter_estimate_method is JModelica:
            if self.mopath is None:
                raise ValueError('Must supply modelica file to use JModelica estimation method.  Cannot only use FMU.  If only looking to simulate the fmu, use systems.EmulationFromFMU object.')
        # Check state estimation method compatible with model
        if state_estimate_method is UKFState:
            if self.fmu_target is not 'me':
                raise ValueError('Must supply model-exchange FMU to use UKFState estimation method.')
        self.set_parameter_estimate_method(parameter_estimate_method);
        self.set_state_estimate_method(state_estimate_method);
        self.set_validate_method(validate_method);
        
    def parameter_estimate(self, start_time, final_time, measurement_variable_list, global_start=0, seed=None, use_initial_values=True):
        '''Estimate the parameters of the model.
        
        The estimation of the parameters is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute, 
        the parameter_data dictionary attribute, and any exodata inputs.
        
        An optional global start algorithm where multiple estimations are 
        preformed with different initial guesses within the ranges of each 
        free parameter provided.  It is implemented as tested in 
        Blum et al. (2019).  The algorithm uses latin hypercube sampling 
        to choose the initial parameter guess values for each iteration and 
        the iteration with the lowest estimation problem objective value is 
        chosen.  A user-provided guess is included by default using initial
        values given to parameter data of the model, though this option can be 
        turned off to use only sampled initial guesses.
        
        Blum, D.H., Arendt, K., Rivalin, L., Piette, M.A., Wetter, M., and 
        Veje, C.T. (2019). "Practical factors of envelope model setup and 
        their effects on the performance of model predictive control for 
        building heating, ventilating, and air conditioning systems." 
        Applied Energy 236, 410-425. 
        https://doi.org/10.1016/j.apenergy.2018.11.093
        
        Parameters
        ----------
        start_time : string
            Start time of estimation period.
            Setting to 'continue' will result in error.
        final_time : string
            Final time of estimation period.
        measurement_variable_list : list
            List of strings defining for which variables defined in the 
            measurements dictionary attirubute the estimation will 
            try to minimize the error.
        global_start : int, optional
            Number of iterations of a global start algorithm.
            If 0, the global start algorithm is disabled and the values in
            the parameter_data dictionary are used as initial guesses.
            Default is 0.
        seed : numeric or None, optional
            Specific seed of the global start algorithm for the random selection
            of initial value guesses.
            Default is None.
        use_initial_values : boolean, optional
            True to include initial parameter values in the estimation iterations.
            Default is True.

        Yields
        ------
        Updates the ``'Value'`` key for each estimated parameter in the 
        parameter_data attribute.

        '''
        
        # Check for free parameters
        free = False;
        for key in self.parameter_data.keys():
            if self.parameter_data[key]['Free'].get_base_data():
                free = True;
                break
            else:
                free = False;
        if not free:
            # If none free raise error
            raise ValueError('No parameters set as "Free" in parameter_data dictionary. Cannot run parameter estimation.');
        # Check for measurements
        for meas in measurement_variable_list:
            if meas not in self.measurements.keys():
                raise ValueError('Measurement {0} defined in measurement_variable_list not defined in measurements dictionary.'.format(meas))
        # Check for continue
        if start_time == 'continue':
            raise ValueError('"continue" is not a valid entry for start_time for parameter estimation problems.')
        # Perform parameter estimation
        self._set_time_interval(start_time, final_time);
        self.measurement_variable_list = measurement_variable_list;
        # Without global start
        if not global_start:
            self._parameter_estimate_method._estimate(self);
        # With global start
        else:
            # Detect free parameters
            free_pars = [];
            for par in self.parameter_data.keys():
                if self.parameter_data[par]['Free'].display_data():
                    free_pars.append(par)
            # Create lhs sample for all parameters
            np.random.seed(seed)  # Random seed for LHS initialization
            n_free_pars = len(free_pars);
            lhs = doe.lhs(n_free_pars, samples=global_start, criterion='c');
            # Scale and store lhs samples for parameters between min and max bounds
            par_vals = dict();
            for par, i in zip(free_pars, range(n_free_pars)):
                par_min = self.parameter_data[par]['Minimum'].display_data();
                par_max = self.parameter_data[par]['Maximum'].display_data();                                
                par_vals[par] = (lhs[:,i]*(par_max-par_min)+par_min).tolist();
                # Add initial value guesses if wanted
                if use_initial_values:
                    par_vals[par].append(self.parameter_data[par]['Value'].display_data())
            # Estimate for each sample
            J = float('inf');
            par_best = dict();
            glo_est_data = dict()
            if use_initial_values:
                iterations = range(global_start+1)
            else:
                iterations = range(global_start)
            for i in iterations:
                # Create dictionary to save all estimation iteration data
                glo_est_data[i] = dict()
                # Set lhs sample values for each parameter
                for par in par_vals.keys():
                    # Use latin hypercube selections
                    self.parameter_data[par]['Value'].set_data(par_vals[par][i]);
                    glo_est_data[i][par] = par_vals[par][i]
                # Make estimate for iteration
                self._parameter_estimate_method._estimate(self);
                # Validate estimate for iteration
                self.validate(start_time, final_time, 'validate', plot = 0);
                # Save RMSE for initial_guess
                for key in self.RMSE:
                    glo_est_data[i]['RMSE_{0}'.format(key)] = self.RMSE[key].display_data();
                # If solve succeeded, compare objective and if less, save best par values
                solver_message = self._parameter_estimate_method.opt_problem.get_optimization_statistics()[0]
                J_curr = self._parameter_estimate_method.opt_problem.get_optimization_statistics()[2]
                glo_est_data[i]['Message'] = solver_message
                glo_est_data[i]['J'] = J_curr
                if ((J_curr < J) and (J_curr > 0.0)) or ((J_curr < J) and (solver_message == 'Solve_Succeeded')):
                    J = J_curr;
                    for par in free_pars:
                        par_best[par] = self.parameter_data[par]['Value'].display_data();
            # Save all estimates
            glo_est_data['J_Best'] = J
            self.glo_est_data = glo_est_data
            # Set best parameters in model if found
            if par_best:
                for par in par_vals.keys():
                    self.parameter_data[par]['Value'].set_data(par_best[par]);
        
    def state_estimate(self, start_time, final_time, measurement_variable_list):
        '''Estimate the states of the model.
        
        The estimation of the states is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute, 
        the estimated_state_data dictionary attribute, and any exodata inputs.
        
        Parameters
        ----------
        start_time : string
            Start time of estimation period.
            Setting to 'continue' will result in error.
        final_time : string
            Final time of estimation period.
        measurement_variable_list : list
            List of strings defining for which variables defined in the 
            measurements dictionary attribute the estimation will use.

        Yields
        ------
        Updates the ``'Value'`` key for each estimated state in the 
        estimated_state_data attribute.
        
        In the case of using the JModelicaState state estimation method, which
        implements a moving horizon state estimator, the ``'Value'`` key for 
        each parameter corresponding to an estimated state in the 
        parameter_data attribute is also updated with the optimal result.

        '''
        
        # Check for state estimate data
        if not self.estimated_state_data:
            raise ValueError('No state estimate data set with estimated_state_data dictionary. Cannot run state estimation.');
        # Check for measurements
        for meas in measurement_variable_list:
            if meas not in self.measurements.keys():
                raise ValueError('Measurement {0} defined in measurement_variable_list not defined in measurements dictionary.'.format(meas))
        # Check for continue
        if start_time == 'continue':
            raise ValueError('"continue" is not a valid entry for start_time for state estimation problems.')
        # Perform state estimation
        self._set_time_interval(start_time, final_time);
        self.measurement_variable_list = measurement_variable_list;
        self._state_estimate_method._estimate(self);        
        
    def validate(self, start_time, final_time, validate_filename, plot = 1):
        '''Validate the estimated parameters of the model.

        The validation of the parameters is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute, 
        the parameter_data dictionary attribute, and any exodata inputs.

        Parameters
        ----------
        start_time : string
            Start time of validation period.
            Set to 'continue' in order to continue the model simulation
            from the final time of the previous simulation, estimation, or 
            validation.  Continuous states from simulation and validation are 
            saved.  Exodata input objects must contain values for the 
            continuation timestamp.  The measurements in a continued 
            simulation replace previous values.  They do not append to a 
            previous simulation's measurements.
        final_time : string
            Final time of validation period.
        validate_filepath : string
            File path without an extension for which to save validation 
            results.  Extensions will be added depending on the file type 
            (e.g. .png for figures, .txt for data).
        plot : [0,1], optional
            Plot flag for some validation or estimation methods.
            Default = 1.

        Yields
        ------
        Various results depending on the validation method.  Please check the
        documentation for the validation method chosen.

        '''

        # Simulate model
        self.simulate(start_time, final_time);
        # Perform validation        
        self._validate_method._validate(self, validate_filename, plot = plot);
            
    def simulate(self, start_time, final_time, ):
        '''Simulate the model with current parameter estimates and any exodata 
        inputs.

        Parameters
        ----------
        start_time : string
            Start time of validation period.
            Set to 'continue' in order to continue the model simulation
            from the final time of the previous simulation, estimation, or 
            validation.  Continuous states from simulation and validation are 
            saved.  Exodata input objects must contain values for the 
            continuation timestamp.  The measurements in a continued 
            simulation replace previous values.  They do not append to a 
            previous simulation's measurements.
        final_time : string
            Final time of simulation period.  Must be greater than the
            start time.

        Yields
        ------
        Updates the ``'Simulated'`` key for each measurement in the 
        measurements attribute.

        '''
        
        self._set_time_interval(start_time, final_time);
        self._simulate_fmu();
        
    def set_parameter_estimate_method(self, parameter_estimate_method):
        '''Set the parameter estimation method for the model.

        Parameters
        ----------
        estimate_method : estimation method class from mpcpy.models
            Method for performing the parameter estimation.

        '''

        self._parameter_estimate_method = parameter_estimate_method(self);
        
    def set_validate_method(self, validate_method):
        '''Set the validation method for the model.

        Parameters
        ----------
        validate_method : validation method class from mpcpy.models
            Method for performing the parameter validation.

        '''

        self._validate_method = validate_method(self);
        
    def set_state_estimate_method(self, state_estimate_method):
        '''Set the state estimation method for the model.

        Parameters
        ----------
        state_estimate_method : estimation method class from mpcpy.models
            Method for performing the state estimation.

        '''

        if state_estimate_method:
            self._state_estimate_method = state_estimate_method(self);
        else:
            self._state_estimate_method = None
        
    def get_global_estimate_data(self):
        '''Get the estimation data if using the global estimation algorithm.
        
        Must have completed the estimation using the global algorithm.
        
        Returns
        -------
        glo_est_data : dictionary
            Estimation data from each iteration of the global estimation
            algorithm, including the training RMSE for each measurement
            variable, initial guess for each parameter, returned objective 
            value, returned solver status, and best objective value.
        
        '''
        
        glo_est_data = self.glo_est_data
        
        return glo_est_data
        
class Occupancy(utility._mpcpyPandas, utility._Measurements):
    '''Class for models of occupancy.

    Parameters
    ----------
    occupancy_method : occupancy method class from mpcpy.models
    measurements : dictionary
        Measurement variables for the model.  Same as the measurements 
        attribute from a ``systems`` class.  See documentation for ``systems`` 
        for more information.  This measurement dictionary should only have
        one variable key, which represents occupancy count.
    tz_name : string, optional
        Name of timezone according to the package ``tzwhere``.  If 
        ``'from_geography'``, then geography kwarg is required.
    geography : list or tuple, optional
        List or tuple with (latitude, longitude) in degrees.   

    Attributes
    ----------
    measurements : dictionary
        ``systems`` measurement object attribute.
    parameter_data : dictionary
        ``exodata`` parameter object data attribute.
    lat : numeric
        Latitude in degrees.  For timezone.
    lon : numeric
        Longitude in degrees.  For timezone.
    tz_name : string
        Timezone name.

    '''

    def __init__(self, occupancy_method, measurements, **kwargs):
        '''Constructor of an occupancy model object.

        '''

        # Initialize variables and model method
        self.name = 'occupancy';
        self.measurements = measurements;
        self.set_occupancy_method(occupancy_method);
        self.parameters_data = {};
        self._parse_time_zone_kwargs(kwargs);
        
    def estimate(self, start_time, final_time, **kwargs):
        '''Estimate the parameters of the model using measurement data.
        
        The estimation of the parameters is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute of the 
        model object.

        Parameters
        ----------
        start_time : string
            Start time of estimation period.
        final_time : string
            Final time of estimation period.
        estimate_options : dictionary, optional
            Use the ``get_estimate_options`` method to obtain and edit.

        Yields
        ------
        parameter_data : dictionary
            Updates the ``'Value'`` key for each estimated parameter in the 
            parameter_data attribute.

        '''

        # Set the training time interval
        self._set_time_interval(start_time, final_time);
        # Set the estimation options
        if 'estimate_options' in kwargs:
            self.set_estimate_options(kwargs['estimate_options']);
        # Perform estimation
        self._occupancy_method._estimate(self);
        
    def validate(self, start_time, final_time, validate_filename, plot = 1):
        '''Validate the estimated parameters of the model with measurement data.

        The validation of the parameters is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute of the 
        model object.
        
        Parameters
        ----------
        start_time : string
            Start time of validation period.
        final_time : string
            Final time of validation period.
        validate_filepath : string
            File path without an extension for which to save validation 
            results.  Extensions will be added depending on the file type 
            (e.g. .png for figures, .txt for data).
        plot : [0,1], optional
            Plot flag for some validation or estimation methods.

        Yields
        ------
        Various results depending on the validation method.  Please check the
        documentation for the occupancy model chosen.

        '''

        # Set the name of all validation output files
        self.validate_filename = validate_filename;
        # Set the validation time interval
        self._set_time_interval(start_time, final_time);
        # Simulate the model using currently estimated parameters
        self.simulate(start_time, final_time);
        # Perform the validation against measured data
        self._occupancy_method._validate(self, plot);
        
    def simulate(self, start_time, final_time, **kwargs):
        '''Simulate the model with current parameter estimates.

        Parameters
        ----------
        start_time : string
            Start time of simulation period.
        final_time : string
            Final time of simulation period.
        simulate_options : dictionary, optional
            Use the ``get_simulate_options`` method to obtain and edit.

        Yields
        ------
        measurements : dictionary
            Updates the ``'Simulated'`` key for each measurement in the 
            measurements attribute.  If available by the occupancy method, 
            also updates the ``'SimulatedError'`` key for each measurement in
            the measurements attribute.

        '''
        
        # Set the simulation time interval
        self._set_time_interval(start_time, final_time);
        # Set the simulation options
        if 'simulate_options' in kwargs:
            self.set_simulate_options(kwargs['simulate_options']);
        # Perform the simulation
        self._occupancy_method._simulate(self);
        
    def get_load(self, load_per_person):
        '''Get a load timeseries based on the predicted occupancy.

        Parameters
        ----------
        load_per_person : mpcpy.variables.Static
            Scaling factor of occupancy prediction to produce load timeseries.
        
        Returns
        -------
        load : mpcpy.variables.Timeseries
            Load timeseries.

        '''

        # Get occupancy prediction
        ts = self.measurements[self._occupancy_method.occ_key]['Simulated'].get_base_data();
        # Multiply by load factor
        ts_load = load_per_person*ts;
        # Return timeseries
        return ts_load;
        
    def get_constraint(self, occupied_value, unoccupied_value):
        '''Get a constraint timeseries based on the predicted occupancy.

        Parameters
        ----------
        occupied_value : mpcpy.variables.Static
            Value of constraint during occupied times.
        unoccupied_value : mpcpy.variables.Static
            Value of constraint during unoccupied times.
        
        Returns
        -------
        constraint : mpcpy.variables.Timeseries
            Constraint timeseries.

        '''

        # Get occupancy prediction
        ts = self.measurements[self._occupancy_method.occ_key]['Simulated'].get_base_data();
        # Determine when occupied
        ts_occ = ts>=0.5;
        # Apply occupied and unoccupied values
        ts_occ_value = ts_occ.apply(lambda x: occupied_value if x == 1 else unoccupied_value);
        # Return timeseries
        return ts_occ_value;

    def set_occupancy_method(self, occupancy_method):
        '''Set the occupancy method for the model.

        Parameters
        ----------
        occupancy_method : occupancy method class from mpcpy.models

        '''

        self._occupancy_method = occupancy_method();
        
    def set_simulate_options(self, simulate_options):
        '''Set the simulation options for the model.

        Parameters
        ----------
        simulate_options : dictionary
            Options for simulation of occupancy model.  Please see
            documentation for specific occupancy model for more information.

        '''

        for key in self._occupancy_method.simulate_options.keys():
            self._occupancy_method.simulate_options[key] = simulate_options[key];

    def set_estimate_options(self, estimate_options):
        '''Set the estimation options for the model.

        Parameters
        ----------
        estimate_options : dictionary
            Options for estimation of occupancy model parameters.  Please see
            documentation for specific occupancy model for more information.

        '''

        for key in self._occupancy_method.estimate_options.keys():
            self._occupancy_method.estimate_options[key] = estimate_options[key];

    def get_simulate_options(self):
        '''Get the simulation options for the model.

        Returns
        -------
        simulate_options : dictionary
            Options for simulation of occupancy model.  Please see
            documentation for specific occupancy model for more information.

        '''

        return self._occupancy_method.simulate_options;
            
    def get_estimate_options(self):
        '''Set the estimation options for the model.

        Returns
        -------
        estimate_options : dictionary
            Options for estimation of occupancy model parameters.  Please see
            documentation for specific occupancy model for more information.

        '''

        return self._occupancy_method.estimate_options;
        
        