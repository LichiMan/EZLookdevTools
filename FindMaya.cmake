
if (NOT_DEFINED MAYA_VERSION)
    set(MAYA_VERSION 2018 CACHE STRING "Maya Version")
endif()

set(MAYA_INSTALL_BASE_SUFFIX "")
set(MAYA_LIB_SUFFIX "lib")
set(MAYA_INC_SUFFIX "include")
if (WIN32)
    # Windows
    set(MAYA_INSTALL_BASE_DEFAULT "C:\Program Files\Autodesk"
    set(OPENMAYA OpenMaya.lib)
elseif(APPLE)
    # Mac
    set(MAYA_INNSTALL_BASE_DEFAULT "//Applications/Autodesk"
    set(OPEN_MAYA libOpenMaya.dylib)
    set(MAYA_LIB_SUFFIX "Maya.app/Contents/MacOS")
    set(MAYA_INC_SUFFIX "devkit/include")
else()
    # Linux
    set(MAYA_INSTALL_BASE_DEFAULT "usr/autodesk")
    set(MAYA_INSTALL_BASE_SUFFIX -x64)
    set(OPENMAYA libOpenMaya.so)
endif()

set(MAYA_INSTALL_BASE_PATH ${MAYA_INSTALL_BASE_DEFAULT} CACHE STRING "Root Maya installation path")
set(MAYA_LOCATION ${MAYA_INSTALL_BASE_PATH}/maya${MAYA_VERSION}${MAYA_INSTALL_BASE_SUFFIX})

find_path(MAYA_LIBRARY_DIR ${OPENMAYA}
    PATHS
        ${MAYA_LOCATION}
        $env{MAYA_LOCATION}
    PATH_SUFFIXES
        "${MAYA_LIB_SUFFIX}/"
    DOC "Maya library path"
}

find_path(MAYA_INCLUDE_DIR maya/MFn.h
    PATHS
        ${MAYA_LOCATION}
        $env{MAYA_LOCATION}
    PATH_SUFFIXES
        "${MAYA_LIB_SUFFIX}/"
    DOC "Maya library path"