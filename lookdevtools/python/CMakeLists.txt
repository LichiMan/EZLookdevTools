#set(SOURCE_FILES
#    "__init_.py"
#)
#set(SOURCE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/python/maya/maya/__init__.py")

#add_custom_target(compile_py ALL COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/maya/maya/__init__.py WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
find_program(PYTHON "python")

if (PYTHON)
    set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
    set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/module/__init__.py")
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

    configure_file(${SETUP_PY_IN} ${SETUP_PY})

    add_custom_command(OUTPUT ${OUTPUT}
                       COMMAND ${PYTHON} ${SETUP_PY} build
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                       DEPENDS ${DEPS})

    add_custom_target(target ALL DEPENDS ${OUTPUT})

    install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install)")
endif()

macro(add_python_target tgt)
  foreach(file IN LISTS ARGN)
    set(OUT ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/python/maya/maya/${file}.pyc)
    list(APPEND OUT_FILES ${OUT})
    add_custom_command(
        OUTPUT ${OUT}]
        COMMAND ${PYTHON ${file}.py
        COMMAND ${CMAKE_COMMAND} -E touch ${OUT}
    )
  endforeach()
  add_custom_target(${tgt} ALL DEPENDS ${OUT_FILES})
endmacro(add_python_target)


add_python_target(compile_pyc ${CMAKE_CURRENT_SOURCE_DIR}/lookdevtools/python/maya/maya/__init__.py)

find_package(Maya REQUIRED)

include_directories(${MAYA_INCLUDE_DIR})
link_directories(${MAYA_LIBRARY_DIR})

add_library(${PROJECT_NAME} MODULE ${compile_pyc})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})

MAYA_PLUGIN(${PROJECT_NAME})