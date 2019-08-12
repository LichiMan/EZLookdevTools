cmake_minimum_required(VERSION "3.10.2")

project("EZTools")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIRECTORY}/modules)

add_subdirectory(maya_toolkit)
#add_executable("$(PROJECT_NAME)" "__init__.py")

#install(TARGETS "$(PROJECT_NAME)" DESTINATION bin)
#install(FILES "katana/__init__.py" "maya/__init__.py" DESTINATION source)