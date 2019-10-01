#set(SOURCE_FILES
#    "__init_.py"
#)
#set(SOURCE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/maya/maya/__init__.py")

add_custom_target(compile_py ALL COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/maya/maya/__init__.py WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
macro(add_python_target tgt)
  foreach(file IN LISTS ARGN)
    set(OUT ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/maya/maya/${file}.pyc)
    list(APPEND OUT_FILES ${OUT})
    add_custom_command(
        OUTPUT ${OUT}
        COMMAND python ${file}.py
        COMMAND ${CMAKE_COMMAND} -E touch ${OUT}
    )
  endforeach()
  add_custom_target(${tgt} ALL DEPENDS ${OUT_FILES})
endmacro(add_python_target)

add_python_target(compile_pyc ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/maya/maya/__init__.py)

find_package(Maya REQUIRED)

include_directories(${MAYA_INCLUDE_DIR})
link_directories(${MAYA_LIBRARY_DIR})

add_library(${PROJECT_NAME} MODULE ${compile_py})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})

MAYA_PLUGIN(${PROJECT_NAME})