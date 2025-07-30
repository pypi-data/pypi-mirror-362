#include "fastjet/tools/Subtractor.hh"
#include <iostream>
#include "fastjet/ClusterSequenceArea.hh"
using namespace fastjet;
using namespace std;

extern "C" {
void fctestc_() {
  // a subtractor with rho=1 (or not)
  Subtractor subtractor(1.0);
  vector<PseudoJet> particles;
  particles.push_back( PtYPhiM(100.0, 0,0,0));
  
  ClusterSequenceArea cs(particles, JetDefinition(antikt_algorithm, 0.5), AreaDefinition());
  PseudoJet jet = cs.inclusive_jets()[0];
  cout << jet.perp() << endl;
  PseudoJet subjet = subtractor(jet);
  cout << subjet.perp() << endl;
}
}
