Introduction
============
MPCPy facilitates the testing and implementation of occupant-integrated model predictive control (MPC) for building systems.  The software package focuses on the use of data-driven simplified physical or statistical models to predict building performance and optimize control.  Four main modules contain object classes to import data, interact with real or emulated systems, estimate and validate data-driven models, and optimize control inputs.  Three other modules contain classes to help track units and provide additional, mainly internal, functionality to MPCPy.

- **ExoData** classes collect external data and process it for use within MPCPy.
- **System** classes represent real or emulated systems to be controlled, collecting measurements from and providing control inputs to the systems.
- **Models** classes represent system models for MPC, managing model simulation, estimation, and validation.
- **Optimization** classes formulate and solve the MPC optimization problems using Models objects.
- **Variable** and **Unit** classes together maintain the association of static or timeseries data with units.
- **Utility** classes provide functionality needed across modules and for interactions with external components.

While MPCPy provides an integration platform, it relies on third-party software packages for model implementation, simulators, parameter estimation algorithms, and optimization solvers.  See Section 2 for a dependencies list of the current release.
