adh_add_library(
    NAME ZFitsIO
    SOURCES
        Checksum.cpp
        IZStream.cpp
        ricecomp.cpp
        MemoryManager.cpp
        ProtobufIFits.cpp
        ZIFits.cpp
        Huffman.cpp
        minilzo.cpp
        ProtobufToFits.cpp
        ProtobufZOFits.cpp
        ProtobufOFits.cpp
        ProtoSerialZOFits.cpp
        ZOFits.cpp
        IFits.cpp
        OFits.cpp
        FlatProtobufZOFits.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/Checksum.h
        ${CMAKE_CURRENT_LIST_DIR}/FitsDefs.h
        ${CMAKE_CURRENT_LIST_DIR}/Huffman.h
        ${CMAKE_CURRENT_LIST_DIR}/IFits.h
        ${CMAKE_CURRENT_LIST_DIR}/IZStream.h
        ${CMAKE_CURRENT_LIST_DIR}/lzoconf.h
        ${CMAKE_CURRENT_LIST_DIR}/lzodefs.h
        ${CMAKE_CURRENT_LIST_DIR}/MemoryManager.h
        ${CMAKE_CURRENT_LIST_DIR}/minilzo.h
        ${CMAKE_CURRENT_LIST_DIR}/OFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufIFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufToFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtoSerialZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ricecomp.h
        ${CMAKE_CURRENT_LIST_DIR}/ZIFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/Queue.h
        ${CMAKE_CURRENT_LIST_DIR}/FlatProtobufZOFits.h
    LINK_LIBRARIES
        ADHCore
        zstd::libzstd_shared
        ZLIB::ZLIB
    EXPORT ${PROJECT_NAME}Targets
)
add_library(${PROJECT_NAME}::ZFitsIO ALIAS ZFitsIO)

target_include_directories(ZFitsIO PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDE_DIR}>
)
target_compile_features(ZFitsIO PUBLIC cxx_std_11)
set_target_properties(
    ZFitsIO PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)

macro(zfits_add_test TESTNAME)
    add_executable(${TESTNAME} ${ARGN})
    target_link_libraries(${TESTNAME} PRIVATE ZFitsIO zstd::libzstd_shared)
    add_test(NAME ${TESTNAME} COMMAND ${TESTNAME})
endmacro()

zfits_add_test(UnitTestHeaderKeys UnitTestHeaderKeys.cpp)
zfits_add_test(UnitTestAnyArrayTypesToFits UnitTestAnyArrayTypesToFits.cpp)
zfits_add_test(UnitTestMultipleFitsTables UnitTestMultipleFitsTables.cpp)
zfits_add_test(UnitTestProtobufZFits UnitTestProtobufZFits.cpp)
zfits_add_test(UnitTestSimultaneousReadWrite UnitTestSimultaneousReadWrite.cpp)
zfits_add_test(UnitTestCtaR1ToZFits UnitTestCtaR1ToZfits.cpp)
zfits_add_test(UnitTestReadExistingFiles UnitTestReadExistingFiles.cpp)
