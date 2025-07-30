# =============================================================================
#      Top-level CMake for APIs of the CTA Array Data Handler project
# =============================================================================
cmake_minimum_required (VERSION 3.15...3.19 FATAL_ERROR)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
include(ADHVersion)
project(ADH-APIS VERSION "${ADH_VERSION_MAJOR}.${ADH_VERSION_MINOR}.${ADH_VERSION_PATCH}" LANGUAGES C CXX)

if(APPLE)
    # SWAT currently does not work on MACOS, so switching off by default
    # Can be turned on to test if its working
    option(SWAT "Build swat interface" OFF)
else()
    option(SWAT "Build swat interface" ON)
endif()

include(GNUInstallDirs) # initialize CMAKE_INSTALL_*DIR
include(CTest)

include(RPATHHandling)
include(DefaultBuildType)
include(Git)
include(ADHAddLibrary)


# find dependencies
find_package(Threads REQUIRED)
find_package(ZEROMQ REQUIRED) # uses cmake/FindZEROMQ.cmake
find_package(ZLIB REQUIRED)
include(Protobuf)
find_package(zstd REQUIRED)

# Locate source protobuf files
set(PROTOBUF_PATTERN "${CMAKE_CURRENT_LIST_DIR}/data_model/raw/*.proto")
message(STATUS "Looking for protobuf files with pattern ${PROTOBUF_PATTERN}")
file(GLOB DataModelProto "${PROTOBUF_PATTERN}")
protobuf_generate_cpp(ProtoSources ProtoHeaders ${DataModelProto})

configure_file (
  CMakeDefs.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/CMakeDefs.h
)
adh_add_library(
    NAME ADHCore
    SOURCES
        BasicDefs.cpp
        ThreadedObject.cpp
        AnyArrayHelper.cpp
        zmq_streamer/ZMQStreamer.cpp
        Logger.cpp
        commandline_input/Config.cpp
        commandline_input/ConfigService.cpp
        commandline_input/InsertionOperator.cpp
        ${ProtoSources}
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/AnyArrayHelper.h
        ${CMAKE_CURRENT_LIST_DIR}/ThreadedObject.h
        ${CMAKE_CURRENT_LIST_DIR}/Logger.h
        ${CMAKE_CURRENT_LIST_DIR}/BasicDefs.h
        ${CMAKE_CURRENT_LIST_DIR}/ColoredOutput.h
        ${ProtoHeaders}
    LINK_LIBRARIES
    #link core library against protocol buffers, zeroMQ and the configuration service
    ${ZEROMQ_LIBRARIES} Threads::Threads
    EXPORT ${PROJECT_NAME}Targets
)
add_library(${PROJECT_NAME}::ADHCore ALIAS ADHCore)

# recent versions of cmake (e.g. cmake3 on centos7) provide the modern cmake target
# which is preferable as it correctly handles both libraries and include dirs including
# transitive dependencies
if(TARGET protobuf::libprotobuf)
    message(STATUS "Linking protobuf via cmake target")
    target_link_libraries(ADHCore PUBLIC protobuf::libprotobuf)
else()
    message(STATUS "Linking protobuf via Protobuf_{LIBRARIES,INCLUDE_DIRS}")
    target_link_libraries(ADHCore PUBLIC ${Protobuf_LIBRARIES})
    target_include_directories(ADHCore PUBLIC ${Protobuf_INCLUDE_DIRS})
endif()

target_include_directories(ADHCore PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/commandline_input>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/zmq_streamer>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_compile_features(ADHCore PUBLIC cxx_std_11)
set_target_properties(
    ADHCore PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)

add_subdirectory(zfits)

add_executable(example_events_server ExecExampleEventsServer.cpp)
target_link_libraries(example_events_server PRIVATE ADHCore)

add_executable(example_events_server_flashcam ExecExampleEventsServerFlashcamStyle.cpp
                                      R1CherenkovDataImpl.cpp)
target_link_libraries(example_events_server_flashcam PRIVATE ADHCore)

add_executable(example_events_reader_flashcam ExecExampleEventsReaderFlashcamStyle.cpp
                                      R1CherenkovDataImpl.cpp)
target_link_libraries(example_events_reader_flashcam PRIVATE ADHCore)

add_executable(example_events_consumer ExecExampleEventsConsumer.cpp)
target_link_libraries(example_events_consumer PRIVATE ADHCore)

install(
    TARGETS example_events_server example_events_consumer
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    COMPONENT Development
)

if(SWAT)
    add_subdirectory(swat)
    add_executable(example_swat_client ExecExampleSWATClient.cpp)
    target_link_libraries(example_swat_client PRIVATE swat)
    target_link_libraries(example_swat_client PRIVATE ADHCore)
    target_compile_options(example_swat_client PRIVATE -std=c++11 -g -O1 -Wno-write-strings -Wno-sign-compare)

    install(
        TARGETS example_swat_client
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        COMPONENT Development
    )
endif()

# Creating the export files, so other projects can use this project via `find_package`

# provide version information
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    ${PROJECT_NAME}ConfigVersion.cmake
    VERSION ${PACKAGE_VERSION}
    COMPATIBILITY SameMajorVersion
)

# create the file describing all targets exported by this project
install(
    EXPORT ${PROJECT_NAME}Targets
    NAMESPACE ${PROJECT_NAME}::
    DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/${PROJECT_NAME}
)

# install the main Config file and the ConfigVersion file
install(
    FILES
        "${PROJECT_NAME}Config.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        "cmake/FindZEROMQ.cmake"
        "cmake/Protobuf.cmake"
        "cmake/Findzstd.cmake"
    DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/${PROJECT_NAME}
)

include(CPack)
