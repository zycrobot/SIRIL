cmake_minimum_required(VERSION 3.0.2)
project(forcep)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  omni_msgs
  robot_state_publisher
  roscpp
  sensor_msgs
  std_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES forcep
  CATKIN_DEPENDS geometry_msgs omni_msgs robot_state_publisher roscpp sensor_msgs std_msgs
  DEPENDS system_lib
)


include_directories(
  ${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS}
  )


add_executable(forcep_node src/forcep_node.cpp src/GalilControl.cpp)
target_link_libraries(forcep_node gclib gclibo ncurses ${catkin_LIBRARIES})
add_dependencies(forcep_node ${catkin_LIBRARIES})

