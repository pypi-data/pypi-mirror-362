set(CMAKE_POSITION_INDEPENDENT_CODE ON)
if(UNIX AND NOT APPLE)
    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++ -static-libgcc")
    endif()
elseif(APPLE)
    set(CMAKE_CXX_FLAGS "")
elseif(WIN32)

    set(CMAKE_CXX_FLAGS "/DWIN32")
endif()


find_package(Threads REQUIRED)
include_directories(include)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11/include)
aux_source_directory(src SOURCE)
pybind11_add_module(acc
        pyfunc.cpp
        src/wignerSymbols.cpp
        src/func.cpp
        )