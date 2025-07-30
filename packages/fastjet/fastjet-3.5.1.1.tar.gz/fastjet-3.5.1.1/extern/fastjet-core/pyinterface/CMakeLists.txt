cmake_minimum_required(VERSION 3.16...3.31)

set(UseSWIG_MODULE_VERSION 2)
include(UseSWIG)

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

set_property(SOURCE fastjet.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE fastjet.i PROPERTY SWIG_MODULE_NAME __init__)

swig_add_library(fastjet_swig LANGUAGE python SOURCES fastjet.i OUTPUT_DIR fastjet_swig)
set_property(TARGET fastjet_swig PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)
#set_property(TARGET fastjet_swig PROPERTY INSTALL_RPATH lib)
#set_property(TARGET fastjet_swig PROPERTY INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# NB this is specifically for building scikit-hep/fastjet wheels
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  set_target_properties(fastjet_swig PROPERTIES INSTALL_RPATH "@loader_path/../${CMAKE_INSTALL_LIBDIR};@loader_path/../../../../${CMAKE_INSTALL_LIBDIR}")
else()
  set_target_properties(fastjet_swig PROPERTIES INSTALL_RPATH "$ORIGIN/../${CMAKE_INSTALL_LIBDIR}:$ORIGIN/../../../../${CMAKE_INSTALL_LIBDIR}")
endif()

if (MSVC)
  set_property(TARGET fastjet_swig PROPERTY SUFFIX ".${Python_SOABI}.pyd")
else()
  set_property(TARGET fastjet_swig PROPERTY SUFFIX ".${Python_SOABI}${CMAKE_SHARED_MODULE_SUFFIX}")
endif()

target_link_libraries(fastjet_swig PUBLIC fastjet::fastjet)
target_link_libraries(fastjet_swig PUBLIC fastjet::fastjettools)
target_link_libraries(fastjet_swig PUBLIC Python::Module)

#set_target_properties(fastjet_swig PROPERTIES INSTALL_RPATH "$ORIGIN/../../../../lib")
#set_target_properties(fastjet_swig PROPERTIES INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

if ("${SWIG_VERSION}" VERSION_LESS "4.2.0")
  target_compile_definitions(fastjet_swig PUBLIC -DSWIG)
  target_compile_definitions(fastjet_swig PUBLIC -DSWIG_TYPE_TABLE=fastjet_swig)
endif()

target_include_directories(fastjet_swig 
                           PUBLIC 
                            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                            $<INSTALL_INTERFACE:include>
                           )
add_library(fastjet::fastjet_swig ALIAS fastjet_swig)

# Really should go to ${Python_SITEARCH} or into the wheel dir of scikit-build-core
if (FASTJET_USE_PYTHON_SITEARCH)
  set(FASTJET_PYTHON_INSTALL_DIR "${Python_SITEARCH}")
elseif(NOT "${FASTJET_CUSTOM_PYTHON_INSTALL}" STREQUAL "")
  set(FASTJET_PYTHON_INSTALL_DIR "${FASTJET_CUSTOM_PYTHON_INSTALL}")
else()
  set(FASTJET_PYTHON_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages")
  #set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
  #set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
  #message(STATUS "CMAKE_INSTALL_RPATH: ${CMAKE_INSTALL_RPATH}")
endif()
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/fastjet_swig/__init__.py" DESTINATION "${FASTJET_PYTHON_INSTALL_DIR}/${FASTJET_PYTHON_PACKAGE_NAME}")
install(TARGETS fastjet_swig EXPORT FastjetTargets DESTINATION "${FASTJET_PYTHON_INSTALL_DIR}/${FASTJET_PYTHON_PACKAGE_NAME}")
set(FASTJET_PYTHON_INSTALL_DIR ${FASTJET_PYTHON_INSTALL_DIR} PARENT_SCOPE) 

