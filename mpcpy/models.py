# -*- coding: utf-8 -*-
"""
Model.py
by David Blum

This module contains the classes and interfaces for reduced order models (Model).
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
from occupant.presence.queueing.adaptive_breakpoint_placement import adaptive_breakpoint_placement
from occupant.presence.queueing.simulate_queue import simulate_queue
from occupant.presence.queueing.unique_last import unique_last
from occupant.presence.queueing.interp1 import interp1
from occupant.presence.queueing.parameter_inference_given_segments import parameter_inference_given_segment
from estimationpy.fmu_utils import model as ukf_model
from estimationpy.ukf.ukf_fmu import UkfFmu
from estimationpy.fmu_utils import estimationpy_logging
from pymodelica import compile_fmu

#%% Model Class
class Model(utility.mpcpyPandas):
    '''Abstract class for representing a model for MPC.'''
    __metaclass__ = ABCMeta;
    @abstractmethod
    def estimate(self):
        pass;
    @abstractmethod        
    def validate(self):
        pass;
    @abstractmethod        
    def simulate(self):
        pass;
        
#%% Model Implementations
class Modelica(Model, utility.FMU, utility.Building):
    '''An fmu implementation of an mpcpy Model.'''
    def __init__(self, estimate_method, validate_method, measurements, **kwargs):
        self.name = 'modelica';    
        self.measurements = measurements;
        if 'fmupath' in kwargs:
            self.fmupath = kwargs['fmupath'];
            self.mopath = None;
            self.modelpath = None
            self.libraries = None;
        if 'moinfo' in kwargs:
            self.mopath = kwargs['moinfo'][0];
            self.modelpath = kwargs['moinfo'][1];
            self.libraries = kwargs['moinfo'][2];
            self.fmupath = compile_fmu(self.modelpath, \
                                       self.mopath, \
                                       compiler_options = {'extra_lib_dirs':self.libraries});
        self.input_names = self.get_input_names();                                       
        self._estimate_method = estimate_method(self);
        self._validate_method = validate_method(self);
        self._parse_building_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        
    def estimate(self, start_time, final_time, measurement_variable_list):
        self._set_time_interval(start_time, final_time);        
        self.measurement_variable_list = measurement_variable_list;
        self._estimate_method._estimate(self);
        
    def validate(self, start_time, final_time, validate_filename, plot = 1):
        # Change free parameters to fixed so they get simulated
        free_parameters = [];
        for key in self.parameter_data.keys():
            if self.parameter_data[key]['Free'].get_base_data():
                free_parameters.append(key);
                self.parameter_data[key]['Free'] = variables.Static(key+'_free', False, units.boolean);
        # Simulate model
        self.simulate(start_time, final_time);
        # Perform validation        
        self._validate_method._validate(self, validate_filename, plot = plot);
        # Change free parameters back to free
        for key in free_parameters:
            self.parameter_data[key]['Free'] = variables.Static(key+'_free', True, units.boolean);
            
    def simulate(self, start_time, final_time):
        '''Simulate the model with current parameter estimates.'''
        self._set_time_interval(start_time, final_time);
        self._simulate_fmu();
        
    def set_estimate_method(self, estimate_method):
        self._estimate_method = estimate_method(self);  
        
    def set_validate_method(self, validate_method):
        self._validate_method = validate_method(self);
        
class Occupancy(Model):
    '''An occupant presence implementation of an mpcpy Model.'''
    def __init__(self, occupant_presence_method, measurements, **kwargs):
        '''Constructor of an occupant presence model.'''
        # Initialize variables and model method
        self.name = 'occupancy';
        self.measurements = measurements;
        self._occupant_presence_method = occupant_presence_method();
        self.parameters_data = {};
        self._parse_time_zone_kwargs(kwargs);
        
    def estimate(self, start_time, final_time, **kwargs):
        '''Estimate the parameters of the model using training data.'''
        # Set the training time interval
        self._set_time_interval(start_time, final_time);
        # Set the estimation options
        if 'estimate_options' in kwargs:
            self.set_estimate_options(kwargs['estimate_options']);
        # Perform estimation
        self._occupant_presence_method._estimate(self);
        
    def validate(self, start_time, final_time, validate_filename, plot = 1):
        '''Compare the model predictions with measured data.'''
        # Set the name of all validation output files
        self.validate_filename = validate_filename;
        # Set the validation time interval
        self._set_time_interval(start_time, final_time);
        # Simulate the model using currently estimated parameters
        self.simulate(start_time, final_time);
        # Perform the validation against measured data
        self._occupant_presence_method._validate(self);
        
    def simulate(self, start_time, final_time, **kwargs):
        '''Simulate the model using currently estimated parameters.'''
        # Set the simulation time interval
        self._set_time_interval(start_time, final_time);
        # Set the simulation options
        if 'simulate_options' in kwargs:
            self.set_simulate_options(kwargs['simulate_options']);
        # Perform the simulation
        self._occupant_presence_method._simulate(self);
        
    def generate_load(self, load_per_person):
        '''Use predicted occupancy to generate load timeseries.'''
        # Get occupancy prediction
        ts = self.measurements[self._occupant_presence_method.occ_key]['Simulated'].get_base_data();
        # Multiply by load factor
        ts_load = load_per_person*ts;
        # Return timeseries
        return ts_load;
        
    def generate_constraint(self, occupied_value, unoccupied_value):
        '''Use predicted occupancy to generate constraint timeseries.'''
        # Get occupancy prediction
        ts = self.measurements[self._occupant_presence_method.occ_key]['Simulated'].get_base_data();
        # Determine when occupied
        ts_occ = ts>=0.5;
        # Apply occupied and unoccupied values
        ts_occ_value = ts_occ.apply(lambda x: occupied_value if x == 1 else unoccupied_value); 
        # Return timeseries
        return ts_occ_value;
        
    def set_simulate_options(self, simulate_options):
        '''Set the simulation options for the model.'''
        for key in self._occupant_presence_method.simulate_options.keys():
            self._occupant_presence_method.simulate_options[key] = simulate_options[key];

    def set_estimate_options(self, estimate_options):
        '''Set the estimation options for the model.'''
        for key in self._occupant_presence_method.estimate_options.keys():
            self._occupant_presence_method.estimate_options[key] = estimate_options[key];

    def get_simulate_options(self):
        '''Get the simulation options for the model.'''
        return self._occupant_presence_method.simulate_options;
            
    def get_estimate_options(self):
        '''Get the estimation options for the model.'''
        return self._occupant_presence_method.estimate_options;
        
        
#%% IdentifyMethod Interface
class Estimate(utility.mpcpyPandas):
    ''' Interface for a model identifcation method.'''
    __metaclass__ = ABCMeta;   
    @abstractmethod
    def _estimate():
        pass;
        
#%% ValidateMethod Interface
class Validate(utility.mpcpyPandas):
    ''' Interface for a model validation method.'''
    __metaclass__ = ABCMeta;
    @abstractmethod
    def _validate():
        pass;
    def plot_simple(self,Model,validate_filename):
        self.plot = {};
        i = 0;
        for key in Model.measurements.keys():
            self.plot[key] = plt.figure(i);
            measurement = Model.measurements[key]['Measured'];
            estimated_measurement = Model.measurements[key]['Simulated'];
            measurement.display_data(tz_name = Model.tz_name)[Model.start_time:Model.final_time].plot( \
                   label = key+'_measured', linewidth = 2.0, linestyle = '-', rot = 90);
            estimated_measurement.display_data()[Model.start_time:Model.final_time].plot( \
                   label = key+'_estimated', linewidth = 2.0, linestyle = '--', rot = 90);
            plt.legend();
            plt.xlabel('Time (hr)');
            yname = measurement.quantity_name;
            yunit = measurement.get_display_unit_name();
            plt.ylabel(yname + ' [' + yunit + ']');
            plt.rcParams.update({'font.size': 16});
            i = i + 1; 
        plt.savefig(validate_filename + '_.png');

#%% OccupancyModelMethod Interface
class OccupancyMethod(utility.mpcpyPandas):
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
             
#%% IdentifyMethod Interface Implementations
class UKF(Estimate):
    '''A Model interface for the UKF identification method.'''
    def __init__(self, Model):
        self.name = 'UKF';
        # Instantiate UKF model
        self.model = ukf_model.Model(Model.fmupath);          
    def _estimate(self, Model):
        estimationpy_logging.configure_logger(log_level = logging.DEBUG, log_level_console = logging.INFO, log_level_file = logging.DEBUG)
        # Write the inputs, measurements, and parameters to csv
        self.writeukfcsv(Model);
        # Select inputs
        for name in Model.input_names:
            inputvar = self.model.get_input_by_name(name);
            inputvar.get_csv_reader().open_csv(Model.csv_path);
            inputvar.get_csv_reader().set_selected_column(name);    
        # Select outputs
        for name in Model.measured_data.keys():
            outputvar = self.model.get_output_by_name(name);
            outputvar.get_csv_reader().open_csv(Model.csv_path);
            outputvar.get_csv_reader().set_selected_column(name);        
            outputvar.set_measured_output()
            outputvar.set_covariance(0.5)        
        # Select the parameters to be identified
        i = 0;
        for name in Model.parameter_data.keys():
            if Model.parameter_data[name]['Free'].get_base_data():
                self.model.add_parameter(self.model.get_variable_object(name));
                par = self.model.get_parameters()[i];
                par.set_initial_value(Model.parameter_data[name]['Value']);
                par.set_covariance(Model.parameter_data[name]['Covariance']);
                par.set_min_value(Model.parameter_data[name]['Minimum']);
                par.set_max_value(Model.parameter_data[name]['Maximum']);
                par.set_constraint_low(True);
                par.set_constraint_high(True);
                i = i + 1;
        # Initialize the model for the simulation
        self.model.initialize_simulator();
        # Set model parameters
        for name in Model.parameter_data.keys():
            self.model.set_real(self.model.get_variable_object(name),Model.parameter_data[name]['Data']); 
        for name in Model.coefficients.keys():
            self.model.set_real(self.model.get_variable_object(name),Model.coefficients[name]['InitialGuess']);
            print(self.model.get_real(self.model.get_variable_object(name)));
        # Instantiate the UKF for the FMU
        ukf_FMU = UkfFmu(self.model);
        # Start filter
        t0 = pd.to_datetime(0, unit = "s", utc = True);
        t1 = pd.to_datetime(Model.final_time, unit = "s", utc = True);
        time, x, sqrtP, y, Sy, y_full = ukf_FMU.filter(start = t0, stop = t1);
        
    def writeukfcsv(self, Model):
        ## Write the inputs, measurements, and coefficients to csv
        Model.csv_path = 'ukf.csv';        
        self.other_inputs = {};
        for key_meas in Model.measured_data.keys():
            self.other_inputs[key_meas] = {};
            self.other_inputs[key_meas]['Data'] = Model.measured_data[key_meas]['Data'];
            self.other_inputs[key_meas]['Time'] = Model.measured_data[key_meas]['Time'];
        for key_coeff in Model.coefficients.keys():
            if Model.parameter_data[key_coeff]['Free'].get_base_data():
                self.other_inputs[key_coeff] = {};
                self.other_inputs[key_coeff]['Data'] = Model.parameter_data[key_coeff]['Value']*np.ones(len(Model.measured_data[key_meas]['Time']));
                self.other_inputs[key_coeff]['Time'] = Model.measured_data[key_meas]['Time'];
        # Add measurements and coefficients to "input_names" for input object
        input_names = Model.input_names + Model.measured_data.keys() + Model.coefficients.keys();
        # Create input object to write to csv
        input_object = utility.createInputObject(Model.final_time, \
                                                 input_names, \
                                                 Model.weather_data, \
                                                 Model.internal_data, \
                                                 self.other_inputs);
        # Write to csv                                                 
        with open(Model.csv_path, 'wb') as f:
            ukfwriter = csv.writer(f);
            ukfwriter.writerow(['time'] + list(input_object[0]));
            for i in range(len(input_object[1][:,0])):
                ukfwriter.writerow(input_object[1][i]);        

class JModelica(Estimate):
    def __init__(self, Model):
        self.name = 'Jmo';        
        
    def _estimate(self, Model):
        self.opt_problem = optimization.Optimization(Model, optimization.ParameterEstimate, optimization.JModelica, {});
        self.opt_problem.optimize(Model.start_time, Model.final_time, measurement_variable_list = Model.measurement_variable_list);
        
#%% Validate Method Interfaces
class RMSE(Validate):
    def __init__(self, Model):
        pass;

    def _validate(self, Model, validate_filename, plot = 1):
        Model.RMSE = {};
        for key in Model.measurements.keys():
            data = Model.measurements[key]['Measured'].get_base_data()[Model.start_time:Model.final_time];
            data_est = Model.measurements[key]['Simulated'].get_base_data()[Model.start_time:Model.final_time];
            RMSE = np.sqrt(sum((data_est-data)**2)/len(data));
            unit_class = Model.measurements[key]['Measured'].get_base_unit();
            Model.RMSE[key] = variables.Static('RMSE_'+key, RMSE, unit_class);
        if plot == 1:
            self.plot_simple(Model, validate_filename);
            
#%% OccupanctPresence Model Types
class QueueModel(OccupancyMethod):
    '''Occupant presence prediction based on a queueing approach.
    
    Based on Jia, R. and C. Spanos (2016). "Occupancy modelling in shared 
    spaces of buildings: a queueing approach." Journal of Building Performance 
    Simulation. DOI: 10.1080/19401493.2016.1267802.
    
    '''

    def __init__(self):
        '''Constructor of an occupancy prediction object using a queueing approach.'''
        # Initialize options
        self.estimate_options = {};
        self.estimate_options['res'] = 3;
        self.estimate_options['margin'] = 3;
        self.estimate_options['n_max'] = 24;
        self.simulate_options = {};
        self.simulate_options['iter_num'] = 100;
        
    def _estimate(self, Model):
        '''Use measured occupancy data to estimate the queue model parameters.'''
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
        
    def _validate(self, Model):
        '''Compare occupancy predictions to measurements.'''
        # Load prediction and measurement data
        prediction = Model.measurements[self.occ_key]['Simulated'].display_data();
        std = Model.measurements[self.occ_key]['SimulatedError'].display_data();
        measurements = Model.measurements[self.occ_key]['Measured'].display_data()[Model.start_time:Model.final_time];
        prediction_pstd = prediction+std;
        prediction_mstd = prediction-std;
        prediction_mstd = (prediction_mstd>=0)*prediction_mstd;
        # Plot data to compare
        measurements.plot(label = 'measured', color = 'k', alpha = 0.5);
        prediction.plot(label='prediction', color = 'r', alpha = 0.5);
        plt.fill_between(prediction.index, prediction_pstd, prediction_mstd, color = 'r', alpha = 0.5);     
        plt.legend();
        plt.savefig(Model.validate_filename+'.png')        
        
    def _simulate(self, Model):
        '''Use Monte Carlo simulation to predict an occupancy timeseries.'''
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
                if jmptimes == None:
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
        '''Format the training data for use in parameter estimation.'''
        # Set the occupancy measurement key
        self.occ_key = Model.measurements.keys()[0];
        # Get the training data from measurements
        self.df_data_train = Model.measurements[self.occ_key]['Measured'].get_base_data()[Model.start_time:Model.final_time];        
        # Specify the weekday number of each measurement point
        self.df_data_train['day'] = self.df_data_train.index.weekday;
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
        self.data_train = df_interest.as_matrix();
        self.data_train = self.data_train.reshape((self.data_train.size/self.points_per_day, self.points_per_day));
    
