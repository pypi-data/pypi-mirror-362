#------------------------------------------------------------------------
# illustrative examples
#------------------------------------------------------------------------

# example 01-basic
add_executable(01-basic 01-basic.cc)
target_link_libraries(01-basic fastjet)

# example 02-jetdef
add_executable(02-jetdef 02-jetdef.cc)
target_link_libraries(02-jetdef fastjet)

# example 03-plugin
add_executable(03-plugin 03-plugin.cc)
target_link_libraries(03-plugin fastjet)
if (FASTJET_ENABLE_PLUGIN_SISCONE)
  target_include_directories(03-plugin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../plugins/SISCone)
  target_link_libraries(03-plugin fastjetplugins siscone::siscone siscone::siscone_spherical)
endif()

# example 04-constituents
add_executable(04-constituents 04-constituents.cc)
target_link_libraries(04-constituents fastjet)

# example 05-eplus_eminus
add_executable(05-eplus_eminus 05-eplus_eminus.cc)
target_link_libraries(05-eplus_eminus fastjet)

# example 06-area
add_executable(06-area 06-area.cc)
target_link_libraries(06-area fastjet)

# example 07-subtraction
add_executable(07-subtraction 07-subtraction.cc)
target_link_libraries(07-subtraction fastjettools)

# example 08-selector
add_executable(08-selector 08-selector.cc)
target_link_libraries(08-selector fastjet)

# example 09-user_info
add_executable(09-user_info 09-user_info.cc)
target_link_libraries(09-user_info fastjet)

# example 10-subjets
add_executable(10-subjets 10-subjets.cc)
target_link_libraries(10-subjets fastjet)

# example 11-filter
add_executable(11-filter 11-filter.cc)
target_link_libraries(11-filter fastjettools)

# example 12-boosted_higgs
add_executable(12-boosted_higgs 12-boosted_higgs.cc)
target_link_libraries(12-boosted_higgs fastjettools)

# example 13-boosted_top
add_executable(13-boosted_top 13-boosted_top.cc)
target_link_libraries(13-boosted_top fastjettools)

# example 14-groomers
add_executable(14-groomers 14-groomers.cc)
target_link_libraries(14-groomers fastjettools)


#------------------------------------------------------------------------
# historic examples
#------------------------------------------------------------------------
add_executable(fastjet_example fastjet_example.cc)
target_link_libraries(fastjet_example fastjet)

add_executable(fastjet_areas fastjet_areas.cc)
target_link_libraries(fastjet_areas fastjet)
if (FASTJET_ENABLE_PLUGIN_SISCONE)
  target_link_libraries(fastjet_areas fastjetplugins siscone::siscone siscone::siscone_spherical)
endif()

# fastjet_timing_plugins
add_executable(fastjet_timing_plugins fastjet_timing_plugins.cc CmdLine.cc)
target_link_libraries(fastjet_timing_plugins PUBLIC fastjetplugins fastjettools)
if (FASTJET_ENABLE_PLUGIN_SISCONE)
  target_link_libraries(fastjet_timing_plugins PUBLIC siscone::siscone siscone::siscone_spherical)
endif()
# loop over all LIST_ALL_PLUGINS and make sure that the corresponding
# directories are added to the include list for fastjet_timing_plugins
foreach(plugin ${LIST_ALL_PLUGINS})
  target_include_directories(fastjet_timing_plugins PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../plugins/${plugin})
endforeach()

