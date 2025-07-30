//FJSTARTHEADER
// $Id$
//
// Copyright (c) 2005-2025, Matteo Cacciari, Gavin P. Salam and Gregory Soyez
//
//----------------------------------------------------------------------
// This file is part of FastJet.
//
//  FastJet is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  The algorithms that underlie FastJet have required considerable
//  development. They are described in the original FastJet paper,
//  hep-ph/0512210 and in the manual, arXiv:1111.6097. If you use
//  FastJet as part of work towards a scientific publication, please
//  quote the version you use and include a citation to the manual and
//  optionally also to hep-ph/0512210.
//
//  FastJet is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with FastJet. If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------
//FJENDHEADER


//----------------------------------------------------------------------
// fastjet example program to show how to access subjets;
// 
// See also fastjet_higgs_decomp.cc to see the use of subjets for
// identifying boosted higgs (and other objects)
//
// Compile it with: make fastjet_subjets
// run it with    : ./fastjet_subjets < data/single-event.dat
//
//----------------------------------------------------------------------
#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include<iostream> // needed for io
#include<sstream>  // needed for internal io
#include<vector> 
#include <cstdio>

using namespace std;

// to avoid excessive typing, define an abbreviation for the
// fastjet namespace
namespace fj = fastjet;


// a declaration of a function that pretty prints a list of jets
void print_jets (const vector<fj::PseudoJet> &);

// and this pretty prinst a single jet
void print_jet (const fj::PseudoJet & jet);

// pretty print the jets and their subjets
void print_jets_and_sub (const vector<fj::PseudoJet> & jets,
                         double dcut);

/// an example program showing how to use fastjet
int main (int argc, char ** argv) {
  
  vector<fj::PseudoJet> input_particles;
  
  // read in input particles
  double px, py , pz, E;
  while (cin >> px >> py >> pz >> E) {
    // create a fj::PseudoJet with these components and put it onto
    // back of the input_particles vector
    input_particles.push_back(fj::PseudoJet(px,py,pz,E)); 
  }
  
  // We'll do two subjet analyses, physically rather different
  double R = 1.0;
  //fj::JetDefinition kt_def(fj::kt_algorithm, R);
  fj::JetDefinition cam_def(fj::cambridge_algorithm, R);

  // run the jet clustering with the above jet definition
  //fj::ClusterSequence kt_seq(input_particles, kt_def);
  fj::ClusterSequence cam_seq(input_particles, cam_def);

  // tell the user what was done
  cout << "Ran " << cam_def.description() << endl;
  cout << "Strategy adopted by FastJet was "<<
       cam_seq.strategy_string()<<endl<<endl;

  // extract the inclusive jets with pt > 5 GeV
  double ptmin = 5.0;
  vector<fj::PseudoJet> inclusive_jets = cam_seq.inclusive_jets(ptmin);

  // for the subjets  
  double smallR = 0.4;
  double dcut_cam = pow(smallR/R,2);

  // print them out
  cout << "Printing inclusive jets (R = "<<R<<") with pt > "<< ptmin<<" GeV\n";
  cout << "and their subjets with smallR = " << smallR << "\n";
  cout << "---------------------------------------\n";
  print_jets_and_sub(inclusive_jets, dcut_cam);
  cout << endl;


  // print them out
  vector<fj::PseudoJet> exclusive_jets = cam_seq.exclusive_jets(dcut_cam);
  cout << "Printing exclusive jets with dcut = "<< dcut_cam<<" \n";
  cout << "--------------------------------------------\n";
  print_jets(exclusive_jets);


}


//----------------------------------------------------------------------
/// a function that pretty prints a list of jets
void print_jets (const vector<fj::PseudoJet> & jets) {

  // sort jets into increasing pt
  vector<fj::PseudoJet> sorted_jets = sorted_by_pt(jets);  

  // label the columns
  printf("%5s %15s %15s %15s %15s\n","jet #", "rapidity", 
	 "phi", "pt", "n constituents");
  
  // print out the details for each jet
  for (unsigned int i = 0; i < sorted_jets.size(); i++) {
    printf("%5u ",i);
    print_jet(sorted_jets[i]);
  }

}


//----------------------------------------------------------------------
/// a function that pretty prints a list of jets
void print_jets_and_sub (const vector<fj::PseudoJet> & jets,
                         double dcut) {

  // sort jets into increasing pt
  vector<fj::PseudoJet> sorted_jets = sorted_by_pt(jets);  

  // label the columns
  printf("%5s %15s %15s %15s %15s\n","jet #", "rapidity", 
	 "phi", "pt", "n constituents");
  
  // print out the details for each jet
  for (unsigned int i = 0; i < sorted_jets.size(); i++) {
    printf("%5u       ",i);
    print_jet(sorted_jets[i]);
    vector<fj::PseudoJet> subjets = sorted_by_pt(sorted_jets[i].exclusive_subjets(dcut));
    for (unsigned int j = 0; j < subjets.size(); j++) {
      printf("    -sub-%02u ",j);
      print_jet(subjets[j]);
    }
  }

}


//----------------------------------------------------------------------
/// print a single jet
void print_jet (const fj::PseudoJet & jet) {
  int n_constituents = jet.constituents().size();
  printf("%15.8f %15.8f %15.8f %8u\n",
         jet.rap(), jet.phi(), jet.perp(), n_constituents);
}
