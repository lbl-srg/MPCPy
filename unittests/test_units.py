# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the units of mpcpy.

"""

import unittest
from mpcpy import variables
from mpcpy import units
        
#%% Temperature tests
class Temperature(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Temperature';
    def test_K(self):
        self.var = variables.Static('var1', 293.15, units.K);        
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 293.15, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 293.15, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'K');
    def test_degC(self):
        self.var = variables.Static('var1', 20.0, units.degC);    
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 293.15, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 20, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'degC');        
    def test_degF(self):
        self.var = variables.Static('var1', 72.0, units.degF);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 295.372, places = 3);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 72.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'degF');        
    def test_degR(self):
        self.var = variables.Static('var1', 531.0, units.degR);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 295, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 531.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'degR');        
        
#%% Power tests        
class Power(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Power';    
    def test_W(self):
        self.var = variables.Static('var1', 1.0, units.W);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'W');    
    def test_kW(self):
        self.var = variables.Static('var1', 1.0, units.kW);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kW');         
    def test_MW(self):
        self.var = variables.Static('var1', 1.0, units.MW);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1e6, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'MW');         
    def test_Btuh(self):
        self.var = variables.Static('var1', 1.0, units.Btuh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.293071, places = 6);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Btuh');         
    def test_kBtuh(self):
        self.var = variables.Static('var1', 1.0, units.kBtuh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 293.071, places = 3);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
                # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kBtuh'); 
    def test_hp(self):
        self.var = variables.Static('var1', 1.0, units.hp);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 745.7, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'hp'); 
        
#%% Energy tests        
class Energy(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Energy';     
    def test_J(self):
        self.var = variables.Static('var1', 1.0, units.J);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'J');         
    def test_kJ(self):
        self.var = variables.Static('var1', 1.0, units.kJ);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kJ');         
    def test_MJ(self):
        self.var = variables.Static('var1', 1.0, units.MJ);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'MJ');         
    def test_Btu(self):
        self.var = variables.Static('var1', 1.0, units.Btu);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1055.05585, places = 5);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Btu'); 
    def test_kBtu(self):
        self.var = variables.Static('var1', 1.0, units.kBtu);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1055055.85, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kBtu');         
    def test_Wh(self):
        self.var = variables.Static('var1', 1.0, units.Wh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Wh');         
    def test_kWh(self):
        self.var = variables.Static('var1', 1.0, units.kWh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600000, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kWh');         
    def test_MWh(self):
        self.var = variables.Static('var1', 1.0, units.MWh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600000000, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'MWh');         
        
#%% Power Flux tests        
class PowerFlux(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'PowerFlux';       
    def test_W_m2(self):
        self.var = variables.Static('var1', 1.0, units.W_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'W/m2');         
    def test_kW_m2(self):
        self.var = variables.Static('var1', 1.0, units.kW_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kW/m2');           
    def test_W_sf(self):
        self.var = variables.Static('var1', 1.0, units.W_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 10.7639, places = 4);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'W/sf');           
    def test_kW_sf(self):
        self.var = variables.Static('var1', 1.0, units.kW_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 10763.9, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kW/sf');           
    def test_Btuh_sf(self):
        self.var = variables.Static('var1', 1.0, units.Btuh_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3.154594, places = 6);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Btuh/sf');        
    def test_kBtuh_sf(self):
        self.var = variables.Static('var1', 1.0, units.kBtuh_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3154.594, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kBtuh/sf');           

#%% Energy Intensity tests        
class EnergyIntensity(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'EnergyIntensity';       
    def test_J_m2(self):
        self.var = variables.Static('var1', 1.0, units.J_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'J/m2');         
    def test_Wh_m2(self):
        self.var = variables.Static('var1', 1.0, units.Wh_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Wh/m2');           
    def test_kWh_m2(self):
        self.var = variables.Static('var1', 1.0, units.kWh_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600000, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kWh/m2');           
    def test_Wh_sf(self):
        self.var = variables.Static('var1', 1.0, units.Wh_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 38750.04, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Wh/sf');           
    def test_kWh_sf(self):
        self.var = variables.Static('var1', 1.0, units.kWh_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 38750040, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kWh/sf');           
    def test_Btu_sf(self):
        self.var = variables.Static('var1', 1.0, units.Btu_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 11356.516, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Btu/sf');           
    def test_kBtu_sf(self):
        self.var = variables.Static('var1', 1.0, units.kBtu_sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 11356515.66, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kBtu/sf');           

#%% Pressure tests        
class Pressure(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Pressure';      
    def test_Pa(self):
        self.var = variables.Static('var1', 1.0, units.Pa);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'Pa');         
    def test_kPa(self):
        self.var = variables.Static('var1', 1.0, units.kPa);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kPa');         
    def test_MPa(self):
        self.var = variables.Static('var1', 1.0, units.MPa);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'MPa');         
    def test_bar(self):
        self.var = variables.Static('var1', 1.0, units.bar);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 100000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'bar');         
    def test_inwg(self):
        self.var = variables.Static('var1', 1.0, units.inwg);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 248.84, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'inwg');         
    def test_inHg(self):
        self.var = variables.Static('var1', 1.0, units.inHg);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3386.389, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'inHg');         
    def test_psi(self):
        self.var = variables.Static('var1', 1.0, units.psi);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 6894.757, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'psi');         
    def test_atm(self):
        self.var = variables.Static('var1', 1.0, units.atm);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 101325, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.Pa);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'atm');         
        
#%% Dimensionless Ratio tests        
class DimensionlessRatio(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'DimensionlessRatio';        
    def test_unit1(self):
        self.var = variables.Static('var1', 1.0, units.unit1);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.unit1);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '1');          
    def test_percent(self):
        self.var = variables.Static('var1', 1.0, units.percent);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.01, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.unit1);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'percent');
    def test_unit10(self):
        self.var = variables.Static('var1', 1.0, units.unit10);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.1, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.unit1);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '10');          
        
#%% Angle tests        
class Angle(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Angle';        
    def test_rad(self):
        self.var = variables.Static('var1', 1.0, units.rad);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.rad);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'rad');          
    def test_deg(self):
        self.var = variables.Static('var1', 1.0, units.deg);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.0174533, places = 7);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.rad);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'deg');        
        
#%% Time tests        
class Time(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Time';    
    def test_s(self):
        self.var = variables.Static('var1', 1.0, units.s);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 's');          
    def test_minute(self):
        self.var = variables.Static('var1', 1.0, units.minute);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 60.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'min');         
    def test_hour(self):
        self.var = variables.Static('var1', 1.0, units.hour);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 3600.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
                # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'h'); 
    def test_day(self):
        self.var = variables.Static('var1', 1.0, units.day);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 86400.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'd');         

#%% Mass tests        
class Mass(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Mass';       
    def test_kg(self):
        self.var = variables.Static('var1', 1.0, units.kg);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.kg);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kg');        
        
#%% Length tests        
class Length(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Length';       
    def test_m(self):
        self.var = variables.Static('var1', 1.0, units.m);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'm');          
    def test_cm(self):
        self.var = variables.Static('var1', 1.0, units.cm);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.01, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cm');          
    def test_mm(self):
        self.var = variables.Static('var1', 1.0, units.mm);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.001, places = 3);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);  
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'mm');          
    def test_km(self):
        self.var = variables.Static('var1', 1.0, units.km);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1000.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'km');          
    def test_inch(self):
        self.var = variables.Static('var1', 1.0, units.inch);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.0254, places = 4);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'inch');          
    def test_ft(self):
        self.var = variables.Static('var1', 1.0, units.ft);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.3048, places = 4);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'ft');          
    def test_yd(self):
        self.var = variables.Static('var1', 1.0, units.yd);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.9144, places = 4);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'yd');          

#%% Area tests        
class Area(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Area';       
    def test_m2(self):
        self.var = variables.Static('var1', 1.0, units.m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'm2');         
    def test_sf(self):
        self.var = variables.Static('var1', 1.0, units.sf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.092903, places = 6);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'sf');         
        
#%% Volume tests        
class Volume(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Volume';     
    def test_m3(self):
        self.var = variables.Static('var1', 1.0, units.m3);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m3);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'm3');           
    def test_cf(self):
        self.var = variables.Static('var1', 1.0, units.cf);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.0283168, places = 7);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m3);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cf');           

#%% Mass Flow tests        
class MassFlow(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'MassFlow';      
    def test_kg_s(self):
        self.var = variables.Static('var1', 1.0, units.kg_s);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.kg_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kg/s');          

#%% Volumetric Flow tests        
class VolumetricFlow(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'VolumetricFlow';     
    def test_m3_s(self):
        self.var = variables.Static('var1', 1.0, units.m3_s);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m3_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'm3/s');          
    def test_cfm(self):
        self.var = variables.Static('var1', 1.0, units.cfm);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.0004719474, places = 10);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m3_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cfm');          
        
#%% Velocity tests        
class Velocity(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Velocity';     
    def test_m_s(self):
        self.var = variables.Static('var1', 1.0, units.m_s);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'm/s');          
    def test_mph(self):
        self.var = variables.Static('var1', 1.0, units.mph);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.44704, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'mph');        
    def test_km_h(self):
        self.var = variables.Static('var1', 1.0, units.km_h);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.277778, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m_s);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'km/h');        

#%% Illuminance tests        
class Illuminance(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Illuminance';     
    def test_lx(self):
        self.var = variables.Static('var1', 1.0, units.lx);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.lx);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'lx');         
    def test_fc(self):
        self.var = variables.Static('var1', 1.0, units.fc);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 10.764, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.lx);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'fc');          

#%% Luminance tests        
class Luminance(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Luminance';     
    def test_cd_m2(self):
        self.var = variables.Static('var1', 1.0, units.cd_m2);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cd_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cd/m2');        
    def test_nt(self):
        self.var = variables.Static('var1', 1.0, units.nt);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cd_m2);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'nt');          

#%% EnergyPrice tests        
class EnergyPrice(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'EnergyPrice';     
    def test_cents_kWh(self):
        self.var = variables.Static('var1', 1.0, units.cents_kWh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cents/kWh');          
    def test_dol_kWh(self):
        self.var = variables.Static('var1', 1.0, units.dol_kWh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 100.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '$/kWh');         
    def test_dol_MWh(self):
        self.var = variables.Static('var1', 1.0, units.dol_MWh);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.1, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '$/MWh');         
        
#%% PowerPrice tests        
class PowerPrice(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'PowerPrice';     
    def test_cents_kW(self):
        self.var = variables.Static('var1', 1.0, units.cents_kW);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'cents/kW');          
    def test_dol_kW(self):
        self.var = variables.Static('var1', 1.0, units.dol_kW);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 100.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '$/kW');          
    def test_dol_MW(self):
        self.var = variables.Static('var1', 1.0, units.dol_MW);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 0.1, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.cents_kWh);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '$/MW');          
        
#%% SpecificHeatCapacity tests        
class SpecificHeatCapacity(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'SpecificHeatCapacity';      
    def test_J_kgK(self):
        self.var = variables.Static('var1', 1.0, units.J_kgK);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_kgK);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'J/(kg.K)');         

#%% HeatCapacity tests        
class HeatCapacity(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'HeatCapacity';       
    def test_J_K(self):
        self.var = variables.Static('var1', 1.0, units.J_K);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'J/K');  
    
#%% HeatCapacityCoefficient tests        
class HeatCapacityCoefficient(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'HeatCapacityCoefficient';       
    def test_J_m2K(self):
        self.var = variables.Static('var1', 1.0, units.J_m2K);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.J_m2K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'J/(m2.K)');          

#%% HeatResistance tests        
class HeatResistance(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'HeatResistance';     
    def test_K_W(self):
        self.var = variables.Static('var1', 1.0, units.K_W);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.K_W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'K/W');  
        
#%% HeatResistance tests        
class HeatResistanceCoefficient(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'HeatResistanceCoefficient';     
    def test_m2K_W(self):
        self.var = variables.Static('var1', 1.0, units.m2K_W);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.m2K_W);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), '(m2.K)/W');        
        

#%% HeatTransferCoefficient tests        
class HeatTransferCoefficient(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'HeatTransferCoefficient';      
    def test_W_m2K(self):
        self.var = variables.Static('var1', 1.0, units.W_m2K);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2);
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.W_m2K);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'W/(m2.K)');           
        
#%% Density tests        
class Density(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Density';      
    def test_kg_m3(self):
        self.var = variables.Static('var1', 1.0, units.kg_m3);
        # Test conversion to base unit
        self.assertAlmostEqual(self.var.get_base_data(), 1.0, places = 2);
        # Test conversion from base unit        
        self.assertAlmostEqual(self.var.display_data(), 1.0, places = 2); 
        # Test the base unit quantity        
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.kg_m3);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'kg/m3');
        
#%% Boolean tests
class Boolean(unittest.TestCase):
    def setUp(self):
        self.quantity_name = 'Boolean';
    def test_boolean_integer(self):
        self.var = variables.Static('var1', 1, units.boolean_integer);        
        # Test conversion to base unit
        self.assertEqual(self.var.get_base_data(), 1);
        # Test conversion from base unit        
        self.assertEqual(self.var.display_data(), 1);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.boolean_integer);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'boolean_integer');
    def test_boolean(self):
        self.var = variables.Static('var1', True, units.boolean);    
        # Test conversion to base unit
        self.assertEqual(self.var.get_base_data(), 1);
        # Test conversion from base unit        
        self.assertEqual(self.var.display_data(), True);
        # Test the base unit quantity
        self.assertEqual(self.var.quantity_name, self.quantity_name);
        # Test the base unit class
        self.assertEqual(self.var.get_base_unit(), units.boolean_integer);
        # Test the display unit name string
        self.assertEqual(self.var.get_display_unit_name(), 'boolean');            
        
if __name__ == '__main__':
    unittest.main()