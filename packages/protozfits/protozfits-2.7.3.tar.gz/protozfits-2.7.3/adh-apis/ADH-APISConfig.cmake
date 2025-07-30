# export file, so other projects can use this via `find_package`
include(CMakeFindDependencyMacro)

# we need to find the external depedencies here
# essentially we need to repeat all the `find_package` calls from the build
# here as `find_dependency`
find_dependency(Threads REQUIRED)

# uses Protobuf.cmake and FindZEROMQ.cmake
# which are installed to the same directory as this file
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})
include(Protobuf)
find_dependency(zstd REQUIRED)
find_dependency(ZEROMQ REQUIRED)
find_dependency(ZLIB REQUIRED)


# Include the auto-generated targets file
include("${CMAKE_CURRENT_LIST_DIR}/ADH-APISTargets.cmake")
