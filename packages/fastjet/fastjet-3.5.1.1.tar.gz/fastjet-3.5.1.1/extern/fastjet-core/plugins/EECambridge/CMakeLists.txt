# sources
list(APPEND EECambridgePlugin_SOURCES
  EECambridgePlugin.cc
)

# build a local library
add_library(EECambridgePlugin OBJECT ${EECambridgePlugin_SOURCES})
set_property(TARGET EECambridgePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(EECambridgePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/EECambridgePlugin.hh DESTINATION include/fastjet)
