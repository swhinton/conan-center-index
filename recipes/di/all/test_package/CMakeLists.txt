cmake_minimum_required(VERSION 3.1.3)
project(PackageTest CXX)

find_package(di REQUIRED CONFIG)

add_executable(test_package example.cpp)
set_target_properties(test_package PROPERTIES CXX_STANDARD 14)
target_link_libraries(test_package di::di)
