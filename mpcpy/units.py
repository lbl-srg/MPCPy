# -*- coding: utf-8 -*-
"""
units.py
by David Blum

This module contains the classes and interfaces for the units of mpcpy.
"""

from abc import ABCMeta, abstractmethod
import numpy as np

#%% Display unit abstract interface
class DisplayUnit(object):
    __metaclass__ = ABCMeta; 
    @abstractmethod
    def define_quantity(self):
        pass;
    @abstractmethod
    def define_display_unit(self):
        pass;           
    @abstractmethod
    def convert_to_base(self):
        pass;
    @abstractmethod
    def convert_from_base(self):
        pass;
    def __init__(self,variable):
        self.define_quantity(variable);
        self.define_display_unit();       

#%% Display unit quantity implementation
class Boolean(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Boolean';
        variable.base_unit = boolean_integer;
        
class Temperature(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Temperature';
        variable.base_unit = K;
        
class Power(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Power';
        variable.base_unit = W;
        
class Energy(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Energy';
        variable.base_unit = J;

class PowerFlux(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'PowerFlux';
        variable.base_unit = W_m2;
        
class EnergyIntensity(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'EnergyIntensity';
        variable.base_unit = J_m2; 
        
class Pressure(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Pressure';
        variable.base_unit = Pa;
        
class DimensionlessRatio(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'DimensionlessRatio';
        variable.base_unit = unit1;
        
class Angle(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Angle';
        variable.base_unit = rad;
        
class Time(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Time';
        variable.base_unit = s;       
        
class Mass(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Mass';
        variable.base_unit = kg;         

class Length(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Length';
        variable.base_unit = m;

class Area(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Area';
        variable.base_unit = m2;
        
class Volume(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Volume';
        variable.base_unit = m3;
        
class MassFlow(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'MassFlow';
        variable.base_unit = kg_s;
        
class VolumetricFlow(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'VolumetricFlow';
        variable.base_unit = m3_s;
        
class Velocity(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Velocity';
        variable.base_unit = m_s;
        
class Illuminance(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Illuminance';
        variable.base_unit = lx;

class Luminance(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Luminance';
        variable.base_unit = cd_m2;
        
class EnergyPrice(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'EnergyPrice';
        variable.base_unit = cents_kWh;
        
class PowerPrice(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'PowerPrice';
        variable.base_unit = cents_kWh;
        
class SpecificHeatCapacity(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'SpecificHeatCapacity';
        variable.base_unit = J_kgK;   

class HeatCapacity(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'HeatCapacity';
        variable.base_unit = J_K;
        
class HeatCapacityCoefficient(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'HeatCapacityCoefficient';
        variable.base_unit = J_m2K;        

class HeatResistance(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'HeatResistance';
        variable.base_unit = K_W;
        
class HeatResistanceCoefficient(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'HeatResistanceCoefficient';
        variable.base_unit = m2K_W;        

class HeatTransferCoefficient(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'HeatTransferCoefficient';
        variable.base_unit = W_m2K;
        
class Density(DisplayUnit):
    def define_quantity(self, variable):
        variable.quantity_name = 'Density';
        variable.base_unit = kg_m3;          

#%% Boolean display unit implementation     
class boolean_integer(Boolean):
    def define_display_unit(self):
        self.name = 'boolean_integer';
    def convert_to_base(self, display_data):
        base_data = int(display_data);
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class boolean(Boolean):
    def define_display_unit(self):
        self.name = 'boolean';
    def convert_to_base(self, display_data):
        base_data = int(display_data);
        return base_data;
    def convert_from_base(self, base_data):
        display_data = bool(base_data);
        return display_data;
        
#%% Temperature display unit implementation
class K(Temperature):
    def define_display_unit(self):
        self.name = 'K';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class degC(Temperature):
    def define_display_unit(self):
        self.name = 'degC';
    def convert_to_base(self, display_data):
        base_data = display_data + 273.15;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data - 273.15;
        return display_data;
        
class degF(Temperature):
    def define_display_unit(self):
        self.name = 'degF';
    def convert_to_base(self, display_data):
        base_data = (display_data-32)*5/9 + 273.15;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = (base_data-273.15)*9/5 + 32;
        return display_data;

class degR(Temperature):
    def define_display_unit(self):
        self.name = 'degR';
    def convert_to_base(self, display_data):
        base_data = ((display_data - 459.67)-32)*5/9 + 273.15;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = (base_data-273.15)*9/5 + 32 + 459.67;
        return display_data;
        
#%% Power display unit implementation     
class W(Power):
    def define_display_unit(self):
        self.name = 'W';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kW(Power):
    def define_display_unit(self):
        self.name = 'kW';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;
        
class MW(Power):
    def define_display_unit(self):
        self.name = 'MW';
    def convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;        
        
class Btuh(Power):
    def define_display_unit(self):
        self.name = 'Btuh';
    def convert_to_base(self, display_data):
        base_data = display_data*0.29307107;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.29307107;
        return display_data;
        
class kBtuh(Power):
    def define_display_unit(self):
        self.name = 'kBtuh';
    def convert_to_base(self, display_data):
        base_data = (display_data*1e3)*0.29307107;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.29307107/1e3;
        return display_data;
        
class hp(Power):
    def define_display_unit(self):
        self.name = 'hp';
    def convert_to_base(self, display_data):
        base_data = display_data*745.699872;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/745.699872;
        return display_data;
        
#%% Energy display unit implementation     
class J(Energy):
    def define_display_unit(self):
        self.name = 'J';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kJ(Energy):
    def define_display_unit(self):
        self.name = 'kJ';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;

class MJ(Energy):
    def define_display_unit(self):
        self.name = 'MJ';
    def convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;
        
class Btu(Energy):
    def define_display_unit(self):
        self.name = 'Btu';
    def convert_to_base(self, display_data):
        base_data = display_data*1055.05585;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1055.05585;
        return display_data;

class kBtu(Energy):
    def define_display_unit(self):
        self.name = 'kBtu';
    def convert_to_base(self, display_data):
        base_data = (display_data*1e3)*1055.05585;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1055.05585/1e3;
        return display_data;
        
class Wh(Energy):
    def define_display_unit(self):
        self.name = 'Wh';
    def convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data; 
        
class kWh(Energy):
    def define_display_unit(self):
        self.name = 'kWh';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600/1e3;
        return display_data;

class MWh(Energy):
    def define_display_unit(self):
        self.name = 'MWh';
    def convert_to_base(self, display_data):
        base_data = display_data*1e6*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600/1e6;
        return display_data;
        
#%% Power Flux display unit implementation     
class W_m2(PowerFlux):
    def define_display_unit(self):
        self.name = 'W/m2';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kW_m2(PowerFlux):
    def define_display_unit(self):
        self.name = 'kW/m2';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;        

class W_sf(PowerFlux):
    def define_display_unit(self):
        self.name = 'W/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/10.7639;
        return display_data;
        
class kW_sf(PowerFlux):
    def define_display_unit(self):
        self.name = 'kW/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/10.7639/1e3;
        return display_data;        
        
class Btuh_sf(PowerFlux):
    def define_display_unit(self):
        self.name = 'Btuh/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*3.154594;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3.154594;
        return display_data;
        
class kBtuh_sf(PowerFlux):
    def define_display_unit(self):
        self.name = 'kBtuh/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*3.154594;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3.154594/1e3;
        return display_data;        
        
#%% Energy Intensity display unit implementation     
class J_m2(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'J/m2';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class Wh_m2(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'Wh/m2';
    def convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data;
        
class kWh_m2(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'kWh/m2';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600/1e3;
        return display_data;
        
class Wh_sf(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'Wh/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*3600*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600/10.7639;
        return display_data;
        
class kWh_sf(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'kWh/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*3600*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600/10.7639/1e3;
        return display_data;
        
class Btu_sf(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'Btu/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*1055.05585*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1055.05585/10.7639;
        return display_data;
        
class kBtu_sf(EnergyIntensity):
    def define_display_unit(self):
        self.name = 'kBtu/sf';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3*1055.05585*10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1055.05585/10.7639/1e3;
        return display_data;
        
#%% Pressure display unit implementation     
class Pa(Pressure):
    def define_display_unit(self):
        self.name = 'Pa';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kPa(Pressure):
    def define_display_unit(self):
        self.name = 'kPa';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data; 

class MPa(Pressure):        
    def define_display_unit(self):
        self.name = 'MPa';
    def convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;        
        
class bar(Pressure):
    def define_display_unit(self):
        self.name = 'bar';
    def convert_to_base(self, display_data):
        base_data = display_data*1e5;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e5;
        return display_data;

class inwg(Pressure):
    def define_display_unit(self):
        self.name = 'inwg';
    def convert_to_base(self, display_data):
        base_data = display_data*248.84;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/248.84;
        return display_data;
        
class inHg(Pressure):
    def define_display_unit(self):
        self.name = 'inHg';
    def convert_to_base(self, display_data):
        base_data = display_data*3386.389;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3386.389;
        return display_data; 
        
class psi(Pressure):
    def define_display_unit(self):
        self.name = 'psi';
    def convert_to_base(self, display_data):
        base_data = display_data*6894.757;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/6894.757;
        return display_data;
        
class atm(Pressure):
    def define_display_unit(self):
        self.name = 'atm';
    def convert_to_base(self, display_data):
        base_data = display_data*101325;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/101325;
        return display_data;
        
#%% Dimensionless Ratio display unit implementation     
class unit1(DimensionlessRatio):
    def define_display_unit(self):
        self.name = '1';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class percent(DimensionlessRatio):
    def define_display_unit(self):
        self.name = 'percent';
    def convert_to_base(self, display_data):
        base_data = display_data/100;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*100;
        return display_data;
        
class unit10(DimensionlessRatio):
    def define_display_unit(self):
        self.name = '10';
    def convert_to_base(self, display_data):
        base_data = display_data/10;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*10;
        return display_data;        
        
#%% Angle display unit implementation     
class rad(Angle):
    def define_display_unit(self):
        self.name = 'rad';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class deg(Angle):
    def define_display_unit(self):
        self.name = 'deg';
    def convert_to_base(self, display_data):
        base_data = display_data/180*np.pi;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*180/np.pi;
        return display_data;
        
#%% Time display unit implementation     
class s(Time):
    def define_display_unit(self):
        self.name = 's';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class minute(Time):
    def define_display_unit(self):
        self.name = 'min';
    def convert_to_base(self, display_data):
        base_data = display_data*60;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/60;
        return display_data;

class hour(Time):
    def define_display_unit(self):
        self.name = 'h';
    def convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data;
        
class day(Time):
    def define_display_unit(self):
        self.name = 'd';
    def convert_to_base(self, display_data):
        base_data = display_data*86400;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/86400;
        return display_data;
        
#%% Mass display unit implementation     
class kg(Mass):
    def define_display_unit(self):
        self.name = 'kg';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;  
        
#%% Length display unit implementation     
class m(Length):
    def define_display_unit(self):
        self.name = 'm';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class cm(Length):
    def define_display_unit(self):
        self.name = 'cm';
    def convert_to_base(self, display_data):
        base_data = display_data/1e2;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*1e2;
        return display_data;
        
class mm(Length):
    def define_display_unit(self):
        self.name = 'mm';
    def convert_to_base(self, display_data):
        base_data = display_data/1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*1e3;
        return display_data;        
        
class km(Length):
    def define_display_unit(self):
        self.name = 'km';
    def convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;
        
class inch(Length):
    def define_display_unit(self):
        self.name = 'inch';
    def convert_to_base(self, display_data):
        base_data = display_data*0.0254;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.0254;
        return display_data;
        
class ft(Length):
    def define_display_unit(self):
        self.name = 'ft';
    def convert_to_base(self, display_data):
        base_data = display_data*12*0.0254;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.0254/12;
        return display_data;
        
class yd(Length):
    def define_display_unit(self):
        self.name = 'yd';
    def convert_to_base(self, display_data):
        base_data = display_data*12*0.0254*3;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.0254/12/3;
        return display_data;
        
#%% Area display unit implementation     
class m2(Area):
    def define_display_unit(self):
        self.name = 'm2';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class sf(Area):
    def define_display_unit(self):
        self.name = 'sf';
    def convert_to_base(self, display_data):
        base_data = display_data/10.7639;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*10.7639;
        return display_data;
        
#%% Volume display unit implementation     
class m3(Volume):
    def define_display_unit(self):
        self.name = 'm3';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class cf(Volume):
    def define_display_unit(self):
        self.name = 'cf';
    def convert_to_base(self, display_data):
        base_data = display_data/35.3147;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*35.3147;
        return display_data; 
        
#%% Mass Flow display unit implementation     
class kg_s(MassFlow):
    def define_display_unit(self):
        self.name = 'kg/s';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Volumetric Flow display unit implementation     
class m3_s(VolumetricFlow):
    def define_display_unit(self):
        self.name = 'm3/s';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
   
class cfm(VolumetricFlow):
    def define_display_unit(self):
        self.name = 'cfm';
    def convert_to_base(self, display_data):
        base_data = display_data/2118.88;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data*2118.88;
        return display_data;
        
#%% Velocity display unit implementation     
class m_s(Velocity):
    def define_display_unit(self):
        self.name = 'm/s';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class mph(Velocity):
    def define_display_unit(self):
        self.name = 'mph';
    def convert_to_base(self, display_data):
        base_data = display_data*0.44704;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.44704;
        return display_data;

class km_h(Velocity):
    def define_display_unit(self):
        self.name = 'km/h';
    def convert_to_base(self, display_data):
        base_data = display_data*0.277778;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/0.277778;
        return display_data;
        
#%% Illuminance display unit implementation     
class lx(Illuminance):
    def define_display_unit(self):
        self.name = 'lx';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class fc(Illuminance):
    def define_display_unit(self):
        self.name = 'fc';
    def convert_to_base(self, display_data):
        base_data = display_data*10.764 ;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/10.764 ;
        return display_data;
        
#%% Luminance display unit implementation     
class cd_m2(Luminance):
    def define_display_unit(self):
        self.name = 'cd/m2';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class nt(Luminance):
    def define_display_unit(self):
        self.name = 'nt';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% EnergyPrice unit implementation     
class cents_kWh(EnergyPrice):
    def define_display_unit(self):
        self.name = 'cents/kWh';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class dol_kWh(EnergyPrice):
    def define_display_unit(self):
        self.name = '$/kWh';
    def convert_to_base(self, display_data):
        base_data = display_data*100;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/100;
        return display_data;
        
class dol_MWh(EnergyPrice):
    def define_display_unit(self):
        self.name = '$/MWh';
    def convert_to_base(self, display_data):
        base_data = display_data*100/1000;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/100*1000;
        return display_data;
        
#%% PowerPrice unit implementation     
class cents_kW(PowerPrice):
    def define_display_unit(self):
        self.name = 'cents/kW';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class dol_kW(PowerPrice):
    def define_display_unit(self):
        self.name = '$/kW';
    def convert_to_base(self, display_data):
        base_data = display_data*100;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/100;
        return display_data;
        
class dol_MW(PowerPrice):
    def define_display_unit(self):
        self.name = '$/MW';
    def convert_to_base(self, display_data):
        base_data = display_data*100/1000;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data/100*1000;
        return display_data;
        
#%% Specific heat capacity unit implementation     
class J_kgK(SpecificHeatCapacity):
    def define_display_unit(self):
        self.name = 'J/(kg.K)';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Heat capacity unit implementation     
class J_K(HeatCapacity):
    def define_display_unit(self):
        self.name = 'J/K';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;           

#%% Heat capacity coefficient unit implementation     
class J_m2K(HeatCapacityCoefficient):
    def define_display_unit(self):
        self.name = 'J/(m2.K)';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Heat resistance unit implementation     
class K_W(HeatResistance):
    def define_display_unit(self):
        self.name = 'K/W';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;     

#%% Heat resistance coefficient unit implementation     
class m2K_W(HeatResistanceCoefficient):
    def define_display_unit(self):
        self.name = '(m2.K)/W';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

#%% Heat transfer coefficient unit implementation     
class W_m2K(HeatTransferCoefficient):
    def define_display_unit(self):
        self.name = 'W/(m2.K)';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Density unit implementation     
class kg_m3(Density):
    def define_display_unit(self):
        self.name = 'kg/m3';
    def convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;