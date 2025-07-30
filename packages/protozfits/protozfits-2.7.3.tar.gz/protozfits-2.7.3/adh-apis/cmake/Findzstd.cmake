# try first via config
find_package(zstd CONFIG QUIET)
if (zstd_FOUND)
    message(STATUS "Found zstd via config")

    # provide legacy variables additionally to targets
    if(TARGET zstd::libzstd_shared)
        message(STATUS "Using shared zstd library zstd::libzstd")
        get_target_property(zstd_INCLUDE_DIR zstd::libzstd_shared INTERFACE_INCLUDE_DIRECTORIES)
        get_target_property(zstd_LIBRARY zstd::libzstd_shared LOCATION)
    else()
        message(STATUS "Using static zstd library for zstd::libzstd")
        get_target_property(zstd_INCLUDE_DIR zstd::libzstd_static INTERFACE_INCLUDE_DIRECTORIES)
        get_target_property(zstd_LIBRARY zstd::libzstd_static LOCATION)
    endif()
else()
    message(STATUS "Did not find zstd via config, trying pkg-config")
    # use pkg config to get a starting point for search
    find_package(PkgConfig QUIET)
    pkg_check_modules(PC_zstd QUIET libzstd)
    set(zstd_VERSION ${PC_zstd_VERSION})

    # search for headers and library
    find_path(zstd_INCLUDE_DIR
        NAMES "zstd.h"
        PATHS ${PC_zstd_INCLUDE_DIRS}
    )
    find_library(zstd_LIBRARY
        NAMES "${CMAKE_SHARED_LIBRARY_PREFIX}zstd${CMAKE_SHARED_LIBRARY_SUFFIX}"
        PATHS ${PC_zstd_LIBRARY_DIRS}
    )

    if(zstd_LIBRARY AND zstd_INCLUDE_DIR)
        set(zstd_FOUND ON)
    endif()

    # provide target
    if(zstd_FOUND AND NOT TARGET zstd::libzstd_shared)
        add_library(zstd::libzstd_shared UNKNOWN IMPORTED GLOBAL)
        set_target_properties(zstd::libzstd_shared PROPERTIES
            IMPORTED_LOCATION "${zstd_LIBRARY}"
            INTERFACE_COMPILE_OPTIONS "${PC_zstd_CFLAGS_OTHER}"
            INTERFACE_INCLUDE_DIRECTORIES "${zstd_INCLUDE_DIR}"
        )
    endif()
endif()

message(STATUS "zstd library: ${zstd_LIBRARY}")
message(STATUS "zstd include: ${zstd_INCLUDE_DIR}")

# target without namespace for backwards compatibility
add_library(zstd ALIAS zstd::libzstd_shared)


include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(zstd
  FOUND_VAR zstd_FOUND
  REQUIRED_VARS
    zstd_LIBRARY
    zstd_INCLUDE_DIR
  VERSION_VAR zstd_VERSION
)
