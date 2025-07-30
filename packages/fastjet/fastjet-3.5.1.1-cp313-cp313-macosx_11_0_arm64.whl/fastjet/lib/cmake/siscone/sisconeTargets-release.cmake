#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "siscone::siscone" for configuration "Release"
set_property(TARGET siscone::siscone APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(siscone::siscone PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsiscone.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libsiscone.dylib"
  )

list(APPEND _cmake_import_check_targets siscone::siscone )
list(APPEND _cmake_import_check_files_for_siscone::siscone "${_IMPORT_PREFIX}/lib/libsiscone.dylib" )

# Import target "siscone::siscone_spherical" for configuration "Release"
set_property(TARGET siscone::siscone_spherical APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(siscone::siscone_spherical PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsiscone_spherical.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libsiscone_spherical.dylib"
  )

list(APPEND _cmake_import_check_targets siscone::siscone_spherical )
list(APPEND _cmake_import_check_files_for_siscone::siscone_spherical "${_IMPORT_PREFIX}/lib/libsiscone_spherical.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
