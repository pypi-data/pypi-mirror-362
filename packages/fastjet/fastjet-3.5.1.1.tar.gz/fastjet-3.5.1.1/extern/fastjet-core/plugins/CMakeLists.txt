
# Beware: LIST_ALL_PLUGINS variable name is used also in fastjet-config
# and autotools, so changing it will cause trouble elsewhere

set(combined_objects)
if (FASTJET_ENABLE_PLUGIN_ATLASCONE)
   add_subdirectory(ATLASCone)
   list(APPEND combined_objects $<TARGET_OBJECTS:ATLASConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "ATLASCone")
endif()
if (FASTJET_ENABLE_PLUGIN_CDFCONES)
   add_subdirectory(CDFCones)
   list(APPEND combined_objects $<TARGET_OBJECTS:CDFConesPlugin>)
   list(APPEND LIST_ALL_PLUGINS "CDFCones")
endif()
if (FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE)
   add_subdirectory(CMSIterativeCone)
   list(APPEND combined_objects $<TARGET_OBJECTS:CMSIterativeConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "CMSIterativeCone")
endif()
if (FASTJET_ENABLE_PLUGIN_D0RUNICONE)
   add_subdirectory(D0RunICone)
   list(APPEND combined_objects $<TARGET_OBJECTS:D0RunIConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "D0RunICone")
endif()
if (FASTJET_ENABLE_PLUGIN_D0RUNIICONE)
   add_subdirectory(D0RunIICone)
   list(APPEND combined_objects $<TARGET_OBJECTS:D0RunIIConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "D0RunIICone")
endif()
if (FASTJET_ENABLE_PLUGIN_EECAMBRIDGE)
   add_subdirectory(EECambridge)
   list(APPEND combined_objects $<TARGET_OBJECTS:EECambridgePlugin>)
   list(APPEND LIST_ALL_PLUGINS "EECambridge")
endif()
if (FASTJET_ENABLE_PLUGIN_GRIDJET)
   add_subdirectory(GridJet)
   list(APPEND combined_objects $<TARGET_OBJECTS:GridJetPlugin>)
   list(APPEND LIST_ALL_PLUGINS "GridJet")
endif()
if (FASTJET_ENABLE_PLUGIN_JADE)
   add_subdirectory(Jade)
   list(APPEND combined_objects $<TARGET_OBJECTS:JadePlugin>)
   list(APPEND LIST_ALL_PLUGINS "Jade")
endif()
if (FASTJET_ENABLE_PLUGIN_NESTEDDEFS)
   add_subdirectory(NestedDefs)
   list(APPEND combined_objects $<TARGET_OBJECTS:NestedDefsPlugin>)
   list(APPEND LIST_ALL_PLUGINS "NestedDefs")
endif()
if (FASTJET_ENABLE_PLUGIN_PXCONE)
   include(CheckLanguage)
   check_language(Fortran)
   enable_language(Fortran)
   add_compile_options($<$<COMPILE_LANGUAGE:Fortran>:-O3>)
   add_subdirectory(PxCone)
   list(APPEND combined_objects $<TARGET_OBJECTS:PxConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "PxCone")
endif()
if (FASTJET_ENABLE_PLUGIN_SISCONE)
   add_subdirectory(SISCone)
   list(APPEND combined_objects $<TARGET_OBJECTS:SISConePlugin>)
   list(APPEND LIST_ALL_PLUGINS "SISCone")
endif()
if (FASTJET_ENABLE_PLUGIN_TRACKJET)
   add_subdirectory(TrackJet)
   list(APPEND combined_objects $<TARGET_OBJECTS:TrackJetPlugin>)
   list(APPEND LIST_ALL_PLUGINS "TrackJet")
endif()

# make sure the parent gets access to the list of plugins
set(LIST_ALL_PLUGINS "${LIST_ALL_PLUGINS}" PARENT_SCOPE)

# build a local library
add_library(fastjetplugins SHARED ${combined_objects})
target_link_libraries(fastjetplugins PUBLIC fastjet)

target_include_directories(fastjetplugins PUBLIC 
                             $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/Jade>
                             $<INSTALL_INTERFACE:include>
                           )

add_library(fastjet::fastjetplugins ALIAS fastjetplugins)

# NB this is specifically for building scikit-hep/fastjet wheels
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  set_target_properties(fastjetplugins PROPERTIES INSTALL_RPATH "@loader_path")
else()
  set_target_properties(fastjetplugins PROPERTIES INSTALL_RPATH "$ORIGIN")
endif()

# make sure the SISCone libraries are included if necessary
if (FASTJET_ENABLE_PLUGIN_SISCONE)
   target_link_libraries(fastjetplugins PUBLIC siscone::siscone siscone::siscone_spherical)
endif()

# here we specify that runtime library components (e.g. .dlls, but not .so or .dylib)
# go into the binary directory (e.g. /bin, rather than the library directory e.g /lib)
# this is typical organization on windows installs
install(TARGETS
          fastjetplugins
        EXPORT
          FastjetTargets
        RUNTIME
          COMPONENT Runtime
          DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY
          COMPONENT Runtime
          DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE
          COMPONENT Development
          DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
