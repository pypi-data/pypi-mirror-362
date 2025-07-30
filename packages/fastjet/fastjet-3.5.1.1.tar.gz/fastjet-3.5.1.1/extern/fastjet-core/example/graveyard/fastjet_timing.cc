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
/// fastjet_timing.cc: Program to help time and test the fastjet package
/// 
/// It reads files containing multiple events in the format 
/// p1x p1y p1z E1
/// p2x p2y p2z E2
/// ...
/// #END
/// 
/// An example input file containing 10 events is included as 
/// data/Pythia-PtMin1000-LHC-10ev.dat
///
/// Usage:
///   fastjet_timing [-strategy NUMBER] [-repeat nrepeats] [-massive] \
///                  [-combine nevents] [-r Rparameter] [-incl ptmin] [...] \
///                  < data_file
///
/// where the clustering can be repeated to aid timing and multiple
/// events can be combined to get to larger multiplicities. Some options:
///
///   -strategy N   indicate stratgey from the enum FjStrategy (see
///                 FjClusterSequence.hh).
///
///   -combine nev  for combining multiple events from the data file in order
///                 to get to large multiplicities.
///
///   -incl ptmin   output of all inclusive jets with pt > ptmin is obtained
///                 with the -incl option.
///
///   -excld dcut   output of all exclusive jets as obtained in a clustering
///                 with dcut
///
///   -massless     read in only the 3-momenta and deduce energies assuming
///                 that particles are massless
///
///   -write        for writing out detailed clustering sequence (valuable
///                 for testing purposes)
///
///   -unique_write writes out the sequence of dij's according to the
///                 "unique_history_order" (useful for verifying consistency
///                 between different clustering strategies).
///
///   -cam          switch to the inclusive Cambridge/Aachen algorithm --
///                 note that the option -excld dcut provides a clustering
///                 up to the dcut which is the minimum squared
///                 distance between any pair of jets.
///
#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include<iostream>
#include<sstream>
#include<valarray>
#include<vector>
#include <cstdio>
#include <cstdlib>
#include<cstddef> // for size_t
#include "CmdLine.hh"

using namespace std;

// to avoid excessive typing, define an abbreviation for the 
// fastjet namespace
namespace fj = fastjet;

inline double pow2(const double x) {return x*x;}

/// a program to test and time the kt algorithm as implemented in fastjet
int main (int argc, char ** argv) {

  CmdLine cmdline(argc,argv);
  // allow the use to specify the fj::Strategy either through the
  // -clever or the -strategy options (both will take numerical
  // values); the latter will override the former.
  fj::Strategy  strategy  = fj::Strategy(cmdline.int_val("-strategy",
                                        cmdline.int_val("-clever", fj::Best)));
  int  repeat  = cmdline.int_val("-repeat",1);
  int  combine = cmdline.int_val("-combine",1);
  bool write   = cmdline.present("-write");
  bool unique_write = cmdline.present("-unique_write");
  bool hydjet  = cmdline.present("-hydjet");
  double ktR   = cmdline.double_val("-r",1.0);
  double inclkt = cmdline.double_val("-incl",-1.0);
  int    excln  = cmdline.int_val   ("-excln",-1);
  double excld  = cmdline.double_val("-excld",-1.0);
  double etamax = cmdline.double_val("-etamax",1.0e305);
  bool   show_constituents = cmdline.present("-const");
  bool   massless = cmdline.present("-massless");
  int  nev     = cmdline.int_val("-nev",1);
  bool add_dense_coverage = cmdline.present("-dense");

  // The following option causes the Cambridge algo to be used.
  // Note that currently the only output that works sensibly here is
  // "-incl 0"
  fj::JetAlgorithm jet_algorithm;
  if (cmdline.present("-cam")) {
    jet_algorithm = fj::cambridge_algorithm;
  } else {
    jet_algorithm = fj::kt_algorithm;
  }

  if (!cmdline.all_options_used()) {cerr << 
      "Error: some options were not recognized"<<endl; 
    exit(-1);}


  for (int iev = 0; iev < nev; iev++) {
  vector<fj::PseudoJet> jets;
  string line;
  int  ndone = 0;
  while (getline(cin, line)) {
      //cout << line<<endl;
    istringstream linestream(line);
    if (line == "#END") {
      ndone += 1;
      if (ndone == combine) {break;}
    }
    if (line.substr(0,1) == "#") {continue;}
    valarray<double> fourvec(4);
    if (hydjet) {
      // special reading from hydjet.txt event record (though actually
      // this is supposed to be a standard pythia event record, so
      // being able to read from it is perhaps not so bad an idea...)
      int ii, istat,id,m1,m2,d1,d2;
      double mass;
      linestream >> ii>> istat >> id >> m1 >> m2 >> d1 >> d2
		 >> fourvec[0] >> fourvec[1] >> fourvec[2] >> mass;
      // current file contains mass of particle as 4th entry
      if (istat == 1) {
	fourvec[3] = sqrt(+pow2(fourvec[0])+pow2(fourvec[1])
			  +pow2(fourvec[2])+pow2(mass));
      }
    } else {
      if (massless) {
	linestream >> fourvec[0] >> fourvec[1] >> fourvec[2];
	fourvec[3] = sqrt(pow2(fourvec[0])+pow2(fourvec[1])+pow2(fourvec[2]));}
      else {
	linestream >> fourvec[0] >> fourvec[1] >> fourvec[2] >> fourvec[3];
      }
    }
    fj::PseudoJet psjet(fourvec);
    if (abs(psjet.rap()) < etamax) {jets.push_back(psjet);}
  }

  // add a fake underlying event which is very soft, uniformly distributed
  // in eta,phi so as to allow one to reconstruct the area that is associated
  // with each jet.
  if (add_dense_coverage) {
    srand(2);
    int nphi = 60;
    int neta = 100;
    double kt = 1e-1;
    for (int iphi = 0; iphi<nphi; iphi++) {
      for (int ieta = -neta; ieta<neta+1; ieta++) {
	double phi = (iphi+0.5) * (fj::twopi/nphi) + rand()*0.001/RAND_MAX;
	double eta = ieta * (10.0/neta)  + rand()*0.001/RAND_MAX;
	kt = 0.0000001*(1+rand()*0.1/RAND_MAX);
	double pminus = kt*exp(-eta);
	double pplus  = kt*exp(+eta);
	double px = kt*sin(phi);
	double py = kt*cos(phi);
	//cout << kt<<" "<<eta<<" "<<phi<<"\n";
	fj::PseudoJet mom(px,py,0.5*(pplus-pminus),0.5*(pplus+pminus));
	jets.push_back(mom);
      }
    }
  }
  
  fj::JetDefinition jet_def(jet_algorithm, ktR, strategy);

  for (int irepeat = 0; irepeat < repeat ; irepeat++) {
    fj::ClusterSequence clust_seq(jets,jet_def,write);
    if (irepeat != 0) {continue;}
    cout << "iev "<<iev<< ": number of particles = "<< jets.size() << endl;
    cout << "strategy used =  "<< clust_seq.strategy_string()<< endl;

    // now provide some nice output...
    if (inclkt >= 0.0) {
      vector<fj::PseudoJet> jets = sorted_by_pt(clust_seq.inclusive_jets(inclkt));
      for (size_t j = 0; j < jets.size(); j++) {
	printf("%5u %15.8f %15.8f %15.8f\n",j,jets[j].rap(),jets[j].phi(),sqrt(jets[j].kt2()));
	if (show_constituents) {
	  vector<fj::PseudoJet> const_jets = jets[j].constituents();
	  for (size_t k = 0; k < const_jets.size(); k++) {
	    printf("        jet%03u %15.8f %15.8f %15.8f\n",j,const_jets[k].rap(),
		   const_jets[k].phi(),sqrt(const_jets[k].kt2()));
	  }
	  cout << "\n\n";
	}
      }
    }

    if (excln > 0) {
      vector<fj::PseudoJet> jets = sorted_by_E(clust_seq.exclusive_jets(excln));
 
      cout << "Printing "<<excln<<" exclusive jets\n";
      for (size_t j = 0; j < jets.size(); j++) {
	printf("%5u %15.8f %15.8f %15.8f\n",
	       //j,jets[j].rap(),jets[j].phi(),sqrt(jets[j].kt2()));
	       j,jets[j].rap(),jets[j].phi(),jets[j].kt2());
      }
    }

    if (excld > 0.0) {
      vector<fj::PseudoJet> jets = sorted_by_pt(clust_seq.exclusive_jets(excld));
      cout << "Printing exclusive jets for d = "<<excld<<"\n";
      for (size_t j = 0; j < jets.size(); j++) {
	printf("%5u %15.8f %15.8f %15.8f\n",
	       j,jets[j].rap(),jets[j].phi(),sqrt(jets[j].kt2()));
      }
    }
    
    // useful for testing that recombination sequences are unique
    if (unique_write) {
      vector<int> unique_history = clust_seq.unique_history_order();
      // construct the inverse of the above mapping
      vector<int> inv_unique_history(clust_seq.history().size());
      for (unsigned int i = 0; i < unique_history.size(); i++) {
	inv_unique_history[unique_history[i]] = i;}

      for (unsigned int i = 0; i < unique_history.size(); i++) {
	fj::ClusterSequence::history_element el = 
	  clust_seq.history()[unique_history[i]];
	int uhp1 = el.parent1>=0 ? inv_unique_history[el.parent1] : el.parent1;
	int uhp2 = el.parent2>=0 ? inv_unique_history[el.parent2] : el.parent2;
	printf("%7d u %15.8e %7d u %7d u\n",i,el.dij,uhp1, uhp2);
      }
    }

  } // irepeat

  } // iev
}
