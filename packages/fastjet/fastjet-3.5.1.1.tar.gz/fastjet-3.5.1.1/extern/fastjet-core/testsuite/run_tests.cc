//----------------------------------------------------------------------
/// \file run_tests.cc
///
/// Usage:
///   ./run-tests [-verbose] 
#include "TestBase.hh"
#include "TestPseudoJet.hh"
#include "TestSubStructure.hh"
#include "TestGroomerAreas.hh"
#include "TestRecombiners.hh"
#include "TestGrids.hh"
#include "TestSpecialEvents.hh"
#include "TestEEDotCross.hh"
#include <iomanip>
#include "CmdLine.hh"

int main(int argc, char** argv) {
  CmdLine cmdline(argc,argv);

  bool verbose = cmdline.present("-verbose");
  string only = cmdline.value<string>("-only", "");
  assert(cmdline.all_options_used());
  
  // simply force the banner to appear at the beginning
  vector<PseudoJet> event;
  event.push_back(PtYPhiM(1.0,0.0,0.0));
  JetDefinition jet_def(antikt_algorithm, 0.5);
  ClusterSequence * cs = new ClusterSequence(event, jet_def);
  delete cs;

  // the list of tests we will perform
  vector<TestBase *> tests;
  tests.push_back(new TestPtYPhiM());
  tests.push_back(new TestPJAssignment());
  tests.push_back(new TestPJOperations());
  tests.push_back(new TestPJCSaccess());
  tests.push_back(new TestSubStructure());
  tests.push_back(new TestGroomerAreas());
  tests.push_back(new TestRecombiners());
  tests.push_back(new TestGrids());
  tests.push_back(new TestSpecialEvents());
  tests.push_back(new TestEEDotCross());
  //tests.push_back(new TestGroomerRecombiners()); not for now -- it's empty

  bool all_pass = true;

  // loop over the tests
  for (unsigned i = 0; i < tests.size(); i++) {
    // allow the user to concentrate on one test series
    if (only.size() != 0 && (only != tests[i]->short_name() &&
			     "Test"+only != tests[i]->short_name())) continue;

    bool pass = tests[i]->run_test();

    if (pass) {
      cout << setw(4) << i << "  PASS: " << tests[i]->short_name() <<endl;
      if (verbose) tests[i]->print_OK(cout, 15);
    } else {
      cout << setw(4) << i << "  FAIL: " << tests[i]->short_name() <<endl;
      cout << "      (" << tests[i]->description() << ")" << endl;
      tests[i]->print_failures();
      all_pass = false;
    }
    // clean up after the test....
    delete tests[i];
  }
  
  assert(all_pass);
}
