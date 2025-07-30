# just a bunch of headers to install
install(FILES 
  BackgroundEstimatorBase.hh
  GridMedianBackgroundEstimator.hh
  JetMedianBackgroundEstimator.hh
  Subtractor.hh
  Boost.hh
  Transformer.hh
  Recluster.hh
  Filter.hh
  Pruner.hh
  MassDropTagger.hh
  CASubJetTagger.hh
  TopTaggerBase.hh
  JHTopTagger.hh
  RestFrameNSubjettinessTagger.hh
  DESTINATION include/fastjet/tools)
