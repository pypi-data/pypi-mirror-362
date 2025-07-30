# try modern version of finding protobuf first
# this is needed to get the protobuf_generate_cpp command
set(protobuf_MODULE_COMPATIBLE ON)
# prefer finding Protobuf via cmake config, the modern approach
find_package(Protobuf CONFIG)
if(Protobuf_FOUND)
    message(STATUS "Found protobuf via cmake config")
else()
    message(WARNING "Falling back to cmake FindProtobuf as Protobuf was not found via CONFIG")
    find_package(Protobuf REQUIRED)
endif()
