# if you want to define more build types (e.g. one for profiling / coverage)
# do so by doing list(APPEND SUPPORTED_BUILD_TYPES ...) before including this modules
list(APPEND SUPPORTED_BUILD_TYPES Release Debug RelWithDebInfo MinSizeRel Coverage)

# Set a default build type if none was specified
set(DEFAULT_BUILD_TYPE "Release")

# CMAKE_CONFIGURATION_TYPES is for multi generators, we only need to
# set the build type for the single type generators
if(NOT CMAKE_CONFIGURATION_TYPES)
    if(NOT CMAKE_BUILD_TYPE)
        # if we are in a git repo, use Debug by default
        if(EXISTS "${CMAKE_SOURCE_DIR}/.git")
            message(STATUS "In git repository, setting default build type to 'Debug'")
            set(DEFAULT_BUILD_TYPE "Debug")
        endif()
        message(STATUS "Setting build type to '${DEFAULT_BUILD_TYPE}' as none was specified.")
        set(CMAKE_BUILD_TYPE "${DEFAULT_BUILD_TYPE}" CACHE
            STRING "Choose the type of build." FORCE)
        # Set the possible values of build type for cmake-gui
        set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS ${SUPPORTED_BUILD_TYPES})
    else()
        message(STATUS "Using CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}")
    endif()

    list(FIND SUPPORTED_BUILD_TYPES ${CMAKE_BUILD_TYPE} IS_BUILD_TYPE_SUPPORTED)
    if(${IS_BUILD_TYPE_SUPPORTED} EQUAL -1)
        message(FATAL_ERROR "CMAKE_BUILD_TYPE of ${CMAKE_BUILD_TYPE} is not supported. Use one of ${SUPPORTED_BUILD_TYPES}")
    endif()

endif()
