# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the utility functions of mpcpy.

"""

import unittest
import os
from mpcpy import utility
from mpcpy import units
from mpcpy import systems
from mpcpy import models
from mpcpy import variables
from testing import TestCaseMPCPy

#%% General methods test
class TestEmulationFromFMU(TestCaseMPCPy):
    def setUp(self):
        self.parameter_data = {};
        self.parameter_data['par'] = {};
        self.parameter_data['par']['Value'] = 1;        
        # instantiate building fmu v1.0
        fmupath_1 = os.path.join(self.get_unittest_path(), 'resources', 'building', 'LBNL71T_Emulation_JModelica_v1.fmu');
        self.building_1 = systems.EmulationFromFMU({}, fmupath = fmupath_1, parameter_data = self.parameter_data);
        # instantiate building fmu v2.0
        fmupath_2 = os.path.join(self.get_unittest_path(), 'resources', 'building', 'LBNL71T_Emulation_JModelica_v2.fmu');
        self.building_2 = systems.EmulationFromFMU({}, fmupath = fmupath_2, parameter_data = self.parameter_data);
    def test_fmu_version(self):
        # fmu 1.0
        self.assertEqual(self.building_1.fmu_version, '1.0');
        # fmu 2.0
        self.assertEqual(self.building_2.fmu_version, '2.0');
    def test_get_fmu_variable_units(self):
        # fmu 1.0
        fmu_variables_units_1 = self.building_1._get_fmu_variable_units();
        self.assertEqual(fmu_variables_units_1['wesTdb'], 'K');
        self.assertEqual(fmu_variables_units_1['lat'], 'rad');
        # fmu 2.0
        fmu_variables_units_2 = self.building_2._get_fmu_variable_units();
        self.assertEqual(fmu_variables_units_2['wesTdb'], 'K');
        self.assertEqual(fmu_variables_units_2['lat'], 'rad');
    def test_get_unit_class_from_fmu_variable_units(self):
        fmu_variables_units = self.building_1._get_fmu_variable_units();
        unit_class = self.building_1._get_unit_class_from_fmu_variable_units('wesTdb', fmu_variables_units);
        self.assertIs(unit_class, units.K);      
    def test_get_unit_class_from_unit_string(self):
        unit_class = utility.get_unit_class_from_unit_string('(m2.K)/W');
        self.assertIs(unit_class, units.m2K_W);
    def test_free_parameter_check(self):
        self.assertEqual(self.building_1.parameter_data['par']['Free'].get_base_data(), 0);

class TestFMIVersionDefault(TestCaseMPCPy):
    def setUp(self):
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        self.modelpath = 'Simple.RC';

    def test_fmi_default(self):
        building = systems.EmulationFromFMU({}, moinfo = (self.mopath, self.modelpath, {}));
        self.assertEqual(building.fmu_version, '2.0');
        model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (self.mopath, self.modelpath, {}));
        self.assertEqual(model.fmu_version, '2.0');
        
class TestFMITarget(TestCaseMPCPy):
    def test_fmi_compile(self):
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC';
        for target in ['default', 'cs', 'me']:
            if target == 'default':
                building = systems.EmulationFromFMU({}, moinfo = (mopath, modelpath, {}));
                self.assertEqual(building.fmu_target, 'me');
                model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (mopath, modelpath, {}));
                self.assertEqual(model.fmu_target, 'me');
            else:
                building = systems.EmulationFromFMU({}, moinfo = (mopath, modelpath, {}), target=target);
                self.assertEqual(building.fmu_target, target);
                model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (mopath, modelpath, {}), target=target);
                self.assertEqual(model.fmu_target, target);
                
    def test_fmi_given(self):
        for target in ['1.0', 'me', 'cs']:
            if target == '1.0':
                fmupath = os.path.join(self.get_unittest_path(), 'resources', 'building', 'LBNL71T_Emulation_JModelica_v1.fmu');
                building = systems.EmulationFromFMU({}, fmupath = fmupath);
                self.assertEqual(building.fmu_target, None);
                model = models.Modelica(models.JModelica, models.RMSE, {}, fmupath=fmupath);
                self.assertEqual(model.fmu_target, None);
            else:
                fmupath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple_RC_{0}_2.fmu'.format(target));
                building = systems.EmulationFromFMU({}, fmupath = fmupath);
                self.assertEqual(building.fmu_target, target);
                model = models.Modelica(models.JModelica, models.RMSE, {}, fmupath=fmupath);
                self.assertEqual(model.fmu_target, target);
        
class TestGetInputNames(TestCaseMPCPy):
    def setUp(self):
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        self.modelpath = 'Simple.RC';
        
    def test_fmi_version(self):
        for version in ['1.0', '2.0']:
            building = systems.EmulationFromFMU({}, moinfo = (self.mopath, self.modelpath, {}), version = version);
            self.assertEqual(building.input_names, ['q_flow']);
            model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (self.mopath, self.modelpath, {}), version = version);
            self.assertEqual(model.input_names, ['q_flow']);
            
class TestSimulateFMU(TestCaseMPCPy):
    '''Test simulation of me, cs, 1.0, 2.0 fmus.'''
    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        # Set model paths
        mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        modelpath = 'Simple.RC_noinputs';        
        self.moinfo = (mopath, modelpath, {})

    def test_simulate_me_1(self):
        '''Test simulation me 1.0.'''
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = self.moinfo, 
                                     version = '1.0',
                                     target = 'me');
        # Simulate model
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_fmu_me.csv');

    def test_simulate_cs_1(self):
        '''Test simulation cs 1.0.'''
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = self.moinfo, 
                                     version = '1.0',
                                     target = 'cs');
        # Simulate model
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_fmu_cs.csv');
        
    def test_simulate_me_2(self):
        '''Test simulation me 2.0.'''
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = self.moinfo, 
                                     version = '2.0',
                                     target = 'me');
        # Simulate model
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');     
        self.check_df(df_test, 'simulate_fmu_me.csv');
        
    def test_simulate_cs_2(self):
        '''Test simulation cs 2.0.'''
        # Instantiate model
        self.model = models.Modelica(models.JModelica, \
                                     models.RMSE, \
                                     self.measurements, \
                                     moinfo = self.moinfo, 
                                     version = '2.0',
                                     target = 'cs');
        # Simulate model
        self.model.simulate(self.start_time, self.final_time);
        # Check references
        df_test = self.model.display_measurements('Simulated');
        self.check_df(df_test, 'simulate_fmu_cs.csv');

if __name__ == '__main__':
    unittest.main()