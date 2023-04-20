cmake_minimum_required(VERSION 3.16)
project(test_package C)
set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(cyclonedds COMPONENTS ddsc REQUIRED CONFIG)

include(cmake/idlc/Generate.cmake)

idlc_generate(TARGET HelloWorldData_lib FILES "HelloWorldData.idl" WARNINGS no-implicit-extensibility)

add_executable(test_package test_package.c)
target_include_directories(test_package PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(${PROJECT_NAME} PRIVATE HelloWorldData_lib cyclonedds::ddsc)
