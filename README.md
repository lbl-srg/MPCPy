# MPCPy
This is the development site for MPCPy, the python-based open-source platform for model predictive control in buildings.

## Description
MPCPy facilitates the testing and implementation of Model Predictive Control (MPC) for building systems.  The software package focuses on the use of data-driven simplified physical or statistical models to predict building performance and optimize control.  Python modules and classes exist for importing data, interacting with a real or emulated system, estimating and validating data-driven models, and optimizing control inputs.

## Dependencies
MPCPy takes advantage of many third-party software packages, listed below.  It has been tested on Ubuntu 16.04.

**Python Packages**
- matplotlib 1.5.1
- numpy 1.11.0
- pandas 0.17.1
- python-dateutil 2.4.2
- pytz 2014.10
- scikit-learn 0.18.1
- tzwhere 2.3
- estimationpy

**Modelica Packages**
- Modelica Standard Library 3.2.2
- Modelica Buildings Library 3.0.0

**Modelica Compiler and Optimizer, FMU Simulator**
- JModelica 1.17

## Installation
1. Install all dependencies listed above according to their respective processes.

2. Create the following environmental variables, where ".../" is replaced by the full directory:

    - JMODELICA_HOME        = ".../Jmodelica-1.17"
    - IPOPT_HOME            = ".../Ipop-3.12.5"
    - SUNDIALS_HOME         = ".../Jmodelica-1.17/ThirdParty/Sundials"
    - CPPAD_HOME            = ".../Jmodelica-1.17/ThirdParty/CppAD/"
    - SEPARATE_PROCESS_JVM  = ".../jvm/java-8-openjdk-amd64/"
    - JAVA_HOME             = ".../jvm/java-8-openjdk-amd64/"

3. Add the following to the PYTHONPATH environmental variable, where ".../" is replaced by the full directory:
    - ".../Jmodelica-1.17/Python"
    - ".../Jmodelica-1.17/Python/pymodelica"
    - ".../MPCPy"

4. Add the Modelica Standard Library and Modelica Buildings Library to the MODELICAPATH environmental variable

5. Test the installation and explore MPCPy use-cases by running the [unittests](https://github.com/lbl-srg/MPCPy/tree/master/unittests).  See the [README](https://github.com/lbl-srg/MPCPy/blob/master/bin/README.md) on how to run unit tests.

## License
MPCPy is available under the following open-source [license](https://github.com/lbl-srg/MPCPy/blob/master/license.txt).

## Development and Contribution
You are welcome to report any issues in [Issues](https://github.com/lbl-srg/MPCPy/issues).

You are welcome make a contribution by following the steps outlined on the [Contribution Workflow](https://github.com/lbl-srg/MPCPy/wiki/Contribution-Workflow) page.
