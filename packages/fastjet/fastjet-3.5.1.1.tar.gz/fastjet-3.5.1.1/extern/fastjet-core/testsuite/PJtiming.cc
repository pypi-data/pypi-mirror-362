/// \file PJtiming.cc
///
/// Standalone program for investigating the impact of FJ3.0 v FJ2.4
/// on timing for creation of vectors of PseudoJets.
/// 
/// Results are for g++ 4.4.5 and were obtained on 12 May 2011, around
/// revision 2093. Runs are performed with the following arguments
///
///   ./PJtiming -n 1e3 -sz 1e4 [-array]
///
/// Results on my ubuntu virtual machine (host: OS X 10.6)
///
/// - FJ3.0 (with two shared pointers, no default initialisation of rest):
///   - C++ vector: 110ns / PJ (for vector of size 10^3; 140ns for bigger vector)
///   - C   array:    9ns / PJ
///
/// - FJ3.0 (with two shared pointers, and default initialisation of rest):
///   - C++ vector:  15ns / PJ (for vector of size 10^3; 45ns for bigger vector)
///   - C   array:   15ns / PJ
///
/// - FJ2.4
///   - C++ vector:   0ns / PJ (for vector of size 10^3; near 27ns for smaller vector)
///   - C   array:    0ns / PJ
///
/// Note that these timings seem hugely system dependent. On Gregory's
/// home system the 100ns penalty (top case) is not there (a question
/// of cache?). On Gavin's laptop it's more like 200ns.
///
/// All three systems tested concur that with the full initialisation, timings
/// are down to O(10-20ns) (5ns for Gregory).
///
/// 2014-07-22: with clang [Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)]
///             this program no longer compiled 
///             (variable length array of non-POD element type 'fastjet::PseudoJet')
#include "fastjet/PseudoJet.hh"
#include <iostream>
#include "CmdLine.hh"

using namespace fastjet;
using namespace std;

// // a 
// class TestingObject {
//   TestingObject
//   double px, py, pz, E
// };

void make_vector(int sz) {
  vector<PseudoJet> particles(sz);
  particles[sz-1].reset(0,0,0,0); // make sure something happens
}

void make_array(int sz) {
  PseudoJet * particles = new PseudoJet[sz];
  //PseudoJet particles[sz];
  particles[sz-1].reset(0,0,0,0); // make sure something happens
  delete[] particles;
}

int main(int argc, char** argv) {
  CmdLine cmdline(argc,argv);
  int n = int(cmdline.value("-n",100.0));
  int sz = int(cmdline.value("-sz",100.0));

  bool array = cmdline.present("-array");

  for (int i = 0; i < n; i++) {
    if (array) {make_array(sz);}
    else       {make_vector(sz);}
  }

  cout << "Total number of PseudoJets created was " << double(n)*double(sz) << endl;
}
