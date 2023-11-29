cmake_minimum_required(VERSION 3.16)
project(test_package CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(pfs REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(${PROJECT_NAME} PRIVATE pfs::pfs)
