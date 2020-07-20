# -*- coding: utf-8 -*-
"""

This tutorial will introduce the basic concepts and workflow of mpcpy.
By the end, we will train a simple model based on emulated data, and use 
the model to optimize the control signal of the system.  All required data
files for this tutorial are located in doc/userGuide/tutorial.

The model is a simple RC model of zone thermal response to ambient temperature
and a singal heat input.  It is written in Modelica:

.. code-block:: modelica

    model RC "A simple RC network for example purposes"
      Modelica.Blocks.Interfaces.RealInput weaTDryBul(unit="K") "Ambient temperature";
      Modelica.Blocks.Interfaces.RealInput Qflow(unit="W") "Heat input";
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K") "Zone temperature";
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heatCapacitor(C=1e5) 
      "Thermal capacitance of zone";
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor thermalResistor(R=0.01) 
      "Thermal resistance of zone";
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTemp;
      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor senTemp;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat;
    equation 
      connect(senTemp.T, Tzone)
      connect(preHeat.Q_flow, Qflow)
      connect(heatCapacitor.port, senTemp.port)
      connect(heatCapacitor.port, preHeat.port)
      connect(preTemp.port, thermalResistor.port_a)
      connect(thermalResistor.port_b, heatCapacitor.port)
      connect(preTemp.T, weaTDryBul)
    end RC;


Variables and Units
-------------------

First, lets get familiar with variables and units, the basic building blocks of MPCPy.

>>> from mpcpy import variables
>>> from mpcpy import units

Static variables contain data that is not a timeseries:

>>> setpoint = variables.Static('setpoint', 20, units.degC)
>>> print(setpoint) # doctest: +NORMALIZE_WHITESPACE
Name: setpoint
Variability: Static
Quantity: Temperature
Display Unit: degC

The unit assigned to the variable is the display unit.  
However, each display unit quantity has a base unit that is used to store 
the data in memory.  This makes it easy to convert between units 
when necessary.  For example, the degC display unit has a quantity temperature,
which has base unit in Kelvin.  

>>> # Get the data in display units
>>> setpoint.display_data()
20.0
>>> # Get the data in base units
>>> setpoint.get_base_data()
293.15
>>> # Convert the display unit to degF
>>> setpoint.set_display_unit(units.degF)
>>> setpoint.display_data() # doctest: +NORMALIZE_WHITESPACE
68.0

Timeseries variables contain data in the form of a ``pandas`` Series with a 
datetime index:

>>> # Create pandas Series object
>>> import pandas as pd
>>> data = [0, 5, 10, 15, 20]
>>> index = pd.date_range(start='1/1/2017', periods=len(data), freq='H')
>>> ts = pd.Series(data=data, index=index, name='power_data')

Now we can do the same thing with the timeseries variable as we did with the 
static variable:

>>> # Create mpcpy variable
>>> power_data = variables.Timeseries('power_data', ts, units.Btuh)
>>> print(power_data) # doctest: +NORMALIZE_WHITESPACE
Name: power_data
Variability: Timeseries
Quantity: Power
Display Unit: Btuh
>>> # Get the data in display units
>>> power_data.display_data()
2017-01-01 00:00:00+00:00     0.0
2017-01-01 01:00:00+00:00     5.0
2017-01-01 02:00:00+00:00    10.0
2017-01-01 03:00:00+00:00    15.0
2017-01-01 04:00:00+00:00    20.0
Freq: H, Name: power_data, dtype: float64
>>> # Get the data in base units
>>> power_data.get_base_data()
2017-01-01 00:00:00+00:00    0.000000
2017-01-01 01:00:00+00:00    1.465355
2017-01-01 02:00:00+00:00    2.930711
2017-01-01 03:00:00+00:00    4.396066
2017-01-01 04:00:00+00:00    5.861421
Freq: H, Name: power_data, dtype: float64
>>> # Convert the display unit to kW
>>> power_data.set_display_unit(units.kW)
>>> power_data.display_data()
2017-01-01 00:00:00+00:00    0.000000
2017-01-01 01:00:00+00:00    0.001465
2017-01-01 02:00:00+00:00    0.002931
2017-01-01 03:00:00+00:00    0.004396
2017-01-01 04:00:00+00:00    0.005861
Freq: H, Name: power_data, dtype: float64

There is additional functionality with the units that may be useful, such as
setting new data and getting the units.  Consult the documentation on these 
classes for more information.


Collect model weather and control signal data
---------------------------------------------

Now, we would like to collect the weather data and control signal inputs
for our model.  We do this using exodata objects:

>>> from mpcpy import exodata

Let's take our weather data from an EPW file.  We instantiate the weather 
exodata object by supplying the path to the EPW file:

>>> weather = exodata.WeatherFromEPW('USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw')

Note that using the weather exodata object assumes that weather inputs to our
model are named a certain way.  Consult the documentation on the weather
exodata class for more information.  In this case, the ambient dry bulb
temperature input in our model is named weaTDryBul.

Let's take our control input signal from a CSV file.  The CSV file looks like:

::

    Time,Qflow_csv
    01/01/17 12:00 AM,3000
    01/01/17 01:00 AM,3000
    01/01/17 02:00 AM,3000
    ...
    01/02/17 10:00 PM,3000
    01/02/17 11:00 PM,3000
    01/03/17 12:00 AM,3000
    
We instantiate the control exodata object by supplying the path to the CSV file
as well as a map of the names of the columns to the input of our model.  
We also assume that the data in the CSV file is given in the local time of the 
weather file, and so we supply this optional parameter, tz_name, upon 
instantiation as well.  If no time zone is supplied, it is assumed to be UTC.

>>> variable_map = {'Qflow_csv' : ('Qflow', units.W)}
>>> control = exodata.ControlFromCSV('ControlSignal.csv',
...                                  variable_map,
...                                  tz_name = weather.tz_name)

Now we are ready to collect the exogenous data from our data sources for a
given time period.

>>> start_time = '1/1/2017'
>>> final_time = '1/3/2017'
>>> weather.collect_data(start_time, final_time) # doctest: +ELLIPSIS
-etc-
>>> control.collect_data(start_time, final_time)

Use the ``display_data()`` and ``get_base_data()`` functions for the weather
and control objects to get the data in the form of a pandas dataframe. Note
that the data is given in UTC time.  

>>> control.display_data() # doctest: +ELLIPSIS
                            Qflow
Time                             
2017-01-01 06:00:00+00:00  3000.0
2017-01-01 07:00:00+00:00  3000.0
2017-01-01 08:00:00+00:00  3000.0
-etc-



Simulate as Emulated System
---------------------------

The model has parameters for the resistance and capacitance set in the 
modelica code.  For the purposes of this tutorial, we will assume that the 
model with these parameter values represents the actual system.  We now wish to
collect measurements from this 'actual system.'  For this, we use the systems 
module of mpcpy.

>>> from mpcpy import systems

First, we instantiate our system model by supplying a measurement dictionary, 
information about where the model resides, and information about model exodata.

The measurement dictionary holds information about and data from the variables 
being measured.  We start with defining the variables we are interested in
measuring and their sample rate.  In this case, we have two, the output of 
the model, called 'Tzone' and the control input called 'Qflow'.  
Note that 'heatCapacitor.T' would also be valid instead of 'Tzone'.  

>>> measurements = {'Tzone' : {}, 'Qflow' : {}}
>>> measurements['Tzone']['Sample'] = variables.Static('sample_rate_Tzone',
...                                                    3600,
...                                                    units.s)
>>> measurements['Qflow']['Sample'] = variables.Static('sample_rate_Qflow',
...                                                    3600,
...                                                    units.s)

The model information is given by a tuple containing the path to the 
Modelica (.mo) file, the path of the model within the .mo file, and a list of 
paths of any required libraries other than the Modelica Standard.  
For this example, there are no additional libraries.

>>> moinfo = ('Tutorial.mo', 'Tutorial.RC', {})

Ultimately, the modelica model is compiled into an FMU.  If the emulation model
is already an FMU, than an fmupath can be specified instead of the modelica 
information tuple.  For more information, see the documentation on the systmems
class.

We can now instantiate the system emulation object with our measurement
dictionary, model information, collected exogenous data, and time zone:

>>> emulation = systems.EmulationFromFMU(measurements,
...                                      moinfo = moinfo,
...                                      weather_data = weather.data,
...                                      control_data = control.data,
...                                      tz_name = weather.tz_name)
                                         
Finally, we can collect the measurements from our emulation over a specified
time period and display the results as a pandas dataframe.  The 
``collect_measurements()`` function updates the measurement dictionary with 
timeseries data in the ``'Measured'`` field for each variable.

>>> # Collect the data
>>> emulation.collect_measurements('1/1/2017', '1/2/2017') # doctest: +ELLIPSIS
-etc-
>>> # Display the results
>>> emulation.display_measurements('Measured').applymap('{:.2f}'.format) # doctest: +ELLIPSIS
                             Qflow   Tzone
Time                                      
2017-01-01 06:00:00+00:00  3000.00  293.15
2017-01-01 07:00:00+00:00  3000.00  291.01
2017-01-01 08:00:00+00:00  3000.00  291.32
-etc-

Estimate Parameters
-------------------

Now assume that we do not know the parameters of the model.  Or, that we have
measurements from a real or emulated system, and would like to estimate
parameters of our model to fit the measurements.  For this, we use the models
module from mpcpy.

>>> from mpcpy import models

In this case, we have a Modelica model with two parameters that we would like
to train based on the measured data from our system; the resistance
and capacitance.

We first need to collect some information about our parameters and do so using
a parameters exodata object.  The parameter information is stored in a CSV file
that looks like:

::

    Name,Free,Value,Minimum,Maximum,Covariance,Unit
    heatCapacitor.C,True,40000,1.00E+04,1.00E+06,1000,J/K
    thermalResistor.R,True,0.002,0.001,0.1,0.0001,K/W

The name is the name of the parameter in the model.  The Free field indicates
if the parameter is free to be changed during the estimation method or not.
The Value is the current value of the parameter.  If the parameter is to be
estimated, this would be an initial guess.  If the parameter's Free field is
set to False, then the value is set to the parameter upon simulation.  The
Minimum and Maximum fields set the minimum and maximum value allowed by the 
parameter during estimation.  The Covariance field sets the covariance of
the parameter, and is only used for unscented kalman filtering.  Finally, the 
Unit field specifies the unit of the parameter using the name string of 
MPCPy unit classes.

>>> parameters = exodata.ParameterFromCSV('Parameters.csv')
>>> parameters.collect_data()
>>> parameters.display_data() # doctest: +NORMALIZE_WHITESPACE
                  Covariance  Free Maximum Minimum Unit  Value
Name                                                          
heatCapacitor.C         1000  True   1e+06   10000  J/K  40000
thermalResistor.R     0.0001  True     0.1   0.001  K/W  0.002

Now, we can instantiate the model object by defining the estimation method, 
validation method, measurement dictionary, model information, parameter data, 
and exogenous data.  In this case, we use JModelica optimization to perform 
the parameter estimation and will validate the parameter estimation by 
calculating the root mean square error (RMSE) between measurements from the 
model and emulation.

>>> model = models.Modelica(models.JModelicaParameter,
...                         models.RMSE,
...                         emulation.measurements,
...                         moinfo = moinfo,
...                         parameter_data = parameters.data,
...                         weather_data = weather.data,
...                         control_data = control.data,
...                         tz_name = weather.tz_name)

Let's simulate the model to see how far off we are with our initial parameter
guesses.  The ``simulate()`` function updates the measurement dictionary with 
timeseries data in the ``'Simulated'`` field for each variable.

>>> # Simulate the model
>>> model.simulate('1/1/2017', '1/2/2017') # doctest: +ELLIPSIS
-etc-
>>> # Display the results
>>> model.display_measurements('Simulated').applymap('{:.2f}'.format) # doctest: +ELLIPSIS
                             Qflow   Tzone
Time                                      
2017-01-01 06:00:00+00:00  3000.00  293.15
2017-01-01 07:00:00+00:00  3000.00  266.95
2017-01-01 08:00:00+00:00  3000.00  267.44
-etc-


Now, we are ready to estimate the parameters to better fit the emulated
measurements.  In addtion to a training period, we must supply a list of 
measurement variables for which to minimize the error between the simulated 
and measured data.  In this case, we only have one, ``'Tzone'``.  The
``estimate()`` function updates the Value field for the parameter data in 
the model.  

>>> model.parameter_estimate('1/1/2017', '1/2/2017', ['Tzone']) # doctest: +ELLIPSIS
-etc-

Let's validate the estimation on the training period.  The ``validate()``
method will simulate the model over the specified time period, calculate the
RMSE between the simulated and measured data, and generate a plot in the 
working directory that shows the simulated and measured data for each 
measurement variable.

>>> # Perform validation
>>> model.validate('1/1/2017', '1/2/2017', 'validate_tra', plot=1) # doctest: +ELLIPSIS
-etc-
>>> # Get RMSE
>>> print("%.3f" % model.RMSE['Tzone'].display_data()) # doctest: +NORMALIZE_WHITESPACE
0.041

Now let's validate on a different period of exogenous data:

>>> # Define validation period
>>> start_time_val = '1/2/2017'
>>> final_time_val = '1/3/2017'
>>> # Collect new measurements
>>> emulation.collect_measurements(start_time_val, final_time_val) # doctest: +ELLIPSIS
-etc-
>>> # Assign new measurements to model
>>> model.measurements = emulation.measurements
>>> # Perform validation
>>> model.validate(start_time_val, final_time_val, 'validate_val', plot=1) # doctest: +ELLIPSIS
-etc-
>>> # Get RMSE
>>> print("%.3f" % model.RMSE['Tzone'].display_data()) # doctest: +NORMALIZE_WHITESPACE
0.047

Finally, let's view the estimated parameter values:

>>> for key in model.parameter_data.keys():
...     print(key, "%.2f" % model.parameter_data[key]['Value'].display_data())
('heatCapacitor.C', '119828.30')
('thermalResistor.R', '0.01')


Optimize Control
----------------

We are now ready to optimize control of our system heater using our calibrated 
MPC model.  Specificlaly, we would like to maintain a comfortable temperature
in our zone with the minimum amount of heater energy.  We can do this by using 
the optimization module of MPCPy.

>>> from mpcpy import optimization

First, we need to collect some constraint data to add to our optimization
problem.  In this case, we will constrain the heating input to between 
0 and 4000 W, and the temperature to a comfortable range, between 
20 and 25 degC.  We collect contraint data from a CSV using a constraint 
exodata data object.  The constraint CSV looks like:

::

    Time,Qflow_min,Qflow_max,T_min,T_max
    01/01/17 12:00 AM,0,4000,20,25
    01/01/17 01:00 AM,0,4000,20,25
    01/01/17 02:00 AM,0,4000,20,25
    ...
    01/02/17 10:00 PM,0,4000,20,25
    01/02/17 11:00 PM,0,4000,20,25
    01/03/17 12:00 AM,0,4000,20,25
    
The constraint exodata object is used to determine which column of data matches
with which model variable and whether it is a less-than-or-equal-to (LTE) or 
greater-than-or-equal-to (GTE) constraint:

>>> # Define variable map
>>> variable_map = {'Qflow_min' : ('Qflow', 'GTE', units.W), 
...                 'Qflow_max' : ('Qflow', 'LTE', units.W),
...                 'T_min' : ('Tzone', 'GTE', units.degC),
...                 'T_max' : ('Tzone', 'LTE', units.degC)}
>>> # Instantiate constraint exodata object
>>> constraints = exodata.ConstraintFromCSV('Constraints.csv',
...                                         variable_map,
...                                         tz_name = weather.tz_name)
>>> # Collect data
>>> constraints.collect_data('1/1/2017', '1/3/2017')
>>> # Get data
>>> constraints.display_data() # doctest: +ELLIPSIS
                       	   Qflow_GTE  Qflow_LTE  Tzone_GTE  Tzone_LTE
Time                                                                 
2017-01-01 06:00:00+00:00        0.0     4000.0       20.0       25.0
2017-01-01 07:00:00+00:00        0.0     4000.0       20.0       25.0
2017-01-01 08:00:00+00:00        0.0     4000.0       20.0       25.0
-etc-

We can now instantiate an optimization object using our calibrated MPC model, 
selecting an optimization problem type and solver package, and specifying
which of the variables in the model to treat as the objective variable.
In this case, we choose an energy minimization problem (integral of variable 
over time horizon) to be solved using JModelica, and Qflow to be the variable 
we wish to minimize the integral of over the time horizon.

>>> opt_problem = optimization.Optimization(model, 
...                                         optimization.EnergyMin,
...                                         optimization.JModelica,
...                                         'Qflow',
...                                         constraint_data = constraints.data)

The information provided is used to automatically generate a .mop (optimization
model file for JModelica) and transfer the optimization problem using JModelica.
Using the ``optimize()`` function optimizes the variables defined in the control
data of the model object and updates their timeseries data with the optimal 
solution for the time period specified.  Note that other than the constraints, 
the exogenous data within the model object is used, and the control interval
is assumed to be the same as the measurement sampling rate of the model. Use
the ``get_optimization_options()`` and ``set_optimization_options()`` to see
and change the options for the optimization solver; for instance number
of control points, maximum iteration number, tolerance, or maximum CPU time.
See the documentation for these functions for more information.

>>> opt_problem.optimize('1/2/2017', '1/3/2017') # doctest: +ELLIPSIS
-etc-

We can get the optimization solver statistics in the form of
(return message, # of iterations, objective value, solution time in seconds):

>>> opt_problem.get_optimization_statistics() # doctest: +ELLIPSIS
('Solve_Succeeded', 12, -etc-)

We can retrieve the optimal control solution and verify that the 
constraints were satisfied.  The intermediate points are a result of the 
direct collocation method used by JModelica.

>>> opt_problem.display_measurements('Simulated').applymap('{:.2f}'.format) # doctest: +ELLIPSIS
                                    Qflow   Tzone
Time                                             
2017-01-02 06:00:00+00:00          669.93  298.15
2017-01-02 06:09:18.183693+00:00  1512.95  293.15
2017-01-02 06:38:41.816307+00:00  2599.01  293.15
2017-01-02 07:00:00+00:00         1888.28  293.15
-etc-

Finally, we can simulate the model using the optimized control trajectory.
Note that the ``model.control_data`` dictionary is updated by the 
``opt_problem.optimize()`` function.

>>> model.control_data['Qflow'].display_data().loc[pd.to_datetime('1/2/2017  06:00:00'):pd.to_datetime('1/3/2017 06:00:00')].map('{:.2f}'.format) # doctest: +ELLIPSIS
2017-01-02 06:00:00+00:00            669.93
2017-01-02 06:09:18.183693+00:00    1512.95
2017-01-02 06:38:41.816307+00:00    2599.01
2017-01-02 07:00:00+00:00           1888.28
-etc-
>>> model.simulate('1/2/2017', '1/3/2017') # doctest: +ELLIPSIS
-etc-
>>> model.display_measurements('Simulated').applymap('{:.2f}'.format) # doctest: +ELLIPSIS
                             Qflow   Tzone
Time                                      
2017-01-02 06:00:00+00:00   669.93  293.15
2017-01-02 07:00:00+00:00  1888.28  291.41
2017-01-02 08:00:00+00:00  2277.67  293.03
-etc-

Note there is some mismatch between the simulated model output temperature 
and the raw optimal control solution model output temperature output.  
This is due to the interpolation of control input results during simulation 
not aligning with the collocation polynomials and timestep determined by the
optimization solver.  We can solve the optimization problem again, this 
time updating the ``model.control_data`` with a greater time resolution of 1 
second.  Some mismatch will still occur due to the optimization solution
using collocation being an approximation of the true dynamic model.

>>> opt_problem.optimize('1/2/2017', '1/3/2017', res_control_step=1.0) # doctest: +ELLIPSIS
-etc-
>>> model.control_data['Qflow'].display_data().loc[pd.to_datetime('1/2/2017 06:00:00'):pd.to_datetime('1/3/2017 06:00:00')].map('{:.2f}'.format) # doctest: +ELLIPSIS
2017-01-02 06:00:00+00:00     669.93
2017-01-02 06:00:01+00:00     671.66
2017-01-02 06:00:02+00:00     673.38
-etc-
>>> model.simulate('1/2/2017', '1/3/2017') # doctest: +ELLIPSIS
-etc-
>>> model.display_measurements('Simulated').applymap('{:.2f}'.format) # doctest: +ELLIPSIS
                             Qflow   Tzone
Time                                      
2017-01-02 06:00:00+00:00   669.93  293.15
2017-01-02 07:00:00+00:00  1888.28  292.67
2017-01-02 08:00:00+00:00  2277.67  293.13
-etc-

"""

if __name__ == "__main__":
    import doctest
    doctest.ELLIPSIS_MARKER = '-etc-'
    (n_fails, n_tests) = doctest.testmod()
    if n_fails:
        print('\nTutorial finished with {0} fails.'.format(n_fails));
    else:
        print('\nTutorial finished OK.')
