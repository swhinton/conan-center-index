cmake_minimum_required(VERSION 3.16)
project(test_package C)
set(CMAKE_VERBOSE_MAKEFILE ON)
find_package(gherkin-c REQUIRED CONFIG)

add_executable(test_package test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE gherkin-c::gherkin)
