# sources
list(APPEND TrackJetPlugin_SOURCES
  TrackJetPlugin.cc
)

# build a local library
add_library(TrackJetPlugin OBJECT ${TrackJetPlugin_SOURCES})
set_property(TARGET TrackJetPlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_include_directories(TrackJetPlugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(TrackJetPlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/TrackJetPlugin.hh DESTINATION include/fastjet)
