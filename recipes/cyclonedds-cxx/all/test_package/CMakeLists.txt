cmake_minimum_required(VERSION 3.8)
project(test_package CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(cyclonedds COMPONENTS ddsc REQUIRED CONFIG)
find_package(cyclonedds-cxx COMPONENTS ddscxx REQUIRED CONFIG)

add_executable(test_package test_package.cpp HelloWorldData.cpp)
target_include_directories(test_package PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(${PROJECT_NAME} PRIVATE cyclonedds-cxx::ddscxx cyclonedds::ddsc)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
