#ifndef __TESTSPECIALEVENTS_HH__
#define __TESTSPECIALEVENTS_HH__

#include "TestBase.hh"
#include "fastjet/tools/GridMedianBackgroundEstimator.hh"
#include "fastjet/GridJetPlugin.hh"


/// class to test some special events that have been reported
/// and that caused issues in older FJ versions
class TestSpecialEvents : public TestBase {
  std::string short_name()  const {return "TestSpecialEvents";}

  virtual bool run_test () {


    vector<PseudoJet> event;
    JetDefinition jd;

    string dir = "special-events/";
    string filename;
    
    //----------------------------------------------------------------------
    // tests related to 2015-02-infinite-loop issue
    //
    // (despite name, infinite loop should no longer occur; wrong
    // reclustering of already-clustered particle should instead be
    // caught & throws InternalError)
    filename = "2015-02-infinite-loop-simplified.txt";
    event = get_event(dir+filename);

    RecombinationScheme rec_scheme = E_scheme;
    
    jd = JetDefinition(fastjet::cambridge_algorithm, 0.8, rec_scheme, N2MHTLazy25);
    VERIFY_RUNS(ClusterSequence cs(event,jd), "special event: "+filename+" with CA08 Lazy25");
    jd = JetDefinition(fastjet::cambridge_algorithm, 0.4, rec_scheme, N2MHTLazy9);
    VERIFY_RUNS(ClusterSequence cs(event,jd), "special event: "+filename+" with CA04 Lazy9");
    jd = JetDefinition(fastjet::cambridge_algorithm, 0.4, rec_scheme, N2MHTLazy9Alt);
    VERIFY_RUNS(ClusterSequence cs(event,jd), "special event: "+filename+" with CA04 Lazy9Alt");
    jd = JetDefinition(fastjet::cambridge_algorithm, 0.4, rec_scheme, N2MHTLazy9AntiKtSeparateGhosts);
    VERIFY_RUNS(ClusterSequence cs(event,jd), "special event: "+filename+" with CA04 Lazy9SeparateGhosts");

    //----------------------------------------------------------------------
    // tests related to 2015-02-out-of-bounds issue
    filename = "2015-02-out-of-bounds-reduced.txt";
    event = get_event(dir+filename);
    jd = JetDefinition(fastjet::antikt_algorithm, 0.4, rec_scheme, N2MHTLazy9);
    VERIFY_RUNS(ClusterSequence cs(event,jd), "special event: "+filename+" with AK04 Lazy9");


    
    return _pass_test;
  }
};
#endif // __TESTSPECIALEVENTS_HH__
