cmake_minimum_required(VERSION 3.10)
project(Lab7_CV_Threads)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

file(GLOB SOURCES "*.cpp")
add_executable(lab7 ${SOURCES})

target_link_libraries(lab7 ${OpenCV_LIBS} pthread)
