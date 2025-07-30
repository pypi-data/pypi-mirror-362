# cmake

Common cmake modules for CTAO computing


Include this repository in your projects as a submodule and then `include()`
modules.

## Provided Modules

### `RPATHHandling.cmake`

Module to add proper RPATH to build and installed libraries and executables
so that setting an ``LD_LIBRARY_PATH`` is unnecessary.

Just include into your project like this:
```
include(cmake/RPATHHandling.cmake)
```

### `BuildType.cmake`

cmake highly recommends always defining a `-DCMAKE_BUILD_TYPE`,
but does not actually have a default for it and also doesn't validate
whether the chosen build type is actually defined.

This module can just be included like this:
```
include(cmake/BuildType.cmake)
```
It will set a default value (Debug if inside a git repository, Release otherwise)
and also validate the given type.

### `GitVersion.cmake`

Module to determine version information from git tag information.

Include the module and then call the `version_from_git` function,
after that, you can use the resulting variables to define the project
version in the `project()` call and for configuring the source file.
```
include(cmake/GitVersion.cmake)
version_from_git(Example LOG)

project(Example VERSION ${Example_GIT_VERSION})
```
The extracted info is stored in `generated/${PROJECT_NAME}GitVersion.cmake` relative from where this file is included.
This file should be included in source distributions, so that version information is available without the full git repository.
