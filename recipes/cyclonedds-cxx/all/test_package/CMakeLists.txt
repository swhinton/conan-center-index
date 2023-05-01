cmake_minimum_required(VERSION 3.8)
project(test_package CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)

#find_package(iceoryx COMPONENTS iceoryx_binding_c REQUIRED CONFIG)
find_package(cyclonedds COMPONENTS ddsc REQUIRED CONFIG)
find_package(cyclonedds-cxx COMPONENTS idlcxx ddscxx REQUIRED CONFIG)

include(cmake/idlc/Generate.cmake)
include(cmake/idlcxx/Generate.cmake)

idlcxx_generate(TARGET helloworlddata FILES HelloWorldData.idl WARNINGS no-implicit-extensibility)

add_executable(test_package test_package.cpp)
target_include_directories(test_package PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(${PROJECT_NAME} PRIVATE helloworlddata cyclonedds-cxx::ddscxx cyclonedds::ddsc)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
