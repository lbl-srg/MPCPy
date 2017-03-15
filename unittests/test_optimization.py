# -*- coding: utf-8 -*-
"""
test_optimization.py
by David Blum

This module contains the classes for testing the optimization module of mpcpy.
"""
import unittest
import os
from matplotlib import pyplot as plt
from mpcpy import models
from mpcpy import optimization
from mpcpy import exodata
from mpcpy import utility
from mpcpy import variables
from mpcpy import units

#%% Temperature tests
class Optimize_Jmo(unittest.TestCase):
    '''Tests for the optimization of a model using JModelica.'''
    def setUp(self):
        self.MPCPyPath = utility.get_MPCPy_path();
        ## Setup model
        self.mopath = self.MPCPyPath + '/resources/model/LBNL71T_MPC.mo';
        self.modelpath = 'LBNL71T_MPC.MPC';
        self.libraries = os.environ.get('MODELICAPATH');
        self.estimate_method = models.JModelica; 
        self.validation_method = models.RMSE;
        self.zone_names = ['wes', 'hal', 'eas'];                   
        # Measurements
        self.measurements = {};
        self.measurements['wesTdb'] = {'Sample' : variables.Static('wesTdb_sample', 1800, units.s)};
        self.measurements['halTdb'] = {'Sample' : variables.Static('halTdb_sample', 1800, units.s)};
        self.measurements['easTdb'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['wesPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['halPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};     
        self.measurements['easPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['Ptot'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)}; 
        self.measurements['intCon_eas'] = {'Sample' : variables.Static('intCon_eas_sample', 1800, units.s)}; 
        self.measurements['intRad_eas'] = {'Sample' : variables.Static('intRad_eas_sample', 1800, units.s)};
        self.measurements['intCon_wes'] = {'Sample' : variables.Static('intCon_wes_sample', 1800, units.s)}; 
        self.measurements['intRad_wes'] = {'Sample' : variables.Static('intRad_wes_sample', 1800, units.s)}; 
        self.measurements['intCon_hal'] = {'Sample' : variables.Static('intCon_hal_sample', 1800, units.s)}; 
        self.measurements['intRad_hal'] = {'Sample' : variables.Static('intRad_hal_sample', 1800, units.s)};         
        
        ## Exodata
        # Exogenous collection time
        self.start_time_exodata = '1/1/2015';
        self.final_time_exodata = '1/30/2015';
        # Optimization time
        self.start_time_optimization = '1/2/2015';
        self.final_time_optimization = '1/3/2015';       
        # Weather
        self.weather_path = self.MPCPyPath + '/resources/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw';
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.weather.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Internal
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
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.internal.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Control (as initialization)
        self.control_path = self.MPCPyPath + '/resources/optimization/ControlCSV.csv';
        self.control_variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                                     'conHeat_hal' : ('conHeat_hal', units.unit1), \
                                     'conHeat_eas' : ('conHeat_eas', units.unit1)};        
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);
        self.control.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Parameters
        self.parameters_path = self.MPCPyPath + '/unittests/resources/model_parameters.txt';
        self.parameters = exodata.ParameterFromCSV(self.parameters_path);
        self.parameters.collect_data();
        # Constraints
        self.constraints_path = self.MPCPyPath + '/resources/optimization/sampleConstraintCSV_Constant.csv';   
        self.constraints_variable_map = {'wesTdb_min' : ('wesTdb', 'GTE', units.degC), \
                                         'wesTdb_max' : ('wesTdb', 'LTE', units.degC), \
                                         'easTdb_min' : ('easTdb', 'GTE', units.degC), \
                                         'easTdb_max' : ('easTdb', 'LTE', units.degC), \
                                         'halTdb_min' : ('halTdb', 'GTE', units.degC), \
                                         'halTdb_max' : ('halTdb', 'LTE', units.degC), \
                                         'der_wesTdb_min' : ('wesTdb', 'dGTE', units.K), \
                                         'der_wesTdb_max' : ('wesTdb', 'dLTE', units.K), \
                                         'der_easTdb_min' : ('easTdb', 'dGTE', units.K), \
                                         'der_easTdb_max' : ('easTdb', 'dLTE', units.K), \
                                         'der_halTdb_min' : ('halTdb', 'dGTE', units.K), \
                                         'der_halTdb_max' : ('halTdb', 'dLTE', units.K), \
                                         'conHeat_wes_min' : ('conHeat_wes', 'GTE', units.unit1), \
                                         'conHeat_wes_max' : ('conHeat_wes', 'LTE', units.unit1), \
                                         'conHeat_hal_min' : ('conHeat_hal', 'GTE', units.unit1), \
                                         'conHeat_hal_max' : ('conHeat_hal', 'LTE', units.unit1), \
                                         'conHeat_eas_min' : ('conHeat_eas', 'GTE', units.unit1), \
                                         'conHeat_eas_max' : ('conHeat_eas', 'LTE', units.unit1)};
        self.constraints = exodata.ConstraintFromCSV(self.constraints_path, self.constraints_variable_map, tz_name = self.weather.tz_name);
        self.constraints.collect_data(self.start_time_exodata, self.final_time_exodata);
        self.constraints.data['wesTdb']['Cyclic'] = variables.Static('wesTdb_cyclic', 1, units.boolean_integer);
        self.constraints.data['easTdb']['Cyclic'] = variables.Static('easTdb_cyclic', 1, units.boolean_integer);
        self.constraints.data['halTdb']['Cyclic'] = variables.Static('halTdb_cyclic', 1, units.boolean_integer);
        # Prices
        self.prices_path = self.MPCPyPath + '/resources/optimization/PriceCSV.csv';
        self.price_variable_map = {'pi_e' : ('pi_e', units.unit1)};        
        self.prices = exodata.PriceFromCSV(self.prices_path, self.price_variable_map, tz_name = self.weather.tz_name);
        self.prices.collect_data(self.start_time_exodata, self.final_time_exodata);        
        
        ## Parameters
        self.parameters.data['lat'] = {};
        self.parameters.data['lat']['Value'] = self.weather.lat;     
        ## Instantiate model
        self.model = models.Modelica(self.estimate_method, \
                                     self.validation_method, \
                                     self.measurements, \
                                     moinfo = (self.mopath, self.modelpath, self.libraries), \
                                     zone_names = self.zone_names, \
                                     weather_data = self.weather.data, \
                                     internal_data = self.internal.data, \
                                     control_data = self.control.data, \
                                     parameter_data = self.parameters.data, \
                                     tz_name = self.weather.tz_name);                                     
    def test_energymin(self):
        '''Test energy minimization of a model.'''
        plt.close('all');        
        # Instanatiate optimization problem
        self.opt_problem = optimization.Optimization(self.model, optimization.EnergyMin, optimization.JModelica, 'Ptot', constraint_data = self.constraints.data)
        # Optimize
        self.opt_problem.optimize(self.start_time_optimization, self.final_time_optimization);
        self.model = self.opt_problem.Model;
        # Plot
        plt.figure(1)
        for measurement in ['wesTdb', 'easTdb', 'halTdb']:
            variable = self.model.measurements[measurement]['Simulated'];
            variable.set_display_unit(units.degC);
            var_data = variable.display_data(tz_name = 'America/Chicago');
            var_data.plot(label = measurement, rot = 90, linewidth = 2.0);
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});
        plt.rcParams.update({'font.size': 16});        
        plt.savefig(self.MPCPyPath+'/unittests/resources/energymin_temperature.png');
        plt.close();
        plt.figure(2)
        for measurement in ['wesPhvac', 'easPhvac', 'halPhvac', 'Ptot']:
            variable = self.model.measurements[measurement]['Simulated'];
            variable.set_display_unit(units.W);
            var_data = variable.display_data(tz_name = 'America/Chicago');
            var_data.plot(label = measurement, rot = 90, linewidth = 2.0);
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});
        plt.rcParams.update({'font.size': 16});        
        plt.savefig(self.MPCPyPath+'/unittests/resources/energymin_heaterpower.png');
        plt.close();

    def test_energycostmin(self):
        '''Test energy cost minimization of a model.'''
        plt.close('all');
        # Instanatiate optimization problem
        self.opt_problem = optimization.Optimization(self.model, optimization.EnergyCostMin, optimization.JModelica, 'Ptot', constraint_data = self.constraints.data)
        # Optimize
        self.opt_problem.optimize(self.start_time_optimization, self.final_time_optimization, price_data = self.prices.data);
        self.model = self.opt_problem.Model;
        # Plot
        plt.figure(1)
        for measurement in ['wesTdb', 'easTdb', 'halTdb']:
            variable = self.model.measurements[measurement]['Simulated'];
            variable.set_display_unit(units.degC);
            var_data = variable.display_data(tz_name = 'America/Chicago');
            var_data.plot(label = measurement, rot = 90, linewidth = 2.0);
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});
        plt.rcParams.update({'font.size': 16});        
        plt.savefig(self.MPCPyPath+'/unittests/resources/energycostmin_temperature.png');
        plt.close();
        plt.figure(2)
        for measurement in ['wesPhvac', 'easPhvac', 'halPhvac', 'Ptot']:
            variable = self.model.measurements[measurement]['Simulated'];
            variable.set_display_unit(units.W);
            var_data = variable.display_data(tz_name = 'America/Chicago');
            var_data.plot(label = measurement, rot = 90, linewidth = 2.0);
        plt.ylabel(variable.quantity_name + ' [' + variable.display_unit.name + ']');
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, prop={'size':12});
        plt.rcParams.update({'font.size': 16});
        plt.savefig(self.MPCPyPath+'/unittests/resources/energycostmin_heaterpower.png');
        plt.close();                                   
    
        
if __name__ == '__main__':
    unittest.main()