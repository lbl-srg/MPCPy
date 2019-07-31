# -*- coding: utf-8 -*-
"""
``units`` classes manage the conversion of units for MPCPy variables.  See 
documentation on ``variables`` for more information.

"""

from abc import ABCMeta, abstractmethod
import numpy as np

#%% Display unit abstract interface
class _DisplayUnit(object):
    __metaclass__ = ABCMeta; 
    @abstractmethod
    def _define_quantity(self):
        pass;
    @abstractmethod
    def _define_display_unit(self):
        pass;           
    @abstractmethod
    def _convert_to_base(self):
        pass;
    @abstractmethod
    def _convert_from_base(self):
        pass;
    def __init__(self, variable):
        self._define_quantity(variable);
        self._define_display_unit();       

#%% Display unit quantity implementation
class _Boolean(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Boolean';
        variable.base_unit = boolean_integer;
        
class _Temperature(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Temperature';
        variable.base_unit = K;
        
class _Power(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Power';
        variable.base_unit = W;
        
class _Energy(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Energy';
        variable.base_unit = J;

class _PowerFlux(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'PowerFlux';
        variable.base_unit = W_m2;
        
class _EnergyIntensity(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'EnergyIntensity';
        variable.base_unit = J_m2; 
        
class _Pressure(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Pressure';
        variable.base_unit = Pa;
        
class _DimensionlessRatio(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'DimensionlessRatio';
        variable.base_unit = unit1;
        
class _Angle(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Angle';
        variable.base_unit = rad;
        
class _Time(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Time';
        variable.base_unit = s;       
        
class _Mass(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Mass';
        variable.base_unit = kg;         

class _Length(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Length';
        variable.base_unit = m;

class _Area(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Area';
        variable.base_unit = m2;
        
class _Volume(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Volume';
        variable.base_unit = m3;
        
class _MassFlow(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'MassFlow';
        variable.base_unit = kg_s;
        
class _VolumetricFlow(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'VolumetricFlow';
        variable.base_unit = m3_s;
        
class _Velocity(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Velocity';
        variable.base_unit = m_s;
        
class _Illuminance(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Illuminance';
        variable.base_unit = lx;

class _Luminance(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Luminance';
        variable.base_unit = cd_m2;
        
class _EnergyPrice(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'EnergyPrice';
        variable.base_unit = dol_J;
        
class _PowerPrice(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'PowerPrice';
        variable.base_unit = dol_W;
        
class _SpecificHeatCapacity(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'SpecificHeatCapacity';
        variable.base_unit = J_kgK;   

class _HeatCapacity(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'HeatCapacity';
        variable.base_unit = J_K;
        
class _HeatCapacityCoefficient(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'HeatCapacityCoefficient';
        variable.base_unit = J_m2K;        

class _HeatResistance(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'HeatResistance';
        variable.base_unit = K_W;
        
class _HeatResistanceCoefficient(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'HeatResistanceCoefficient';
        variable.base_unit = m2K_W;        

class _HeatTransferCoefficient(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'HeatTransferCoefficient';
        variable.base_unit = W_m2K;
        
class _Density(_DisplayUnit):
    def _define_quantity(self, variable):
        variable.quantity_name = 'Density';
        variable.base_unit = kg_m3;          

#%% Boolean display unit implementation     
class boolean_integer(_Boolean):
    def _define_display_unit(self):
        self.name = 'boolean_integer';
    def _convert_to_base(self, display_data):
        base_data = int(display_data);
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class boolean(_Boolean):
    def _define_display_unit(self):
        self.name = 'boolean';
    def _convert_to_base(self, display_data):
        base_data = int(display_data);
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = bool(base_data);
        return display_data;
        
#%% Temperature display unit implementation
class K(_Temperature):
    def _define_display_unit(self):
        self.name = 'K';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class degC(_Temperature):
    def _define_display_unit(self):
        self.name = 'degC';
    def _convert_to_base(self, display_data):
        base_data = display_data + 273.15;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data - 273.15;
        return display_data;
        
class degF(_Temperature):
    def _define_display_unit(self):
        self.name = 'degF';
    def _convert_to_base(self, display_data):
        base_data = (display_data-32)*5/9 + 273.15;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = (base_data-273.15)*9/5 + 32;
        return display_data;

class degR(_Temperature):
    def _define_display_unit(self):
        self.name = 'degR';
    def _convert_to_base(self, display_data):
        base_data = ((display_data - 459.67)-32)*5/9 + 273.15;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = (base_data-273.15)*9/5 + 32 + 459.67;
        return display_data;
        
#%% Power display unit implementation     
class W(_Power):
    def _define_display_unit(self):
        self.name = 'W';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kW(_Power):
    def _define_display_unit(self):
        self.name = 'kW';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;
        
class MW(_Power):
    def _define_display_unit(self):
        self.name = 'MW';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;        
        
class Btuh(_Power):
    def _define_display_unit(self):
        self.name = 'Btuh';
    def _convert_to_base(self, display_data):
        base_data = display_data*0.29307107;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.29307107;
        return display_data;
        
class kBtuh(_Power):
    def _define_display_unit(self):
        self.name = 'kBtuh';
    def _convert_to_base(self, display_data):
        base_data = (display_data*1e3)*0.29307107;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.29307107/1e3;
        return display_data;
        
class hp(_Power):
    def _define_display_unit(self):
        self.name = 'hp';
    def _convert_to_base(self, display_data):
        base_data = display_data*745.699872;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/745.699872;
        return display_data;
        
#%% Energy display unit implementation     
class J(_Energy):
    def _define_display_unit(self):
        self.name = 'J';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kJ(_Energy):
    def _define_display_unit(self):
        self.name = 'kJ';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;

class MJ(_Energy):
    def _define_display_unit(self):
        self.name = 'MJ';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;
        
class Btu(_Energy):
    def _define_display_unit(self):
        self.name = 'Btu';
    def _convert_to_base(self, display_data):
        base_data = display_data*1055.05585;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1055.05585;
        return display_data;

class kBtu(_Energy):
    def _define_display_unit(self):
        self.name = 'kBtu';
    def _convert_to_base(self, display_data):
        base_data = (display_data*1e3)*1055.05585;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1055.05585/1e3;
        return display_data;
        
class Wh(_Energy):
    def _define_display_unit(self):
        self.name = 'Wh';
    def _convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data; 
        
class kWh(_Energy):
    def _define_display_unit(self):
        self.name = 'kWh';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600/1e3;
        return display_data;

class MWh(_Energy):
    def _define_display_unit(self):
        self.name = 'MWh';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e6*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600/1e6;
        return display_data;
        
#%% Power Flux display unit implementation     
class W_m2(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'W/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kW_m2(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'kW/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;        

class W_sf(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'W/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/10.7639;
        return display_data;
        
class kW_sf(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'kW/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/10.7639/1e3;
        return display_data;        
        
class Btuh_sf(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'Btuh/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*3.154594;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3.154594;
        return display_data;
        
class kBtuh_sf(_PowerFlux):
    def _define_display_unit(self):
        self.name = 'kBtuh/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*3.154594;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3.154594/1e3;
        return display_data;        
        
#%% Energy Intensity display unit implementation     
class J_m2(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'J/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class Wh_m2(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'Wh/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data;
        
class kWh_m2(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'kWh/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600/1e3;
        return display_data;
        
class Wh_sf(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'Wh/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*3600*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600/10.7639;
        return display_data;
        
class kWh_sf(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'kWh/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*3600*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600/10.7639/1e3;
        return display_data;
        
class Btu_sf(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'Btu/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*1055.05585*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1055.05585/10.7639;
        return display_data;
        
class kBtu_sf(_EnergyIntensity):
    def _define_display_unit(self):
        self.name = 'kBtu/sf';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3*1055.05585*10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1055.05585/10.7639/1e3;
        return display_data;
        
#%% Pressure display unit implementation     
class Pa(_Pressure):
    def _define_display_unit(self):
        self.name = 'Pa';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class kPa(_Pressure):
    def _define_display_unit(self):
        self.name = 'kPa';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data; 

class MPa(_Pressure):        
    def _define_display_unit(self):
        self.name = 'MPa';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e6;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e6;
        return display_data;        
        
class bar(_Pressure):
    def _define_display_unit(self):
        self.name = 'bar';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e5;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e5;
        return display_data;

class inwg(_Pressure):
    def _define_display_unit(self):
        self.name = 'inwg';
    def _convert_to_base(self, display_data):
        base_data = display_data*248.84;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/248.84;
        return display_data;
        
class inHg(_Pressure):
    def _define_display_unit(self):
        self.name = 'inHg';
    def _convert_to_base(self, display_data):
        base_data = display_data*3386.389;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3386.389;
        return display_data; 
        
class psi(_Pressure):
    def _define_display_unit(self):
        self.name = 'psi';
    def _convert_to_base(self, display_data):
        base_data = display_data*6894.757;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/6894.757;
        return display_data;
        
class atm(_Pressure):
    def _define_display_unit(self):
        self.name = 'atm';
    def _convert_to_base(self, display_data):
        base_data = display_data*101325;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/101325;
        return display_data;
        
#%% Dimensionless Ratio display unit implementation     
class unit1(_DimensionlessRatio):
    def _define_display_unit(self):
        self.name = '1';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class percent(_DimensionlessRatio):
    def _define_display_unit(self):
        self.name = 'percent';
    def _convert_to_base(self, display_data):
        base_data = display_data/100;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*100;
        return display_data;
        
class unit10(_DimensionlessRatio):
    def _define_display_unit(self):
        self.name = '10';
    def _convert_to_base(self, display_data):
        base_data = display_data/10;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*10;
        return display_data;        
        
#%% Angle display unit implementation     
class rad(_Angle):
    def _define_display_unit(self):
        self.name = 'rad';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class deg(_Angle):
    def _define_display_unit(self):
        self.name = 'deg';
    def _convert_to_base(self, display_data):
        base_data = display_data/180*np.pi;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*180/np.pi;
        return display_data;
        
#%% Time display unit implementation     
class s(_Time):
    def _define_display_unit(self):
        self.name = 's';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class minute(_Time):
    def _define_display_unit(self):
        self.name = 'min';
    def _convert_to_base(self, display_data):
        base_data = display_data*60;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/60;
        return display_data;

class hour(_Time):
    def _define_display_unit(self):
        self.name = 'h';
    def _convert_to_base(self, display_data):
        base_data = display_data*3600;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/3600;
        return display_data;
        
class day(_Time):
    def _define_display_unit(self):
        self.name = 'd';
    def _convert_to_base(self, display_data):
        base_data = display_data*86400;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/86400;
        return display_data;
        
#%% Mass display unit implementation     
class kg(_Mass):
    def _define_display_unit(self):
        self.name = 'kg';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;  
        
#%% Length display unit implementation     
class m(_Length):
    def _define_display_unit(self):
        self.name = 'm';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class cm(_Length):
    def _define_display_unit(self):
        self.name = 'cm';
    def _convert_to_base(self, display_data):
        base_data = display_data/1e2;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*1e2;
        return display_data;
        
class mm(_Length):
    def _define_display_unit(self):
        self.name = 'mm';
    def _convert_to_base(self, display_data):
        base_data = display_data/1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*1e3;
        return display_data;        
        
class km(_Length):
    def _define_display_unit(self):
        self.name = 'km';
    def _convert_to_base(self, display_data):
        base_data = display_data*1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/1e3;
        return display_data;
        
class inch(_Length):
    def _define_display_unit(self):
        self.name = 'inch';
    def _convert_to_base(self, display_data):
        base_data = display_data*0.0254;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.0254;
        return display_data;
        
class ft(_Length):
    def _define_display_unit(self):
        self.name = 'ft';
    def _convert_to_base(self, display_data):
        base_data = display_data*12*0.0254;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.0254/12;
        return display_data;
        
class yd(_Length):
    def _define_display_unit(self):
        self.name = 'yd';
    def _convert_to_base(self, display_data):
        base_data = display_data*12*0.0254*3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.0254/12/3;
        return display_data;
        
#%% Area display unit implementation     
class m2(_Area):
    def _define_display_unit(self):
        self.name = 'm2';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

class sf(_Area):
    def _define_display_unit(self):
        self.name = 'sf';
    def _convert_to_base(self, display_data):
        base_data = display_data/10.7639;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*10.7639;
        return display_data;
        
#%% Volume display unit implementation     
class m3(_Volume):
    def _define_display_unit(self):
        self.name = 'm3';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class cf(_Volume):
    def _define_display_unit(self):
        self.name = 'cf';
    def _convert_to_base(self, display_data):
        base_data = display_data/35.3147;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*35.3147;
        return display_data; 
        
#%% Mass Flow display unit implementation     
class kg_s(_MassFlow):
    def _define_display_unit(self):
        self.name = 'kg/s';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Volumetric Flow display unit implementation     
class m3_s(_VolumetricFlow):
    def _define_display_unit(self):
        self.name = 'm3/s';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
   
class cfm(_VolumetricFlow):
    def _define_display_unit(self):
        self.name = 'cfm';
    def _convert_to_base(self, display_data):
        base_data = display_data/2118.88;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*2118.88;
        return display_data;
        
#%% Velocity display unit implementation     
class m_s(_Velocity):
    def _define_display_unit(self):
        self.name = 'm/s';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class mph(_Velocity):
    def _define_display_unit(self):
        self.name = 'mph';
    def _convert_to_base(self, display_data):
        base_data = display_data*0.44704;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.44704;
        return display_data;

class km_h(_Velocity):
    def _define_display_unit(self):
        self.name = 'km/h';
    def _convert_to_base(self, display_data):
        base_data = display_data*0.277778;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/0.277778;
        return display_data;
        
#%% Illuminance display unit implementation     
class lx(_Illuminance):
    def _define_display_unit(self):
        self.name = 'lx';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class fc(_Illuminance):
    def _define_display_unit(self):
        self.name = 'fc';
    def _convert_to_base(self, display_data):
        base_data = display_data*10.764 ;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data/10.764 ;
        return display_data;
        
#%% Luminance display unit implementation     
class cd_m2(_Luminance):
    def _define_display_unit(self):
        self.name = 'cd/m2';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
class nt(_Luminance):
    def _define_display_unit(self):
        self.name = 'nt';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% EnergyPrice unit implementation     
class cents_kWh(_EnergyPrice):
    def _define_display_unit(self):
        self.name = 'cents/kWh';
    def _convert_to_base(self, display_data):
        base_data = display_data/3.6e8;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*3.6e8;
        return display_data;
        
class dol_kWh(_EnergyPrice):
    def _define_display_unit(self):
        self.name = '$/kWh';
    def _convert_to_base(self, display_data):
        base_data = display_data/3.6e6;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*3.6e6;
        return display_data;
        
class dol_MWh(_EnergyPrice):
    def _define_display_unit(self):
        self.name = '$/MWh';
    def _convert_to_base(self, display_data):
        base_data = display_data/3.6e9;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*3.6e9;
        return display_data;

class dol_J(_EnergyPrice):
    def _define_display_unit(self):
        self.name = '$/J';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% PowerPrice unit implementation     
class cents_kW(_PowerPrice):
    def _define_display_unit(self):
        self.name = 'cents/kW';
    def _convert_to_base(self, display_data):
        base_data = display_data/1e5;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*1e5;
        return display_data;
        
class dol_kW(_PowerPrice):
    def _define_display_unit(self):
        self.name = '$/kW';
    def _convert_to_base(self, display_data):
        base_data = display_data/1e3;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*1e3;
        return display_data;
        
class dol_MW(_PowerPrice):
    def _define_display_unit(self):
        self.name = '$/MW';
    def _convert_to_base(self, display_data):
        base_data = display_data/1e6;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data*1e6;
        return display_data;

class dol_W(_PowerPrice):
    def _define_display_unit(self):
        self.name = '$/W';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Specific heat capacity unit implementation     
class J_kgK(_SpecificHeatCapacity):
    def _define_display_unit(self):
        self.name = 'J/(kg.K)';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Heat capacity unit implementation     
class J_K(_HeatCapacity):
    def _define_display_unit(self):
        self.name = 'J/K';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;           

#%% Heat capacity coefficient unit implementation     
class J_m2K(_HeatCapacityCoefficient):
    def _define_display_unit(self):
        self.name = 'J/(m2.K)';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Heat resistance unit implementation     
class K_W(_HeatResistance):
    def _define_display_unit(self):
        self.name = 'K/W';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;     

#%% Heat resistance coefficient unit implementation     
class m2K_W(_HeatResistanceCoefficient):
    def _define_display_unit(self):
        self.name = '(m2.K)/W';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;

#%% Heat transfer coefficient unit implementation     
class W_m2K(_HeatTransferCoefficient):
    def _define_display_unit(self):
        self.name = 'W/(m2.K)';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;
        
#%% Density unit implementation     
class kg_m3(_Density):
    def _define_display_unit(self):
        self.name = 'kg/m3';
    def _convert_to_base(self, display_data):
        base_data = display_data;
        return base_data;
    def _convert_from_base(self, base_data):
        display_data = base_data;
        return display_data;