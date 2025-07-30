# if siscone cannot be found recurse into the external code
if (NOT siscone_FOUND)
  add_subdirectory(siscone)
endif()

# sources within FastJet
list(APPEND SISConePlugin_SOURCES
  SISConeBasePlugin.cc
  SISConePlugin.cc
  SISConeSphericalPlugin.cc
)

# build a local library
add_library(SISConePlugin OBJECT ${SISConePlugin_SOURCES})
set_property(TARGET SISConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

if(NOT siscone_FOUND)
  target_include_directories(SISConePlugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
  target_include_directories(SISConePlugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/siscone)

  # print out the current build directory
  get_property(CMAKE_CURRENT_BUILD_DIR GLOBAL PROPERTY CMAKE_CURRENT_BINARY_DIR)
  target_include_directories(SISConePlugin PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/siscone)
endif()

target_link_libraries(SISConePlugin PUBLIC fastjet siscone::siscone siscone::siscone_spherical)

# directly install the header from here
install(FILES fastjet/SISConeBasePlugin.hh fastjet/SISConePlugin.hh fastjet/SISConeSphericalPlugin.hh DESTINATION include/fastjet)

