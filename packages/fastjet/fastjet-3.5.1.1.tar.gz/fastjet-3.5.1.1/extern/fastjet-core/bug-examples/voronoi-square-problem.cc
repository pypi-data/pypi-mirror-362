//----------------------------------------------------------------------
/// program to illustrate bug with voronoi generation encountered
/// by Gavin on toth (and elsewhere) 2.6.22.1-27.fc7 #1 SMP i686
/// 
/// To reproduce it:
///   > make voronoi-square-problem
///   > ./voronoi-square-problem < voronoi-square-problem.y-phi-pt-m
///
/// With gdb, problems seems to appear around Voronoi.cc:547, whereas
/// valgrind reveals no problem...
///
/// Characteristic of example event (format: y phi pt m) is that
/// it's a small set of momenta occupying a subset of elements of
/// of a square grid (discovered when trying to run output from
/// the unstretched version of our toy calorimeter).
///
/// Once bug looks like being fixed, then run original program that
/// brought it out: from ../../areas
///
///   > ./run-mass-test.pl -kt -R 0.7 -pileup -calo_thresh 0.0 -lhc \
///        -Zp2jets -Zpmass 2000 -out a -nev 200 -rho_uses_kt05  -freq 10  
///
/// and problems should appear after a few 10's-100's of events
///
#include "fastjet/ClusterSequenceArea.hh"
//#include "../../areas/Calorimeter.hh"
#include<iostream>
#include<iomanip>

using namespace std;
using namespace fastjet;

// define our calorimeter to be a little like the CMS one
// double cal_ymax = 6.0;
// double cal_cell = 0.085;
// double calo_thresh = -1.0;
// Calorimeter toy_calo(cal_ymax, cal_cell);


int main() {
  vector<PseudoJet> particles;
  
  JetDefinition jet_def(kt_algorithm,0.5);
  AreaDefinition area_def(voronoi_area);

  //int n = 100;
  //double spacing = 0.25;

  // create particles on a square grid
  bool readrap=true;
  if (readrap) {
    double y,phi,pt,m;
    while (cin >> y >> phi >> pt >> m) {
      particles.push_back(PtYPhiM(pt,y,phi));
    }
  } else {
    double px,py,pz,E;
    while (cin >> px >> py >> pz >> E) {
      particles.push_back(PseudoJet(px,py,pz,E));
    }
  }
  //toy_calo.reset();
  //toy_calo.add_particles(particles);
  
  vector<PseudoJet> procpart = particles;
  //vector<PseudoJet> procpart = toy_calo.cells();
  //cout << setprecision(18) ;
  //cout  << "NEW EVENT *********************************************" << endl;
  //for (unsigned i = 0; i < procpart.size(); i++) {
  //  const PseudoJet & part = procpart[i];
  //  cout << part.rap() << " " 
  //       << part.phi() << " " 
  //       << part.perp() << " " 
  //       << 0.0 << endl;
  //}
  
  for (int i = 0; i < 100; i++) {
    ClusterSequenceArea csa(particles, jet_def, area_def);
    //ClusterSequenceArea csa(procpart, jet_def, area_def);
  }
  
}
