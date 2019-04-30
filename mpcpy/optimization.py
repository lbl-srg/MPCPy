# -*- coding: utf-8 -*-
"""
``Optimization`` objects setup and solve mpc control optimization problems.
The optimization uses ``models`` objects to  setup and solve the specified
optimization problem type with the specified optimization package type.
Constraint informaiton can be added to the optimization problem through the
use of the constraint ``exodata`` object. Please see the ``exodata``
documentation for more information.

Classes
=======

.. autoclass:: mpcpy.optimization.Optimization
    :members: optimize, set_problem_type, set_package_type,
              get_optimization_options, set_optimization_options,
              get_optimization_statistics,

Problem Types
=============

.. autoclass:: mpcpy.optimization.EnergyMin

.. autoclass:: mpcpy.optimization.EnergyCostMin

Package Types
=============

.. autoclass:: mpcpy.optimization.JModelica

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
import copy

#%% Optimization Class
class Optimization(utility._mpcpyPandas, utility._Measurements):
    '''Class for representing an optimization problem.

    Parameters
    ----------
    Model :  mpcpy.model object
        Model with which to perform the optimization.
    problem_type : mpcpy.optimization.problem_type
        The type of poptimization problem to solve.  See specific documentation
        on available problem types.
    package_type : mpcpy.optimization.package_type
        The software package used to solve the optimization problem.  The model
        is translated into an optimization problem accoding to the problem_type
        to be solved in the specified package_type.  See specific documentation
        on available package types.
    objective_variable : string
        The name of the model variable to be used in the objective function.
    constraint_data : dictionary, optional
        ``exodata`` constraint object data attribute.


    Attributes
    ----------
    Model :  mpcpy.model object
        Model with which to perform the optimization.
    objective_variable : string
        The name of the model variable to be used in the objective function.
    constraint_data : dictionary
        ``exodata`` constraint object data attribute.

    '''

    def __init__(self, Model, problem_type, package_type, objective_variable, **kwargs):
        '''Constructor of an optimization problem object.

        '''

        self.Model = Model;
        if 'constraint_data' in kwargs:
            self.constraint_data = kwargs['constraint_data'];
        else:
            self.constraint_data = {};
        self.objective_variable = objective_variable;
        self._problem_type = problem_type();
        self._package_type = package_type(self);
        self.tz_name = Model.tz_name

    def optimize(self, start_time, final_time, **kwargs):
        '''Solve the optimization problem over the specified time horizon.

        Consult the documentation for the solver package type for available
        kwargs.

        Parameters
        ----------
        start_time : string
            Start time of estimation period.
        final_time : string
            Final time of estimation period.

        Yields
        ------
        Upon solving the optimization problem, this method updates the
        ``Model.control_data`` dictionary with the optimal control
        timeseries for each control variable for the time period of
        optimization.  If the optimization horizon extends past the
        final time of ``Model.control_data``, then the extra data is
        appended.  Also creates the Optimization.measurements dictionary
        with the optimization solution measurements under the
        ``'Simulated'`` key.  This is created for the variables defined in
        ``Model.measurements``.

        '''

        # Check for continue
        if start_time == 'continue':
            raise ValueError('"continue" is not a valid entry for start_time for optimization problems.')
        self._set_time_interval(start_time, final_time);
        self._problem_type._optimize(self, **kwargs);

    def set_problem_type(self, problem_type):
        '''Set the problem type of the optimization.

        Note that optimization options will be reset.

        Parameters
        ----------
        problem_type : mpcpy.optimization.problem_type
            New problem type to solve.  See specific documentation
            on available problem types.

        '''

        self._problem_type = problem_type();
        package_type = type(self._package_type);
        self._package_type = package_type(self);

    def set_package_type(self, package_type):
        '''Set the solver package type of the optimization.

        Parameters
        ----------
        package_type : mpcpy.optimization.package_type
            New software package type to use to solve the optimization problem.
            See specific documentation on available package types.

        '''

        self._package_type = package_type(self);

    def get_optimization_options(self):
        '''Get the options for the optimization solver package.

        Returns
        -------
        opt_options : dictionary
            The options for the optimization solver package.  See specific
            documentation on solver package for more information.

        '''

        return self._package_type._get_optimization_options();

    def set_optimization_options(self, opt_options):
        '''Set the options for the optimization solver package.

        Parameters
        ----------
        opt_options : dictionary
            The options for the optimization solver package.  See specific
            documentation on solver package for more information.

        '''

        return self._package_type._set_optimization_options(opt_options);

    def get_optimization_statistics(self):
        '''Get the optimization result statistics from the solver package.

        Returns
        -------
        opt_statistics : dictionary
            The options for the optimization solver package.  See specific
            documentation on solver package for more information.

        '''
        opt_statistics = self._package_type._get_optimization_statistics();
        return opt_statistics;

#%% Problem Type Abstract Interface
class _Problem(object):
    '''Interface for a problem type.

    '''

    __metaclass__ = ABCMeta;

    def __init__(self):
        '''Constructor of a problem type object.

        '''

        pass;

    @abstractmethod
    def _optimize():
        '''Optimization-problem specific call to solve the problem.

        Parameters
        ----------
        Optimization : mpcpy.optimization.Optimization object
            The optimization object containing the Model and solver package
            attributes.

        '''

        pass;

    @abstractmethod
    def _setup_jmodelica():
        '''Setup the problem with JModelica.

        Parameters
        ----------
        JModelica : mpcpy.optimization.JModelica object
            The JModelica solver package object.
        Optimization : mpcpy.optimization.Optimization object
            The optimization object containing the Model and solver package
            attributes.

        '''

        pass;

#%% Solver Type Abstract Interface
class _Package(object):
    '''Interface for a solver package type.

    '''

    __metaclass__ = ABCMeta;

    @abstractmethod
    def _energymin(self):
        '''Optimization package-specific call to minimize the integral of the
        objective variable over the time horizon.

        Yields
        ------
        Upon solving the optimization problem, this method updates the
        ``Optimization.Model.control_data`` dictionary with the optimal control
        timeseries for each control variable and creates the
        Optimization.measurements dictionary with the optimization solution
        measurements under the ``'Simulated'`` key.

        '''

        pass;

    @abstractmethod
    def _energycostmin(self):
        '''Optimization package-specific call to minimize the integral of the
        objective variable times a time-varying weight over the time horizon.

        Yields
        ------
        Upon solving the optimization problem, this method updates the
        ``Optimization.Model.control_data`` dictionary with the optimal control
        timeseries for each control variable and creates the
        Optimization.measurements dictionary with the optimization solution
        measurements under the ``'Simulated'`` key.

        '''

        pass;

    @abstractmethod
    def _parameterestimate(self):
        '''Optimization package-specific call to minimize the error between
        simulated and measured data by tuning model parameters.

        Yields
        ------
        Upon solving the optimization problem, this method updates the
        ``Optimization.Model.parameter_data`` dictionary ``'Value`'' key
        for each parameter with the estimated value.

        '''

        pass;

    @abstractmethod
    def _get_optimization_options(self):
        '''Get the optimization options of the solver package in a dictionary.

        '''

        pass;

    @abstractmethod
    def _set_optimization_options(self):
        '''Set the optimization options of the solver package from a dictionary.

        '''

        pass;

    @abstractmethod
    def _get_optimization_statistics(self):
        '''Get the optimization result statistics from the solver package.

        '''

        pass;

#%% Problem Type Implementation
class EnergyMin(_Problem):
    '''Minimize the integral of the objective variable over the time
    horizon.

    '''

    def _optimize(self, Optimization, **kwargs):
        '''Solve the energy minimization problem.

        '''

        Optimization._package_type._energymin(Optimization, **kwargs);

    def _setup_jmodelica(self, JModelica, Optimization):
        '''Setup the optimization problem for JModelica.

        '''

        JModelica.Model = Optimization.Model;
        JModelica._create_slack_variables(Optimization);
        JModelica.objective = 'mpc_model.' + Optimization.objective_variable;
        for var in JModelica.slack_vars.keys():
            JModelica.objective = JModelica.objective + ' + 1000*({0})'.format(JModelica.slack_vars[var]['Expression'])
        JModelica.extra_inputs = {};
        JModelica._initalize_mop();
        JModelica._write_control_mop(Optimization);
        JModelica._compile_transfer_problem();

class EnergyCostMin(_Problem):
    '''Minimize the integral of the objective variable multiplied by a
    time-varying weighting factor over the time horizon.

    '''

    def _optimize(self, Optimization, **kwargs):
        '''Solve the energy cost minimization problem.

        '''

        Optimization._package_type._energycostmin(Optimization, **kwargs);

    def _setup_jmodelica(self, JModelica, Optimization):
        '''Setup the optimization problem for JModelica.

        '''

        JModelica.Model = Optimization.Model;
        JModelica._create_slack_variables(Optimization)
        JModelica.objective = 'mpc_model.' + Optimization.objective_variable + '*pi_e';
        for var in JModelica.slack_vars.keys():
            JModelica.objective = JModelica.objective + ' + ({0})'.format(JModelica.slack_vars[var]['Expression'])
        JModelica.extra_inputs = {};
        JModelica.extra_inputs['pi_e'] = [];
        JModelica._initalize_mop();
        JModelica._write_control_mop(Optimization);
        JModelica._compile_transfer_problem();

class _ParameterEstimate(_Problem):
    '''Minimize the error between simulated and measured data by adjusting
    time-invariant parameters of the model.

    To be called from mpcpy.models.JModelica only.

    '''

    def _optimize(self, Optimization, **kwargs):
        '''Solve the parameter estimation problem.

        '''

        Optimization._package_type._parameterestimate(Optimization, kwargs['measurement_variable_list']);

    def _setup_jmodelica(self, JModelica, Optimization):
        '''Setup the optimization problem for JModelica.

        '''

        JModelica.Model = Optimization.Model;
        JModelica._create_slack_variables(Optimization)
        JModelica.objective = '0';
        JModelica.extra_inputs = {};
        JModelica._initalize_mop();
        JModelica._write_parameter_estimate_mop();
        JModelica._compile_transfer_problem();

#%% Solver Type Implementation
class JModelica(_Package, utility._FMU):
    '''Use JModelica to solve the optimization problem.

    This package is compatible with ``models.Modelica`` objects.  Please
    consult the JModelica user guide for more information regarding
    optimization options and solver statistics.

    The option 'n_e' is overwritten by default to equal the number of
    points as calculated using the model measurements sample rate and
    length of optimization horizon (same as if model is simulated).
    However, editing this option will overwrite this default.

    Notes
    -----
    ``optimize()`` kwargs:

    res_control_step : int, optional
        The time interval in seconds at which the model.control_data is
        updated with the optimal control results.  The control data comes
        from evaluating the optimal input collocation polynomials at the
        specified time interval.
        The default value is the interval returned by JModelica according
        to the 'result_mode' option.  See JModelica documentation for more
        details.
    price_data : dictionary
        ``exodata`` price object data attribute.
        For EnergyCostMin problems only.

    '''

    def __init__(self, Optimization):
        '''Constructor of the JModelica solver package class.

        '''

        # Setup JModelica optimization problem
        Optimization._problem_type._setup_jmodelica(self, Optimization);
        # Set default optimization options
        self._set_optimization_options(self.opt_problem.optimize_options(), init = True)

    def _energymin(self, Optimization, **kwargs):
        '''Perform the energy minimization.

        '''

        self._simulate_initial(Optimization);
        self._solve(Optimization);
        self._get_control_results(Optimization, **kwargs);

    def _energycostmin(self, Optimization, **kwargs):
        '''Perform the energy cost minimization.

        '''

        price_data = kwargs['price_data'];
        self.other_inputs['pi_e'] = price_data['pi_e'];
        self._simulate_initial(Optimization);
        self._solve(Optimization);
        self._get_control_results(Optimization, **kwargs);

    def _parameterestimate(self, Optimization, measurement_variable_list):
        '''Perform the parameter estimation.

        '''

        self.measurement_variable_list = measurement_variable_list;
        self._simulate_initial(Optimization);
        self._solve(Optimization);
        self._get_parameter_results(Optimization);

    def _initalize_mop(self):
        '''Start writing the mop file.

        '''

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
            elif 'within ;' not in line and 'annotation (uses' not in line and '(version="' not in line:
                self.mopfile.write(line);
        mofile.close();
        # Add initialization model to package.mop (must be same name as model in optimization)
        self.mopfile.write('\n');
        self.mopfile.write('  model ' + self.Model.modelpath.split('.')[-1] + '_initialize\n');
        package = self.Model.modelpath.split('.')[1:];
        self.mopfile.write('    ' + '.'.join(package) + ' mpc_model();\n');
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
        # Add slack variable inputs required for optimization probelm (initial guess is 0 by default)
        for key_new in self.slack_vars.keys():
            self.mopfile.write('    input Real ' + self.slack_vars[key_new]['SlackVar']+';\n');           
        # Instantiate cost function
        self.mopfile.write('    Real J(start = 0, fixed=true);\n');
        # Define cost function
        self.mopfile.write('  equation\n');
        self.mopfile.write('    der(J) = '+self.objective+';\n');  
        # End initalization model
        self.mopfile.write('  end ' + self.Model.modelpath.split('.')[-1] + '_initialize;\n');
        # Save the model path of the initialization and optimziation models
        self.mopmodelpath = self.Model.modelpath.split('.')[0] + '.' + self.Model.modelpath.split('.')[-1];

    def _write_control_mop(self, Optimization):
        '''Complete the mop file for a control optimization problem.

        '''

        self.mopfile.write('\n');
        self.mopfile.write('  optimization ' + self.Model.modelpath.split('.')[-1] + '_optimize (objective = (J(finalTime)), startTime=start_time, finalTime=final_time)\n');
        # Instantiate optimization model
        self.mopfile.write('    extends ' + self.Model.modelpath.split('.')[-1] + '_initialize;\n');
        # Add start time and final time parameter
        self.mopfile.write('    parameter Real start_time = 0;\n');
        self.mopfile.write('    parameter Real final_time = 86400;\n');
        # Remove control variables from input_names for optimization
        self.opt_input_names = [];
        for key in self._init_input_names:
            if key not in self.Model.control_data.keys():
                self.opt_input_names.append(key);
        # Instantiate constraint variables as inputs, add to input_names and other_inputs
        for key in Optimization.constraint_data.keys():
            for field in Optimization.constraint_data[key]:
                if field != 'Cyclic' and field != 'Final' and field != 'Initial':
                    key_new = key.replace('.', '_') + '_' + field;
                    self.opt_input_names.append(key_new);
                    self.other_inputs[key_new] = Optimization.constraint_data[key][field];
                    self.mopfile.write('    input Real ' + key_new + ';\n');                    
        # Define constraint_data
        self.mopfile.write('  constraint\n');
        for key in Optimization.constraint_data.keys():
            for field in Optimization.constraint_data[key]:
                key_new = key.replace('.', '_') + '_' + field;
                if field == 'GTE':
                    self.mopfile.write('    mpc_model.' + key + ' >= ' + key_new + ';\n');
                elif field == 'dGTE':
                    self.mopfile.write('    der(mpc_model.' + key + ') >= ' + key_new + ';\n');
                elif field == 'sGTE':
                    self.mopfile.write('    mpc_model.' + key + ' + ' + self.slack_vars[key_new]['SlackVar'] + ' >= ' + key_new + ';\n')
                elif field == 'LTE':
                    self.mopfile.write('    mpc_model.' + key + ' <= ' + key_new + ';\n');
                elif field == 'dLTE':
                    self.mopfile.write('    der(mpc_model.' + key + ') <= ' + key_new + ';\n');
                elif field == 'sLTE':
                    self.mopfile.write('    mpc_model.' + key + ' - ' + self.slack_vars[key_new]['SlackVar'] + ' <= ' + key_new + ';\n')
                elif field == 'Initial':
                    self.mopfile.write('    mpc_model.' + key + '(startTime)=' + str(Optimization.constraint_data[key][field].get_base_data()) + ';\n');
                elif field == 'Final':
                    self.mopfile.write('    mpc_model.' + key + '(finalTime)=' + str(Optimization.constraint_data[key][field].get_base_data()) + ';\n');
                elif field == 'Cyclic':
                    self.mopfile.write('    mpc_model.' + key + '(startTime)=mpc_model.' + key + '(finalTime);\n');
        for key_new in self.slack_vars.keys():
            self.mopfile.write('   ' + self.slack_vars[key_new]['SlackVar'] + ' >= 0;\n');
        # End optimization portion of package.mop
        self.mopfile.write('  end ' + self.Model.modelpath.split('.')[-1] + '_optimize;\n');
        # End package.mop and save
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[0] + ';\n');

        # Close files
        self.mopfile.close();

    def _write_parameter_estimate_mop(self):
        '''Complete the mop file for a parameter estimation problem.

        '''

        self.mopfile.write('\n');
        self.mopfile.write('optimization ' + self.Model.modelpath.split('.')[-1] + '_optimize (startTime=start_time, finalTime=final_time)\n');
        # Add start time and final time parameter
        self.mopfile.write('    parameter Real start_time = 0;\n');
        self.mopfile.write('    parameter Real final_time = 86400;\n');
        #  Instantiate MPC model with free parameters
        i = 1;
        free_parameters = [];
        for key in self.Model.parameter_data.keys():
            if self.Model.parameter_data[key]['Free'].get_base_data():
                free_parameters.append(key);
        I = len(free_parameters);
        for key in free_parameters:
            if I == 1:
                # If only one parameter
                line = '    extends ' + self.Model.modelpath.split('.')[-1] + '_initialize (mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'));\n';
            else:
                # If more than one parameter
                if i == 1:
                    line = '    extends ' + self.Model.modelpath.split('.')[-1] + '_initialize (mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'),\n';
                elif i == I:
                    line = '      mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'));\n';
                else:
                    line = '      mpc_model.' + key + '(free=true, initialGuess='+str(self.Model.parameter_data[key]['Value'].get_base_data())+', min='+str(self.Model.parameter_data[key]['Minimum'].get_base_data())+', max='+str(self.Model.parameter_data[key]['Maximum'].get_base_data())+'),\n';
                i = i + 1;
            self.mopfile.write(line);
        # End optimization portion of package.mop
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[-1] + '_optimize;\n');
        # End package.mop and save
        self.mopfile.write('end ' + self.Model.modelpath.split('.')[0] + ';\n');
        # Close files
        self.mopfile.close();

    def _simulate_initial(self, Optimization):
        '''Simulate the model for an initial guess of the optimization solution.

        '''

        # Update exogenous except constraints
        self.weather_data = self.Model.weather_data;
        self.internal_data = self.Model.internal_data;
        self.control_data = self.Model.control_data;
        # Update constraints
        if type(Optimization._problem_type) is _ParameterEstimate:
            self.other_inputs = self.Model.other_inputs;
            self.opt_input_names = self._init_input_names;
        else:
            for key in Optimization.constraint_data.keys():
                for field in Optimization.constraint_data[key]:
                    if field != 'Cyclic' and field != 'Final' and field != 'Initial':
                        key_new = key.replace('.', '_') + '_' + field;
                        if key_new not in self.other_inputs.keys():
                            raise ValueError ('New constraint {0} found. The optimization problem needs to be re-instantiated to use this constraint.'.format(key_new))
                        else:
                            self.other_inputs[key_new] = Optimization.constraint_data[key][field];
        # Set parameters
        self.parameter_data = {};
        for key in self.Model.parameter_data.keys():
            self.parameter_data['mpc_model.'+key] = self.Model.parameter_data[key];
        # Set input_names
        self.input_names = self._init_input_names;
        # Set measurements
        self.measurements = {};
        for key in self.Model.measurements.keys():
            self.measurements['mpc_model.' + key] = self.Model.measurements[key];
        # Set timing
        self._continue = Optimization._continue;
        self.start_time_utc = Optimization.start_time_utc;
        self.final_time_utc = Optimization.final_time_utc;
        self._global_start_time_utc = Optimization._global_start_time_utc
        self.elapsed_seconds = Optimization.elapsed_seconds;
        self.total_elapsed_seconds = Optimization.total_elapsed_seconds;
        # Simulate fmu
        self._simulate_fmu();
        # Store initial simulation
        self.res_init = self._res;

    def _solve(self, Optimization):
        '''Solve the optimization problem.

        '''

        # Create input_mpcpy_ts_list
        self._create_input_mpcpy_ts_list_opt();
        # Set inputs
        self._create_input_object_from_input_mpcpy_ts_list(self._input_mpcpy_ts_list_opt);
        # Create ExternalData structure
        self._create_external_data(Optimization);
        # Set optimization options
        self.opt_options['external_data'] = self.external_data;
        self.opt_options['init_traj'] = self.res_init;
        self.opt_options['nominal_traj'] = self.res_init;
        if self._step_from_meas:
            self.opt_options['n_e'] = self._sim_opts['ncp'];
        # Set parameters if they exist
        if hasattr(self, 'parameter_data'):
            for key in self.parameter_data.keys():
                self.opt_problem.set(key, self.parameter_data[key]['Value'].get_base_data());
        # Set start and final time
        start_time = self.total_elapsed_seconds - self.elapsed_seconds;
        final_time = self.total_elapsed_seconds;
        self.opt_problem.set('start_time', start_time);
        self.opt_problem.set('final_time', final_time);
        # Optimize
        self.res_opt = self.opt_problem.optimize(options=self.opt_options);

    def _create_external_data(self, Optimization):
        '''Define external data inputs to optimization problem.

        '''

        quad_pen = OrderedDict();
        N_mea = 0;
        if hasattr(self, 'measurement_variable_list'):
            for key in self.measurement_variable_list:
                df = self.Model.measurements[key]['Measured'].get_base_data().to_frame();
                df_simtime = self._add_simtime_column(df, Optimization._global_start_time_utc);
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
        if self._input_object:
            for key in self._input_object[0]:
                input_traj = np.vstack((np.transpose(self._input_object[1][:,0]), \
                                       np.transpose(self._input_object[1][:,i])));
                eliminated[key] = input_traj;
                N_input = N_input + 1;
                i = i + 1;
        # Create ExternalData structure
        self.external_data = ExternalData(Q=Q, quad_pen=quad_pen, eliminated=eliminated);

    def _get_control_results(self, Optimization, **kwargs):
        '''Update the model control_data and optimization measurements.

        Also add the opt_input object as attribute to Optimization.

        '''

        # Determine time interval
        if 'res_control_step' in kwargs:
            s_start = self.res_opt['time'][0]
            s_final = self.res_opt['time'][-1]
            res_control_step = kwargs['res_control_step'];
            time = np.linspace(s_start,s_final,(s_final-s_start)/res_control_step+1);
        else:
            time = self.res_opt['time']
        # Get fmu variables units
        fmu_variable_units = self._get_fmu_variable_units();
        # Update model control data
        for key in self.Model.control_data.keys():
            # Check variable is model input
            if key in self.Model.input_names:
                # Get optimal control data
                opt_input = self.res_opt.get_opt_input()
                opt_input_traj = opt_input[1]
                i = opt_input[0].index(key)
                data = []
                # Create data
                for t in time:
                    data.append(opt_input_traj(t)[i])
                timedelta = pd.to_timedelta(time, 's');
                timeindex = self._global_start_time_utc + timedelta;
                ts_opt = pd.Series(data = data, index = timeindex).tz_localize('UTC');
                # Get old control data
                ts_old = self.Model.control_data[key].get_base_data();
                # Remove rows with updated data
                first = (ts_old.index == self.start_time_utc).tolist().index(True)
                if ts_old.index[-1] >= self.final_time_utc:
                    # If final time is before end of timeseries, replace only
                    # specific location
                    last = (ts_old.index == self.final_time_utc).tolist().index(True)
                    drop_list = ts_old.index[first:last+1]
                else:
                    # If final time is after end of timeseries, add control to end
                    drop_list = ts_old.index[first:]
                ts_old = ts_old.drop(drop_list);
                # Append opt to old
                ts = ts_old.append(ts_opt)
                # Sort by index
                ts = ts.sort_index()
                # Update control_data
                ts.name = key;
                unit = self._get_unit_class_from_fmu_variable_units('mpc_model.' + key,fmu_variable_units);
                if not unit:
                    unit = units.unit1;
                self.Model.control_data[key] = variables.Timeseries(key, ts, unit);
                # Get opt input object tuple (names, collocation polynomials f(t))
                Optimization.opt_input = opt_input
        # Create optimization measurement dictionary
        Optimization.measurements = {};
        for key in Optimization.Model.measurements.keys():
            # Add optimization results data
            Optimization.measurements[key] = {};
            data = self.res_opt['mpc_model.' + key];
            time = self.res_opt['time'];
            timedelta = pd.to_timedelta(time, 's');
            timeindex = self._global_start_time_utc + timedelta;
            ts_opt = pd.Series(data = data, index = timeindex).tz_localize('UTC');
            # Get old measurement data
            ts_old = self.Model.measurements[key]['Simulated'].get_base_data();
            # Remove rows with updated data
            first = (ts_old.index == self.start_time_utc).tolist().index(True)
            last = (ts_old.index == self.final_time_utc).tolist().index(True)
            drop_list = ts_old.index[first:last+1]
            ts_old = ts_old.drop(drop_list);
            # Append opt to old
            ts = ts_old.append(ts_opt)
            # Sort by index
            ts = ts.sort_index()
            # Update control_data
            ts.name = key;
            unit = self._get_unit_class_from_fmu_variable_units('mpc_model.' + key,fmu_variable_units);
            if not unit:
                unit = units.unit1;
            Optimization.measurements[key]['Simulated'] = variables.Timeseries(key, ts, unit);

    def _get_parameter_results(self, Optimization):
        '''Update the parameter data dictionary in the model with optimization results.

        '''

        for key in Optimization.Model.parameter_data.keys():
            if Optimization.Model.parameter_data[key]['Free'].get_base_data():
                self.fmu_variable_units = self._get_fmu_variable_units();
                unit = self._get_unit_class_from_fmu_variable_units('mpc_model.'+key, self.fmu_variable_units);
                if not unit:
                    unit = units.unit1;
                data = self.res_opt.initial('mpc_model.' + key);
                Optimization.Model.parameter_data[key]['Value'].set_display_unit(unit);
                Optimization.Model.parameter_data[key]['Value'].set_data(data);

    def _compile_transfer_problem(self):
        '''Compile the initialization model and transfer the optimziation problem.

        '''

        # Compile the optimization initializaiton model
        self.fmupath = compile_fmu(self.mopmodelpath + '_initialize', \
                                   self.moppath, \
                                   compiler_options = {'extra_lib_dirs':self.Model.libraries});
        kwargs = {};
        kwargs['fmupath'] = self.fmupath;
        self._create_fmu(kwargs);
        # Transfer optimization problem to casADi
        self.opt_problem = transfer_optimization_problem(self.mopmodelpath + '_optimize', \
                                                         self.moppath, \
                                                         compiler_options = {'extra_lib_dirs':self.Model.libraries});

    def _get_optimization_options(self):
        '''Get the JModelica optimization options in a dictionary.

        '''

        return copy.deepcopy(self.opt_options);

    def _set_optimization_options(self, opt_options, init = False):
        '''Set the JModelica optimization options using a dictionary.

        '''

        # Initialize with specific default options
        if init:
            # Optimization control step
            self._step_from_meas = True;
            opt_options['n_e'] = 0;
        # Check on automatically set options
        else:
            for key in opt_options:
                if key in ['external_data', 'init_traj', 'nominal_traj']:
                    # These cannot be changed
                    if opt_options[key] != self.opt_options[key]:
                        raise KeyError('Key {} is set automatically upon solve.'.format(key));
                if key is 'n_e':
                    # This can be changed but flag needs to be set
                    if opt_options[key] != self.opt_options[key]:
                        self._step_from_meas = False;
        # Set options
        self.opt_options = copy.deepcopy(opt_options);

    def _get_optimization_statistics(self):
        '''Get the JModelica optimization result statistics.

        '''

        return self.res_opt.get_solver_statistics();
        
    def _create_slack_variables(self, Optimization):
        '''Create slack variables and their expressions.
        
        Dictionary of slack variable information
        {<slack_variable_name> : {'Input':<input_name>, 'Expression':<objective expression>}}
        
        Parameters
        ----------
        Optimization : MPCPy Optimization object
        
        '''
        
        n_s = 0
        slack_vars = dict()
        for key in Optimization.constraint_data.keys():
            for field in Optimization.constraint_data[key]:
                if field == 'sGTE' or field == 'sLTE':
                    key_new = key.replace('.', '_') + '_' + field;
                    slack_var = 's{0}'.format(n_s)
                    if field == 'sGTE':
                        exp = '{0}'.format(slack_var)
                    elif field == 'sLTE':
                        exp = '{0}'.format(slack_var)
                    slack_vars[key_new] = {'SlackVar': slack_var, 'Expression':exp}
                    n_s = n_s + 1

        self.slack_vars = slack_vars
