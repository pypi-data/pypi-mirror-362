# HALCON/Python

HALCON/Python is a set of native Python language bindings for HALCON.
This includes interfaces for operators, HDevEngine and interoperability
for third-party libraries like NumPy.

The major design goals for HALCON/Python are simplicity and rapid prototyping.

NOTE: A native installation of HALCON is required in addition to this package.
This package only contains the Python bindings.

### Platform Independence

HALCON/Python is officially supported on all Tier 1 platforms supported by
CPython, the reference implementation of the Python programming language. That
is x64-win64, x64-linux. That said, it is possible that other platforms and
alternative Python implementations are functional, of course native HALCON
binaries also need to be available on that platform.
