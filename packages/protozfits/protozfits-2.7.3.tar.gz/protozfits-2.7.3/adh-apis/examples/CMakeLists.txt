# Minimal example CMakeLists.txt that shows how
# to use adh-apis in a downstream project.
cmake_minimum_required(VERSION 3.15)

project(test VERSION 0.1.0)

find_package(ADH-APIS CONFIG REQUIRED)

add_executable(main main.cpp)
target_link_libraries(main PRIVATE ADH-APIS::ZFitsIO)
