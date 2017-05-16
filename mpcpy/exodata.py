# -*- coding: utf-8 -*-
"""
exodata.py
by David Blum

This module contains the classes and interfaces required for collecting 
exogenous data and converting it into a form that is useable throughout MPCPy.

"""

from abc import ABCMeta, abstractmethod
from mpcpy import utility
import numpy as np
import pandas as pd
from tzwhere import tzwhere
from dateutil.relativedelta import relativedelta
from pytz import exceptions as pytz_exceptions
from mpcpy import units
from mpcpy import variables
     
#%% Abstract source interface class
class Type(utility.mpcpyPandas):
    '''Abstract class for exogenous data sources.'''
    __metaclass__ = ABCMeta;
    
    @abstractmethod
    def collect_data(self):
        pass;
    
    @abstractmethod
    def display_data(self):
        pass;
        
    @abstractmethod
    def get_base_data(self):
        pass;
               
#%% Source implementations

## Weather       
class Weather(Type, utility.FMU):
    '''Interface for obtaining weather-related Exogenous data from a source.
        
    To standardize data transfer within mpcpy, the returned weather data 
    should be saved into a dictionary with the following format:
    
    {
    'Variable Name' : Timeseries mpcpy.Variable 
    }

    In addition, the weather dictionary should only contain a subset from
    the following Key Name list:
    
    ['weaPAtm', 'weaTDewPoi', 'weaTDryBul', 'weaRelHum', 'weaNOpa', 
     'weaCelHei',  'weaNTot', 'weaWinSpe', 'weaWinDir', 'weaHHorIR', 
     'weaHDirNor', 'weaHGloHor', 'weaHDifHor', 'weaIAveHor', 'weaIDirNor', 
     'weaIDifHor', 'weaZLum', 'weaTBlaSky', 'weaTWetBul', 'weaSolZen', 
     'weaCloTim', 'weaSolTim', 'weaTGnd']
 
    
    'weaTGnd' is an exception to the dictionary format rule due
    to the possibility of different temperatures at multiple depths.  
    Therefore, the dictionary format for 'weaTGnd' is:

    {
    'weaTGnd' : {
        'Depth' : mpcpy.Variable}
    }

    ‘lat’, ‘lon’, and ‘timZon’ are Static variables while the rest are
    Timeseries Variables.

    ‘weaCloTim’, ‘weaSolTim’, ‘lat’, and ‘Direct normal radiation’ 
    can be used as inputs into 
    Buildings.BoundaryConditions.SolarIrradiation.DirectTiltedSurface to 
    find the direct solar radiation incident on a façade of given azimuth
    and tilt.

    '''        

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_weather;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_weather;
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for key in self.data.keys():
            if self.data[key].variability == 'Timeseries':
                self._ts_list.append(self.data[key]);        
           
    def _translate_variable_map(self):
        '''Translate csv column to data variable.'''
        varname = self.variable_map[self._key][0];
        unit = self.variable_map[self._key][1];        
        self.data[varname] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                 start_time=self.start_time, final_time=self.final_time, \
                                                                 cleaning_type = self._cleaning_type, \
                                                                 cleaning_args = self._cleaning_args);
                                                                 
    def _checkCelHei(self):
        '''Check and convert ceiling height data.
        
        See Buildings.BoundaryConditions.WeatherData.ReaderTMY3.
        
        '''
        var = self.data['weaCelHei'];
        ts_in = var.get_base_data();
        M_in = ts_in.get_values();     
        M_out = [];
        for data_point in M_in:
            if data_point > 20000:
                M_out.append(2000);
            else:
                M_out.append(data_point);
        ts_out = pd.Series(data = M_out, index = ts_in.index);
        var.set_display_unit(var.get_base_unit());
        var.set_data(ts_out);
        self.data['weaCelHei'] = var;
        
    def _checkPAtm(self):
        '''Check and convert atmospheric pressure data.
        
        See Buildings.BoundaryConditions.WeatherData.ReaderTMY3.
        
        '''
        var = self.data['weaPAtm'];
        index = var.get_base_data().index;
        M_in = var.get_base_data().get_values();
        M_out = 101325*np.ones(len(M_in));
        ts = pd.Series(data = M_out, index = index, name = 'weaPAtm');
        var.set_display_unit(var.get_base_unit());
        var.set_data(ts);
        self.data['weaPAtm'] = var;
        
    def _checkNOpa(self):
        '''Check and convert opaque sky data.
        
        See Buildings.BoundaryConditions.WeatherData.ReaderTMY3.
        
        '''
        var = self.data['weaNOpa'];
        ts_in = var.get_base_data();
        M_in = ts_in.get_values();     
        M_out = [];
        M_max = 1.0;
        M_min = 0.011;
        for data_point in M_in:
            if data_point > M_max:
                M_out.append(M_max);
            elif data_point < M_min:
                M_out.append(M_min);
            else:
                M_out.append(data_point);
        ts_out = pd.Series(data = M_out, index = ts_in.index);
        var.set_display_unit(var.get_base_unit());
        var.set_data(ts_out);                  
        self.data['weaNOpa'] = var;
        
    def _checkNTot(self):
        '''Check and convert total sky coverage data.
        
        See Buildings.BoundaryConditions.WeatherData.ReaderTMY3.
        
        '''
        var = self.data['weaNTot'];
        ts_in = var.get_base_data();
        M_in = ts_in.get_values();  
        M_out = [];
        M_max = 1.0;
        M_min = 0.011;
        for data_point in M_in:
            if data_point > M_max:
                M_out.append(M_max);
            elif data_point < M_min:
                M_out.append(M_min);
            else:
                M_out.append(data_point);
        ts_out = pd.Series(data = M_out, index = ts_in.index);
        var.set_display_unit(var.get_base_unit());
        var.set_data(ts_out);   
        self.data['weaNTot'] = var;
        
    def _checkRelHum(self):
        '''Check and convert relative humidity data.
        
        See Buildings.BoundaryConditions.WeatherData.ReaderTMY3.
        
        '''
        var = self.data['weaRelHum'];
        ts_in = var.get_base_data();
        M_in = ts_in.get_values();
        M_out = [];
        M_max = 0.989;
        M_min = 0.0;
        for data_point in M_in:
            if data_point > M_max:
                M_out.append(M_max);
            elif data_point < M_min:
                M_out.append(M_min);
            else:
                M_out.append(data_point);
        ts_out = pd.Series(data = M_out, index = ts_in.index);
        var.set_display_unit(var.get_base_unit());
        var.set_data(ts_out); 
        self.data['weaRelHum'] = var;
        
    def _process_weather_data(self):
        '''Use process weather fmu to calculate other necessary weather data.'''
        # Set filepath for fmu
        weatherdir = utility.get_MPCPy_path() + '/resources/weather';
        fmuname = 'WeatherProcessor_JModelica_v2.fmu';
        self._create_fmu({'fmupath': weatherdir+'/'+fmuname});
        # Set parameters for fmu
        self.parameter_data = {};
        self.parameter_data['lat'] = {};
        self.parameter_data['lat']['Value'] = self.lat;
        self.parameter_data['lon'] = {};
        self.parameter_data['lon']['Value'] = self.lon;
        self.parameter_data['timZon'] = {};        
        self.parameter_data['timZon']['Value'] = self.time_zone;
        self.parameter_data['modTimOffset'] = {};   
        self.parameter_data['modTimOffset']['Value'] = variables.Static('modTimeOffest', self.year_start_seconds, units.s);
        for key in self.parameter_data.keys():
            self.parameter_data[key]['Free'] = variables.Static(key+'_free', False, units.boolean);
        # Set measurements for fmu
        self.measurements = {};
        for key in self.process_variables:
            self.measurements[key] = {};
            self.measurements[key]['Sample'] = variables.Static(key+'_Sample', 3600, units.s);
        # Simulate the fmu
        self._simulate_fmu();
        # Add process var data 
        for key in self.process_variables:
            self.data[key] = self.measurements[key]['Simulated'];

    def _create_input_mpcpy_ts_list_sim(self):
        '''Create the input list to the weather processing FMU.'''
        # Set input_object for fmu
        self._input_mpcpy_ts_list = (self.data['weaPAtm'], self.data['weaTDewPoi'], \
                                     self.data['weaTDryBul'], self.data['weaRelHum'], \
                                     self.data['weaNOpa'], self.data['weaCelHei'], \
                                     self.data['weaNTot'], self.data['weaWinSpe'], \
                                     self.data['weaWinDir'], self.data['weaHHorIR'], \
                                     self.data['weaHDirNor'], self.data['weaHGloHor']);        
        
## Internal       
class Internal(Type):
    '''Interface for obtaining internal-related Exogenous data from a source.
    
    An object with an Internal interface must gather internal data.
    
    To standardize data transfer within mpcpy, the returned internal data 
    should be saved into a dictionary with the following format:   
    
    {
    “ZoneName” : {
        “intCon” : Timeseries mpcpy.Variable,
        “intRad” : Timeseries mpcpy.Variable,
        “intLat” : Timeseries mpcpy.Variable           
    }   
        
    '''

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_internal = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_internal;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_internal = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_internal;  
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for zone in self.data.keys():
            for key in self.data[zone].keys():
                if self.data[zone][key].variability == 'Timeseries':
                    self._ts_list.append(self.data[zone][key]);
        
    def _translate_variable_map(self):
        '''Translate csv column to data disctionary.'''
        zone = self.variable_map[self._key][0];
        load = self.variable_map[self._key][1];
        varname = load + '_' + zone;
        unit = self.variable_map[self._key][2];        
        try:
            self.data[zone][load] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                       start_time=self.start_time, final_time=self.final_time, \
                                                                       cleaning_type = self._cleaning_type, \
                                                                       cleaning_args = self._cleaning_args);
        except KeyError:
            self.data[zone] = {};
            self.data[zone][load] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                       start_time=self.start_time, final_time=self.final_time, \
                                                                       cleaning_type = self._cleaning_type, \
                                                                       cleaning_args = self._cleaning_args);        
        
              
## Controls       
class Control(Type):
    '''Interface for obtaining control-related Exogenous data from a source.
    
    An object with an ControlType interface must gather control data.
    
    To standardize data transfer within mpcpy, the returned control data 
    should be saved into a dictionary with the following format:   
    
    {
    “ControlName” : Timeseries mpcpy.Variable          
    }   
    
    '''

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_weather;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_weather;
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for key in self.data.keys():
            if self.data[key].variability == 'Timeseries':
                self._ts_list.append(self.data[key]);        
           
    def _translate_variable_map(self):
        '''Translate csv column to data dictionary.'''
        varname = self.variable_map[self._key][0];
        unit = self.variable_map[self._key][1];        
        self.data[varname] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                 start_time=self.start_time, final_time=self.final_time, \
                                                                 cleaning_type = self._cleaning_type, \
                                                                 cleaning_args = self._cleaning_args);   
                                                                 
## Other_Inputs       
class OtherInput(Type):
    '''Interface for obtaining other input-related Exogenous data from a source.

    An object with an OtherInputType interface must gather other input data.
    
    To standardize data transfer within mpcpy, the returned other input data 
    should be saved into a dictionary with the following format:   
    
    {
    “OtherInputName” : Timeseries mpcpy.Variable          
    }   
    
    '''

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_weather;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_weather;
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for key in self.data.keys():
            if self.data[key].variability == 'Timeseries':
                self._ts_list.append(self.data[key]);        
           
    def _translate_variable_map(self):
        '''Translate csv column to data dictionary.'''
        varname = self.variable_map[self._key][0];
        unit = self.variable_map[self._key][1];        
        self.data[varname] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                 start_time=self.start_time, final_time=self.final_time, \
                                                                 cleaning_type = self._cleaning_type, \
                                                                 cleaning_args = self._cleaning_args);
                                                                 
## Parameters       
class Parameter(Type):
    '''Interface for obtaining coefficient-related Exogenous data from a source.    

    An object with an CoefficientType interface must gather coefficient data.
    
    To standardize data transfer within mpcpy, the returned coefficient data 
    should be saved into a dictionary with the following format:   
    
    {
    “ParameterName” : {
        "Free" : Static mpcpy.Variable,            
        "Value" : Static mpcpy.Variable,
        "Minimum" : Static mpcpy.Variable,
        “Maximum” : Static mpcpy.Variable,
        "Covariance" : Static mpcpy.Variable
    }   
        
    '''
        
    def display_data(self):
        '''Display data as pandas dataframe.'''
        d = {};
        for key in self.data.keys():
            d[key] = {};
            for subkey in self.data[key].keys():
                d[key][subkey] = self.data[key][subkey].display_data();
                if subkey == 'Value':
                    d[key]['Unit'] = self.data[key][subkey].get_display_unit_name();
        df_coefficients = pd.DataFrame(data = d).transpose();
        df_coefficients.index.name = 'Name';
        return df_coefficients;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        d = {};
        for key in self.data.keys():
            d[key] = {};
            for subkey in self.data[key].keys():
                d[key][subkey] = self.data[key][subkey].get_base_data();
        df_coefficients = pd.DataFrame(data = d);
        return df_coefficients;    
        
## Constraints       
class Constraint(Type):
    '''Interface for obtaining constraint-related Exogenous data from a source.

    An object with an ConstraintType interface must gather constraint data.
    
    To standardize data transfer within mpcpy, the returned constraint data 
    should be saved into a dictionary with the following format:   
    
    {
    “StateName” : {
        "LTE" : Timeseries mpcpy.Variable,
        "GTE" : Timeseries mpcpy.Variable,
        "E" : Timeseries mpcpy.Variable,
        "Initial" : Static mpcpy.Variable,
        "Final" : Static mpcpy.Variable,
        "Cyclic" : Static mpcpy.Variable,             
    }   
    
        '''

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_internal = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_internal;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_internal = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_internal;  
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for state in self.data.keys():
            for key in self.data[state].keys():
                if self.data[state][key].variability == 'Timeseries':
                    self._ts_list.append(self.data[state][key]);
        
    def _translate_variable_map(self):
        '''Translate csv column to data dictionary.'''
        state = self.variable_map[self._key][0];
        key = self.variable_map[self._key][1];
        varname = state + '_' + key;
        unit = self.variable_map[self._key][2];        
        try:
            self.data[state][key] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                       start_time=self.start_time, final_time=self.final_time, \
                                                                       cleaning_type = self._cleaning_type, \
                                                                       cleaning_args = self._cleaning_args);
        except KeyError:
            self.data[state] = {};
            self.data[state][key] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                       start_time=self.start_time, final_time=self.final_time, \
                                                                       cleaning_type = self._cleaning_type, \
                                                                       cleaning_args = self._cleaning_args);        
        
 
## Prices       
class Price(Type):
    '''Interface for obtaining price-related Exogenous data from a source.

    An object with an PriceType interface must gather price data.
    
    To standardize data transfer within mpcpy, the returned control data 
    should be saved into a dictionary with the following format:   
    
    {
    “PriceName” : Timeseries mpcpy.Variable          
    }   
    
    '''

    def display_data(self):
        '''Display data as pandas dataframe.'''
        self._make_mpcpy_ts_list();
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = True);
        return df_weather;
        
    def get_base_data(self):
        '''Get base data as pandas dataframe.'''
        self._make_mpcpy_ts_list();        
        df_weather = self.mpcpy_ts_list_to_dataframe(self._ts_list, display_data = False);
        return df_weather;
        
    def _make_mpcpy_ts_list(self):
        '''Make a list of timeseries from a data dictionary.'''
        self._ts_list = [];
        for key in self.data.keys():
            if self.data[key].variability == 'Timeseries':
                self._ts_list.append(self.data[key]);        
           
    def _translate_variable_map(self):
        '''Translate csv column to data dictionary.'''
        varname = self.variable_map[self._key][0];
        unit = self.variable_map[self._key][1];        
        self.data[varname] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                 start_time=self.start_time, final_time=self.final_time, \
                                                                 cleaning_type = self._cleaning_type, \
                                                                 cleaning_args = self._cleaning_args);        
   
#%% Weather source implementations    
class WeatherFromEPW(Weather):
    ''' A weather source interface for an epw file data source.'''
    def __init__(self, epw_filepath):
        ''' Constructor of epw weather source.'''
        self.name = 'weather_from_epw';
        self.location = epw_filepath;
        self._read_lat_lon_timZon_from_epw();
        self.tz = tzwhere.tzwhere();
        self.tz_name = self.tz.tzNameAt(self.lat.display_data(), self.lon.display_data());        
        self.data = {};
        self.process_variables = ['weaTBlaSky', \
                                  'weaTWetBul', \
                                  'weaHDifHor', \
                                  'weaCloTim', \
                                  'weaSolTim', \
                                  'weaSolZen'];         

    def collect_data(self, start_time, final_time):
        '''Gather data from epw file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk timeseries weather data
        self._read_timeseries_from_epw();
        # Process weather data
        self._process_weather_data();
        
        return self.data
        
    def _read_lat_lon_timZon_from_epw(self):
        '''Get Latitude, Longitude, and Time Zone from EPW.'''
        df_epw = pd.read_csv(self.location, nrows = 1, header = None, usecols = [6,7,8], names = ['Latitude', 'Longitude', 'TimeZone']);
        self.lat = variables.Static('lat', df_epw.loc[0,'Latitude'], units.deg);
        self.lon = variables.Static('lon', df_epw.loc[0,'Longitude'], units.deg); 
        self.time_zone = variables.Static('timZon', df_epw.loc[0,'TimeZone'], units.hour);
        
    def _read_timeseries_from_epw(self):
        '''Get timeseries data from EPW.'''
        # Define column headers to read in from epw
        header = ['Year', 'Month', 'Day', 'Hour', 'Second', 'Unknown', \
                  'Dry bulb temperature', 'Dew point temperature', \
                  'Relative humidity', 'Atmospheric station pressure', \
                  'Extraterrestrial horizontal radiation', 'Extraterrestrial direct normal radiation', \
                  'Horizontal infrared radiation', 'Global horizontal radiation', \
                  'Direct normal radiation', 'Diffuse horizontal radiation', \
                  'Averaged global horizontal illuminance', 'Direct normal illuminance', \
                  'Diffuse horizontal illuminance', 'Zenith luminance', \
                  'Wind direction', 'Wind speed', \
                  'Total sky cover', 'Opaque sky cover', \
                  'Visibility', 'Ceiling', \
                  'Present weather observation', 'Present weather codes', \
                  'Precipitable water', 'Aerosol optical depth', \
                  'Snow depth', 'Days since last snowfall', \
                  'Albedo', 'Liquid precipitation depth', \
                  'Liquid precipitation quantity'];
        # Read in data
        df_epw = pd.read_csv(self.location, skiprows = 8, header = None, names=header);
        # Convert time columns to timestamp and set as index                           
        df_epw['Hour'] = df_epw['Hour'] - 1;
        
        df_epw['Time'] = str(self.start_time.year) + ' ' + df_epw['Month'].apply(str) + ' ' + df_epw['Day'].apply(str) + ' ' + df_epw['Hour'].apply(str) + ':00';
        time = pd.to_datetime(df_epw['Time'], format= '%Y %m %d %H:%M');
        df_epw.set_index(time, inplace=True);
        # Remove unneeded columns
        df_epw = df_epw.drop(['Time', 'Year', 'Month', 'Day', 'Hour', 'Second', 'Unknown'], axis = 1);
        #  Perform data swap for epw (see Buildings.BoundaryConditions.WeatherData.ReaderTMY3 info)  
        df_epw_last_row = df_epw.head(1);
        df_epw = df_epw_last_row.append(df_epw.iloc[:-1], ignore_index=False);
        new_index = df_epw.index[0:1].append(df_epw.index[1:] + pd.DateOffset(hours=1));
        df_epw.set_index(new_index, inplace=True);
        # Treat daylight savings time
        try:
            df_epw = df_epw.tz_localize(self.tz_name);
        except pytz_exceptions.NonExistentTimeError as time_nonexist:
            time_nonexist = pd.to_datetime(time_nonexist.args[0])
            if time_nonexist.month == 3:
                df_epw_st = df_epw[df_epw.index < time_nonexist];
                df_epw_dst = df_epw[df_epw.index >= time_nonexist];
                df_epw_dst = df_epw_dst.shift(periods = 1, freq = 'H');
                df_epw = pd.concat([df_epw_st, df_epw_dst], axis = 0);
        try:
            df_epw = df_epw.tz_localize(self.tz_name);
        except pytz_exceptions.AmbiguousTimeError as time_ambiguous:
            time_ambiguous = pd.to_datetime(time_ambiguous.args[0].split("'")[1])
            if time_ambiguous.month == 11:
                df_epw_dst = df_epw[df_epw.index < time_ambiguous].tz_localize(self.tz_name);
                df_epw_st = df_epw[(df_epw.index > time_ambiguous + relativedelta(hours = 1))].shift(periods = -1, freq = 'H').tz_localize(self.tz_name);
                df_epw_amb = df_epw[(df_epw.index >= time_ambiguous) & (df_epw.index <= time_ambiguous + relativedelta(hours = 1))];
                df_epw_amb_0 = df_epw_amb.iloc[0:1].tz_localize(self.tz_name, ambiguous = np.array([True]));
                df_epw_amb_1 = df_epw_amb.iloc[1:2].shift(periods = -1, freq = 'H').tz_localize(self.tz_name, ambiguous = np.array([False]));
                df_epw = pd.concat([df_epw_dst, df_epw_amb_0, df_epw_amb_1, df_epw_st], axis = 0);
        #  Retrieve data (not all is retrieved)
        for key in header:
            # Convert to mpcpy standard
            if key == 'Atmospheric station pressure':
                varname = 'weaPAtm';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.Pa, start_time = self.start_time, final_time = self.final_time);
                self._checkPAtm();
            elif key == 'Dew point temperature':
                varname = 'weaTDewPoi';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.degC, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Dry bulb temperature':
                varname = 'weaTDryBul';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.degC, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Relative humidity':
                varname = 'weaRelHum';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.percent, start_time = self.start_time, final_time = self.final_time);                
                self._checkRelHum();
            elif key == 'Opaque sky cover':
                varname = 'weaNOpa';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.unit10, start_time = self.start_time, final_time = self.final_time);                
                self._checkNOpa();
            elif key == 'Ceiling':
                varname = 'weaCelHei';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.m, start_time = self.start_time, final_time = self.final_time);                
                self._checkCelHei();
            elif key == 'Total sky cover':
                varname = 'weaNTot';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.unit10, start_time = self.start_time, final_time = self.final_time);                 
                self._checkNTot();
            elif key == 'Wind speed':
                varname = 'weaWinSpe';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.m_s, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Wind direction':
                varname = 'weaWinDir';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.deg, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Horizontal infrared radiation':
                varname = 'weaHHorIR';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.W_m2, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Direct normal radiation':
                varname = 'weaHDirNor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.W_m2, start_time = self.start_time, final_time = self.final_time); 
            elif key == 'Global horizontal radiation':
                varname = 'weaHGloHor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.W_m2, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Diffuse horizontal radiation':
                varname = 'weaHDifHor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.W_m2, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Averaged global horizontal illuminance':
                varname = 'weaIAveHor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.lx, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Direct normal illuminance':
                varname = 'weaIDirNor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.lx, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Diffuse horizontal illuminance':
                varname = 'weaIDifHor';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.lx, start_time = self.start_time, final_time = self.final_time);
            elif key == 'Zenith luminance':
                varname = 'weaZLum';
                self.data[varname] = self.dataframe_to_mpcpy_ts_variable(df_epw, key, varname, units.cd_m2, start_time = self.start_time, final_time = self.final_time);          
        # Time shift the solar data back 30 minutes by linear interpolation (see Buildings.BoundaryConditions.WeatherData.ReaderTMY3 info)
        for key in self.data.keys():
            if key in ['weaHHorIR', 'weaHGloHor', 'weaHDirNor', 'weaHDifHor', \
                     'weaIAveHor', 'weaIDirNor', 'weaIDifHor', 'weaZLum']:
                ts_old = self.data[key].display_data();
                ts = ts_old.resample('30T').interpolate(method='time');
                ts = ts.shift(freq = '-30T');
                ts = ts.resample(rule='H', how = 'first');
                ts = ts.ix[1:].append(ts_old.tail(n=1));
                self.data[key].set_data(ts);
                     
class WeatherFromCSV(Weather, utility.DAQ):
    '''A weather source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv weather source.'''
        self.name = 'weather_from_csv';
        self.location = csv_filepath;  
        self.data = {};   
        # Dictionary of format {'csvHeader' : ('weaVarName', mpcpyUnit)}
        self.variable_map = variable_map;          
        # Process Variables
        if 'process_variables' in kwargs:
            self.process_variables = kwargs['process_variables'];
        else:
            self.process_variables = None;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        # Assert geography
        assert(bool(self.lat) == True);
        assert(bool(self.lon) == True);
           
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();
        # Process weather data
        if self.process_variables is not None:
            self._process_weather_data();   
                                             
#%% Internal source implementations
class InternalFromCSV(Internal, utility.DAQ):
    '''An internal source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv internal source.'''
        self.name = 'internal_from_csv';
        self.location = csv_filepath;
        self.data = {};   
        # Dictionary of format {'csvHeader' : ('zone', 'RadConLatOcc', mpcpyUnit)}
        self.variable_map = variable_map;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
                   
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();
        
class InternalFromOccupancyModel(Internal):
    '''An internal source interface for occupancy model data source.'''
    def __init__(self, zone_list, load_list, unit, occupancy_model_list, **kwargs):
        '''Constructor of occupancy model internal source.'''
        self.name = 'internal_from_occupancymodel';
        self.zone_list = zone_list;
        self.load_list = load_list;
        self.unit = unit;        
        self.occupancy_model_list = occupancy_model_list;
        self.data = {};
        # Common kwargs    
        self._parse_time_zone_kwargs(kwargs);
        
    def collect_data(self, start_time, final_time):
        '''Use data from the occupancy model to create data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series
        for zone, loads, occupancy_model in zip(self.zone_list, self.load_list, self.occupancy_model_list):
            self.data[zone] = {};
            for varname, load in zip(['intCon', 'intRad', 'intLat'], loads):
                ts = occupancy_model.generate_load(load);
                self.data[zone][varname] = variables.Timeseries(varname+'_'+zone, ts[self.start_time:self.final_time], self.unit);

class InternalFromTable(Internal):
    ''' An internal source interface for a table file data source.'''       
    def __init__(self, table_filepath):
        ''' Constructor of a table file internal data source.'''   
        self.name = 'internal_from_table';
        self.location = table_filepath;
        self.internalkeys = ['intCon', 'intRad', 'intLat'];
        self.data = {};
    def get_internal_data(self, final_time, sample_time):
        ''' Read internal data from table file into internal index.'''        
        table_filepath = self.location;
        zones = self.zone_names;
        internalkeys = self.internalkeys;
        internal = {};
        
        # Create each zone key
        for zone in zones:
            internal[zone] = {};  
        
        # Get data for each internal load type
        for key in internalkeys:
            # For each zone
            for zone in zones:
                # Read the table
                with open(table_filepath, 'r') as table:
                    mark = [];
                    load = [];
                    startline = 0;
                    for line in table:
                        # In correct section
                        if startline == 1:
                            # End table reading if hit next table
                            if 'double' in line:
                                break
                            else:
                                # Mark the timestamp
                                mark.append(float(line.split(',')[0]));
                                # Read the line value
                                if line.split(',')[1].endswith('\n'):
                                    load.append(float(line.split(',')[1][:-1]));
                                else:
                                    load.append(float(line.split(',')[1]));  
                        # Find correct section for particular zone                           
                        if key + '_' + zone in line and startline == 0:
                            startline = 1;
                    if startline == 1:
                        timeseries = [];
                        dataseries = [];
                        for i in range(len(mark))[1:]:
                              if mark[i] != mark[i-1]:
                                # Create load timeseries
                                timeseries = np.hstack((timeseries, np.arange(mark[i-1],mark[i],sample_time)));
                                dataseries = np.hstack((dataseries, load[i]*np.ones((mark[i] - mark[i-1])/sample_time)));
                        # Periodicity
                        if final_time > mark[-1]:
                            difference = final_time - mark[-1];
                            multiple = int(difference/mark[-1]);
                            remainder = np.mod(difference, mark[-1]);
                            # Multiples
                            if multiple > 0:
                                final = len(dataseries);
                                for m in range(multiple+1)[1:]:
                                    timeseries = np.hstack((timeseries, np.arange(timeseries[-1]+sample_time, mark[-1]*(m+1), sample_time)));
                                    dataseries = np.hstack((dataseries, dataseries[0:final]));
                            # Remainder
                            timeseries = np.hstack((timeseries, np.arange(timeseries[-1]+sample_time, timeseries[-1]+sample_time+remainder, sample_time)));
                            dataseries = np.hstack((dataseries, dataseries[0:np.where(timeseries==remainder)[0][0]]));
                        # Under-length (Remainder only)                        
                        elif final_time < mark[-1]:
                            remainder = final_time;
                            timeseries = np.arange(0, remainder, sample_time);
                            dataseries = dataseries[0:remainder/sample_time]; 
                            
                        # Add to dictionary
                        internal[zone][key] = variables.Timeseries(key+'_'+zone, dataseries, units.W_m2, timeseries);
                    
        return internal
        
#%% Control source implementations        
class ControlFromCSV(Control, utility.DAQ):
    '''A control source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv control source.'''
        self.name = 'control_from_csv';
        self.location = csv_filepath;
        self.data = {};   
        # Dictionary of format {'csvHeader' : ('conVarName', mpcpyUnit)}
        self.variable_map = variable_map;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);             
                   
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();
        
#%% Other input source implementations        
class OtherInputFromCSV(OtherInput, utility.DAQ):
    '''An other input source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv other input source.'''
        self.name = 'otherinput_from_csv';
        self.location = csv_filepath;
        self.data = {};   
        # Dictionary of format {'csvHeader' : ('otherinputVarName', mpcpyUnit)}
        self.variable_map = variable_map;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);             
                   
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();        
        
#%% Parameter source implementations 
class ParameterFromCSV(Parameter, utility.DAQ):
    '''A parameter source interface for csv file data source.'''
    def __init__(self, csv_filepath):
        ''' Constructor of csv parameter source.'''
        self.name = 'parameter_from_csv';
        self.location = csv_filepath;
        self.data = {};
    def collect_data(self):
        '''Gather data from the csv file into data dictionary.'''
        # Read coefficients file
        df = pd.read_csv(self.location, index_col='Name', dtype={'Unit':str});
        # Create coefficient dictionary
        for key in df.index.values:
            self.data[key] = {};
            unit = utility.get_unit_class_from_unit_string(df.loc[key, 'Unit']);
            if df.loc[key, 'Free']:  
                self.data[key]['Free'] = variables.Static(key+'_free', True, units.boolean);
                self.data[key]['Value'] = variables.Static(key+'_val', df.loc[key, 'Value'], unit);
                self.data[key]['Minimum'] = variables.Static(key+'_min', df.loc[key, 'Minimum'], unit);
                self.data[key]['Maximum'] = variables.Static(key+'_max', df.loc[key, 'Maximum'], unit);
                self.data[key]['Covariance'] = variables.Static(key+'_cov', df.loc[key, 'Covariance'], unit);
            else: 
                self.data[key]['Free'] = variables.Static(key+'_free', False, units.boolean);
                self.data[key]['Value'] = variables.Static(key+'_val', df.loc[key, 'Value'], unit);              
            
#%% Constraint source implementations
class ConstraintFromCSV(Constraint, utility.DAQ):
    '''A constraint source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv constraint source.'''
        self.name = 'constraint_from_csv';
        self.location = csv_filepath;
        self.data = {};   
        # Dictionary of format {'csvHeader' : (stateVarName, 'key', mpcpyUnit)}
        self.variable_map = variable_map;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
            
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();
        
class ConstraintFromOccupancyModel(Constraint):
    '''A constraint source interface for occupancy model data source.'''
    def __init__(self, state_variable_list, values_list, constraint_type_list, unit_list, occupancy_model, **kwargs):
        '''Constructor of occupancy model constraint source.'''
        self.name = 'constraint_from_occupancymodel';
        self.state_variable_list = state_variable_list;
        self.values_list = values_list;
        self.constraint_type_list = constraint_type_list;
        self.unit_list = unit_list;
        self.occupancy_model = occupancy_model;
        self.data = {};        
        # Common kwargs
        self._parse_time_zone_kwargs(kwargs);
        
    def collect_data(self, start_time, final_time):
        '''Use data from the occupancy model to create data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series
        for state_variable, values, constraint_type, unit in zip(self.state_variable_list, self.values_list, self.constraint_type_list, self.unit_list):
            if state_variable not in self.data:
                self.data[state_variable] = {};
            ts = self.occupancy_model.generate_constraint(values[0], values[1]);
            self.data[state_variable][constraint_type] = variables.Timeseries(state_variable+'_'+constraint_type, ts[self.start_time:self.final_time], unit);

#%% Price source implementations
class PriceFromCSV(Price, utility.DAQ):
    '''A price source interface for csv file data source.'''
    def __init__(self, csv_filepath, variable_map, **kwargs):
        ''' Constructor of csv internal source.'''
        self.name = 'constraint_from_csv';
        self.location = csv_filepath;
        self.data = {};   
        # Dictionary of format {'csvHeader' : (priceVarName, 'key', mpcpyUnit)}
        self.variable_map = variable_map;
        # Common kwargs
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
            
    def collect_data(self, start_time, final_time):
        '''Gather data from the csv file into data dictionary.'''
        # Set time interval
        self._set_time_interval(start_time, final_time);
        # Get bulk time series        
        self._read_timeseries_from_csv();                
        
        