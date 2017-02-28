=======
ExoData
=======

General
=======

``ExoData`` classes are responsible for the representation of exogenous data, with methods to collect this data from various sources and process it for use within MPCPy.  This data comes from sources outside of MPCPy and are not measurements of the system of interest.  The data is split into categories, or types, in order to standardize the organization of variables within the data for a particular type, in the form of a python dictionary, and to allow for any specific data processing that may be required.  This allows exogenous data objects to be used throughout MPCPy regardless of their data source.  To add a data source, one only need to create a class that can convert the data format in the source to that standardized in MPCPy.  The following is a list of exogenous data types:

- Weather
- Internal
- Control
- Other Input
- Parameter
- Constraint
- Price

Instantiation
-------------

``ExoData`` objects may be instantiated using classes of the naming convention ``TypeFromSource``.  For example, the class for collecting weather data from an EPW file is called ``WeatherFromEPW``.  Required arguments for instantiation will differ among the classes depending on the data type and source.  However, all ``ExoData`` classes have the following optional keyword arguments upon instantiation:

- geography - tuple containing (latitude,longitude) in degrees.  Is required for weather data other than from an EPW.  May also be used to detect time zone of data.
- tz_name - the name of the timezone as defined by ``tzwhere``.  If "from_geography" is specified, the latitude and longitude coordinates are used to specify the timezone.
- time_format - timestamp format of the data in a timespec string.  Timestamps naturally read by ``pandas`` do not have to be specified.
- time_header - name of the column or variable containing timestamps of the data.  The names "Time", "time", "Timestamp", and "timestamp" do not have to be specified.
- clean_data - dictionary of the form ``{ "columnHeader" : "cleaning_type" = mpcpy.Variables.cleaning_type, "cleaning_args" = (cleaning_args)}``.  See the ``Variables`` section for more information on data cleaning.

Collecting Data
---------------

Once instantiated, an ``ExoData`` object may collect data using the ``collect_data()`` method.

::

    # Collect data from start_time to final_time
    exodata_class.collect_data(start_time, final_time);

Accessing Data
--------------

Once data is collected, the data dictionary is located at ``exodata_object.data``.  Note that this data dictionary may also be defined and set in the python environment, without the use of ``collect_data``, as long as it conforms to the data type structures described in this section.

The data dictionary may also be converted to a ``pandas`` dataframe using the ``display_data()`` and ``get_base_data()`` methods, with similar differentiation as in MPCPy ``Variable`` classes.

::

    # Make dataframe in display units
    exodata_display_df = exodata_object.display_data();
    # Make dataframe in base units
    exodata_base_df = exodata_object.get_base_data();


Weather
=======

Weather data represents the conditions of the ambient environment.  Weather data objects have special methods for checking the validity of data and use supplied data to calculate data not directly measured, for example black sky temperature, wet bulb temperature, and sun position.

Structure
---------

Exogenous weather data has the following organization:

::

    weather.data = {"Weather Variable Name" : mpcpy.Variables.Timeseries}

The weather data dictionary variable names should be chosen from the following list:

- weaPAtm - atmospheric pressure
- weaTDewPoi - dew point temperature
- weaTDryBul - dry bulb temperature
- weaRelHum - relative humidity
- weaNOpa - opaque sky cover
- weaCelHei - cloud height
- weaNTot - total sky cover
- weaWinSpe - wind speed
- weaWinDir - wind direction
- weaHHorIR - horizontal infrared irradiation
- weaHDirNor - direct normal irradiation
- weaHGloHor - global horizontal irradiation
- weaHDifHor - diffuse horizontal irradiation
- weaIAveHor - global horizontal illuminance
- weaIDirNor - direct normal illuminance
- weaIDifHor - diffuse horizontal illuminance
- weaZLum - zenith luminance
- weaTBlaSky - black sky temperature
- weaTWetBul - wet bulb temperature
- weaSolZen - solar zenith angle
- weaCloTim - clock time
- weaSolTim - solar time
- weaTGnd - ground temperature

Ground temperature is an exception to the data dictionary format  due to the possibility of different temperatures at multiple depths. Therefore, the dictionary format for 'ground temperature' is:

::

    weather.data["weaTGnd"] = {"Depth" : mpcpy.Variables.Timeseries}

Classes
-------

Weather data may be collected using the following classes:

    **WeatherFromEPW**
    
        Collects weather data from an EPW file.
    
    **WeatherFromCSV**
    
        Collects weather data from a CSV file.  This class requires a variable map to match CSV column headers with weather variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("Weather Variable Name", 
                                            mpcpy.Units.unit)}


Internal
========

Internal data represents zone heat gains that may come from people, lights, or equipment.  Internal data objects have special methods for sourcing these heat gains from a predicted occupancy model.

Structure
---------

Exogenous internal data has the following organization:

::

    internal.data = {"Zone Name" : {
                        "Internal Variable Name" : mpcpy.Variables.Timeseries}}

The internal data dictionary variable names should be chosen from the following list:

- intCon - convective internal load
- intRad - radiative internal load
- intLat - latent internal load

The internal variable names in the model should follow the convention ``internalVariableName_zoneName``.  For example, the convective load input for the zone "west" should have the name ``intCon_west``.

Classes
-------

Internal data may be collected using the following classes:

    **InternalFromCSV**
    
        Collects internal data from a CSV file.  This class requires a variable map to match CSV column headers with internal variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("Zone Name", 
                                            "Internal Variable Name", 
                                            mpcpy.Units.unit)}
\
 
    **InternalFromOccupancyModel**
    
        Generates internal load data from an occupancy prediction model.  This class requires a zone list in the form ["Zone Name 1", "Zone Name 2", "Zone Name 3"], a list of numeric values representing the loads per person in the form [Convective, Radiative, Latent] for each zone and collected in a list, the units of the indicated loads from ``mpcpy.Units.unit``, and a list of occupancy model objects with predicted occupancy, one for each zone.


Control
=======

Control data represents control inputs to a system or model.  The variables listed in a Control data object are special in that they are considered optimization variables during model optimization.

Structure
---------

Exogenous control data has the following organization:

::

    control.data = {"Control Variable Name" : mpcpy.Variables.Timeseries}

The control variable names should match those of the model.

Classes
-------

Control data may be collected using the following classes:

    **ControlFromCSV**
    
        Collects control data from a CSV file.  This class requires a variable map to match CSV column headers with control variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("Control Variable Name", 
                                            mpcpy.Units.unit)}


Other Inputs
============

Other Input data represents miscellaneous inputs to a model.  The variables listed in an Other Inputs data object are not acted upon in any special way.

Structure
---------

Other input data has the following organization:

::

    other_input.data = {"Other Input Variable Name" : mpcpy.Variables.Timeseries}

The other input variable names should match those of the model.

Classes
-------

Other input data may be collected using the following classes:

    **OtherInputFromCSV**
    
        Collect other input data from a CSV file.  This class requires a variable map to match CSV column headers with other input variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("Other Input Variable Name", 
                                            mpcpy.Units.unit)}


Price
=====

Price data represents price signals from utility or district energy systems for things such as energy consumption, demand, or other services.  Price data object variables are special because they are used for optimization objective functions involving price signals.

Structure
---------

Exogenous price data has the following organization:

::

    price.data = {"Price Variable Name" : mpcpy.Variables.Timeseries}

The price variable names should be chosen from the following list:

- pi_e - electrical energy price

Classes
-------

Price data may be collected using the following classes:

    **PriceFromCSV**
    
        Collects price data from a CSV file.  This class requires a variable map to match CSV column headers with price variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("Price Variable Name", 
                                            mpcpy.Units.unit)}


Constraints
===========

Constraint data represents limits to which the control and state variables of an optimization solution must abide.  Constraint data object variables are included in the optimization problem formulation.

Structure
---------

Exogenous constraint data has the following organization:

::

    constraint.data = {"State or Control Variable Name" : {
                            "Constraint Variable Name" : mpcpy.Variables.Timeseries/Static}}

The state or control variable name must match those that are in the model.  The constraint variable names should be chosen from the following list:

- LTE - less than or equal to (Timeseries)
- GTE - greater than or equal to (Timeseries)
- E - equal to (Timeseries)
- Initial - initial value (Static)
- Final - final value (Static)
- Cyclic - initial value equals final value (Static - Boolean)

Classes
-------

Constraint data may be collected using the following classes:

    **ConstraintFromCSV**
    
        Collects timeseries constraint data from a CSV file.  Static constraint data must be added by editing the data dictionary directly.  This class requires a variable map to match CSV column headers with constraint variable names.  The variable map is a python dictionary of the form: 

::

    variable_map = {"Column Header Name" : ("State or Control Variable Name", 
                                            "Constraint Variable Name", 
                                            mpcpy.Units.unit)}
\

    **ConstraintFromOccupancyModel**
        
        Generates LTE, GTE, and E constraint data from an occupancy prediction model by implementing occupied and unoccupied values.  This class requires a state or control variable list in the form ["Variable Name 1", "Variable Name 2", "Variable Name 3"], a list of numeric values representing the occupied and unoccupied constraint values in the form [Occupied, Unoccupied] for each variable collected in a list, a list of constraint variable names, one for each variable, and a list of the units of the indicated numeric values from ``mpcpy.Units.unit``.


Parameters
==========

Parameter data represents inputs or coefficients of models that do not change with time during a simulation, which may need to be learned using system measurement data. Parameter data object variables are set when simulating models, and are estimated using model learning techniques if flagged to do so.

Structure
---------

Exogenous parameter data has the following organization:

::

    parameter.data = {"Parameter Name" : {
                        "Parameter Variable Name" : mpcpy.Variables.Static}}

The parameter name must match that which is in the model.  The parameter variable names should be chosen from the following list:

- Free - boolean flag for inclusion in model learning algorithms
- Value - value of the parameter, which is also used as an initial guess for model learning algorithms
- Minimum - minimum value of the parameter for model learning algorithms
- Maximum - maximum value of the parameter for model learning algorithms
- Covariance - covariance of the parameter for model learning algorithms

Classes
-------

Parameter data may be collected using the following classes:

    **ParameterFromCSV**
    
        Collects parameter data from a CSV file.  The CSV file rows must be named as the parameter names and the columns must be named as the parameter variable names.