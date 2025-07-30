# sources
list(APPEND ATLASConePlugin_SOURCES
  Jet.cc
  JetConeFinderTool.cc
  JetSplitMergeTool.cc
  ATLASConePlugin.cc
)

# headers that will eventually have to be installed?
# CommonUtils.hh JetConeFinderTool.hh JetDistances.hh Jet.hh JetSplitMergeTool.hh LorentzVector.hh
# LG - doesn't look like it since they're only needed for defining internal symbols,
#      not an interface.

# build a local library
add_library(ATLASConePlugin OBJECT ${ATLASConePlugin_SOURCES})
set_property(TARGET ATLASConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(ATLASConePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/ATLASConePlugin.hh DESTINATION include/fastjet)

if (MSVC)
  target_compile_definitions(ATLASConePlugin PUBLIC -D_USE_MATH_DEFINES)
endif()
