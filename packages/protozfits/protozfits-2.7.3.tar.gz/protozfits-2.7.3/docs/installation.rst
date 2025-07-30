Installation
============

User Installation
-----------------

As a user, install from PyPI:

.. code-block:: shell

    $ pip install protozfits

Or ``conda-forge``:

.. code-block:: shell

    $ mamba install -c conda-forge protozfits



Developer Setup
---------------

This project uses `scikit-build-core <https://scikit-build-core.readthedocs.io/>`_
and `pybind11 <https://pybind11.readthedocs.io/>`_
to build python bindings to the ``libZFitsIO`` that is part of the
`adh-apis <https://gitlab.cta-observatory.org/cta-computing/common/acada-array-elements/adh-apis>`_
repository.

The ``adh-apis`` are included as a submodule, so clone recursively or run this command in case you forgot:

.. code-block:: shell

   $ git submodule update --init


To build protozfits from source, you need the following C++ libraries and tools available:

- C++ compiler supporting C++11 (newer versions of protobuf require C++14 or C++17)
- ``cmake`` and ``ninja`` (can also be installed with pip)
- ``protobuf`` C++ library and the ``protoc`` compiler (https://protobuf.dev/)
- ``zeromq`` C library

On Alma Linux 9, you can run:

.. code-block:: shell

   $ dnf install -y 'dnf-command(config-manager)'
   $ dnf config-manager -y --set-enabled crb
   $ dnf install -y epel-release
   $ dnf install -y python3 python3-devel cmake ninja-build gcc gcc-c++ protobuf-devel protobuf-compiler zeromq-devel


After that, you create a virtual environment, install the python build requirements
and then install the package in development mode:

.. code-block:: shell

   $ git clone -r git@gitlab.cta-observatory.org:cta-computing/common/protozfits-python
   $ cd protozfits-python
   $ python -m venv venv
   $ source venv/bin/activate
   $ pip install 'scikit-build-core[pyproject]' pybind11 'setuptools_scm[toml]'
   $ pip install -v -e '.[all]' --no-build-isolation

This will give you a development setup where also the C++ code is rebuilt automatically
on import of the python module.

The same also works with conda, create a conda env instead of a venv above and then follow the same steps.
