cmake_minimum_required(VERSION "3.10.2")

project("LookDevTools")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

add_subdirectory(maya)
add_subdirectory(katana)
add_subdirectory(tools)
add_executable("${PROJECT_NAME}" "__init__.py")

install(TARGETS "${PROJECT_NAME}" DESTINATION bin)
install(FILES "katanat/__init__.py" "maya/__init__.py" "tools/__init__.py" DESTINATION source)