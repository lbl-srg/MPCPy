# -*- coding: utf-8 -*-
"""
variables.py
by David Blum

This module contains the classes and interfaces for the variables of mpcpy.

"""

from abc import ABCMeta, abstractmethod
from tzwhere import tzwhere
import numpy as np

#%% Variable abstract class
class Variable(object):
    '''Abstract class for mpcpy variables.'''
    __metaclass__ = ABCMeta;
    
    @abstractmethod
    def set_data(self,data):
        pass;   
        
    def get_base_data(self):
        '''Get the variable data in base units.'''
        return self.data;
        
    def display_data(self, **kwargs):
        '''Get the variable data in display units.'''
        if type(self.data) is list:
            self._timeseries = [self.display_unit.convert_from_base(x) for x in self.data];
        else:
            self._timeseries = self.display_unit.convert_from_base(self.data);        
        if 'geography' in kwargs:
            self._load_time_zone(kwargs['geography']);
            self._timeseries = self._utc_to_local(self._timeseries);
        elif 'tz_name' in kwargs:
            self.tz_name = kwargs['tz_name'];
            self._timeseries = self._utc_to_local(self._timeseries);
        return self._timeseries;
        
    def set_display_unit(self, display_unit):
        '''Set the variable display units.'''
        quantity_old = self.quantity_name;
        self.display_unit = display_unit(self);
        if quantity_old != self.quantity_name:
            raise(AssertionError, 'Display unit to be set has a different quantity than the existing variable display unit.');   
            
    def get_base_unit(self):
        '''Get the variable base unit class.'''
        return self.base_unit;  
        
    def get_display_unit(self):
        '''Get the variable display unit class.'''
        return type(self.display_unit);
        
    def get_display_unit_name(self):
        '''Get the variable display unit name string.'''
        return self.display_unit.name;
        
    def get_base_unit_name(self):
        '''Get the variable base unit name string.'''
        display_unit = self.get_base_unit();
        self.set_display_unit(self.get_base_unit());
        base_unit_name = self.get_display_unit_name();
        self.set_display_unit(display_unit);
        return base_unit_name;
        
    def __str__(self):
        '''Print the information for the variable.'''
        string = 'Name: ' + self.name + '\n';
        string += 'Variability: ' + self.variability + '\n';
        string += 'Quantity: ' + self.quantity_name + '\n';       
        string += 'Display Unit: ' + self.display_unit.name + '\n';
        return string
        
    def __add__(self,variable):
        '''Add two variables.'''
        variable_out = self._perform_operation(variable, 'add');
        return variable_out;
        
    def __sub__(self,variable):
        '''Subtract two variables.'''
        variable_out = self._perform_operation(variable, 'sub');
        return variable_out;        
        
    def _perform_operation(self, variable, operation):
        '''Perform the indicated math operation on the variables.'''
        if self.display_unit.name == variable.display_unit.name:        
            data1 = self.display_data();
            data2 = variable.display_data();
            if operation == 'add':
                data3 = data1 + data2;
            elif operation == 'sub':
                data3 = data1 - data2;              
            if self.variability == 'Timeseries' or variable.variability == 'Timeseries':  
                variable_out = Timeseries(self.name+variable.name, data3, self.get_display_unit());
            else:
                variable_out = Static(self.name+variable.name, data3, self.get_display_unit());        
            return variable_out
        else:
            print('Display units {} and {} are not the same.  Cannot perform operation.'.format(self.display_unit.name, variable.display_unit.name));
            return None
            
    def _local_to_utc(self, df_local):
        '''Convert a pandas array in local time to utc time.'''
        try:
            df_local = df_local.tz_localize(self.tz_name);
            df_utc = df_local.tz_convert('UTC');
        except TypeError:
            df_utc = df_local.tz_convert('UTC');
        return df_utc;
        
    def _utc_to_local(self, df_utc):
        '''Convert a pandas array in utc time to local time.'''
        df_local = df_utc.tz_convert(self.tz_name);
        return df_local;        
        
    def _load_time_zone(self, geography):
        '''Load the time zone from geography.'''
        try:
            self.tz_name = self.tz.tzNameAt(geography[0], geography[1]);
        except AttributeError:
            self.tz = tzwhere.tzwhere();
            self.tz_name = self.tz.tzNameAt(geography[0], geography[1]);               

#%% Variable implementations
class Static(Variable):
    '''Variable class for time-invariant data.'''
    def __init__(self, name, data, display_unit):
        '''Constructor of the static variable class.'''
        self.name = name;
        self.variability = 'Static';
        self.display_unit = display_unit(self);
        self.set_data(data);
        
    def set_data(self, data):
        '''Set the data for the variable.'''
        if type(data) is float:
            self.data = self.display_unit.convert_to_base(float(data));
        elif type(data) is int: 
            self.data = self.display_unit.convert_to_base(float(data));
        elif type(data) is list:
            self.data = [self.display_unit.convert_to_base(float(x)) for x in data];
        elif isinstance(data, np.ndarray):
            self.data = np.array([self.display_unit.convert_to_base(float(x)) for x in data]);
        else:
            self.data = self.display_unit.convert_to_base(data);
        
class Timeseries(Variable):
    '''Variable class for timeseries data.'''
    def __init__(self, name, timeseries, display_unit, tz_name = 'UTC', **kwargs):
        '''Constructor of the timeseries variable class.'''
        self.variability = 'Timeseries';
        self.display_unit = display_unit(self);
        self.set_data(timeseries, tz_name, **kwargs);
        self.name = name;        
        
    def set_data(self, timeseries, tz_name = 'UTC', **kwargs):
        '''Set the data for the variable.'''
        self._timeseries = timeseries;       
        if 'cleaning_type' in kwargs and kwargs['cleaning_type'] is not None:       
            cleaning_type = kwargs['cleaning_type'];
            cleaning_args = kwargs['cleaning_args'];            
            self._timeseries = cleaning_type(self, cleaning_args)
        if 'geography' in kwargs:
            self._load_time_zone(kwargs['geography']);
            self._timeseries = self._local_to_utc(self._timeseries);
        else:
            self.tz_name = tz_name;
            self._timeseries = self._local_to_utc(self._timeseries);
        self.data = self.display_unit.convert_to_base(self._timeseries.apply(float));
    def cleaning_replace(self, (to_replace, replace_with)):
        '''Clean the data by replacement.'''
        timeseries = self._timeseries.replace(to_replace,replace_with);
        return timeseries           