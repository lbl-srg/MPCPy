# -*- coding: utf-8 -*-
"""
optimization.py
by David Blum

This module contains the classes and interfaces for mpc models.
"""

from abc import ABCMeta, abstractmethod
from collections import OrderedDict
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from mpcpy import utility
from mpcpy import variables
from mpcpy import units
from pymodelica import compile_fmu
from pyjmi import transfer_optimization_problem;
from pyjmi.optimization.casadi_collocation import ExternalData

#%% Optimization Class
class Optimization(object):
    '''Class for representing an optimization problem.
        Constraint data uses the following dictionary format:

        { "State Variable Name" : {
              "GTE" : Timeseries variable,
              "LTE" : Timeseries variable,
              "E" : Timeseries variable,
              "Initial" : Static variable,
              "Final" : Static variable},
              "Cyclic" : True}         
        }     
        
        '''
    def __init__(self, Model, problem_type, solver_type, objective_variable, **kwargs):    
        self.Model = Model;
        if 'constraint_data' in kwargs:
            self.constraint_data = kwargs['constraint_data'];
        else:
            self.constraint_data = {};
        self.objective_variable = objective_variable;
        self._problem_type = problem_type();
        self._solver_type = solver_type(self);
    def optimize(self, start_time, final_time, **kwargs):
        self.Model._set_time_interval(start_time, final_time);
        self._problem_type.optimize(self, **kwargs);
    def set_problem_type(self, problem_type, **kwargs):
        self._problem_type = problem_type();       
    def set_solver_type(self, solver_type):
        self._solver_type = solver_type(self);
        
#%% Problem Type Abstract Interface
class Problem(object):
    __metaclass__ = ABCMeta;
    def __init__(self):
        pass;
    @abstractmethod
    def optimize(self):
        pass;      
        
#%% Solver Type Abstract Interface
class Package(object):
    __metaclass__ = ABCMeta;
    @abstractmethod
    def energymin(self):
        pass;
    @abstractmethod
    def energycostmin(self):
        pass;
    @abstractmethod
    def parameterestimate(self):
        pass;          
              
#%% Problem Type Implementation
class EnergyMin(Problem):
    def optimize(self, Optimization, **kwargs):
        Optimization._solver_type.energymin(Optimization);
        
class EnergyCostMin(Problem):
    def optimize(self, Optimization, **kwargs):
        price_data = kwargs['price_data'];
        Optimization._solver_type.energycostmin(Optimization, price_data);
        
class ParameterEstimate(Problem):
    def optimize(self, Optimization, **kwargs):
        Optimization._solver_type.parameterestimate(Optimization, kwargs['measurement_variable_list']);
        
#%% Solver Type Implementation
class JModelica(Package, utility.FMU):
    def __init__(self, Optimization):
        self.Optimization = Optimization;
    
    def energymin(self, Optimization):
        self.Model = Optimization.Model;
        self.measurement_variable_list = {};        
        self.extra_inputs = {};
        self.objective = 'mpc_model.' + Optimization.objective_variable;
        self._initalize_mop();
        self._write_control_mop();
        self._simulate_initial();
        self._solve();
        self._get_control_results(Optimization);           
        
    def energycostmin(self, Optimization, price_data):
        self.Model = Optimization.Model;
        self.measurement_variable_list = {};         
        self.extra_inputs = {};
        self.extra_inputs['pi_e'] = price_data['pi_e'];       
        self.objective = 'mpc_model.' + Optimization.objective_variable + '*pi_e';
        self.measurements = {};
        self._initalize_mop();
        self._write_control_mop();
        self._simulate_initial();
        self._solve();   
        self._get_control_results(Optimization);                                      
        
    def parameterestimate(self, Optimization, measurement_variable_list):
        self.Model = Optimization.Model;
        self.measurement_variable_list = measurement_variable_list;
        self.extra_inputs = {};          
        self.objective = '0';   
        self._initalize_mop();
        self._write_parameter_estimate_mop();
        self._simulate_initial();
        self._solve();
        self._get_parameter_results(Optimization);
        
    def _initalize_mop(self):
        # Open .mo
        mofile = open(self.Model.mopath,'r');
        # Initiate .mop
        self.moppath = self.Model.mopath+'p';        
        self.mopfile = open(self.moppath,'w');
        # Copy .mo
        for line in mofile:
            # Write line to file
            if 'end ' + self.Model.modelpath.split('.')[0] in line:
                break;
            elif 'within ;' not in line and 'uses(Modelica(version=' not in line:
                self.mopfile.write(line);
        mofile.close();                
        # Add initialization model to package.mop (must be same name as model in optimization)
        self.mopfile.write('\n');
        self.mopfile.write('  model ' + self.Model.modelpath.split('.')[-1] + '_initialize\n');
        self.mopfile.write('    ' + self.Model.modelpath.split('.')[-1] + ' mpc_model(\n');
        for key in self.Model.parameter_data.keys()[:-1]:
            self.mopfile.write('     ' + key + '=' + str(self.Model.parameter_data[key]['Value'].get_base_data()) + ',\n');
        self.mopfile.write('     ' + self.Model.parameter_data.keys()[-1] + '=' + str(self.Model.parameter_data[self.Model.parameter_data.keys()[-1]]['Value'].get_base_data()) + ');\n');
        # Instantiate optimization model inputs
        for key in self.Model.input_names:
            self.mopfile.write('    input Real ' + key + '= mpc_model.' + key + ';\n');
        # Add extra inputs required for optimization problem
        self._init_input_names = self.Model.input_names;  
        self.other_inputs = self.Model.other_inputs;
        for key in self.extra_inputs.keys():
            self._init_input_names.append(key);
            self.other_inputs[key] = self.extra_inputs[key];
            self.mopfile.write('    input Real ' + key+';\n');
        # Instantiate cost function
        self.mopfile.write('    Real J(start = 0, fixed=true);\n');
        # Define cost function
        self.mopfile.write('  equation\n');
        self.mopfile.write('    der(J) = '+self.objective+';\n');
        # End initalization model
        self.mopfile.write('  end ' + self.Model.modelpath.split('.')[-1] + '_initialize;\n');
        
    def _write_control_mop(self):
        ## Add control optimization portion to package.mop 
        self.mopfile.write('\n');
        self.mopfile.write('  optimization ' + self.Model.modelpath.split('.')[-1] + '_optimize (objective = (J(finalTime)), startTime=0, finalTime=' + str(self.Model.elapsed_seconds) + ')\n');
        # Instantiate optimization model
        self.mopfile.write('    extends ' + self.Model.modelpath.split('.')[-1] + '_initialize;\n');
        # Remove control variables from input_names for optimization    
        self.opt_input_names = [];
        for key in self._init_input_names:
            if key not in self.Model.control_data.keys():
                self.opt_input_names.append(key);        
        # Instantiate constraint variables as inputs, add to input_names and other_inputs
        for key in self.Optimization.constraint_data.keys():
            for field in self.Optimization.constraint_data[key]:     
                if field != 'Cyclic' and field != 'Final' and field != 'Initial':
                    key_new = key.replace('.', '_') + '_' + field;
                    self.opt_input_names.append(key_new);
                    self.other_inputs[key_new] = self.Optimization.constraint_data[key][field];
                    self.mopfile.write('    input Real ' + key_new + ';\n');
        # Define constraint_data
        self.mopfile.write('  constraint\n');
        for key in self.Optimization.constraint_data.keys():
            for field in self.Optimization.constraint_data[key]:
                key_new = key.replace('.', '_') + '_' + field;                
                if field == 'GTE':
                    self.mopfile.write('    mpc_model.' + key + ' >= ' + key_new + ';\n');
                elif field == 'dGTE':
                    self.mopfile.write('    der(mpc_model.' + key + ') >= ' + key_new + ';\n');                    
                elif field == 'LTE':
                    self.mopfile.write('    mpc_model.' + key + ' <= ' + key_new + ';\n');
                elif field == 'dLTE':
                    self.mopfile.write('    der(mpc_model.' + key + ') <= ' + key_new + ';\n');                      
                elif field == 'Initial':
                    self.mopfile.write('    mpc_model.' + key + '(startTime)=' + str(self.Optimization.constraint_data[key][field].get_base_data()) + ';\n');
                elif field == 'Final':
                    self.mopfile.write('    mpc_model.' + key + '(finalTime)=' + str(self.Optimization.constraint_data[key][field].get_base_data()) + ';\n');
                elif field == 'Cyclic':
                    self.mopfile.write('    mpc_model.' + key + '(startTime)=mpc_model.' + key + '(finalTime);\n');                   
        # End optimization portion of package.mop
        self.mopfile.write('  end ' + self.Model.modelpath.split('.')[-1] + '_optimize;\n');
        # End package.mop and save    
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[0] + ';\n'); 
        # Close files
        self.mopfile.close();      
        
    def _write_parameter_estimate_mop(self):
        # Add parameter estimation optimization portion to package.mop
        self.mopfile.write('\n');
        self.mopfile.write('optimization ' + self.Model.modelpath.split('.')[-1] + '_optimize (startTime=0, finalTime=' + str(self.Model.elapsed_seconds) + ')\n');
        #  Instantiate MPC model with free parameters
        i = 1;
        free_parameters = [];
        for key in self.Model.parameter_data.keys():
            if self.Model.parameter_data[key]['Free'].get_base_data():
                free_parameters.append(key);
        I = len(free_parameters);
        for key in free_parameters:
            if i == 1:
                line = '    extends ' + self.Model.modelpath.split('.')[-1] + '_initialize (mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'),\n';
            elif i == I:
                line = '      mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'));\n';
            else:
                line = '      mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'),\n';
            self.mopfile.write(line);
            i = i + 1;    
        # End optimization portion of package.mop
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[-1] + '_optimize;\n');
        # End package.mop and save    
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[0] + ';\n');
        # Close files
        self.mopfile.close();
        
    def _simulate_initial(self):
        # Compile the optimization initializaiton model                                             
        self.fmupath = compile_fmu(self.Model.modelpath + '_initialize', \
                                   self.moppath, \
                                   compiler_options = {'extra_lib_dirs':self.Model.libraries});
        # Set Exogenous
        self.weather_data = self.Model.weather_data;
        self.internal_data = self.Model.internal_data;
        self.control_data = self.Model.control_data;
        if type(self.Optimization._problem_type) is ParameterEstimate:
            plt.figure(1)
            self.other_inputs = self.Model.other_inputs;
            self.opt_input_names = self._init_input_names;
            # Otherwise inputs set by write control mop
        # Set input_names
        self.input_names = self._init_input_names;
        # Set parameters, set in hard code during mop writing
        self.parameter_data = {};  
        # Set measurements
        self.measurements = {};
        for key in self.Model.measurements.keys():
            self.measurements['mpc_model.' + key] = self.Model.measurements[key];           
        # Set timing
        self.start_time_utc = self.Model.start_time_utc;
        self.final_time_utc = self.Model.final_time_utc;     
        self.elapsed_seconds = self.Model.elapsed_seconds;        
        # Simulate fmu
        self._simulate_fmu();
        # Store initial simulation
        self.res_init = self._res;
                                            
    def _solve(self):
        # Create input_mpcpy_ts_list
        self._create_input_mpcpy_ts_list_opt();
        # Set inputs
        self._create_input_object_from_input_mpcpy_ts_list(self._input_mpcpy_ts_list_opt);          
        # Create ExternalData structure
        self._create_external_data();
        # Transfer optimization problem to casADi                         
        self.opt_problem = transfer_optimization_problem(self.Model.modelpath + '_optimize', \
                                                         self.moppath, \
                                                         compiler_options = {'extra_lib_dirs':self.Model.libraries});
        # Set optimization options
        self.opt_opts = self.opt_problem.optimize_options()
        self.opt_opts['external_data'] = self.external_data;
        self.opt_opts['init_traj'] = self.res_init;
        self.opt_opts['nominal_traj'] = self.res_init;
        self.opt_opts['n_e'] = self.sim_opts['ncp'];
        # Optimize
        self.res_opt = self.opt_problem.optimize(options=self.opt_opts);
        print(self.res_opt.get_solver_statistics());
        
    def _create_external_data(self):   
        # Create measurement trajectory object to be input in training
        quad_pen = OrderedDict();  
        N_mea = 0;
        if self.measurement_variable_list:
            for key in self.measurement_variable_list:
                df = self.Model.measurements[key]['Measured'].get_base_data()[self.Model.start_time:self.Model.final_time].to_frame();
                df_simtime = self.add_simtime_column(df);
                mea_traj = np.vstack((df_simtime['SimTime'].get_values(), \
                                     df_simtime[key].get_values()));
                quad_pen['mpc_model.' + key] = mea_traj;
                N_mea = N_mea + 1;
        else:
            Q = None;
        # Create objective error weights
        Q = np.diag(np.ones(N_mea));
        # Eliminate inputs from optimization problem 
        eliminated = {};
        i = 1;
        N_input = 0;
        if self.input_object != {}:
            for key in self.input_object[0]:
                input_traj = np.vstack((np.transpose(self.input_object[1][:,0]), \
                                       np.transpose(self.input_object[1][:,i])));
                eliminated[key] = input_traj; 
                N_input = N_input + 1;
                i = i + 1;           
        # Create ExternalData structure
        self.external_data = ExternalData(Q=Q, quad_pen=quad_pen, eliminated=eliminated);
        
    def _get_control_results(self, Optimization):
        fmu_variable_units = self.get_fmu_variable_units();                                     
        for key in self.Model.control_data.keys():
            data = self.res_opt['mpc_model.' + key];
            time = self.res_opt['time'];
            timedelta = pd.to_timedelta(time, 's');
            timeindex = self.start_time_utc + timedelta;
            ts = pd.Series(data = data, index = timeindex);
            ts.name = key;
            unit = self.get_unit_class_from_fmu_variable_units('mpc_model.' + key,fmu_variable_units);
            if not unit:
                unit = units.unit1;                
            Optimization.Model.control_data[key] = variables.Timeseries(key, ts, unit);  
        for key in Optimization.Model.measurements.keys():
            data = self.res_opt['mpc_model.' + key];
            time = self.res_opt['time'];
            timedelta = pd.to_timedelta(time, 's');
            timeindex = self.start_time_utc + timedelta;
            ts = pd.Series(data = data, index = timeindex);
            ts.name = key;
            unit = self.get_unit_class_from_fmu_variable_units('mpc_model.' + key,fmu_variable_units);
            if not unit:
                unit = units.unit1;                
            Optimization.Model.measurements[key]['Simulated'] = variables.Timeseries(key, ts, unit);
            
    def _get_parameter_results(self, Optimization):
        for key in Optimization.Model.parameter_data.keys():
            if Optimization.Model.parameter_data[key]['Free'].get_base_data():
                self.fmu_variable_units = self.get_fmu_variable_units();
                unit_class = self.get_unit_class_from_fmu_variable_units('mpc_model.'+key, self.fmu_variable_units);
                data = self.res_opt.initial('mpc_model.' + key);
                Optimization.Model.parameter_data[key]['Value'].set_display_unit(unit_class);
                Optimization.Model.parameter_data[key]['Value'].set_data(data);        
        
