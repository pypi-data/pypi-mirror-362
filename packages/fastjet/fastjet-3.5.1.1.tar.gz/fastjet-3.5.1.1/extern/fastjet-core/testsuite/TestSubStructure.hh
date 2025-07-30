#ifndef __TESTSUBSTRUCTURE_HH__
#define __TESTSUBSTRUCTURE_HH__

/// \file TestPseudoJet.hh 
/// Provides a series of tests of PseudoJets

#include "TestBase.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/tools/CASubJetTagger.hh"
#include "fastjet/tools/MassDropTagger.hh"

/// class to test some of the basic features of the CASubJetTagger
class TestSubStructure : public TestBase {
  std::string short_name()  const {return "TestSubStructure";}

  bool run_test () {
    run_2body_taggers(CASubJetTagger(CASubJetTagger::jade_distance, 0.10), 
		                                         "CASubJetTagger");
    run_2body_taggers(MassDropTagger(), "MassDropTagger");
    return _pass_test;
  }

  // a test that should work
  void run_2body_taggers (const Transformer & tagger, const string & name) {
    const bool ignore_struct = true;
    JetDefinition jet_def(cambridge_algorithm, 1.0);

    vector<PseudoJet> particles;
    // first jet
    // first try a configuration that should not pass
    particles.push_back(PtYPhiM(100.0, 0.0, 0));
    particles.push_back(PtYPhiM(  5.0, 0.5, 0));
    // second jet
    // then one whose two prongs are immediately there
    particles.push_back(PtYPhiM( 80.0, 0.0, 3.0));
    particles.push_back(PtYPhiM( 20.0, 0.5, 3.0));
    // third jet
    // and then another that is less immediate
    particles.push_back(PtYPhiM( 70.0, 2.0, 3.0));
    particles.push_back(PtYPhiM( 20.0, 2.3, 3.0));
    particles.push_back(PtYPhiM(  9.0, 2.8, 3.0));
    
    ClusterSequence cs(particles, jet_def);
    vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());
    verify_equal(int(jets.size()), 3, name+": correct number of CA jets");

    // the first jet should not be tagged (z too small)
    PseudoJet tagged = tagger(jets[0]);
    verify_null(tagged, name+": jet 0 not tagged (z too small)");

    // the second jet should be tagged and equal to jets[1]
    tagged = tagger(jets[1]);
    verify_equal(tagged, jets[1], name+": jet 1 tagged = jet 1", ignore_struct);

    // the third jet should be tagged on its internal structure, particles
    // 4+5
    tagged = tagger(jets[2]);
    verify_almost_equal(tagged, particles[4]+particles[5], 
		        name+": jet 2 tagged = p[4]+p[5]", 1e-10, ignore_struct);

  }
};


#endif // __TESTSUBSTRUCTURE_HH__
