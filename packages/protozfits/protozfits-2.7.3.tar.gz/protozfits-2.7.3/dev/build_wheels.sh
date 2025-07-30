#!/bin/bash
# This script is meant to be run in the manylinux2014 docker container
# to build wheels.
set -euxo pipefail
PYTHON_VERSIONS=${PYTHON_VERSIONS:-"cp39-cp39 cp310-cp310 cp311-cp311 cp312-cp312 cp313-cp313"}

for PYTHON_VERSION in $PYTHON_VERSIONS; do
  PYBIN="/opt/python/${PYTHON_VERSION}/bin"
  "${PYBIN}/python" -m build --wheel -o wheels
done

ls -l wheels

# Bundle external shared libraries into the wheels
for whl in wheels/*.whl; do
  auditwheel repair "$whl" --plat manylinux2014_x86_64 -w dist
done

# run tests
for PYTHON_VERSION in $PYTHON_VERSIONS; do
  # use a subshell to make sure things are cleaned up in each loop iteration
  (
    PYBIN="/opt/python/${PYTHON_VERSION}/bin"
    wheel=(dist/protozfits-*-${PYTHON_VERSION}-*.whl)
    # install wheel, also make sure we are using wheels and not trying to build numpy from source
    "${PYBIN}/pip" install --only-binary numpy -v "$wheel[tests]"
    # move to tmpdir in a subshell to make sure tests are working outside of source directory
    (cd /tmp; "${PYBIN}/python" -m pytest -v --pyargs protozfits)
  )
done


# build sdist
/opt/python/cp311-cp311/bin/python -m build --sdist

ls -l dist
