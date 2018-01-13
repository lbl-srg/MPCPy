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
    :members: estimate, validate, simulate, set_estimate_method, 
              set_validate_method, display_measurements, 
              get_base_measurements

Estimate Methods
================

.. autoclass:: mpcpy.models.JModelica

.. autoclass:: mpcpy.models.UKF

.. autoclass:: mpcpy.models.ModestPy

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
import os
import modestpy

#%% Model Class
class _Model(utility._mpcpyPandas, utility._Measurements):
    '''Base class for representing a model for MPC.
    
    '''

    __metaclass__ = ABCMeta;

    @abstractmethod
    def estimate(self, **kwargs):
        '''Estimate parameters of the model using the measurement and 
        parameter_data dictionary attributes.

        Yields
        ------
        Updates the ``'Value'`` key for each estimated parameter in the 
        parameter_data attribute.

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

#%% Model Implementations
class Modelica(_Model, utility._FMU, utility._Building):
    '''Class for models of physical systems represented by Modelica or an FMU.

    Parameters
    ----------
    estimate_method : estimation method class from mpcpy.models
        Method for performing the parameter estimation.
    validate_method : validation method class from mpcpy.models
        Method for performing the parameter validation.
    measurements : dictionary
        Measurement variables for the model.  Same as the measurements 
        attribute from a ``systems`` class.  See documentation for ``systems`` 
        for more information.
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
    tz_name : string, optional
        Name of timezone according to the package ``tzwhere``.  If 
        ``'from_geography'``, then geography kwarg is required.
    geography : list or tuple, optional
        List or tuple with (latitude, longitude) in degrees.          

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
    
    def __init__(self, estimate_method, validate_method, measurements, **kwargs):
        '''Constructor of a modelica or FMU model object.
        
        '''
        
        self.name = 'modelica';    
        self.measurements = measurements;
        self._create_fmu(kwargs);
        self.input_names = self._get_input_names();                                       
        self._parse_building_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        self.set_estimate_method(estimate_method);
        self.set_validate_method(validate_method);
        
    def estimate(self, start_time, final_time, measurement_variable_list, **kwargs):
        '''Estimate the parameters of the model.
        
        The estimation of the parameters is based on the data in the 
        ``'Measured'`` key in the measurements dictionary attribute, 
        the parameter_data dictionary attribute, and any exodata inputs.
        
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
        kwargs: Optional parameters
            Additional parameters that can be passed to the estimation method.

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
        # Check for continue
        if start_time == 'continue':
            raise ValueError('"continue" is not a valid entry for start_time for parameter estimation problems.')
        # Perform parameter estimation
        self._set_time_interval(start_time, final_time);
        self.measurement_variable_list = measurement_variable_list;
        self._estimate_method._estimate(self, **kwargs);
        
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
            
    def simulate(self, start_time, final_time):
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
        
    def set_estimate_method(self, estimate_method):
        '''Set the estimation method for the model.

        Parameters
        ----------
        estimate_method : estimation method class from mpcpy.models
            Method for performing the parameter estimation.

        '''

        self._estimate_method = estimate_method(self);  
        
    def set_validate_method(self, validate_method):
        '''Set the validation method for the model.

        Parameters
        ----------
        validate_method : validation method class from mpcpy.models
            Method for performing the parameter validation.

        '''

        self._validate_method = validate_method(self);
        
class Occupancy(_Model):
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
        
        
#%% Estimate Method Interface
class _Estimate(utility._mpcpyPandas):
    '''Interface for a model identifcation method.
    
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
             
#%% Estimate Method Interface Implementations
class JModelica(_Estimate):
    '''Estimation method using JModelica optimization.
    
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
        

class UKF(_Estimate, utility._FMU):
    '''Estimation method using the Unscented Kalman Filter.
    
    This estimation method uses the UKF implementation EstimationPy-KA_, 
    which is a fork of EstimationPy_ that allows for parameter estimation 
    without any state estimation.
    
    .. _EstimationPy: https://github.com/lbl-srg/EstimationPy
    
    .. _EstimationPy-KA: https://github.com/krzysztofarendt/EstimationPy-KA

    '''

    def __init__(self, Model):
        '''Constructor of UKF estimation method.
        
        '''

        self.name = 'UKF';
        # Check correct fmu version
        if Model.fmu_version != '1.0':
            raise ValueError('Compiled fmu version is {0} and needs to be 1.0.'.format(Model.fmu_version));
        else:
            self.fmu_version = Model.fmu_version;
        # Instantiate UKF model
        self.model = ukf_model.Model(Model.fmupath);
        
    def _estimate(self, Model):
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
                

class ModestPy(_Estimate):
    """
    ModestPy_ estimation algorithm based on a multi-step estimation. Available steps:
    * genetic algorithm ('GA')
    * pattern search ('PS')
    * sequential quadratic programming ('SQP')

    GA followed by PS is the default method sequence. Both are able to handle models
    with possibly non-linear and non-continuous terms. Typically, the estimation
    takes more time than using JModelica, but there are higher chances to find
    the global optimum.

    The method saves additional output files: 

        * best_per_run.csv - estimates and errors from all runs (run per row),

        * final.csv - final estimated parameters

        * summary_N.csv - errors, methods, parameters from all iterations

        * errors.png - plot of errors from all runs

        * ga_N.png and ps_N.png - parameter evolution plots for N run of GA and PS (n/a for SQP)

    By default the files are saved in the current working directory. A custom
    directory can be chosen with the ``workdir`` argument.

    The estimation methods (GA, PS, SQP) have method specific options that can
    be overwritten by the user. The most often used options are (default values shown):

        * ``ga_opts = {'maxiter': 50, 'pop_size': max(4 * n_parameters, 20), 'tol': 1e-6, 'lhs': False}``

        * ``ps_opts = {'maxiter': 500, 'tol': 1e-11}``

        * ``sqp_opts = {'scipy_opts': {'disp': True, 'iprint': 2, 'maxiter': 150, 'full_output': True}}``

    where ``maxiter`` is the maximum number of iterations, ``pop_size`` is the GA population size,
    ``tol`` is the error tolerance, ``lhs`` is the Latin Hypercube Sampling initialization. The SQP
    method is based on the SciPy implementation. Refer to the `SciPy documentation`_ to see what
    parameters can be passed in ``scipy_opts``.

    .. _ModestPy: https://github.com/sdu-cfei/modest-py
    .. _SciPy documentation: https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html

    Optional parameters
    -------------------
    workdir: string
        Working directory
    fmi_opts: dict
        Optional parameters passed to the solver via FMI
    ga_opts: dict
        Optional GA parameters
    ps_opts: dict
        Optional PS parameters
    sqp_opts: dict
        Optional SQP parameters (passed to SLSQP solver in SciPy)
    lp_n: int
        Number of learning runs, default 1
    methods: tuple(str)
        Method sequence, default ('GA', 'PS')
    seed: int
        Random number seed (used in GA)
    ftype: str
        Cost function type, 'RMSE' (default) or 'NRMSE' (advised if cost function includes multiple variables)
    """

    def __init__(self, Model):
        self.name = 'ModestPy'

    def _estimate(self, Model, **kwargs):

        # Settings
        # ========
        # Default
        workdir = os.getcwd() # Directory to save outputs of modestpy (can be changed by the user)
        fmu_path = Model.fmupath

        fmi_opts = {}       # Options passed to the model solver via FMI
        ga_opts = {}        # Genetic Algorithm options
        ps_opts = {}        # Pattern Search options
        sqp_opts = {}       # Sequential Quadratic Programming options (SLSQP from SciPy)
        methods = ('GA', 'PS')

        lp_n = 1            # One learning period (can be changed by the user)
        ic_param = None     # TODO: Decide with Dave what to do with IC parameters
        seed = None         # Random number seed, can be None
        ftype = 'RMSE'      # Cost function type, 'RMSE' or 'NRMSE'

        # Custom settings from kwargs
        for key in kwargs:
            if key == 'workdir':
                workdir = kwargs[key]
            elif key == 'fmi_opts':
                fmi_opts = kwargs[key]
            elif key == 'ga_opts':
                ga_opts = kwargs[key]
            elif key == 'ps_opts':
                ps_opts = kwargs[key]
            elif key == 'sqp_opts':
                sqp_opts = kwargs[key]
            elif key == 'methods':
                methods = kwargs[key]
            elif key == 'lp_n':
                lp_n = kwargs[key]
            # elif key == 'ic_param':
            #     ic_param = kwargs[key]
            elif key == 'seed':
                seed = kwargs[key]
            elif key == 'ftype':
                ftype = kwargs[key]
    
        # Get measurements
        # ================
        ideal = pd.DataFrame()
        meas_vars = Model.measurement_variable_list
        for v in meas_vars:
            base = Model.measurements[v]['Measured'].get_base_data()
            # Drop duplicates to avoid pandas errors
            base = base[~base.index.duplicated(keep='first')]
            ideal[v] = base

        # Get inputs
        # ==========
        input_names = Model.input_names
        inp = pd.DataFrame(columns=input_names)

        # Add weather variables (but only those used in the model)
        weather_vars = Model.weather_data.keys()
        for v in weather_vars:
            if v in input_names:
                base = Model.weather_data[v].get_base_data()
                # Drop duplicates to avoid pandas errors
                base = base[~base.index.duplicated(keep='first')]
                inp[v] = base

        # Add internal heat gain variables (only those used in the model)
        zones = Model.internal_data.keys()
        for zone in zones:
            internal_vars = Model.internal_data[zone].keys()
            for v in internal_vars:
                v_zone = v + '_' + zone
                if v_zone in input_names:
                    base = Model.internal_data[zone][v].get_base_data()
                    # Drop duplicates to avoid pandas errors
                    base = base[~base.index.duplicated(keep='first')]
                    inp[v_zone] = base

        # Add control variables (only those used in the model)
        control_vars = Model.control_data.keys()
        for v in control_vars:
            if v in input_names:
                base = Model.control_data[v].get_base_data()
                # Drop duplicates to avoid pandas errors
                base = base[~base.index.duplicated(keep='first')]
                inp[v] = base

        # Add other input variables (only those used in the model)
        other_vars = Model.other_inputs.keys()
        for v in other_vars:
            if v in input_names:
                base = Model.other_inputs[v].get_base_data()
                # Drop duplicates to avoid pandas errors
                base = base[~base.index.duplicated(keep='first')]
                inp[v] = base

        # Get parameters
        # ==============
        est = dict()
        known = dict()

        for par_name in Model.parameter_data:

            # Initial value
            val = Model.parameter_data[par_name]['Value'].get_base_data()
            # Variability
            is_free = Model.parameter_data[par_name]['Free'].get_base_data()

            if is_free is 1:
                # Estimated parameter
                lo = Model.parameter_data[par_name]['Minimum'].get_base_data()
                hi = Model.parameter_data[par_name]['Maximum'].get_base_data()
                est[par_name] = (val, lo, hi)
            else:
                # Known parameter
                known[par_name] = val

        # Trim dataframes and adjust indexes
        # ==================================
        # Define start and end of learning period
        start = Model.start_time_utc
        end = Model.final_time_utc
        # Learning period
        ideal = ideal.loc[start:end]
        inp = inp.loc[start:end]
        # Adjust index to the smallest step
        inp_step = inp.index[1] - inp.index[0]
        ideal_step = ideal.index[1] - ideal.index[1]

        if ideal_step <= inp_step:
            inp = inp.reindex(ideal.index, method='ffill')
        else:
            ideal = ideal.reindex(inp.index, method='ffill')

        # Indexes to seconds
        inp.index = inp.index.astype(np.int64) // 10**9
        ideal.index = ideal.index.astype(np.int64) // 10**9

        # Rename indexes
        inp.index.name = 'time'
        ideal.index.name = 'time'

        # Estimation using ModestPy
        # =========================
        session = modestpy.Estimation(workdir, fmu_path, inp, known, est, ideal,
                                      lp_n=lp_n, lp_len=None, lp_frame=None, 
                                      vp=None, ic_param=None, methods=methods,
                                      fmi_opts=fmi_opts, ga_opts=ga_opts, ps_opts=ps_opts,
                                      sqp_opts=sqp_opts, seed=seed, ftype=ftype)
        estimates = session.estimate()

        # Put estimates into Model.parameter_data
        for par_name in estimates:
            Model.parameter_data[par_name]['Value'].set_data(estimates[par_name])

        return None
        
#%% Validate Method Interfaces
class RMSE(_Validate):
    '''Validation method that computes the RMSE between estimated and measured data.
    
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
            data = Model.measurements[key]['Measured'].get_base_data()[Model.start_time:Model.final_time];
            data_est = Model.measurements[key]['Simulated'].get_base_data()[Model.start_time:Model.final_time];
            RMSE = np.sqrt(sum((data_est-data)**2)/len(data));
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
    
