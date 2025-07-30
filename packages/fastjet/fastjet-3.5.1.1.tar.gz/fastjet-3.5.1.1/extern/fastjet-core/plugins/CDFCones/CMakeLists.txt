# sources
list(APPEND CDFConesPlugin_SOURCES
  CDFcode/CalTower.cc
  CDFcode/Centroid.cc
  CDFcode/Cluster.cc
  CDFcode/ClusterComparisons.cc
  CDFcode/JetCluAlgorithm.cc
  CDFcode/LorentzVector.cc
  CDFcode/MidPointAlgorithm.cc
  CDFcode/PhysicsTower.cc
  CDFJetCluPlugin.cc
  CDFMidPointPlugin.cc
)

# build a local library
add_library(CDFConesPlugin OBJECT ${CDFConesPlugin_SOURCES})
set_property(TARGET CDFConesPlugin PROPERTY POSITION_INDEPENDENT_CODE ON)

target_include_directories(CDFConesPlugin PUBLIC CDFcode)
target_link_libraries(CDFConesPlugin PUBLIC fastjet)

# directly install the header from here
install(FILES fastjet/CDFJetCluPlugin.hh fastjet/CDFMidPointPlugin.hh DESTINATION include/fastjet)
