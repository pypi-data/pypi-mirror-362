##Basic CMake environment to build adh stuff within acada
##Coming originally from the deprecated "CTATools" project, with contributions from LAPP

include (CMakeParseArguments)

include(ADHAddLibrary)
include(Git)


##
## Add files starting with test_ as test simple cases (simple meaning
## they have no arguments). for fancier ones, you need to add them
## manually
##
function(adh_add_tests MODULENAME TEST_PATTERN)
  set(options )
  set(oneValueArgs MODULENAME PATTERN)
  set(multiValueArgs SOURCES )
  cmake_parse_arguments( TEST "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  # add C++ tests (files named test_*.cpp)
  file(GLOB testfiles ${TEST_PATTERN})
  foreach(file ${testfiles})
    get_filename_component( name ${file} NAME_WE )
    add_executable( ${name} ${file} )
    target_link_libraries(${name} PRIVATE ${MODULENAME} ${EXTRA_LIBS} )
    add_test(NAME ${MODULENAME}::${name} COMMAND ${PROJECT_BINARY_DIR}/bin/${name} )
    message( STATUS "added c++ test ${MODULENAME} -> ${name}")
  endforeach()
endfunction()

#Colored output
string(ASCII 27 Esc)
set(ColorReset  "${Esc}[m")
set(Bold        "${Esc}[1m")
set(Red         "${Esc}[31m")
set(Green       "${Esc}[32m")
set(Yellow      "${Esc}[33m")
set(Blue        "${Esc}[34m")
set(Magenta     "${Esc}[35m")
set(Cyan        "${Esc}[36m")
set(White       "${Esc}[37m")
set(BoldRed     "${Esc}[1;31m")
set(BoldGreen   "${Esc}[1;32m")
set(BoldYellow  "${Esc}[1;33m")
set(BoldBlue    "${Esc}[1;34m")
set(BoldMagenta "${Esc}[1;35m")
set(BoldCyan    "${Esc}[1;36m")
set(BoldWhite   "${Esc}[1;37m")

# Allow CTests to run
enable_testing()

# Put exectiables and libraries in a common place (so that when
# developing code they are in a similar file structure to where they
# would be copied if you ran 'make install')
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib)

#ensure a build type is specified
IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Debug CACHE STRING
      "If from Makefile: Please set BUILD_TYPE env variable to define the type of build\n\
       If from CMake: please pass option as CMAKE_BUILD_TYPE.\n\
       Options are: Debug Release ACS or Profiler."
      FORCE)
ENDIF(NOT CMAKE_BUILD_TYPE)

IF (CMAKE_BUILD_TYPE MATCHES ACS)
    message("Building for ACS components integration")
    add_definitions(-DACS_BUILD)
ENDIF(CMAKE_BUILD_TYPE MATCHES ACS)

include(ADHVersion)
#add extra warnings
set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wextra")

#Removed -march=native so that software is portable
#set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native")

# ==============================================================================
# set up compiler optimization and flags
# ==============================================================================
if ( ${CMAKE_BUILD_TYPE} STREQUAL "Coverage")
	set(CMAKE_CXX_FLAGS "-O0 -g")
elseif($CMAKE_BUILD_TYPE} STREQUAL "Debug")
	set(CMAKE_CXX_FLAGS "-O0 -g")
else()
	set(CMAKE_CXX_FLAGS "-O3")
endif()

set(C_PLUSPLUS_11_FLAG "-std=c++11")
set(OLD_GCC "false")

# ==============================================================================
# Make sure that the compiler is up to date
# ==============================================================================
if(${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU")
    # require at least gcc 4.1 with compatibility WARNING, v4.7 for full compatibility
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4.1)
        message(FATAL_ERROR "GCC version must be at least 4.1!")
    endif()
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4.7)
        message(WARNING "${Yellow}You are using an old version of gcc: this project may not compile, use at your own risks !${ColorReset}")
        set(C_PLUSPLUS_11_FLAG "-std=c++0x")
        set(OLD_GCC "true")
    endif()
elseif (${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang")
    # or at least clang 3.2
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 3.2)
        message(FATAL_ERROR "Clang version must be at least 3.3!")
    endif()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
else()
    message(WARNING "#{Yellow}You are using an unsupported compiler! Compilation has only been tested with Clang (>=3.3) and GCC (>=4.7).  Try 'CXX=<path-to-g++> cmake ..' to set a specific GCC version${ColorReset}")
endif()

## enable C++11 standard
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${C_PLUSPLUS_11_FLAG}")

# ==============================================================================
# Add a CMAKE_BUILD_TYPE for a profiler compilation
# This target add -pg option to compiler
# ==============================================================================
SET( CMAKE_CXX_FLAGS_PROFILER "-pg -O0" CACHE STRING
    "Flags used by the C++ compiler during profiler builds."
    FORCE )

MARK_AS_ADVANCED(CMAKE_CXX_FLAGS_PROFILER)

#make sure that we can import other cmake files in the same directory as this file
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_LIST_DIR}/")

include(CheckIncludeFiles)
include(CheckLibraryExists)

if (${CMAKE_BUILD_TYPE} STREQUAL "Coverage")
  include (CodeCoverage)
	append_coverage_compiler_flags()
	set(NAME "Coverage")
	setup_target_for_coverage_gcovr_xml(NAME "Coverage" EXECUTABLE "ctest")
endif()

# ==============================================================================
# check for necessary libraries:
# ==============================================================================

find_package(Threads)

## include ZeroMQ libraries
find_package(ZEROMQ REQUIRED) # use Resources/CMakeModules/FindZEROMQ.cmake ? Apparently not
include_directories(${ZEROMQ_INCLUDE_DIR})
set (ZMQ_INCLUDES ${ZEROMQ_INCLUDE_DIR})
set (ZMQ_LIBS     ${ZEROMQ_LIBRARIES})
set (EXTRA_LIBS ${EXTRA_LIBS} ${ZMQ_LIBS} )

# include Protocol Buffers
find_package(Protobuf REQUIRED) # use cmake default FindProtobuf.cmake
include_directories(BEFORE ${PROTOBUF_INCLUDE_DIRS})

message(STATUS "Using zeromq at ${ZMQ_INCLUDES}")
message(STATUS "Using protobuf library: ${PROTOBUF_LIBRARY}")
message(STATUS "Using protobuf compiler: ${PROTOBUF_PROTOC_EXECUTABLE}")
message(STATUS "Using protobuf includes: ${PROTOBUF_INCLUDE_DIR}")

# ==============================================================================
# Generate header file with compilation configuration
# ==============================================================================
configure_file (
  "${CMAKE_CURRENT_LIST_DIR}/../CMakeDefs.h.in"
  "${CMAKE_BINARY_DIR}/CMakeDefs.h"
  )

# ==============================================================================
# Add base include useful for all subprojects
# ==============================================================================
include_directories("${PROJECT_SOURCE_DIR}")

# ==============================================================================
# Locate source protobuf files
# ==============================================================================
set(PROTOBUF_FILES_LOCATION "${CMAKE_CURRENT_LIST_DIR}/../data_model/raw/*.proto")
MESSAGE("Looking for protobuf files at ${PROTOBUF_FILES_LOCATION}")
file (GLOB DataModelProto "${PROTOBUF_FILES_LOCATION}")

#allow sub-projects to link to generated protobufs headers
include_directories (${CMAKE_BINARY_DIR})
include_directories (${CMAKE_SOURCE_DIR})
include_directories (${CMAKE_CURRENT_LIST_DIR}/..)
include_directories (${CMAKE_CURRENT_LIST_DIR}/../zfits)
include_directories (${CMAKE_CURRENT_LIST_DIR}/../zmq_streamer)
include_directories (${CMAKE_CURRENT_LIST_DIR}/../commandline_input)

PROTOBUF_GENERATE_CPP(ProtoSources ProtoHeaders ${DataModelProto})

adh_add_library(
    NAME ADHCore
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/../BasicDefs.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../ThreadedObject.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../AnyArrayHelper.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zmq_streamer/ZMQStreamer.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../Logger.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/Config.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/ConfigService.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/InsertionOperator.cpp
         ${ProtoSources}
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/../AnyArrayHelper.h
        ${CMAKE_CURRENT_LIST_DIR}/../ThreadedObject.h
        ${CMAKE_CURRENT_LIST_DIR}/../Logger.h
        ${CMAKE_CURRENT_LIST_DIR}/../BasicDefs.h
         ${ProtoHeaders}
    LINK_LIBRARIES
    #link core library against protocol buffers, zeroMQ and the configuration service
        ${ZMQ_LIBS} ${CMAKE_THREAD_LIBS_INIT} ${PROTOBUF_LIBRARY}
)

adh_add_library(
    NAME ZFitsIO
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/Checksum.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/FlatProtobufZOFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/Huffman.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/IFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/IZStream.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/MemoryManager.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/minilzo.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/OFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtobufIFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtobufOFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtobufToFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtobufZOFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtoSerialZOFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ricecomp.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ZIFits.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ZOFits.cpp

    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/ProtobufZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/../zfits/FlatProtobufZOFits.h
)

find_package(zstd REQUIRED)
add_dependencies(ZFitsIO ADHCore zstd::libzstd_shared)
