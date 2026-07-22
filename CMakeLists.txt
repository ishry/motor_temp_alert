cmake_minimum_required(VERSION 3.0.2)
project(motor_temp_alert)

find_package(catkin REQUIRED COMPONENTS
  rospy
  trans_ros_bridge
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/motor_temp_alert.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
