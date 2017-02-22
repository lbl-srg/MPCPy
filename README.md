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

**Modelica Compiler and Optimizer, FMU Simulator**
- JModelica 1.17

## Installation
Install MPCPy by placing the parent directory on the PYTHONPATH environmental variable.  Modules and classes can then be imported into a python environment.

Explore the [unittests](https://github.com/lbl-srg/MPCPy/tree/master/unittests) directory for example MPCPy use-cases.  See the [README](https://github.com/lbl-srg/MPCPy/blob/master/bin/README.md) on how to run unit tests.

## License
MPCPy is available under the following open-source [license](https://github.com/lbl-srg/MPCPy/blob/master/license.txt)

## Development and Contribution
You are welcome to report any issues in [Issues](https://github.com/lbl-srg/MPCPy/issues).

You are welcome to suggest contributions in the form of [Pull Requests](https://github.com/lbl-srg/MPCPy/pulls).  Please visit the [Contribution Workflow](https://github.com/lbl-srg/MPCPy/wiki/Contribution-Workflow) page for guidance.
