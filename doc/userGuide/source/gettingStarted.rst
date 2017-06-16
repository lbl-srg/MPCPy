Getting Started
===============

To get started with MPCPy, first follow the installation instructions below.  Then, explore the ipython notebooks in the ``examples`` directory to get a feel for the workflow of MPCPy.  You can always consult the user guide for more information.

Installation Instructions For Linux (Ubuntu 16.04 LTS)
------------------------------------------------------

1. Install Python Packages

    - matplotlib 1.5.1
    - numpy 1.11.0
    - pandas 0.17.1
    - python-dateutil 2.4.2
    - pytz 2014.10
    - scikit-learn 0.18.1
    - tzwhere 2.3
    - sphinx 1.3.6
    - estimationpy

2. Install JModelica 2.0 (for Modelica compiling, optimization, and fmu simulation)

3. Create JModelica environmental variables
    - add the following lines to your bashrc script:

        ::

            export JMODELICA_HOME=".../JModelica-Inst/JModelica"
            export IPOPT_HOME=".../JModelica-Inst/Ipopt-3.12.4-inst"
            export SUNDIALS_HOME="$JMODELICA_HOME/ThirdParty/Sundials"
            export CPPAD_HOME="$JMODELICA_HOME/ThirdParty/CppAD/"
            export SEPARATE_PROCESS_JVM="/usr/lib/jvm/java-8-openjdk-amd64/"
            export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"

4. Download or Clone MPCPy
    - go to https://github.com/lbl-srg/MPCPy and clone or download repository into a directory (let's call it ``.../MPCPy``).


5. Edit PYTHONPATH environmental variable
    - add the following lines to your bashrc script (assumes 3. above sets JMODELICA_HOME):
        
        ::
        
            export PYTHONPATH=$PYTHONPATH:"$JMODELICA_HOME/Python"
            export PYTHONPATH=$PYTHONPATH:"$JMODELICA_HOME/Python/pymodelica"
            export PYTHONPATH=$PYTHONPATH:".../MPCPy"

6. Test the installation
    - Run the ipython notebook examples located in ``examples`` or run the unit tests as outlined below.

Run Unit Tests
--------------
The script bin/runUnitTests.py runs the unit tests of MPCPy.  By default, all of the unit tests are run.  An optional argument -s [module.class] will run only the specified unit tests module or class.

To run all unit tests from command-line, use the command:

    .. code-block:: text

    	> python bin/runUnitTests

To run only unit tests in the module test_models from command-line, use the command:

    .. code-block:: text

	   > python bin/runUnitTests -s test_models

To run only unit tests in the class SimpleRC from the module test_models from the command-line, use the command:

    .. code-block:: text

	   > python bin/runUnitTests -s test_models.SimpleRC

