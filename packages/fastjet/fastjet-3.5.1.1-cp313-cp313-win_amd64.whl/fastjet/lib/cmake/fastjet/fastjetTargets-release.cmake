#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fastjet::fastjet" for configuration "Release"
set_property(TARGET fastjet::fastjet APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjet PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/fastjet.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/fastjet.dll"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjet )
list(APPEND _cmake_import_check_files_for_fastjet::fastjet "${_IMPORT_PREFIX}/lib/fastjet.lib" "${_IMPORT_PREFIX}/bin/fastjet.dll" )

# Import target "fastjet::fastjettools" for configuration "Release"
set_property(TARGET fastjet::fastjettools APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjettools PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/fastjettools.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/fastjettools.dll"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjettools )
list(APPEND _cmake_import_check_files_for_fastjet::fastjettools "${_IMPORT_PREFIX}/lib/fastjettools.lib" "${_IMPORT_PREFIX}/bin/fastjettools.dll" )

# Import target "fastjet::fastjetplugins" for configuration "Release"
set_property(TARGET fastjet::fastjetplugins APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjetplugins PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/fastjetplugins.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/fastjetplugins.dll"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjetplugins )
list(APPEND _cmake_import_check_files_for_fastjet::fastjetplugins "${_IMPORT_PREFIX}/lib/fastjetplugins.lib" "${_IMPORT_PREFIX}/bin/fastjetplugins.dll" )

# Import target "fastjet::fastjet_swig" for configuration "Release"
set_property(TARGET fastjet::fastjet_swig APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::fastjet_swig PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELEASE ""
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/_swig/_fastjet_swig.cp313-win_amd64.pyd"
  )

list(APPEND _cmake_import_check_targets fastjet::fastjet_swig )
list(APPEND _cmake_import_check_files_for_fastjet::fastjet_swig "${_IMPORT_PREFIX}/_swig/_fastjet_swig.cp313-win_amd64.pyd" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
