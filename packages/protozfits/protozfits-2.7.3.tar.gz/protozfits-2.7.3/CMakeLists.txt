cmake_minimum_required (VERSION 3.17...3.25 FATAL_ERROR)

project(python-protozfits VERSION 2.3.0 LANGUAGES C CXX)

include(./cmake/BuildType.cmake)
include(./cmake/Coverage.cmake)
include(./cmake/RPATHHandling.cmake)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

# while the bindings are still part of adh-apis, we need to switch those of, since
# we only want to build our local version, also turn swat off
set(PYTHON OFF)
set(SWAT OFF)
set(CMAKE_INSTALL_LIBDIR "protozfits")
add_subdirectory(adh-apis)

# generate the python protobuf bindings
include(adh-apis/cmake/Protobuf.cmake)
set(PROTOBUF_PATTERN "adh-apis/data_model/raw/*.proto")
message(STATUS "Looking for protobuf files with pattern ${PROTOBUF_PATTERN}")
file(GLOB DataModelProto "${PROTOBUF_PATTERN}")
message(STATUS "Found protobuf files: ${DataModelProto}")
protobuf_generate_python(PROTO_MODULES ${DataModelProto} APPEND_PATH)

# This fixes import statements in the generated python files
# see https://github.com/protocolbuffers/protobuf/issues/1491
add_custom_target(fixed_pyprotos ALL
    sed -E -i\"\" -e 's/^\(import.*_pb2\)/from . \\1/' *.py
    DEPENDS ${PROTO_MODULES}
    COMMAND_EXPAND_LISTS
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

# we call it py internally to make clear its a python target
pybind11_add_module(pyrawzfits src/rawzfits.cpp)
add_dependencies(pyrawzfits fixed_pyprotos)
# but the output library will just be called rawzfits
set_target_properties(pyrawzfits PROPERTIES OUTPUT_NAME rawzfits)

target_link_libraries(pyrawzfits PUBLIC ZFitsIO)
install(TARGETS pyrawzfits DESTINATION protozfits COMPONENT Python)
install(FILES ${PROTO_MODULES} DESTINATION protozfits COMPONENT Python)
