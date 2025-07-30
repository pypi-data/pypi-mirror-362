# sources
list(APPEND NestedDefsPlugin_SOURCES
  NestedDefsPlugin.cc
)

# build a local library
add_library(NestedDefsPlugin OBJECT ${NestedDefsPlugin_SOURCES})
set_property(TARGET NestedDefsPlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_include_directories(NestedDefsPlugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(NestedDefsPlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/NestedDefsPlugin.hh DESTINATION include/fastjet)
