# sources
list(APPEND CMSIterativeConePlugin_SOURCES
  CMSIterativeConePlugin.cc
)


# build a local library
add_library(CMSIterativeConePlugin OBJECT ${CMSIterativeConePlugin_SOURCES})
set_property(TARGET CMSIterativeConePlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(CMSIterativeConePlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/CMSIterativeConePlugin.hh DESTINATION include/fastjet)

if (MSVC)
  target_compile_definitions(CMSIterativeConePlugin PUBLIC -D_USE_MATH_DEFINES)
endif()
