cmake_minimum_required(VERSION 2.8.3)
project(ransac_cpp)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)
set(CMAKE_BUILD_TYPE Release)


## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)
find_package(Eigen3 REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES target_processing
#  CATKIN_DEPENDS cv_bridge geometry_msgs pcl_ros roscpp rospy sensor_msgs std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)


# Declaration of package required

## Declare a C++ library
add_library(${PROJECT_NAME}
   src/ransac.cpp
)

add_executable(ransac_curve test/ransac_curve.cpp)
add_dependencies(ransac_curve ${main_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(ransac_curve ${catkin_LIBRARIES} ${PROJECT_NAME})
