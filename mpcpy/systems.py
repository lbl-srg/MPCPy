# -*- coding: utf-8 -*-
"""
systems.py
by David Blum

This module contains the classes and interfaces required for collecting 
measurements from and setting control signals to system sources.

"""

from abc import ABCMeta, abstractmethod
from mpcpy import utility

#%% System class
class System(utility.mpcpyPandas, utility.Building):
    '''Abstract class for representing systems.'''  
    __metaclass__ = ABCMeta;
    @abstractmethod
    def collect_measurements():
        '''An object of the System class must gather system measurements.
        
        To standardize data transfer within mpcpy, the returned measurements 
        should be saved into a dictionary with the following format:   

        {
        “Key Name” : {
        		"Simulated" : Timeseries variable for simulated measurement,
                "Measured" : Timeseries variable for measured measurement,
                "Sample" : Static variable for measurement sample rate,
                "SimulatedError" : Timeseries variable for simulated standard error,
                "MeasuredError" : Timeseries variable for measured standard error}
        }    
        
        '''
        
        pass;
        
#%% System implementations
class Emulation(System):
    '''Emulation implementation of the abstract System class.'''
    __metaclass__ = ABCMeta;
    def collect_measurements(self, start_time, final_time):
        '''Collect measurement data dictionary for the system via emulation.'''
        self._set_time_interval(start_time, final_time);
        self._simulate();
        for key in self.measurements.keys():
            self.measurements[key]['Measured'] = self.measurements[key]['Simulated']; 

class Real(System):
    def __init__(self, source, source_location, zone_names):
        '''Constructor of a real system source.'''        
        self.name = 'Real';   
        
    def collect_measurements(self, start_time, final_time):
        '''Collect measurement data dictionary for the system via a real source.'''
        self._set_time_interval(start_time, final_time);
        self._collect_data();
        
#%% Source implementations
class EmulationFromFMU(Emulation, utility.FMU):
    ''' A system source interface for an fmu source.'''
    def __init__(self, measurements, **kwargs):
        ''' Constructor of a system fmu simulation source.'''
        self.name = 'emulation_from_fmu';
        self._create_fmu(kwargs);
        self.measurements = measurements
        self.input_names = self.get_input_names();
        self._parse_building_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        
    def _simulate(self):
        '''Simulate the fmu.'''
        self._simulate_fmu();
        
class RealFromCSV(Real, utility.DAQ):
    ''' A system source interface for data coming from a csv file.'''
    def __init__(self, csv_filepath, measurements, variable_map, **kwargs):
        ''' Constructor of a system fmu simulation source.'''
        self.name = 'real_from_csv';
        self.location = csv_filepath;
        self.measurements = measurements;
        self.variable_map = variable_map;
        self._parse_daq_kwargs(kwargs);
        self._parse_time_zone_kwargs(kwargs);
        
    def _collect_data(self):
        '''Collect data from csv into measurement dictionary.'''
        self._read_timeseries_from_csv();

    def _translate_variable_map(self):
        '''Translate csv column to measurement dictionary.'''
        varname = self.variable_map[self._key][0];
        unit = self.variable_map[self._key][1];
        self.measurements[varname]['Measured'] = self.dataframe_to_mpcpy_ts_variable(self._df_csv, self._key, varname, unit, \
                                                                                     start_time=self.start_time, final_time=self.final_time, \
                                                                                     cleaning_type = self._cleaning_type, \
                                                                                     cleaning_args = self._cleaning_args);             