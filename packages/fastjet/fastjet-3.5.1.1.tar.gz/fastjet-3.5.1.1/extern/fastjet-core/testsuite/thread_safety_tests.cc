/// 
/// Thread safety tests, based on example program provided by 
/// ATLAS via Chris Delitzsch. Requires C++14.
/// 
#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <memory>
#include <iomanip>
#include <thread>
#include "fastjet/ClusterSequence.hh"
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/Pruner.hh"
#include "TestThreadsBase.hh"
#include "CmdLine.hh"

using namespace fastjet;
using namespace std;

void groomJets(const Transformer* f, const vector<fastjet::PseudoJet>& ungroomed_jets, unsigned int ig) {
  unsigned int ij=0;
  // loop on jet candidates
  for (const PseudoJet & u : ungroomed_jets){
    // apply groomer f to jet u
    PseudoJet j = (*f)(u);
    cout << "Groomer " << ig << " jet " << ij << " pt: " << setprecision(4) << j.perp() << endl;
    ++ij;
  }
}

int main(int argc, char ** argv) {

  CmdLine cmdline(argc,argv);
  unsigned int nrepeat = cmdline.value("-n",1);

// #ifndef FASTJET_HAVE_THREAD_SAFETY
//   cout << argv[0] << ": FastJet not configured with thread safety, bailing out gracefully" << endl;
//   return 0;
// #endif


  // Declare the set of tests
  vector<unique_ptr<TestBase> > tests;
  tests.emplace_back(make_unique<TestThread<ThreadedBanner>>());
  tests.emplace_back(make_unique<TestThread<ThreadedWarning>>());
  tests.emplace_back(make_unique<TestThread<ThreadedError>>());
  tests.emplace_back(make_unique<TestThread<ThreadedTestPhiRap>>());
  tests.emplace_back(make_unique<TestThread<ThreadedTestRapPhi>>());
  tests.emplace_back(make_unique<TestThread<ThreadedPseudoJetResetMomB>>());
  tests.emplace_back(make_unique<TestThread<ThreadedPseudoJetAssignment>>());


  tests.emplace_back(make_unique<TestThread<ThreadedClustering1EvManyR>>());
  tests.emplace_back(make_unique<TestThread<ThreadedClustering1EvCommonCS>>());
  tests.emplace_back(make_unique<TestThread<ThreadedClustering10Ev>>());
  tests.emplace_back(make_unique<TestThread<ThreadedClustering10EvAreas>>(AreaDefinition(active_area_explicit_ghosts)));
  tests.emplace_back(make_unique<TestThread<ThreadedClustering10EvAreas>>(AreaDefinition(voronoi_area, VoronoiAreaSpec())));
  tests.emplace_back(make_unique<TestThread<ThreadedClustering10EvAreasGlobalRand>>(AreaDefinition(active_area_explicit_ghosts)));
  tests.emplace_back(make_unique<TestThread<ThreadedClusteringPrllGroomers>>());
  tests.emplace_back(make_unique<TestThread<ThreadedGMBGE>>());
  tests.emplace_back(make_unique<TestThread<ThreadedJMBGE>>());
  tests.emplace_back(make_unique<TestThread<ThreadedBGEBase>>(
      new JetMedianBackgroundEstimator(SelectorStrip(1.5), 
      JetDefinition(kt_algorithm, 0.5), 
      AreaDefinition(active_area_explicit_ghosts))));
  tests.emplace_back(make_unique<TestThread<ThreadedBGEBase>>(new GridMedianBackgroundEstimator(2.5, 0.6))); 
  tests.emplace_back(make_unique<TestThread<ThreadedJMBGECommonEvent>>());

  // run over them
  bool overall_outcome = true;
  for (auto & test: tests) {
    cout << "Testing ... " << test->short_name() << flush;
    bool outcome = test->run_test(nrepeat);
    overall_outcome &= outcome;
    if (!outcome) {
      cout << "\rFailure for " << test->short_name() << endl;
      test->print_failures();
    }
    else {
      cout << "\rSuccess for " << test->short_name() << endl;
    } 
  }
  if (overall_outcome) return 0;
  else                 return -1;

}
