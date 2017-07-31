# -*- coding: utf-8 -*-
"""
The ``utility`` module contains classes and functions that are primarily for 
back-end functionality that is common across the other mpcpy modules.  These
include interactions with ``pandas`` objects, fmu objects, and various other
data management tasks.  For this reason, most of the classes and methods 
contained in this module are intended for internal use. Exceptions are listed 
in the following section.

=========
Functions
=========

.. automethod:: mpcpy.utility.get_unit_class_from_unit_string

.. automethod:: mpcpy.utility.get_MPCPy_path

"""

from abc import ABCMeta
import os
import numpy as np
import pandas as pd
from pyfmi.common import core
from pyfmi.common import xmlparser
import inspect
from mpcpy import variables
from mpcpy import units
from tzwhere import tzwhere
from dateutil.relativedelta import relativedelta
from pytz import exceptions as pytz_exceptions
from pyfmi import load_fmu
from pymodelica import compile_fmu


#%%
class _mpcpyPandas(object):
    '''Mixin class for methods related to pandas integration.
    
    '''
    
    __metaclass__ = ABCMeta;   
    
    def _mpcpy_ts_list_to_dataframe(self, mpcpy_ts_list, display_data = False):
        '''Combine mpcpy timeseries into one pandas dataframe with base units.
        
        Parameters
        ----------
        mpcpy_ts_list : list of variables.Timeseries objects
            List of mpcpy timeseries veriables to be combined into a dataframe.
        display_data : boolean, default = False
            True will use display units, False will use base units.
            
        Returns
        -------
        df : ``pandas`` dataframe
            Dataframe where the columns are formed by the supplied list of 
            mpcpy timeseries variables.
        
        '''
        
        d = {};
        for mpcpy_ts in mpcpy_ts_list:
            if display_data:
                d[mpcpy_ts.name] = mpcpy_ts.display_data();
            else:
                d[mpcpy_ts.name] = mpcpy_ts.get_base_data();
        try:
            df = pd.DataFrame(d).interpolate(method='linear');
        except ValueError:
            for mpcpy_ts_name in d.keys():
                d[mpcpy_ts_name].to_frame().to_csv(get_MPCPy_path() + os.sep + mpcpy_ts_name);
        df.index.name = 'Time'; 
        
        return df
    
    def _dataframe_to_mpcpy_ts_variable(self, df, key, varname, unit, **kwargs):
        '''Convert dataframe column to mpcpy timeseries variable.
        
        Parameters
        ----------
        df : ``pandas`` dataframe object
            Dataframe with a datetime index.
        key : string
            Column name to convert to mpcpy timeseries variable.
        varname : string
            Variable name to assign to mpcpy timeseries variable.
        unit : units.unit class
            Unit to assign to mpcpy timeseries variable
        cleaning_type : variables.Timseries.cleaning_type class, optional
            Cleaning to be done to the data.
        cleaning_args : tuple, required if cleaning_type
            Arguments of the cleaning type.
            
        Returns
        -------
        var : variables.Timeseries
            mpcpy timeseries variable resulting from the dataframe column.
        
        '''
        
        if 'start_time' in kwargs:
            start_time = kwargs['start_time'];
        else:
            start_time = df.index.values[0];
        if 'final_time' in kwargs:
            final_time = kwargs['final_time'];
        else:
            final_time = df.index.values[-1];
        if 'cleaning_type' in kwargs:
            cleaning_type = kwargs['cleaning_type'];
            cleaning_args = kwargs['cleaning_args'];
            var = variables.Timeseries(varname, df.loc[start_time:final_time, key], unit, tz_name = self.tz_name, \
                                       cleaning_type = cleaning_type, \
                                       cleaning_args = cleaning_args);
        else:
            var = variables.Timeseries(varname, df.loc[start_time:final_time, key], unit, tz_name = self.tz_name);
        
        return var
     
    def _add_simtime_column(self, df):
        '''Add a simulation time column to a dataframe from the DateTimeIndex.
        
        The simulation time is added in seconds starting at 0.
        
        Parameters
        ----------
        df : ``pandas`` dataframe object
            Dataframe for which to add a simulation time column.
        
        Returns
        -------
        df_simtime : ``pandas`` dataframe object
            Dataframe with ``'SimTime'`` column added.

        '''
        
        t = df.index.to_series();
        dt = t - t[0];
        dt = dt.apply(lambda x: x / np.timedelta64(1, 's'));
        dt.name = 'SimTime';
        df_simtime = df.join(dt)
        
        return df_simtime
        
    def _set_time_interval(self, start_time, final_time):
        '''Convert start and final time to utc timestamps and other metrics.

        Parameters
        ----------
        start_time : string
            Starting time of period.
        final_time : string
            Final time of period.
    
        Yields
        ------
        start_time : datetime object
            Attribute for starting time of period in local time.
        final_time : datetime object
            Attribute for final time of period in local time.
        start_time_utc : datetime object
            Attribute for starting time of period in utc time.
        final_time_utc : datetime object
            Attribute for final time of period in utc time.
        elapsed_seconds : float
            Attribute for number of seconds elapsed during time period specified.
        year_start_seconds : float
            Attribute for number of seconds elapsed from start of year to start time.
        year_final_seconds : float
            Attribute for number of seconds elapsed from start of year to final time.

        '''

        try:
            getattr(self, 'tz_name')
        except AttributeError:
            self.tz_name = 'UTC';
        try:
            self.start_time = pd.to_datetime(start_time).tz_localize(self.tz_name);
            self.final_time = pd.to_datetime(final_time).tz_localize(self.tz_name);
        except TypeError:
            self.start_time = start_time;
            self.final_time = final_time;
        start_of_year = pd.to_datetime('1/1/' + str(self.start_time.year)).tz_localize(self.tz_name);
        year_start_timedelta = self.start_time - start_of_year;
        year_final_timedelta = self.final_time - start_of_year;
        self.start_time_utc = self.start_time.tz_convert('UTC');
        self.final_time_utc = self.final_time.tz_convert('UTC');
        self.elapsed_seconds = (self.final_time - self.start_time).total_seconds();
        self.year_start_seconds = year_start_timedelta.total_seconds();
        self.year_final_seconds = year_final_timedelta.total_seconds();
        
    def _parse_time_zone_kwargs(self, kwargs):
        '''Set the timezone using geography or timezone name.
        
        If no timezone is supplied, than utc is assigned.
        
        Parameters
        ----------
        tz_name : string, optional
            Name of timezone according to the package ``tzwhere``.  If 
            ``'from_geography'``, then geography kwarg is required.
        geography : list or tuple, optional
            List or tuple with (latitude, longitude) in degrees.   
            
        Yields
        ------
        tz_name : string
            Attribute for timezone name.
        
        '''
        
        # Geography
        if 'geography' in kwargs:
            self.lat = variables.Static('lat', kwargs['geography'][0], units.deg);
            self.lon = variables.Static('lon', kwargs['geography'][1], units.deg);
        else:
            self.lat = None;
            self.lon = None;
        # UTC Time Input
        if 'tz_name' in kwargs:
            if kwargs['tz_name'] == 'from_geography':
                self.tz = tzwhere.tzwhere();
                self.tz_name = self.tz.tzNameAt(kwargs['geography'][0], kwargs['geography'][1]);
            else:            
                self.tz_name = kwargs['tz_name'];
        else:
            self.tz_name = 'UTC';        

#%%
class _FMU(_mpcpyPandas):
    '''Mixin class for methods related to utilizing fmus.
    
    '''
    
    __metaclass__ = ABCMeta;
       
    def _simulate_fmu(self):
        '''Simulate an fmu with pyfmi and using any given exodata inputs.
        
        Yields
        ------
        measurements[key]['Simulated'] : variables.Timeseries
            Populates the `Simulated` key of the ``measurements`` dictionary 
            attribute with mpcpy timeseries variables.
        
        '''
        
        # Create input_mpcpy_ts_list
        self._create_input_mpcpy_ts_list_sim();
        # Set inputs
        self._create_input_object_from_input_mpcpy_ts_list(self._input_mpcpy_ts_list);       
        # Load simulation fmu  
        simulate_model = load_fmu(self.fmupath);
        # Set parameters in fmu if they exist
        if hasattr(self, 'parameter_data'):
            for key in self.parameter_data.keys():
                simulate_model.set(key, self.parameter_data[key]['Value'].get_base_data());
        # Get minimum measurement sample rate for simulation
        min_sample = 3600;
        for key in self.measurements.keys():
            sample = self.measurements[key]['Sample'].get_base_data();
            if sample < min_sample:
                min_sample = sample; 
        # Set Options
        self._sim_opts = simulate_model.simulate_options();
        self._sim_opts['ncp'] = int(self.elapsed_seconds/min_sample);
        # Simulate
        self._res = simulate_model.simulate(start_time = 0, \
                                           final_time = self.elapsed_seconds, \
                                           input = self._input_object, \
                                           options = self._sim_opts);
        # Retrieve measurements
        fmu_variable_units = self._get_fmu_variable_units();
        for key in self.measurements.keys():
            data = self._res[key];
            time = self._res['time'];
            timedelta = pd.to_timedelta(time, 's');
            timeindex = self.start_time_utc + timedelta;
            ts = pd.Series(data = data, index = timeindex);
            ts.name = key;
            unit = self._get_unit_class_from_fmu_variable_units(key,fmu_variable_units);
            if not unit:
                unit = units.unit1;                
            self.measurements[key]['Simulated'] = variables.Timeseries(key, ts, unit);
            
    def _create_input_mpcpy_ts_list_sim(self):
        '''Create a list of mpcpy timeseries for input into fmu for simulation.
        
        '''
        
        self._input_mpcpy_ts_list = [];
        # Weather
        for key in self.weather_data.keys():
            if key in self.input_names:
                self._input_mpcpy_ts_list.append(self.weather_data[key]);
        # Internal
        for zone in self.internal_data.keys():
            for intLoad in ['intCon', 'intRad', 'intLat']:
                if intLoad+'_'+zone in self.input_names:
                    self._input_mpcpy_ts_list.append(self.internal_data[zone][intLoad]);
        # Controls
        for key in self.control_data.keys():
            if key in self.input_names:
                self._input_mpcpy_ts_list.append(self.control_data[key]);                     
        # Other inputs                   
        for key in self.other_inputs.keys():
            if key in self.input_names:
                self._input_mpcpy_ts_list.append(self.other_inputs[key]);

    def _create_input_mpcpy_ts_list_opt(self):
        '''Create a list of mpcpy timeseries for input into fmu for optimization.
        
        '''
        
        self._input_mpcpy_ts_list_opt = [];
        # Weather
        for key in self.weather_data.keys():
            if key in self.opt_input_names:
                self._input_mpcpy_ts_list_opt.append(self.weather_data[key]);
        # Internal
        for zone in self.internal_data.keys():
            for intLoad in ['intCon', 'intRad', 'intLat']:
                if intLoad+'_'+zone in self.input_names:
                    self._input_mpcpy_ts_list_opt.append(self.internal_data[zone][intLoad]);
        # Controls
        for key in self.control_data.keys():
            if key in self.opt_input_names:
                self._input_mpcpy_ts_list_opt.append(self.control_data[key]);                     
        # Other inputs                   
        for key in self.other_inputs.keys():
            if key in self.opt_input_names:
                self._input_mpcpy_ts_list_opt.append(self.other_inputs[key]);

    def _create_input_object_from_input_mpcpy_ts_list(self, input_mpcpy_ts_list):
        '''Create a fmu input object from list of mpcpy timeseries.
        
        '''
        
        # Check if empty
        if input_mpcpy_ts_list:
            # If not, fill input object
            self._input_df = self._mpcpy_ts_list_to_dataframe(input_mpcpy_ts_list);
            self._input_object = self._dataframe_to_input_object(self._input_df[self.start_time_utc:self.final_time_utc]);
        else:
            # Otherwise, create empty input object
            self._input_object = ();

    
    def _create_fmu(self, kwargs):
        '''Load fmu or compile and load fmu from Modelica code.
        
        Parameters
        ----------
        fmupath : string, required if moinfo not specified
            Path to fmu file.
        moinfo : (string, string, list), required if fmupath not specified
            Tuple where [0] is path to .mo file, [1] is modelica path to model, 
            [2] is list of required modelica library paths.
            
        Yields
        ------
        fmupath : string
            Attribute for path to fmu file.
        mopath : string
            Attribute for path to .mo file.
        modelpath : string
            Attribute for modelica path to model.
        libraries : list
            Attribute for list of paths to required modelica libraries.
        fmu : ``pyfmi`` fmu object
            Attribute for fmu object using the load_fmu method of pyfmi.
        fmu_version : string
            Attribute for version of fmu.  ``'1.0'`` or ``'2.0'``.

        '''
        
        if 'fmupath' in kwargs:
            self.fmupath = kwargs['fmupath'];
            self.mopath = None;
            self.modelpath = None
            self.libraries = None;
        if 'moinfo' in kwargs:
            self.mopath = kwargs['moinfo'][0];
            self.modelpath = kwargs['moinfo'][1];
            self.libraries = kwargs['moinfo'][2];
            if 'version' in kwargs:
                version = kwargs['version'];
            else:
                version = '2.0';
            self.fmupath = compile_fmu(self.modelpath, \
                                       self.mopath, \
                                       compiler_options = {'extra_lib_dirs':self.libraries}, 
                                       version = version);
        self.fmu = load_fmu(self.fmupath);
        self.fmu_version = self.fmu.get_version();
        
    def _dataframe_to_input_object(self, df):
        '''Create a fmu input object from dataframe.
        
        Parameters
        ----------
        df : ``pandas`` dataframe object
            Dataframe to convert to fmu input_object.
            
        Returns
        -------
        input_object : tuple
            Input object that can be used to simulate an fmu with pyfmi.

        '''

        input_names = tuple(df);
        input_df_simtime = self._add_simtime_column(df);
        input_trajectory = input_df_simtime['SimTime'].get_values();
        for header in input_names:
            input_trajectory = np.vstack((input_trajectory, df[header].get_values()));
        input_object = (input_names, np.transpose(input_trajectory));
        
        return input_object;
                          
    def _get_input_names(self):
        '''Get the names of the input variables of the fmu.
        
        Returns
        -------
        input_names : list
            List of variable names that are fmu inputs.
        
        '''
        
        if self.fmu_version == '1.0':
            input_names = self.fmu.get_model_variables(causality = 0).keys();
        elif self.fmu_version == '2.0':
            input_names = self.fmu.get_model_variables(causality = 2).keys();
        else:
            raise TypeError ('fmu version {0} is not compatable.'.format(self.fmu_version));

        return input_names;
        
    def _get_fmu_variable_units(self):
        '''Get fmu model variable units.
        
        Returns
        -------
        fmu_variable_units : dictionary
            Dictionary where the keys are variable names and values are unit
            strings.  These unit strings can be used by 
            ``_get_unit_class_from_fmu_variable_units`` to get the 
            corresponding mpcpy unit class.
        
        '''
        
        tmpdir = core.unzip_unit(self.fmupath);
        element_tree = xmlparser._parse_XML(tmpdir+os.sep + 'modelDescription.xml');
        root = element_tree.getroot();
        model_variables = root.find('ModelVariables');
        type_definitions = root.find('TypeDefinitions');
        variables = model_variables.getchildren();
        if type_definitions is not None:
            types = type_definitions.getchildren();
        fmu_variable_units = {};
        for variable in variables:
            real = variable.find('Real');
            if real is not None:
                items = real.items();
                attributes = [];
                for attribute in items:
                    attributes.append(attribute[0]);
                if 'unit' in attributes:
                    unit = real.get('unit');
                elif 'declaredType' in attributes and 'unit' not in attributes:
                    variable_type = real.get('declaredType');
                    for type_instance in types:
                        if variable_type == type_instance.get('name'):
                            if self.fmu_version == '1.0':
                                sub_type = type_instance.find('RealType');
                            elif self.fmu_version == '2.0':
                                sub_type = type_instance.find('Real');
                            else:
                                raise TypeError('Cannot get variable units for fmu {0}.'.format(self.fmu_version));
                            if sub_type is not None:
                                unit = sub_type.get('unit');
                else:
                    unit = None;
                
                fmu_variable_units[variable.get('name')] = unit;
            
        return fmu_variable_units
    
    def _get_unit_class_from_fmu_variable_units(self, variable_name, fmu_variable_units):
        '''Get units.unit class for the given variable.
        
        Parameters
        ----------
        variable_name : string
            Name of the fmu variable for which to get the mpcpy unit class.
        fmu_variable_units : dictionary
            Dictionary where the keys are variable names and values are unit
            strings.  Can be gotten by ``_get_fmu_variable_units``.
            
        Returns
        -------
        unit_class : units.unit
            mpcpy unit class of fmu variable.
        
        '''
        
        unit_class_items = inspect.getmembers(units);
        unit_class = [];
        for unit_class_item in unit_class_items:
            try:
                temp_var = variables.Static('tempvar', 1, unit_class_item[1]);   
                if fmu_variable_units[variable_name] == temp_var.get_display_unit_name():
                    unit_class = unit_class_item[1];
                    break
            except:
                continue
            
        return unit_class
        
#%%
class _Building(object):
    '''Mixin class for methods related to building models.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    def _parse_building_kwargs(self, kwargs):
        '''Parse the kwargs associated with initializing a building model.
        
        Yields
        ------
        zone_names : list
            Zone name list attribute.
        weather_data : dictionary
            Weather ``exodata`` data dictionary attribute.
        internal_data : dictionary
            Internal load ``exodata`` data dictionary attribute.
        control_data : dictionary
            Control ``exodata`` data dictionary attribute.
        other_inputs : dictionary
            Other input ``exodata`` data dictionary attribute.
        parameter_data : dictionary
            Parameter ``exodata`` data dictionary attribute.

        '''
        
        # Zone names
        if 'zone_names' in kwargs:
            self.zone_names = kwargs['zone_names'];
        else:
            self.zone_names = {};
        # Weather
        if 'weather_data' in kwargs:
            self.weather_data = kwargs['weather_data'];
        else:
            self.weather_data = {};
        # Internal
        if 'internal_data' in kwargs:
            self.internal_data = kwargs['internal_data'];
        else:
            self.internal_data = {};
        # Control
        if 'control_data' in kwargs:
            self.control_data = kwargs['control_data'];
        else:
            self.control_data = {};
        # Other inputs
        if 'other_inputs' in kwargs:
            self.other_inputs = kwargs['other_inputs'];
        else:
            self.other_inputs = {};
        # Parameters
        if 'parameter_data' in kwargs:
            self.parameter_data = kwargs['parameter_data'];
            # Check if free tag exists
            for key in self.parameter_data.keys():
                if 'Free' not in self.parameter_data[key]:
                    self.parameter_data[key]['Free'] = variables.Static(key+'_free', False, units.boolean);
        else:
            self.parameter_data = {};
        
#%%
class _DAQ(object):
    '''Mixin class for methods related to collecting data.
    
    '''
    
    __metaclass__ = ABCMeta;
    
    def _parse_daq_kwargs(self, kwargs):
        '''Parse the kwargs related to data collection.
        
        Yields
        ------
        time_format = timespec string
            Attribute for the specification of the time format.
        time_header = string
            Attribute for the column header containing time stamp data.
        clean_data : dictionary
            Attribute to specify data cleaning.  
            { 'csvHeader' : 'cleaning_type' = variables.Timeseries.cleaning_type,
            'cleaning_args' = (cleaning_args)}
        
        '''
    
        # Time Format
        if 'time_format' in kwargs:
            # String of timespec
            self.time_format = kwargs['time_format'];
        else:
            self.time_format = None;
        # Time Header
        if 'time_header' in kwargs:
            # String of column header representing time
            self.time_header = kwargs['time_header'];
        else:
            self.time_header = None;
        # Data Cleaning
        if 'clean_data' in kwargs:
            self.clean_data = kwargs['clean_data'];
        else:
            self.clean_data = None;
        
    def _search_variable_map(self, mpcpy_varname):
        '''Search variable map for column name matching the mpcpy variable name.
        
        Parameters
        ----------
        mpcpy_varname : string
            Variable name used in mpcpy.
            
        Returns
        -------
        key : string
            Variable name in column header.
        
        '''
        
        for key in self.variable_map:
            if self.variable_map[key][0] == mpcpy_varname:
                break
            
        return key
        
    def _read_timeseries_from_csv(self):
        '''Read timeseries data from a csv into mpcpy data.
        
        This method assumes the concrete class will define the method
        ``_translate_variable_map``.
        
        '''
        
        # Set time index from default or user-specified time header
        if self.time_header is not None:
            time_headers = self.time_header;
        else:
            time_headers = ['Time', 'time', 'Timestamp', 'timestamp']; 
        self._df_csv = pd.read_csv(self.file_path);        
        for key in self._df_csv.columns.values:
            if key in time_headers:
                time = pd.to_datetime(self._df_csv[key], format = self.time_format);
                self._df_csv.set_index(time, inplace=True);
                self._df_csv.index.name = 'Time';
                try:
                    self._df_csv = self._df_csv.tz_localize(self.tz_name);
                except pytz_exceptions.AmbiguousTimeError as time_ambiguous:
                    time_ambiguous = pd.to_datetime(time_ambiguous.args[0].split("'")[1])
                    if time_ambiguous.month == 11:
                        _df_csv_dst = self._df_csv[self._df_csv.index < time_ambiguous].tz_localize(self.tz_name);
                        _df_csv_st = self._df_csv[(self._df_csv.index > time_ambiguous + relativedelta(hours = 1))].shift(periods = -1, freq = 'H').tz_localize(self.tz_name);
                        _df_csv_amb = self._df_csv[(self._df_csv.index >= time_ambiguous) & (self._df_csv.index <= time_ambiguous + relativedelta(hours = 1))];
                        _df_csv_amb_0 = _df_csv_amb.iloc[0:1].tz_localize(self.tz_name, ambiguous = np.array([True]));
                        _df_csv_amb_1 = _df_csv_amb.iloc[1:2].shift(periods = -1, freq = 'H').tz_localize(self.tz_name, ambiguous = np.array([False]));
                        self._df_csv = pd.concat([_df_csv_dst, _df_csv_amb_0, _df_csv_amb_1, _df_csv_st], axis = 0);
                
        # Get timeseries data according to variable map and cleaning
        for self._key in self.variable_map:
            if self._key not in time_headers:
                try:
                    self._cleaning_type = self.clean_data[self._key]['cleaning_type'];
                    self._cleaning_args = self.clean_data[self._key]['cleaning_args'];
                except (TypeError,KeyError):
                    self._cleaning_type = None;
                    self._cleaning_args = None;   
                self._translate_variable_map();    
    
class _Measurements(object):
    '''Mixin class to handle operations on measurement dictionaries.
    
    Concrete class requires _mpcpyPandas methods.
    
    '''
    
    def display_measurements(self, measurement_key):
        '''Get measurements data in display units as pandas dataframe.
        
        Parameters
        ----------
        measurement_key : string
            The measurement dictionary key for which to get the data for all 
            of the variables.
        
        Returns
        -------
        df : ``pandas`` dataframe
            Timeseries dataframe in display units containing data for all 
            measurement variables.
        
        '''

        mpcpy_ts_list = self._make_mpcpy_ts_list(measurement_key);
        df = self._mpcpy_ts_list_to_dataframe(mpcpy_ts_list, display_data = True);
        
        return df;

    def get_base_measurements(self, measurement_key):
        '''Get measurements data in base units as pandas dataframe.
        
        Parameters
        ----------
        measurement_key : string
            The measurement dictionary key for which to get the data for all 
            of the variables.
        
        Returns
        -------
        df : ``pandas`` dataframe
            Timeseries dataframe in base units containing data for all 
            measurement variables.
        
        '''

        mpcpy_ts_list = self._make_mpcpy_ts_list(measurement_key);
        df = self._mpcpy_ts_list_to_dataframe(mpcpy_ts_list, display_data = False);
        
        return df;
        
    def _make_mpcpy_ts_list(self, measurement_key):
        '''Create mpcpy ts list from measurement dictionary.
    
        Parameters
        ----------
        measurement_key : string
            The measurement dictionary key for which to get the data for all 
            of the variables.

        Returns
        -------
        mpcpy_ts_list : list
            List of mpcpy timeseries variables.
            
        '''
        
        mpcpy_ts_list = [];
        for key in self.measurements.keys():
            mpcpy_ts_list.append(self.measurements[key][measurement_key])
        
        return mpcpy_ts_list
       
#%% Get the MPCPy path
def get_MPCPy_path():
    '''Get the MPCPy home path.

    Returns
    -------
    MPCPy_path : string
        Absolute path to the MPCPy home directory.

    '''
    
    rel_path = os.sep + 'mpcpy' + os.sep + 'utility.py'
    MPCPy_path = os.path.abspath(__file__)[:-len(rel_path)];
    
    return MPCPy_path
    
#%% Get a unit class from a unit string
def get_unit_class_from_unit_string(unit_string):
    '''Get mpcpy.unit class for the given variable string.

    Parameters
    ----------
    unit_string : string
        Unit string.  For example, the unit string for a heat transfer
        coefficient in SI units would be ``'W/(m2.K)'``.
        
    Returns
    -------
    unit_class : units.unit class
        The mpcpy unit class for the given unit string.  This class can be used
        to define an mpcpy variable object.  See ``variables``.
    
    '''

    unit_class_items = inspect.getmembers(units);
    unit_class = [];
    for unit_class_item in unit_class_items:
        try:
            temp_var = variables.Static('tempvar', 1, unit_class_item[1]);   
            if unit_string == temp_var.get_display_unit_name():
                unit_class = unit_class_item[1];
                break
        except:
            continue

    return unit_class