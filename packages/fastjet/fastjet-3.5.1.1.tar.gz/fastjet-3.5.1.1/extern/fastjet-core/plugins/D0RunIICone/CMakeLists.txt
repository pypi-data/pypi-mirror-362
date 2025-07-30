# sources
list(APPEND D0RunIIConePlugin_SOURCES
  D0RunIIConePlugin.cc
)

# build a local library
add_library(D0RunIIConePlugin OBJECT ${D0RunIIConePlugin_SOURCES})
set_property(TARGET D0RunIIConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_definitions(D0RunIIConePlugin PRIVATE -Dfastjetplugins_EXPORTS)

if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  target_compile_options(D0RunIIConePlugin PUBLIC /Ob0)
else()
  check_cxx_compiler_flag(-fno-inline D0_CHECK_NO_INLINE)
  if (D0_CHECK_NO_INLINE)
    target_compile_options(D0RunIIConePlugin PUBLIC -fno-inline)
  else()
    check_cxx_compiler_flag(-O0 D0_CHECK_O0)
    if (D0_CHECK_O0)
      target_compile_options(D0RunIIConePlugin PUBLIC -O0)
    endif() 
  endif()
endif()

target_link_libraries(D0RunIIConePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/D0RunIIConePlugin.hh DESTINATION include/fastjet)
