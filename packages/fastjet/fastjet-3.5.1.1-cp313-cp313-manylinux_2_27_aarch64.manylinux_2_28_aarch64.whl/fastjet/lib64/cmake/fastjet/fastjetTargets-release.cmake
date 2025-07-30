#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fastjet::fastjet" for configuration "Release"
set_property(TARGET fastjet::fastjet APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjet PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libfastjet.so"
  IMPORTED_SONAME_RELEASE "libfastjet.so"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjet )
list(APPEND _cmake_import_check_files_for_fastjet::fastjet "${_IMPORT_PREFIX}/lib64/libfastjet.so" )

# Import target "fastjet::fastjettools" for configuration "Release"
set_property(TARGET fastjet::fastjettools APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjettools PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libfastjettools.so"
  IMPORTED_SONAME_RELEASE "libfastjettools.so"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjettools )
list(APPEND _cmake_import_check_files_for_fastjet::fastjettools "${_IMPORT_PREFIX}/lib64/libfastjettools.so" )

# Import target "fastjet::fastjetplugins" for configuration "Release"
set_property(TARGET fastjet::fastjetplugins APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjetplugins PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libfastjetplugins.so"
  IMPORTED_SONAME_RELEASE "libfastjetplugins.so"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjetplugins )
list(APPEND _cmake_import_check_files_for_fastjet::fastjetplugins "${_IMPORT_PREFIX}/lib64/libfastjetplugins.so" )

# Import target "fastjet::fastjet_swig" for configuration "Release"
set_property(TARGET fastjet::fastjet_swig APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjet_swig PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELEASE ""
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/_swig/_fastjet_swig.cpython-313-aarch64-linux-gnu.so"
  IMPORTED_NO_SONAME_RELEASE "TRUE"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjet_swig )
list(APPEND _cmake_import_check_files_for_fastjet::fastjet_swig "${_IMPORT_PREFIX}/_swig/_fastjet_swig.cpython-313-aarch64-linux-gnu.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
