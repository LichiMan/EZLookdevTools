cmake_minimum_required(VERSION "3.10.2")

project("LookDevTools")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

set(CUR_MAYA_DIR "C:\\git\\LookDevTools\\lookdevtools")
set(ENV{PYTHONPATH} "${CUR_MAYA_DIR}")


add_subdirectory(lookdevtools/python)

#add_executable("${PROJECT_NAME}" "lookdevtools/python/maya/__init__.py")

install(TARGETS "${PROJECT_NAME}" DESTINATION bin)
#install(FILES "lookdevtools/maya/__init__.py" DESTINATION source)