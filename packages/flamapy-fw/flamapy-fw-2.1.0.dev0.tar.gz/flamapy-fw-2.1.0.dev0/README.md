# Flamapy
Flamapy is a Python-based AAFM framework that takes into consideration previous AAFM tool designs and enables multi-solver and multi-metamodel support for the integration of AAFM tooling on the Python ecosystem.

The main features of the framework are:
* Easy to extend by enabling the creation of new plugins following a semi-automatic generator approach.
* Support multiple variability models. Currently, it provides support for cardinality-based feature models. However, it is easy to integrate others such as attributed feature models
* Support multiple solvers. Currently, it provides support for the PySAT metasolver, which enables more than ten different solvers.
* Support multiple operations. It is developed, having in mind multi-model operations such as those depicted by Familiar  and single-model operations.

## Available plugins
[flamapy](https://github.com/flamapy/flamapy). This is a meta-package that installs all plugins for feature modelling analysis and the CLI and Python interfaces. 
[flamapy-fm](https://github.com/flamapy/fm_metamodel) This is a plugin that provides support for feature modelling. Include several readers/writers from different formats.
[flamapy-sat](https://github.com/flamapy/pysat_metamodel) This plugin enable different analysis operations that require sat as backend.
[flamapy-bdd](https://github.com/flamapy/bdd_metamodel) This plugin enable different analysis operations that require bdd as backend. 

## Documentation

All the proyect related documentation can be found in wiki format at [the tool website](https://flamapy.github.io/)

## Changelog
Detailed changes for each release are documented in the [release notes](https://github.com/diverso-lab/core/releases)

## Contributing

See [CONTRIBUTING.md](https://github.com/diverso-lab/core/blob/master/CONTRIBUTING.md)
