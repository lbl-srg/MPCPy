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
        self.building = systems.EmulationFromFMU({}, fmupath = utility.get_MPCPy_path()+'/resources/building/Examples_LBNL71T_Emulation_WithHeaters_ME1.fmu', parameter_data = self.parameter_data);
    def test_get_fmu_variable_units(self):
        fmu_variables_units = self.building.get_fmu_variable_units();
        self.assertEqual(fmu_variables_units['wesTdb'], 'K');
    def test_get_unit_class_from_fmu_variable_units(self):
        fmu_variables_units = self.building.get_fmu_variable_units();
        unit_class = self.building.get_unit_class_from_fmu_variable_units('wesTdb', fmu_variables_units);
        self.assertIs(unit_class, units.K);      
    def test_get_unit_class_from_unit_string(self):
        unit_class = utility.get_unit_class_from_unit_string('(m2.K)/W');
        self.assertIs(unit_class, units.m2K_W);
    def test_free_parameter_check(self):
        self.assertEqual(self.building.parameter_data['par']['Free'].get_base_data(), 0);
    def tearDown(self):
        os.remove('RapidMPC_Examples_LBNL71T_0Emulate_Emulation_log.txt');

class TestFMIVersionDefault(unittest.TestCase):
    def test_fmi_default(self):
        building = systems.EmulationFromFMU({}, moinfo = (utility.get_MPCPy_path()+'/resources/model/SimpleRC.mo', 'SimpleRC', {}));
        self.assertEqual(building.fmu.get_version(), '2.0');
        model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (utility.get_MPCPy_path()+'/resources/model/SimpleRC.mo', 'SimpleRC', {}));
        self.assertEqual(model.fmu.get_version(), '2.0');
        
class TestGetInputNames(unittest.TestCase):
    def test_fmi_version(self):
        for version in ['1.0', '2.0']:
            building = systems.EmulationFromFMU({}, moinfo = (utility.get_MPCPy_path()+'/resources/model/SimpleRC.mo', 'SimpleRC', {}), version = version);
            self.assertEqual(building.input_names, ['Tamb']);
            model = models.Modelica(models.JModelica, models.RMSE, {}, moinfo = (utility.get_MPCPy_path()+'/resources/model/SimpleRC.mo', 'SimpleRC', {}), version = version);
            self.assertEqual(model.input_names, ['Tamb']);

if __name__ == '__main__':
    unittest.main()