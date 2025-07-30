# sources
list(APPEND JadePlugin_SOURCES
  JadePlugin.cc
)

# build a local library
add_library(JadePlugin OBJECT ${JadePlugin_SOURCES})
set_property(TARGET JadePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_include_directories(JadePlugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(JadePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/JadePlugin.hh DESTINATION include/fastjet)
