# sources
list(APPEND PxConePlugin_SOURCES
  pxcone.f
  PxConePlugin.cc
)

# build a local library
add_library(PxConePlugin OBJECT ${PxConePlugin_SOURCES})
set_property(TARGET PxConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(PxConePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/PxConePlugin.hh DESTINATION include/fastjet)
