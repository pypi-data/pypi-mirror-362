##=======================================================================
## Retrieve the current git revision
##=======================================================================
set(GIT_REVISION_ADH "unknown")
set(GIT_REVISION_ADH_APIS "unknown")

find_package(Git)

if(GIT_FOUND)
  execute_process(
    COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
    WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/.."
    OUTPUT_VARIABLE GIT_REVISION_ADH_APIS
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  message( STATUS "ADH-APIS GIT hash: ${GIT_REVISION_ADH_APIS}")
else()
  message(STATUS "GIT not found")
endif()
