# sources
list(APPEND D0RunIConePlugin_SOURCES
  D0RunIBaseConePlugin.cc
)

# build a local library
add_library(D0RunIConePlugin OBJECT ${D0RunIConePlugin_SOURCES})
set_property(TARGET D0RunIConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_definitions(D0RunIConePlugin PRIVATE -Dfastjetplugins_EXPORTS)

target_include_directories(D0RunIConePlugin
                           PUBLIC
                            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                            $<INSTALL_INTERFACE:include>
                           )
target_link_libraries(D0RunIConePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/D0RunIConePlugin.hh DESTINATION include/fastjet)
install(FILES fastjet/D0RunIpre96ConePlugin.hh DESTINATION include/fastjet)
install(FILES fastjet/D0RunIBaseConePlugin.hh DESTINATION include/fastjet)