# List of useful CMake arguments:
#  CMAKE_INSTALL_PREFIX=...     path for the installation
#                               (can be replaced be cmake --install . -- prefix <patth>)

cmake_minimum_required(VERSION 3.10.0...4.0.1)
include(CMakePrintHelpers)

# set the project name
project(SISCone VERSION 3.1.2 LANGUAGES CXX)
# set a pre-release version if relevant, e.g. "-beta1"
set(PROJECT_VERSION_PRERELEASE "")
include(GNUInstallDirs)

#----------------------------------------------------------------------
# version information
set(SISCONE_VERSION "${PROJECT_VERSION}${PROJECT_VERSION_PRERELEASE}")

# print out the project name and version
cmake_print_variables(PROJECT_NAME SISCONE_VERSION)

# warn in windows if we are building outside of scikit-build-core
if (MSVC)
  if (NOT DEFINED SKBUILD_STATE)
    message(WARNING "BUILDING SISCONE ON WINDOWS IS NOT SUPPORTED BY THE SISCONE AUTHORS!!!\nDO NOT EXPECT SUPPORT IF THINGS GO WRONG!!!\nWITHIN SCIKIT-BUILD-CORE, CONTACT SCIKIT DEVELOPERS FOR HELP")
  endif()
endif()

#----------------------------------------------------------------------
# default build type
#----------------------------------------------------------------------
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
message(STATUS "CMAKE_BUILD_TYPE = ${CMAKE_BUILD_TYPE}")
if (MSVC)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

#----------------------------------------------------------------------
# basic C++ checks
#----------------------------------------------------------------------

# specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR})

# There are many sets of compiler flags in CMake:
#
# 1. CMAKE_CXX_FLAGS
# 2. CMAKE_CXX_FLAGS_<BUILD_TYPE>
# 3. COMPILE_OPTIONS (target / directory specific)
# 
# All three get used together. So below we modify flags specific
# to certain build types and then add some common flags to all builds.
# In practite, we add to CMAKE_CXX_FLAGS.
#
# By default, we start from the set of compiler arguments provided by
# CMake, with extra warnings. Windows has been left as is from Lindsey Gray.
if (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zc:__cplusplus /utf-8 /W4 /Ox")
else()
  # for all builds, we want to add flags that 
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wshadow")
endif()

#-------------------------------------------------------------------------
# a series of user-defined options
# If you add something here, remember to add a corresponding 
# entry in config.h.cmake.in
#
option(SISCONE_ENABLE_DEBUG "Turn on debug compiler information [default=ON]" ON)
if (SISCONE_ENABLE_DEBUG)
  if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zi")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
  endif()
endif()

option(SISCONE_BUILD_EXAMPLES "Build the executables in the examples directory [default=ON]" ON)

# try to output the list of compiler options for this build
get_directory_property(EXTRA_OPTIONS COMPILE_OPTIONS)
# use an upper case BUILD_TYPE_UPPER to deduce the build flags for this kind of build
string(TOUPPER "${CMAKE_BUILD_TYPE}" BUILD_TYPE_UPPER)
message(STATUS "SISCone compiler options: ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${BUILD_TYPE_UPPER}} ${EXTRA_OPTIONS} (add -DCMAKE_EXPORT_COMPILE_COMMANDS=ON and see output json file to be sure)")

#-------------------------------------------------------------------------
# check compiler supports

#-------------------------------------------------------------------------
# libm
if (NOT MSVC)
  find_library(LIBM_LIBRARIES m)
endif()

#-------------------------------------------------------------------------
# generate the configure file
configure_file(config.h.cmake.in siscone/config.h)

#-------------------------------------------------------------------------
# get into directories:
add_subdirectory(siscone)  # for the SISCone library
if (SISCONE_BUILD_EXAMPLES)
  add_subdirectory(examples) # for examples (gets built after all the rest)
endif()

# allow Siscone to work with find_package
export(EXPORT SisconeTargets
  NAMESPACE siscone::
  FILE "${CMAKE_CURRENT_BINARY_DIR}/sisconeTargets.cmake"
)

install(EXPORT SisconeTargets
  NAMESPACE siscone::
  FILE sisconeTargets.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/siscone
)

include(CMakePackageConfigHelpers)

configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/sisconeConfig.cmake"
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/siscone
  NO_SET_AND_CHECK_MACRO
  NO_CHECK_REQUIRED_COMPONENTS_MACRO
  )

write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/sisconeConfigVersion.cmake"
  VERSION "${PROJECT_VERSION}"
  COMPATIBILITY AnyNewerVersion
  )

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/sisconeConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/sisconeConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/siscone
  )

