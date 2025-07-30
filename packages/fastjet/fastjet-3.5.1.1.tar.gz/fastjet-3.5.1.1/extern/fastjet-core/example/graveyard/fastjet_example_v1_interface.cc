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
// fastjet example program using fastjet-v1 interface
//
// Compile it with: make fastjet_example_v1_interface
// run it with    : ./fastjet_example_v1_interface < data/single-event.dat
//
// People who are familiar with the ktjet package are encouraged to
// compare this file to the ktjet_example.cc program which does the
// same thing in the ktjet framework.
//----------------------------------------------------------------------
#include "FjPseudoJet.hh"
#include "FjClusterSequence.hh"
#include<iostream> // needed for io
#include<sstream>  // needed for internal io
#include<vector> 

using namespace std;

// a declaration of a function that pretty prints a list of jets
void print_jets (const FjClusterSequence &, const vector<FjPseudoJet> &);

/// an example program showing how to use fastjet
int main (int argc, char ** argv) {
  
  vector<FjPseudoJet> input_particles;
  
  // read in input particles
  double px, py , pz, E;
  while (cin >> px >> py >> pz >> E) {
    // create a FjPseudoJet with these components and put it onto
    // back of the input_particles vector
    input_particles.push_back(FjPseudoJet(px,py,pz,E)); 
  }

  // run the jet clustering with option R=1.0 and strategy=Best
  double Rparam = 1.0;
  FjClusterSequence clust_seq(input_particles, Rparam, Best);

  // tell the user what was done
  cout << "Strategy adopted by FastJet was "<<
       clust_seq.strategy_string()<<endl<<endl;

  // extract the inclusive jets with pt > 5 GeV, sorted by pt
  double ptmin = 5.0;
  vector<FjPseudoJet> inclusive_jets = clust_seq.inclusive_jets(ptmin);

  // print them out
  cout << "Printing inclusive jets with pt > "<< ptmin<<" GeV\n";
  cout << "---------------------------------------\n";
  print_jets(clust_seq, inclusive_jets);
  cout << endl;

  // extract the exclusive jets with dcut = 25 GeV^2 
  double dcut = 25.0;
  vector<FjPseudoJet> exclusive_jets = clust_seq.exclusive_jets(dcut);

  // print them out
  cout << "Printing exclusive jets with dcut = "<< dcut<<" GeV^2\n";
  cout << "--------------------------------------------\n";
  print_jets(clust_seq, exclusive_jets);


}


//----------------------------------------------------------------------
/// a function that pretty prints a list of jets
void print_jets (const FjClusterSequence & clust_seq, 
		 const vector<FjPseudoJet> & jets) {

  // sort jets into increasing pt
  vector<FjPseudoJet> sorted_jets = sorted_by_pt(jets);  

  // label the columns
  printf("%5s %15s %15s %15s %15s\n","jet #", "rapidity", 
	 "phi", "pt", "n constituents");
  
  // print out the details for each jet
  for (unsigned int i = 0; i < sorted_jets.size(); i++) {
    int n_constituents = clust_seq.constituents(sorted_jets[i]).size();
    printf("%5u %15.8f %15.8f %15.8f %8u\n",
	   i, sorted_jets[i].rap(), sorted_jets[i].phi(),
	   sorted_jets[i].perp(), n_constituents);
  }

}
