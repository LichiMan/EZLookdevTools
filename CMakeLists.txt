cmake_minimum_required(VERSION "3.10.2")

project("EZTools")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIRECTORY}/modules)

add_subdirectory(maya_toolkit)
add_subdirectory(katana_toolkit)
add_subdirectory(tools)
#add_executable("${PROJECT_NAME}" "__init__.py")

#install(TARGETS "${PROJECT_NAME}" DESTINATION bin)
#install(FILES "katana_toolkit/__init__.py" "maya_toolkit/__init__.py" "tools/__init__.py" DESTINATION source)