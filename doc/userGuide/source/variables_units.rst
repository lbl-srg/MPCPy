===================
Variables and Units
===================

General
=======

The ``variables`` and ``units`` modules are the fundamental building blocks of data management in MPCPy.  They provide functionality for assigning and converting between units as well as processing timeseries data.  

Generally speaking, variables in MPCPy contain three components:

    name

        A descriptor of the variable.

    data

        Constant value or a timeseries.

    unit

        Assigned to variables and act on the data depending on the requested functionality, such as converting between between units or extracting the data.

A unit assigned to a variable is called the display unit and is associated with a quantity.  For each quantity, there is a predefined base unit.  The data entered into a variable with a display unit is automatically converted to and stored as the quantity base unit.  This way, if the display unit were to be changed, the data only needs to be converted to the new unit upon extraction.  For example, the unit Degrees Celsius is of the quantity temperature, for which the base unit is Kelvin.  Therefore, data entered with a display unit of Degrees Celsius would be converted to and stored in Kelvin.  If the display unit were to be changed to Degrees Fahrenheit, then the data would be converted from Kelvin upon extraction.

Instantiation
=============

Variables are instantiated by defining the variable type and the three components listed in the previous section.  If the data of the variable does not change with time, the variable must be instantiated using the ``variables.Static`` class.  Data supplied to static variable may be a single value, a list, or a numpy array.  If the data of the variable is a timeseries, the variable must be instantiated using the ``variables.Timeseries`` class.  Data supplied to a timeseries variable must be in the form of a pandas series object with a datetime index.  This brings to MPCPy all of the functionality of the pandas package.  The unit assigned is a class chosen from the ``units`` module.

::

    # Instantiate a static variable with units in Degrees Celsius
    var = variables.Static('var', 20, units.degC)

Timeseries variables have capabilities to manage the the timezone of the data as well as clean the data upon instantiation with the following optional keyword arguments:

    tz_name

        The name of the timezone as defined by ``tzwhere``.  By default, the UTC timezone is assigned to the data.  If a different timezone is assigned, the data is converted to a stored in UTC.  Similar to the treatment of data units, the timezone is only converted to the assigned timezone upon data extraction.

    geography

        Tuple containing (latitude,longitude) in degrees.  If geography is defined, the timezone associated with that location will be assigned to the variable.

    cleaning_type

        The type of cleaning to be performed on the data.  This should be a class selected from ``variables.Timeseries``.

    cleaning_args

        Arguments of the cleaning_type defined.


Variable Management
==============

Accessing Data
--------------
Data may be extracted from a variable by using the ``display_data()`` and ``get_base_data()`` methods.  The former will extract the data in the assigned unit, while the latter will extract the data in the base unit.

Setting Display Unit
--------------
The display unit of a variable may be changed using the ``set_display_unit()`` method.  This requires a class of the ``units`` module as an argument.

Setting Data
------------
The data of a variable may be changed using the ``set_data()`` method.  This requires a single value or pandas series object as an argument, depending on the variable type.  

Operations
----------
Variables with the same display unit can be added and subtracted using the "+" and "-" operands.  The result is a third variable with the resulting data, same display unit, and name as "var1_var2".
