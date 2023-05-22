cmake_minimum_required(VERSION 3.16)
project(test_package CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)
find_package(gunit REQUIRED CONFIG)

add_executable(test_package test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE gunit::gunit)
