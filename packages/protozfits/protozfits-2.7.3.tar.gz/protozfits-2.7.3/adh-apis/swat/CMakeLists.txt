find_package(Threads REQUIRED)
adh_add_library(
    NAME swat
    SOURCES
        swat_api.cpp
        swat_api_config.cpp
        swat_packet.cpp
        swat_support.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/swat_api_config.h
        ${CMAKE_CURRENT_LIST_DIR}/swat_api.h
)

target_include_directories(swat PUBLIC ..)
target_compile_features(swat PUBLIC cxx_std_11)
set_target_properties(
    swat PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)
target_compile_options(swat PRIVATE -Wno-write-strings -Wno-sign-compare)
target_link_libraries(swat PUBLIC Threads::Threads m ADHCore)
