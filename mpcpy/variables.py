# -*- coding: utf-8 -*-
"""
``variables`` classes together with ``units`` classes form the fundamental 
building blocks of data management in MPCPy.  They provide functionality for 
assigning and converting between units as well as processing timeseries data.  

Generally speaking, variables in MPCPy contain three components:

    name

        A descriptor of the variable.

    data

        Single value or a timeseries.

    unit

        Assigned to variables and act on the data depending on the requested 
        functionality, such as converting between between units or extracting 
        the data.

A unit assigned to a variable is called the display unit and is associated 
with a quantity.  For each quantity, there is a predefined base unit.  The 
data entered into a variable with a display unit is automatically converted 
to and stored as the quantity base unit.  This way, if the display unit were 
to be changed, the data only needs to be converted to the new unit upon 
extraction.  For example, the unit Degrees Celsius is of the quantity 
temperature, for which the base unit is Kelvin.  Therefore, data entered with 
a display unit of Degrees Celsius would be converted to and stored in Kelvin.  
If the display unit were to be changed to Degrees Fahrenheit, then the data 
would be converted from Kelvin upon extraction.


Classes
=======

.. autoclass:: mpcpy.variables.Static
    :members: set_data, display_data, get_base_data, get_display_unit,
              get_base_unit, set_display_unit, get_display_unit_name, 
              get_base_unit_name

.. autoclass:: mpcpy.variables.Timeseries
    :members: set_data, display_data, get_base_data, get_display_unit, 
              get_base_unit, set_display_unit, get_display_unit_name, 
              get_base_unit_name, cleaning_replace

"""

from abc import ABCMeta, abstractmethod
from tzwhere import tzwhere
import numpy as np
import os

#%% Variable abstract class
class _Variable(object):
    '''Base class for variables.
    
    '''

    __metaclass__ = ABCMeta;
    
    @abstractmethod
    def set_data(self,data):
        '''Set the data of the variable including any conversions to be 
        performed.
        
        '''
        
        pass;   
        
    def get_base_data(self):
        '''Return the data of the variable in base units.

        Returns
        -------
        data : data object
            Data object of the variable in base units.

        '''

        return self.data;
        
    def display_data(self, **kwargs):
        '''Return the data of the variable in display units.
        
        Parameters
        ----------
        geography : list, optional
            Latitude [0] and longitude [1] in degrees.  Will return timeseries
            index in specified timezone.
        tz_name : string, optional
            Time zone name according to ``tzwhere`` package.  Will return timeseries index in specified 
            timezone.
            
        Returns
        -------
        data : data object
            Data object of the variable in display units.
            
        '''
        if type(self.data) is list:
            self._timeseries = [self.display_unit._convert_from_base(x) for x in self.data];
        else:
            self._timeseries = self.display_unit._convert_from_base(self.data);        
        if 'geography' in kwargs:
            self._load_time_zone(kwargs['geography']);
            self._timeseries = self._utc_to_local(self._timeseries);
        elif 'tz_name' in kwargs:
            self.tz_name = kwargs['tz_name'];
            self._timeseries = self._utc_to_local(self._timeseries);
            
        return self._timeseries;
        
    def set_display_unit(self, display_unit):
        '''Set the display unit of the variable.
        
        Parameters
        ----------        
        display_unit : mpcpy.units.unit
            Display unit to set.   

        '''
        
        quantity_old = self.quantity_name;
        self.display_unit = display_unit(self);
        if quantity_old != self.quantity_name:
            raise(AssertionError, 'Display unit to be set has a different quantity than the existing variable display unit.');   
            
    def get_base_unit(self):
        '''Returns the base unit of the variable.

        Returns
        -------
        base_unit : mpcpy.units.unit
            Base unit of variable.

        '''

        return self.base_unit;  
        
    def get_display_unit(self):
        '''Returns the display unit of the variable.

        Returns
        -------
        display_unit : mpcpy.units.unit
            Display unit of variable.

        '''

        return type(self.display_unit);
        
    def get_display_unit_name(self):
        '''Returns the display unit name of the variable.

        Returns
        -------
        display_unit_name : string
            Display unit name of variable.

        '''

        return self.display_unit.name;
        
    def get_base_unit_name(self):
        '''Returns the base unit name of the variable.

        Returns
        -------
        base_unit_name : string
            Base unit name of variable.

        '''

        display_unit = self.get_base_unit();
        self.set_display_unit(self.get_base_unit());
        base_unit_name = self.get_display_unit_name();
        self.set_display_unit(display_unit);

        return base_unit_name;        
        
    def __str__(self):
        '''Returns variable name, variability, unit quantity, and display unit name.

        Returns
        -------
        string : string
            String of variable information.

        '''
        
        string = 'Name: ' + self.name + '\n';
        string += 'Variability: ' + self.variability + '\n';
        string += 'Quantity: ' + self.quantity_name + '\n';       
        string += 'Display Unit: ' + self.display_unit.name + '\n';
        
        return string
        
    def __add__(self,variable):
        '''Returns resulting variable of addition of other variables to self variable.

        Parameters
        ----------
        variable : Static or Timeseries
            Other variable with which to perform requested operation.

        Returns
        -------
        variable_out : Static or Timeseries
            Resulting variable from addition of two other variables.

        '''

        variable_out = self._perform_operation(variable, 'add');
        
        return variable_out;
        
    def __sub__(self,variable):
        '''Returns resulting variable of subtraction of other variable from self variable.

        Parameters
        ----------
        variable : Static or Timeseries
            Other variable with which to perform requested operation.

        Returns
        -------
        variable_out : Static or Timeseries
            Resulting variable from subtraction of two other variables.

        '''
        
        variable_out = self._perform_operation(variable, 'sub');
        
        return variable_out;        
        
    def _perform_operation(self, variable, operation):
        '''Perform operation of addition or subtraction.
        
        Parameters
        ----------
        variable : Static or Timeseries
            Other variable with which to perform requested operation.
        operation : string
            Request addition ('add') or subtraction ('sub').
            
        Returns
        -------
        variable_out : Static or Timeseries
            Resulting variable from operation.

        '''
        
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
        '''Convert a pandas timeseries in local time to utc time.
        
        '''

        try:
            df_local = df_local.tz_localize(self.tz_name);
            df_utc = df_local.tz_convert('UTC');
        except TypeError:
            df_utc = df_local.tz_convert('UTC');
        
        return df_utc;
        
    def _utc_to_local(self, df_utc):
        '''Convert a pandas timeseries in utc time to local time.
        
        '''

        df_local = df_utc.tz_convert(self.tz_name);
        
        return df_local;        
        
    def _load_time_zone(self, geography):
        '''Load the time zone name from geography.

        Parameters
        ----------
        geography : list
            List specifying [latitude, longitude] in degrees.

        Yields
        ------
        tz_name : string
            Timezone attribute named according to ``tzwhere`` package.

        '''

        try:
            self.tz_name = self.tz.tzNameAt(geography[0], geography[1]);
        except AttributeError:
            self.tz = tzwhere.tzwhere();
            self.tz_name = self.tz.tzNameAt(geography[0], geography[1]);               

#%% Variable implementations
class Static(_Variable):
    '''Variable class with data that is not a timeseries.
    
    Parameters
    ----------
    name : string
        Name of variable.
    data : float, int, bool, list, ``numpy`` array
        Data of variable
    display_unit : mpcpy.units.unit
        Unit of variable data being set.
        
    Attributes
    ----------
    name : string
        Name of variable.
    data : float, int, bool, list, ``numpy`` array
        Data of variable
    display_unit : mpcpy.units.unit
        Unit of variable data when returned with ``display_data()``.
    quantity_name : string
        Quantity type of the variable (e.g. Temperature, Power, etc.).        
    variability : string
        Static.

    '''
    
    def __init__(self, name, data, display_unit):
        '''Constructor of the Static variable object.
        
        '''
        
        self.name = name;
        self.variability = 'Static';
        self.display_unit = display_unit(self);
        self.set_data(data);
        
    def set_data(self, data):
        '''Set data of Static variable.
        
        Parameters
        ----------
        data : float, int, bool, list, ``numpy`` array
            Data to be set for variable.

        Yields
        ----------
        data : float, int, bool, list, ``numpy`` array
            Data attribute.            

        '''
        
        if type(data) is float:
            self.data = self.display_unit._convert_to_base(float(data));
        elif type(data) is int: 
            self.data = self.display_unit._convert_to_base(float(data));
        elif type(data) is list:
            self.data = [self.display_unit._convert_to_base(float(x)) for x in data];
        elif isinstance(data, np.ndarray):
            self.data = np.array([self.display_unit._convert_to_base(float(x)) for x in data]);
        else:
            self.data = self.display_unit._convert_to_base(data);
        
class Timeseries(_Variable):
    '''Variable class with data that is a timeseries.

    Parameters
    ----------
    name : string
        Name of variable.
    timeseries : ``pandas`` Series
        Timeseries data of variable.  Must have an index of timestamps.
    display_unit : mpcpy.units.unit
        Unit of variable data being set.
    tz_name : string
        Timezone name according to ``tzwhere``.
    geography : list, optional
        List specifying [latitude, longitude] in degrees.
    cleaning_type : dict, optional
        Dictionary specifying {'cleaning_type' : mpcpy.variables.Timeseries.cleaning_type, 'cleaning_args' : cleaning_args}.

    Attributes
    ----------
    name : string
        Name of variable.
    data : float, int, bool, list, ``numpy`` array
        Data of variable
    display_unit : mpcpy.units.unit
        Unit of variable data when returned with ``display_data()``.
    quantity_name : string
        Quantity type of the variable (e.g. Temperature, Power, etc.).        
    variability : string
        Timeseries.

    '''
    
    def __init__(self, name, timeseries, display_unit, tz_name = 'UTC', **kwargs):
        '''Constructor of Timeseries variable object.

        '''

        self.variability = 'Timeseries';
        self.display_unit = display_unit(self);
        self.set_data(timeseries, tz_name, **kwargs);
        self.name = name;        
        
    def set_data(self, timeseries, tz_name = 'UTC', **kwargs):
        '''Set data of Timeseries variable.

        Parameters
        ----------
        data : ``pandas`` Series
            Timeseries data of variable.  Must have an index of timestamps.
        tz_name : string
            Timezone name according to ``tzwhere``.
        geography : list, optional
            List specifying [latitude, longitude] in degrees.
        cleaning_type : dict, optional
            Dictionary specifying {'cleaning_type' : mpcpy.variables.Timeseries.cleaning_type, 'cleaning_args' : cleaning_args}.

        Yields
        ------
        data : ``pandas`` Series
            Data attribute.            

        '''

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
        self.data = self.display_unit._convert_to_base(self._timeseries.apply(float));
        
    def cleaning_replace(self, (to_replace, replace_with)):
        '''Cleaning method to replace values within timeseries.

        Parameters
        ----------
        to_replace
            Value to replace.
        replace_with
            Replacement value.
            
        Returns
        -------
        timeseries
            Timeseries with data replaced according to to_replace and replace_with.        

        '''

        timeseries = self._timeseries.replace(to_replace,replace_with);

        return timeseries           