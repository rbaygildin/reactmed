cmake_minimum_required(VERSION 3.8)
project(reactmed_client)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_PREFIX_PATH "/Applications/Qt/5.9.2/clang_64")
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5Core REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Gui REQUIRED)

set(BOOST_INCLUDE_DIR /usr/local/Cellar/boost/1.65.1/include)
set(BOOST_LIBRARY_DIR /usr/local/Cellar/boost/1.65.1/lib)
find_package(Boost COMPONENTS system filesystem REQUIRED)
include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIR})


set(SOURCE_FILES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui)

add_executable(reactmed_client ${SOURCE_FILES})
target_link_libraries(reactmed_client Qt5::Core Qt5::Widgets ${Boost_LIBRARIES})