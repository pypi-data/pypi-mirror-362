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
// fastjet example program, illustration of carrying out boosted
// Higgs subjet ID analysis
//
// It illustrates two kinds of functionality: 
//
//  - following the decomposition of a jet into pieces
//  - following information on a b-tag through the jet
//
// This kind of functionality was used in arXiv:0802.2470
// (Butterworth, Davison, Rubin & Salam) for boosted Higgs searches,
// and related functionality was used in arXiv:0806.0848 (Kaplan,
// Rehermann, Schwartz & Tweedie) in searching for boosted tops
// (without b-tag assumptions).

// Compile it with: make fastjet_boosted_higgs
// run it with    : ./fastjet_boosted_higgs < data/HZ-event-Hmass115.dat
//
//----------------------------------------------------------------------

#include "fastjet/ClusterSequence.hh"
#include<iostream> // needed for io
#include<sstream>  // needed for internal io
#include<iomanip>  
#include<cmath>

using namespace std;
namespace fj = fastjet;




//----------------------------------------------------------------------
/// set up a class to give standard (by default E-scheme)
/// recombination, with additional tracking of flavour information in
/// the user_index. 
///
/// If you use this, you must explicitly set the user index to 0 for
/// non-flavoured particles (the default value is -1);
///
/// This will work for native algorithms, but not for all plugins
typedef fj::JetDefinition::DefaultRecombiner DefRecomb;
class FlavourRecombiner : public  DefRecomb {
public:
  FlavourRecombiner(fj::RecombinationScheme recomb_scheme = fj::E_scheme) : 
    DefRecomb(recomb_scheme) {};

  virtual std::string description() const {return DefRecomb::description()
      +" (with user index addition)";}

  /// recombine pa and pb and put result into pab
  virtual void recombine(const fj::PseudoJet & pa, 
                         const fj::PseudoJet & pb, 
                         fj::PseudoJet & pab) const {
    DefRecomb::recombine(pa,pb,pab);
    pab.set_user_index(pa.user_index() + pb.user_index());
  }

};


/// forward declaration for printing out info about a jet
ostream & operator<<(ostream &, fj::PseudoJet &);


//----------------------------------------------------------------------
int main (int argc, char ** argv) {
  
  vector<fj::PseudoJet> particles;

  // read in data in format px py pz E b-tag [last of these is optional]
  string line;
  while (getline(cin,line)) {
    if (line.substr(0,1) == "#") {continue;}
    istringstream linestream(line);
    double px,py,pz,E;
    linestream >> px >> py >> pz >> E;

    // optionally read in btag information
    int    btag;
    if (! (linestream >> btag)) btag = 0;

    // construct the particle
    fj::PseudoJet particle(px,py,pz,E);
    particle.set_user_index(btag); // btag info goes in user index, for flavour tracking
    particles.push_back(particle);
  }


  // set up the jet finding
  double R = 1.2;
  FlavourRecombiner flav_recombiner; // for tracking flavour
  fj::JetDefinition jet_def(fj::cambridge_algorithm, R, &flav_recombiner);

  
  // run the jet finding; find the hardest jet
  fj::ClusterSequence cs(particles, jet_def);
  vector<fj::PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());


  cout << "Ran: " << jet_def.description() << endl << endl;
  cout << "Hardest jet: " << jets[0] << endl << endl;


  /// now do the subjet decomposition;
  //
  /// when unpeeling a C/A jet, often only a very soft piece may break off;
  /// the mass_drop_threshold indicates how much "lighter" the heavier of the two
  /// resulting pieces must be in order for us to consider that we've really
  /// seen some form of substructure
  double mass_drop_threshold = 0.667; 
  /// QCD backgrounds that give larger jet masses have a component
  /// where a quite soft gluon is emitted; to eliminate part of this
  /// one can place a cut on the asymmetry of the branching; 
  ///
  /// Here the cut is expressed in terms of y, the kt-distance scaled
  /// to the squared jet mass; an easier way to see it is in terms of
  /// a requirement on the momentum fraction in the splitting: z/(1-z)
  /// and (1-z)/z > rtycut^2 [the correspondence holds only at LO]
  double rtycut              = 0.3;

  fj::PseudoJet this_jet = jets[0], parent1, parent2;
  bool had_parents;

  while ((had_parents = this_jet.has_parents(parent1,parent2))) {
    // make parent1 the more massive jet
    if (parent1.m() < parent2.m()) swap(parent1,parent2);
    //
    // if we pass the conditions on the mass drop and its degree of
    // asymmetry (z/(1-z) \sim kt_dist/m^2 > rtycut), then we've found
    // something interesting, so exit the loop
    if (parent1.m() < mass_drop_threshold * this_jet.m() &&
	parent1.kt_distance(parent2) > pow(rtycut,2) * this_jet.m2()) {
      break;
    } else {
      // otherwise try a futher decomposition on the more massive jet
      this_jet = parent1;
    }
  }

  // look to see what we found
  if (had_parents) {
    cout << "Found suitable pair of subjets: " << endl;
    cout << " " << parent1 << endl;
    cout << " " << parent2 << endl;
    cout << "Total = " << endl;
    cout << " " << this_jet << endl << endl;

    // next we "filter" it, to remove UE & pileup contamination
    //
    // [there are two ways of doing this; here we directly use the
    // exsiting cluster sequence and find the exclusive subjets of
    // this_jet (i.e. work backwards within the cs starting from
    // this_jet); alternatively one can recluster just the
    // constituents of the jet]
    //
    // first get separation between the subjets (called Rbb -- assuming it's a Higgs!)
    double   Rbb = sqrt(parent1.squared_distance(parent2));
    double   Rfilt = min(Rbb/2, 0.3); // somewhat arbitrary choice
    unsigned nfilt = 3;               // number of pieces we'll take
    cout << "Subjet separation (Rbb) = " << Rbb << ", Rfilt = " << Rfilt << endl;

    double   dcut  = pow(Rfilt/R,2);  // for C/A get a view at Rfilt by
				    // using a dcut=(Rfilt/R)^2
    vector<fj::PseudoJet> filt_subjets = sorted_by_pt(this_jet.exclusive_subjets(dcut));

    // now print out the filtered jets and reconstruct total 
    // at the same time
    cout << "Filtered pieces are " << endl;
    cout << " " << filt_subjets[0] << endl;
    fj::PseudoJet filtered_total = filt_subjets[0];
    for (unsigned i = 1; i < nfilt && i < filt_subjets.size(); i++) {
      cout << " " << filt_subjets[i] << endl;
      flav_recombiner.plus_equal(filtered_total, filt_subjets[i]);
    }
    cout << "Filtered total is " << endl;
    cout << " " << filtered_total << endl;

  } else {
    cout << "Did not find suitable hard substructure in this event." << endl;
  }
}


/// does the actual work for printing out a jet
ostream & operator<<(ostream & ostr, fj::PseudoJet & jet) {
  ostr << "pt, y, phi =" 
       << " " << setw(10) << jet.perp() 
       << " " << setw(6) <<  jet.rap()  
       << " " << setw(6) <<  jet.phi()  
       << ", mass = " << setw(10) << jet.m()
       << ", btag = " << jet.user_index();
  return ostr;
}
