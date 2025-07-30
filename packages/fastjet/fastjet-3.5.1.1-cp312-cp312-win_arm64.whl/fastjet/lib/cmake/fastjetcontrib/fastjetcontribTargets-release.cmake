#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fastjet::contrib::fastjetcontribfragile" for configuration "Release"
set_property(TARGET fastjet::contrib::fastjetcontribfragile APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastjet::contrib::fastjetcontribfragile PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/fastjetcontribfragile.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/fastjetcontribfragile.dll"
  )

list(APPEND _cmake_import_check_targets fastjet::contrib::fastjetcontribfragile )
list(APPEND _cmake_import_check_files_for_fastjet::contrib::fastjetcontribfragile "${_IMPORT_PREFIX}/lib/fastjetcontribfragile.lib" "${_IMPORT_PREFIX}/bin/fastjetcontribfragile.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
