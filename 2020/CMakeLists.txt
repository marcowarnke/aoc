cmake_minimum_required(VERSION 3.13)
project(aoc2020)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add project files
set(ROOT "${CMAKE_CURRENT_SOURCE_DIR}")

# User files
# Add source files
file(GLOB_RECURSE SRCFILES
        ${CMAKE_SOURCE_DIR}/src/*.c
        ${CMAKE_SOURCE_DIR}/src/*.cpp
        )

# Add header files
file(GLOB_RECURSE HEADER_FILES
        ${CMAKE_SOURCE_DIR}/include/*.h
        ${CMAKE_SOURCE_DIR}/include/*.hpp
        )

include_directories(
        "${CMAKE_SOURCE_DIR}/src"
        "${CMAKE_SOURCE_DIR}/include"
)

add_executable(aoc ${SRCFILES} ${HEADER_FILES})
target_precompile_headers(aoc PRIVATE include/pch.h)
