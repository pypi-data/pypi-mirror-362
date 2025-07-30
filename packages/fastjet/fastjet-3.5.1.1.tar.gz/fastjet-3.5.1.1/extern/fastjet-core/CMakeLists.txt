# List of useful CMake arguments:
#  CMAKE_INSTALL_PREFIX=...     path for the installation
#                               (can be replaced be cmake --install . -- prefix <patth>)
#  FASTJET_ENABLE_DEBUG=ON|OFF  switch debugging info on/off [default:ON]
#  FASTJET_ENABLE_CGAL=ON|OFF   enable CGAL support [default:OFF]
#  FASTJET_ENABLE_PLUGIN_<name>=ON|OFF
#      with <name> in ATLASCONE, CDFCONES, CMSITERATIVECONE, D0RUNICONE, D0RUNIICONE,
#      EECAMBRIDGE, GRIDJET, JADE, NESTEDDEFS, PXCONE, SISCONE, TRACKJET; enable the
#      corresponding FastJet plugin [default:ON except for PxCone]
#
# Note on config file:
#  . include/fastjet/config_auto.h is generated from config-cmake.hh.in
#
# TODO:
# - [ ] incorporate build from cmake-installed version also into CI
# - [ ] have the option of building the testsuite
# - [ ] web page cmake documentation (e.g. quick-start) -> not for 3.5.0, wait until it's been used for a while
# - [x] fastjet-config script
#   - [x] support for --list-plugins
#   - [x] correct list of libraries when --plugins requested
#   - [x] --pythonpath
#   - [x] it is correctly installed
#   - [x] --config option?
# - [x] we are manually setting various compile flags, e.g. -g, -O2, etc.
#       which is not compatible with standard CMake build types
# - [x] checks
#   - [x] that siscone submodule is there 
#   - [x] that siscone/config.h does not exist in the source directory
# - [x] add PxCone support
# - [x] Check the "Release" build
# - [x] add missing examples -> simply moved them into examples/graveyard/
# - [x] make sure all CMakeLists.txt, config-cmake.hh.in, Config.cmake.in files included in tarball
# - [x] add Python support
# - [x] make sure we use shared libs# 
# - [x] specific compilation flags for the D0RunIICone
# - [x] print config summary
# - [x] scripts/set-version.sh should set the version info also in this file
# - [x] ctest to reproduce what make check does
#   - [x] and add it to CI
# - [x] check autotools tarball for cmake in CI
# - [x] CI also for cmake
#   - [x] basic functionality
#   - [x] address comments from M Feickert in !10 on test-all-algs and on python library path
#   - [x] check build from installed system, including fastjet-config and cmake routes
#         (see internal )
# - [x] Add instructions for CMake usage to documentation
#   - [x] for build & installation, and compilation as a text file
#   - [x] similarly in fastjet-doc.tex 
# - [x] make some decisions
#   - [x] what plugins turned on by default -> aim for same list as in autotools + enable-all, enable-allcxx
#   - [x] will we deprecate auto-tools? Schedule for removal when? -> not for 3.5.0
#   - [x] are we happy with Python arrangement (needing swig) -> Yes
# - [x] make sure out-of-source autotools build is (still?) working

cmake_minimum_required(VERSION 3.10.0..4.0.1)
include(CMakePrintHelpers)

# set the project name
project(FastJet VERSION 3.5.1 LANGUAGES CXX)
# set a pre-release version if relevant, e.g. "-beta1"
set(PROJECT_VERSION_PRERELEASE "")
include(GNUInstallDirs)

#----------------------------------------------------------------------
# version information
set(FASTJET_VERSION "${PROJECT_VERSION}${PROJECT_VERSION_PRERELEASE}")

set(FASTJET_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
set(FASTJET_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
set(FASTJET_VERSION_PATCHLEVEL "${PROJECT_VERSION_PATCH}")
set(FASTJET_VERSION_PRERELEASE "${PROJECT_VERSION_PRERELEASE}")
# build a unique version number
if (FASTJET_VERSION_MINOR LESS 10)
  set(FASTJET_VERSION_MINOR_FOR_NUMBER "0${FASTJET_VERSION_MINOR}")
else()
  set(FASTJET_VERSION_MINOR_FOR_NUMBER "${FASTJET_VERSION_MINOR}")
endif()
if (FASTJET_VERSION_PATCHLEVEL LESS 10)
  set(FASTJET_VERSION_PATCHLEVEL_FOR_NUMBER "0${FASTJET_VERSION_PATCHLEVEL}")
else()
  set(FASTJET_VERSION_PATCHLEVEL_FOR_NUMBER "${FASTJET_VERSION_PATCHLEVEL}")
endif()
set(FASTJET_VERSION_NUMBER "${FASTJET_VERSION_MAJOR}${FASTJET_VERSION_MINOR_FOR_NUMBER}${FASTJET_VERSION_PATCHLEVEL_FOR_NUMBER}")

# print out the project name and version
cmake_print_variables(PROJECT_NAME FASTJET_VERSION)

# need this to be able to set the installation prefix in fastjet-config
include(GNUInstallDirs)

#----------------------------------------------------------------------
# basic C++ checks
#----------------------------------------------------------------------

# specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)  # <--- GPS 2025-05-22: disable GNU extensions, which cause problems with CGAL on amd64
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR})
if (MSVC)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
message(STATUS "CMAKE_BUILD_TYPE = ${CMAKE_BUILD_TYPE}")



# Bail out if config_auto.h exists in the source directory
set (AUTOTOOLS_ERROR_MESSAGE "Found ${PROJECT_SOURCE_DIR}/include/fastjet/config_auto.h in source directory. This would typically have been generated by the autotools (non-CMake) build process. Please run cmake from a clean source directory.")
if (EXISTS "${PROJECT_SOURCE_DIR}/include/fastjet/config_auto.h")
  message(FATAL_ERROR "${AUTOTOOLS_ERROR_MESSAGE}")
endif()

#-------------------------------------------------------------------------
# a series of user-defined options
# If you add something here, check if one also needs to add a corresponding 
# entry in config-cmake.hh.in
#
# CGAL support
option(FASTJET_ENABLE_CGAL  
       "Enable compilation with CGAL (header-only) support, required for most of the NlnN strategies"  
       OFF)

# do we build the examples?
option(FASTJET_BUILD_EXAMPLES "Build the executables in the examples directory [default=ON]" ON)

# thread safety
option(FASTJET_HAVE_THREAD_SAFETY         "Turn on thread safety [default=ON]" ON)
option(FASTJET_HAVE_LIMITED_THREAD_SAFETY "Turn on limited thread safety [default=ON]" ON)
if (FASTJET_HAVE_THREAD_SAFETY)
  set(FASTJET_HAVE_LIMITED_THREAD_SAFETY ON)
endif()


# plugins on/off
option(FASTJET_ENABLE_PLUGIN_CDFCONES         "Enable the CDFCones plugin [default=ON]"           ON)
option(FASTJET_ENABLE_PLUGIN_EECAMBRIDGE      "Enable the EECambridge plugin [default=ON]"        ON)
option(FASTJET_ENABLE_PLUGIN_GRIDJET          "Enable the GridJet plugin [default=ON]"            ON)
option(FASTJET_ENABLE_PLUGIN_JADE             "Enable the Jade plugin [default=ON]"               ON)
option(FASTJET_ENABLE_PLUGIN_NESTEDDEFS       "Enable the NestedDefs plugin [default=ON]"         ON)
option(FASTJET_ENABLE_PLUGIN_SISCONE          "Enable the SISCone plugin [default=ON]"            ON)
option(FASTJET_USE_INSTALLED_SISCONE          "Use an existing installed version of siscone"     OFF)
option(FASTJET_ENABLE_PLUGIN_ATLASCONE        "Enable the ATLASCone plugin [default=OFF]"        OFF)
option(FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE "Enable the CMSIterativeCone plugin [default=OFF]" OFF)
option(FASTJET_ENABLE_PLUGIN_D0RUNICONE       "Enable the D0RunICone plugin [default=OFF]"       OFF)
option(FASTJET_ENABLE_PLUGIN_D0RUNIICONE      "Enable the D0RunIICone plugin [default=OFF]"      OFF)
option(FASTJET_ENABLE_PLUGIN_PXCONE           "Enable the PxCone plugin [default=OFF]"           OFF)
option(FASTJET_ENABLE_PLUGIN_TRACKJET         "Enable the TrackJet plugin [default=OFF]"         OFF)

option(FASTJET_ENABLE_ALLCXXPLUGINS           "Enable all the C++ plugins [default=OFF]"       OFF)
option(FASTJET_ENABLE_ALLPLUGINS              "Enable all the plugins [default=OFF]"           OFF)

if (FASTJET_ENABLE_ALLCXXPLUGINS OR FASTJET_ENABLE_ALLPLUGINS)
  set(FASTJET_ENABLE_PLUGIN_ATLASCONE          ON)
  set(FASTJET_ENABLE_PLUGIN_CDFCONES           ON)
  set(FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE   ON)
  set(FASTJET_ENABLE_PLUGIN_D0RUNICONE         ON)
  set(FASTJET_ENABLE_PLUGIN_D0RUNIICONE        ON)
  set(FASTJET_ENABLE_PLUGIN_EECAMBRIDGE        ON)
  set(FASTJET_ENABLE_PLUGIN_GRIDJET            ON)
  set(FASTJET_ENABLE_PLUGIN_JADE               ON)
  set(FASTJET_ENABLE_PLUGIN_NESTEDDEFS         ON)
  set(FASTJET_ENABLE_PLUGIN_SISCONE            ON)
  set(FASTJET_ENABLE_PLUGIN_TRACKJET           ON)
endif()

if (FASTJET_ENABLE_ALLPLUGINS)
  set(FASTJET_ENABLE_PLUGIN_PXCONE             ON)
endif()

# compile-time debugging info
option(FASTJET_ENABLE_DEBUG "Turn on debug compiler information [default=ON]" ON)

# disable auto-ptr by defaukt
option(FASTJET_HAVE_AUTO_PTR_INTERFACE  "Enable the (deprecated) auto_ptr interface [default=OFF]"  OFF)

# extra warnings
option(FASTJET_ENABLE_EXTRA_WARNINGS  "Enable compile=time extra warnings [default=OFF]"  OFF)

# support for "override" comes automatically as part of C++11 (can be manually disabled)
option(FASTJET_HAVE_OVERRIDE   "Compiler supports override"  ON)

# support for "[[deprecated]]" comes automatically as part of C++14 (can be manually disabled)
option(FASTJET_HAVE_CXX14_DEPRECATED   "Compiler supports [[deprecated]] (C++14)"  ON)

# support for "__attribute__(deprecated)" off by default (use [[deprecated instead]])
option(FASTJET_HAVE_GNUCXX_DEPRECATED "Compiler supports __attribute__(deprecated) (use [[deprecated]] instead"  OFF)

# support for "explicit operator" comes automatically as part of C++11 (can be manually disabled)
option(FASTJET_HAVE_EXPLICIT_FOR_OPERATORS  "Compiler supports explicit operator (C++11)"  ON)

# support for swig-based python bindings
option(FASTJET_ENABLE_PYTHON "Enable building of swig-based fastjet python bindings" OFF)
option(FASTJET_PYINTERFACE_ONLY "Only build the pyinterface model, relying on an external install of fastjet" OFF)

#-------------------------------------------------------------------------
# compile-time options
# add modules to help check compiler support
include(CheckCXXCompilerFlag)
include(CheckIncludeFileCXX)

if (MSVC)
  message(WARNING "BUILDING FASTJET ON WINDOWS IS NOT SUPPORTED BY THE FASTJET AUTHORS!!!\nDO NOT EXPECT SUPPORT IF THINGS GO WRONG!!!\nWITHIN SCIKIT-BUILD-CORE, CONTACT SCIKIT DEVELOPERS FOR HELP")
  # This flags has been requested in some MRs. While it is included here
  # it has not been tested by the FastJet authors.
  add_compile_definitions(-D_USE_MATH_DEFINES)
endif()

# for every flag in FLAG_LIST, we will check if the compiler supports it
# and if so, add it to the list of compile options
set (FLAG_LIST "")
if (NOT MSVC)
  list(APPEND FLAG_LIST -Wall -Wshadow)
endif()


if (FASTJET_ENABLE_DEBUG)
  if (MSVC)
    list(APPEND FLAG_LIST /Zi)
  else()
    list(APPEND FLAG_LIST -g)
    list(APPEND FLAG_LIST -Woverloaded-virtual)
  endif()
endif()

if (FASTJET_ENABLE_EXTRA_WARNINGS)
  if (MSVC)
    list(APPEND FLAG_LIST /W4)
  else()
    list(APPEND FLAG_LIST -pedantic -Wextra -Wshadow)
  endif()
endif()

foreach(flag  ${FLAG_LIST})
  check_cxx_compiler_flag(${flag} FLAG_SUPPORTED)
  if (FLAG_SUPPORTED)
    message(STATUS "Checking if the compiler supports ${flag}: supported")
    # add_compile_options(...) would potentially apply to all languages, i.e. maybe 
    # also Fortran (PxCone) even though we have tested flags only for C++
    # so we use CMAKE_CXX_FLAGS here.
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${flag}")
    #add_compile_options(${flag})  
  else()
    message(STATUS "Checking if the compiler supports ${flag}: not supported")
  endif()
endforeach()

check_include_file_cxx(execinfo.h FASTJET_HAVE_EXECINFO_H)

if (FASTJET_HAVE_EXECINFO_H)
  try_compile(CXX_ABI_COMPILE_SUCCEEDED ${CMAKE_BINARY_DIR}/compiler-tests ${CMAKE_CURRENT_SOURCE_DIR}/compiler-tests/cxx_abi.cc)
  if (CXX_ABI_COMPILE_SUCCEEDED)
    message("-- C++ ABI support test passed; enabling demangling")
    option(FASTJET_HAVE_DEMANGLING_SUPPORT "Enabling C++ demangling (requires CXX ABI support)" ON)
  else()
    message("-- C++ ABI support test failed; disabling demangling")
    option(FASTJET_HAVE_DEMANGLING_SUPPORT "Enabling C++ demangling (requires CXX ABI support)" OFF)
  endif()
else()
  set(FASTJET_HAVE_DEMANGLING_SUPPORT  OFF)
endif()

#-------------------------------------------------------------------------
# libm
find_library(LIBM_LIBRARIES m)
            
#-------------------------------------------------------------------------
# CGAL Support (off by default)
#
# See https://doc.cgal.org/latest/Manual/devman_create_and_use_a_cmakelist.html
if (FASTJET_ENABLE_CGAL)
  # Note that CGAL will complain about potential performance issues if
  # the build type is anything other than Release
  find_package(CGAL REQUIRED)
endif()

# try to output the list of compiler options for this build
get_directory_property(EXTRA_OPTIONS COMPILE_OPTIONS)
# use an upper case BUILD_TYPE_UPPER to deduce the build flags for this kind of build
string(TOUPPER "${CMAKE_BUILD_TYPE}" BUILD_TYPE_UPPER)
message(STATUS "FastJet compiler options: ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${BUILD_TYPE_UPPER}} ${EXTRA_OPTIONS} (add -DCMAKE_EXPORT_COMPILE_COMMANDS=ON and see output json file to be sure)")

#-------------------------------------------------------------------------
# python Support (off by default)
#
if (FASTJET_ENABLE_PYTHON)
  find_package(SWIG 3.0 COMPONENTS python REQUIRED)
endif()
set(FASTJET_PYTHON_PACKAGE_NAME "fastjet" CACHE STRING "The name of the installed fastjet python package.")
set(FASTJET_USE_PYTHON_SITEARCH OFF CACHE BOOL "Force the usage of ${Python_SITEARCH} if CMAKE_INSTALL_PREFIX was defined.")
set(FASTJET_CUSTOM_PYTHON_INSTALL "" CACHE STRING "Specify a custom python install path, can be absolute or relative to lib.")


# Decide where we get SISCone from and run a few checks
if (FASTJET_ENABLE_PLUGIN_SISCONE)  
  if (FASTJET_USE_INSTALLED_SISCONE)
    message("-- Looking for pre-existing installed version of siscone!")
    find_package(siscone)
    if (siscone_FOUND)
      message("-- Found Siscone: ${siscone_DIR}")
    else()
      message(FATAL_ERROR "Siscone not found. Please install siscone with CMake, and possibly include its prefix/lib/cmake directory in CMAKE_PREFIX_PATH; or set FASTJET_USE_INSTALLED_SISCONE to OFF.")
    endif()
  else()
    message("-- Using git submodule for SISCone!")
    # check if the submodule is there
    if (NOT EXISTS "${PROJECT_SOURCE_DIR}/plugins/SISCone/siscone/config.h.in")
      message(FATAL_ERROR "Siscone submodule not found. Please run 'git submodule update --init --recursive' to fetch the submodule.")
    endif()
    if (EXISTS "${PROJECT_SOURCE_DIR}/plugins/SISCone/siscone/config.h")
      message(FATAL_ERROR "Siscone has ${PROJECT_SOURCE_DIR}/plugins/SISCone/siscone/config.h: has it been configured with autotools? That is not compatible with a CMake build.")
    endif()
  endif()
endif()

#-------------------------------------------------------------------
# build a string with a description of the configuration

set(thread_safety_string "OFF")
if (FASTJET_HAVE_LIMITED_THREAD_SAFETY)
   set(thread_safety_string "limited")
endif()
if (FASTJET_HAVE_THREAD_SAFETY)
   set(thread_safety_string "ON")
endif()

set(CONFIGURE_INVOCATION "[Unavailable when using CMake]")
set(CONFIG_SUMMARY "FastJet configuration summary:
----------------------
  Installation directory     ${CMAKE_INSTALL_PREFIX}
  Debug flag                 ${FASTJET_ENABLE_DEBUG}
  CGAL support               ${FASTJET_ENABLE_CGAL}
  Thread safety              ${thread_safety_string}
  Plugins: EECambridge       ${FASTJET_ENABLE_PLUGIN_EECAMBRIDGE}
           Jade              ${FASTJET_ENABLE_PLUGIN_JADE}
           NestedDefs        ${FASTJET_ENABLE_PLUGIN_NESTEDDEFS}
           SISCone           ${FASTJET_ENABLE_PLUGIN_SISCONE}
           CDFCones          ${FASTJET_ENABLE_PLUGIN_CDFCONES}
           D0RunICone        ${FASTJET_ENABLE_PLUGIN_D0RUNICONE}
           D0RunIICone       ${FASTJET_ENABLE_PLUGIN_D0RUNIICONE}
           ATLASCone         ${FASTJET_ENABLE_PLUGIN_ATLASCONE}
           CMSIterativeCone  ${FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE}
           PxCone            ${FASTJET_ENABLE_PLUGIN_PXCONE}
           TrackJet          ${FASTJET_ENABLE_PLUGIN_TRACKJET}
           GridJet           ${FASTJET_ENABLE_PLUGIN_GRIDJET}
  Monolithic plugins lib     forced ON
  Python interface (swig)    ${FASTJET_ENABLE_PYTHON}
"
)

#-------------------------------------------------------------------------
# get into directories:
if (NOT FASTJET_PYINTERFACE_ONLY)
  add_subdirectory(include)  # for basic FJ headers
  add_subdirectory(src)      # for the main FJ library
  add_subdirectory(tools)    # fastjet toolkit
  add_subdirectory(plugins)  # fastjet clustering plugins
endif()
message(STATUS "Installation prefix is ${CMAKE_INSTALL_PREFIX}")
if (FASTJET_ENABLE_PYTHON)
  if (FASTJET_PYINTERFACE_ONLY)
    find_package(fastjet REQUIRED)
    if(fastjet_FOUND)
      message(STATUS "Found fastjet for pyinterface-only build: ${fastjet_DIR}")    
    endif()
  endif()
  add_subdirectory(pyinterface) # for python interface
  if (NOT IS_ABSOLUTE "${FASTJET_PYTHON_INSTALL_DIR}")
    set(FASTJET_PYTHON_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/${FASTJET_PYTHON_INSTALL_DIR}")
  endif()
  message(STATUS "Python interface enabled and will be installed to ${FASTJET_PYTHON_INSTALL_DIR}")
endif()
if (NOT FASTJET_PYINTERFACE_ONLY AND FASTJET_BUILD_EXAMPLES)
  add_subdirectory(example)  # for examples (gets built after all the rest)
endif()


# generate the configure file
configure_file(config-cmake.hh.in include/fastjet/config_auto.h)




# set up a range of variables for the fastjet-config script; one question
# is whether, with such generic names, they might conflict with other CMake variables
set(prefix ${CMAKE_INSTALL_PREFIX})
set(libdir "${prefix}/${CMAKE_INSTALL_LIBDIR}")
set(includedir "${prefix}/${CMAKE_INSTALL_INCLUDEDIR}")
set(PACKAGE_VERSION ${FASTJET_VERSION})
if (FASTJET_ENABLE_PYTHON)
  set(pyexecdir "${FASTJET_PYTHON_INSTALL_DIR}")
  set(pythondir "${FASTJET_PYTHON_INSTALL_DIR}")
endif()
set(CONFIG_LIBS_PLUGINS "-lfastjetplugins")
if (FASTJET_ENABLE_PLUGIN_SISCONE) 
  set(CONFIG_LIBS_PLUGINS "${CONFIG_LIBS_PLUGINS} -lsiscone -lsiscone_spherical")
endif()
configure_file(fastjet-config.in fastjet-config)

install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/fastjet-config DESTINATION ${CMAKE_INSTALL_BINDIR})


#--------------------------------------------------------------------------
# enable testing functionality
if(NOT FASTJET_PYINTERFACE_ONLY)
  if (FASTJET_BUILD_EXAMPLES)
    enable_testing()
    if (UNIX OR (WIN32 AND MINGW))
      add_test(
        NAME test_compare
        COMMAND ${PROJECT_SOURCE_DIR}/test-compare.sh
      )
    endif()
  endif()

  #--------------------------------------------------------------------------
  # for accessing fastjet from other CMake projects
  include(CMakePackageConfigHelpers)

  # allow Fastjet to work with find_package
  export(EXPORT FastjetTargets
    NAMESPACE fastjet::
    FILE "${CMAKE_CURRENT_BINARY_DIR}/fastjetTargets.cmake"
  )

  install(EXPORT FastjetTargets
    NAMESPACE fastjet::
    FILE fastjetTargets.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/fastjet
  )

  configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/fastjetConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/fastjet
    NO_SET_AND_CHECK_MACRO
    NO_CHECK_REQUIRED_COMPONENTS_MACRO
  )

  write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/fastjetConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY AnyNewerVersion
  )

  install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/fastjetConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/fastjetConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/fastjet
  )
endif()

message(STATUS "${CONFIG_SUMMARY}")



# # Add a similar check at build time (not working)
# add_custom_target(check_config_auto ALL
#   COMMAND ${CMAKE_COMMAND} -E if 
#       "[ -f \"${PROJECT_SOURCE_DIR}/include/fastjet/config_auto.h\" ]"
#       "${CMAKE_COMMAND}" -E echo 
#       "${AUTOTOOLS_ERROR_MESSAGE}"
#       "&& exit 1"
#   COMMENT "Checking for config_auto.h in source directory")
# 
# # Make all major targets depend on this check
# # (Add this after all other targets are defined)
# add_dependencies(fastjet check_config_auto)


# 
# dnl-------------------------------------------------------------------
# dnl check if the linker supports --enable-new-dtags (rpath-related)
# dnl-------------------------------------------------------------------
# AC_MSG_CHECKING([if $CXX supports -Wl,--enable-new-dtags flag])
# SAVE_CXXFLAGS="$CXXFLAGS"
# CXXFLAGS="-Werror -Wl,--enable-new-dtags"
# AC_LANG_PUSH(C++)
# AC_LINK_IFELSE([AC_LANG_SOURCE([int main(void){ return 0;}])],
#    [ac_enable_new_dtags_ok=yes],[ac_enable_new_dtags_ok=no])
# AC_LANG_POP(C++)
# CXXFLAGS="$SAVE_CXXFLAGS"
# AC_MSG_RESULT([$ac_enable_new_dtags_ok])
# HAS_RUNPATH_SUPPORT="no"
# CONFIG_RUNPATH_FLAGS=""
# dnl if test x"$ac_enable_new_dtags_ok" = x"yes"; then
# if test "x${ac_enable_new_dtags_ok}" = "xyes" ; then
#    HAS_RUNPATH_SUPPORT="yes"
#    CONFIG_RUNPATH_FLAGS="-Wl,--enable-new-dtags"
# fi
# AC_SUBST(HAS_RUNPATH_SUPPORT)
# AC_SUBST(CONFIG_RUNPATH_FLAGS)
# 
