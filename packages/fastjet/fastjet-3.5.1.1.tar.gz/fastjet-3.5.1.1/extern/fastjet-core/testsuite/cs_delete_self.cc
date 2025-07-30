#include <fastjet/ClusterSequence.hh>
#include <fastjet/ClusterSequenceArea.hh>
#include <iostream> // needed for io
#include <cstdio>   // needed for io

using namespace std;
using namespace fastjet;

const JetDefinition jet_def(antikt_algorithm, 1.0);
const AreaDefinition area_def(active_area, GhostedAreaSpec(5.0, 1, 0.02));

/// do the clustering and retrieve the hardest of the jets
PseudoJet hardest_jet(const ClusterSequence & cs){
  return sorted_by_pt(cs.inclusive_jets())[0];
}

/// do the clustering and retrieve the hardest of the jets
PseudoJet hardest_jet(const vector<PseudoJet> & particles){
  //ClusterSequence * cs = new ClusterSequence(particles, jet_def);
  ClusterSequence * cs = new ClusterSequenceArea(particles, jet_def, area_def);
  PseudoJet jet = hardest_jet(*cs);
  cs->delete_self_when_unused();
  return jet;
}

/// print jet info
void show_jet(const PseudoJet & jet, bool expected_to_throw = false){
  bool threw = false;
  try{
    cout << "Jet has pt=" << jet.perp() << " and " << jet.constituents().size() << " constituents";
    if (jet.has_area()) cout << ", area = " << jet.area();
    cout << endl;
  } catch (fastjet::Error){
    if (expected_to_throw) cerr << "Expected ";
    cerr << "fastjet::Error caught" << endl;
    threw = true;
  }
  assert(threw == expected_to_throw);
  //if (threw != expected_to_throw) throw fastjet::Error("unexpected throw");
}

/// an example program showing how to use fastjet
int main (int argc, char ** argv) {
  // read in input particles
  //----------------------------------------------------------
  vector<PseudoJet> particles;
  double px, py , pz, E;
  while (cin >> px >> py >> pz >> E)
    particles.push_back(PseudoJet(px,py,pz,E)); 
  
  // series of tests:
  //----------------------------------------------------------
  // 0. empty cluster sequence
  ClusterSequence * cs0 = new ClusterSequence();
  delete cs0;
  cout << "Test 0 passed" << endl;

  //----------------------------------------------------------
  // 1. regular CS, no PJ left using it
  ClusterSequence * cs1 = new ClusterSequenceArea(particles, jet_def, area_def);
  delete cs1;
  cout << "Test 1 passed" << endl;

  //----------------------------------------------------------
  // 2. regular CS, no PJ left using it
  ClusterSequence * cs2 = new ClusterSequenceArea(particles, jet_def, area_def);
  PseudoJet j2 = hardest_jet(*cs2);
  show_jet(j2);
  delete cs2;
  show_jet(j2, true); // should throw
  cout << "Test 2 passed" << endl;

  //----------------------------------------------------------
  // 3. owned CS, no PJ left using it
  PseudoJet * j3 = new PseudoJet(hardest_jet(particles));
  show_jet(*j3);
  cout << "Just about to delete j3 " << endl;
  delete j3;
  cout << "Test 3 passed" << endl;

  //----------------------------------------------------------
  // 4. owned CS, explicitly delete the CS
  PseudoJet * j4 = new PseudoJet(hardest_jet(particles));
  show_jet(*j4);
  delete j4->associated_cluster_sequence();
  show_jet(*j4,true);  // should throw
  delete j4;
  cout << "Test 4 passed" << endl;

  return 0;
}
