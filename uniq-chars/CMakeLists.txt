cmake_minimum_required(VERSION 2.8)
project(unique-chars)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_FLAGS "-std=c++11 -g -O0 -Wall -fpermissive -Wextra -pedantic")

add_executable(uniq-chars uniq-chars.cpp)

