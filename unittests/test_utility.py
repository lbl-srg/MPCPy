# -*- coding: utf-8 -*-
"""
test_utility.py
by David Blum

This module contains the classes for testing the utility functions of mpcpy.
"""

import unittest
import os
from mpcpy import utility
from mpcpy import units
from mpcpy import systems
from mpcpy import models

#%% General methods test
class TestEmulationFromFMU(unittest.TestCase):
    def setUp(self):
        self.parameter_data = {};
        self.parameter_data['par'] = {};
        self.parameter_data['par']['Value'] = 1;        
        # instantiate building fmu v1.0
        self.building_1 = systems.EmulationFromFMU({}, fmupath = utility.get_MPCPy_path()+'/resources/building/Examples_LBNL71T_Emulation_WithHeaters_ME1.fmu', parameter_data = self.parameter_data);
        # instantiate building fmu v2.0
        self.building_2 = systems.EmulationFromFMU({}, fmupath = utility.get_MPCPy_path()+'/resources/building/Examples_LBNL71T_Emulation_WithHeaters_ME2.fmu', parameter_data = self.parameter_data);
    def test_fmu_version(self):
        # fmu 1.0
        self.assertEqual(self.building_1.fmu_version, '1.0');
        # fmu 2.0
        self.assertEqual(self.building_2.fmu_version, '2.0');
    def test_get_fmu_variable_units(self):
        # fmu 1.0
        fmu_variables_units_1 = self.building_1.get_fmu_variable_units();
        self.assertEqual(fmu_variables_units_1['wesTdb'], 'K');
        self.assertEqual(fmu_variables_units_1['lat'], 'rad');
        # fmu 2.0
        fmu_variables_units_2 = self.building_2.get_fmu_variable_units();
        self.assertEqual(fmu_variables_units_2['wesTdb'], 'K');
        self.assertEqual(fmu_variables_units_2['lat'], 'rad');
    def test_get_unit_class_from_fmu_variable_units(self):
        fmu_variables_units = self.building_1.get_fmu_variable_units();
        unit_class = self.building_1.get_unit_class_from_fmu_variable_units('wesTdb', fmu_variables_units);
        self.assertIs(unit_class, units.K);      
    def test_get_unit_class_from_unit_string(self):
        unit_class = utility.get_unit_class_from_unit_string('(m2.K)/W');
        self.assertIs(unit_class, units.m2K_W);
    def test_free_parameter_check(self):
        self.assertEqual(self.building_1.parameter_data['par']['Free'].get_base_data(), 0);
    def tearDown(self):
        os.remove('RapidMPC_Examples_LBNL71T_0Emulate_Emulation_log.txt');

class TestFMIVersionDefault(unittest.TestCase):
    def setUp(self):
        self.mopath = utility.get_MPCPy_path()+'/resources/model/Simple.mo';
        self.modelpath = 'Simple.RC';

    def test_fmi_default(self):
        building = systems.EmulationFromFMU({}, moinfo = (self.mopath, self.modelpath, {}));
        self.assertEqual(building.fmu_version, '2.0');
        model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (self.mopath, self.modelpath, {}));
        self.assertEqual(model.fmu_version, '2.0');
        
class TestGetInputNames(unittest.TestCase):
    def setUp(self):
        self.mopath = utility.get_MPCPy_path()+'/resources/model/Simple.mo';
        self.modelpath = 'Simple.RC';
        
    def test_fmi_version(self):
        for version in ['1.0', '2.0']:
            building = systems.EmulationFromFMU({}, moinfo = (self.mopath, self.modelpath, {}), version = version);
            self.assertEqual(building.input_names, ['q_flow']);
            model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (self.mopath, self.modelpath, {}), version = version);
            self.assertEqual(model.input_names, ['q_flow']);

if __name__ == '__main__':
    unittest.main()