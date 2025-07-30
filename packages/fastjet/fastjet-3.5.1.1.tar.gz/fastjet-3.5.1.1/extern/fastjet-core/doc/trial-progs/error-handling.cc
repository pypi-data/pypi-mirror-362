#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/Selector.hh"
#include "fastjet/tools/JetMedianBackgroundEstimator.hh"
#include "fastjet/LimitedWarning.hh"
#include <string>
#include <iostream>
#include <fstream>

using namespace std;
using namespace fastjet;

int main() {

//  filebuf fb;
//  fb.open ("warnings.txt",ios::out);
//  ostream myfile(&fb);

ofstream myfile("warnings.txt");
ofstream myfile1("errors.txt");
//ostream * myfile = std::cout;

//myfile << "FFFF" << endl;
//myfile << "EEEE" << endl;
Error errors;
//errors.set_default_stream(&myfile);
errors.set_print_errors(true);
errors.set_print_backtrace(true);

LimitedWarning warnings;
//warnings.set_default_stream(&myfile);

JetDefinition jet_def(antikt_algorithm, 0.5);
AreaDefinition area_def(active_area);
vector<PseudoJet> input_particles;

PseudoJet jet(PtYPhiM(100.,0.,0.,0.));
input_particles.push_back(jet);

ClusterSequenceArea csa(input_particles,jet_def,area_def);
vector<PseudoJet> jets = csa.inclusive_jets();

Selector sel = SelectorAbsRapMax(4.5);
JetMedianBackgroundEstimator bge(sel,csa);
JetMedianBackgroundEstimator bge1(sel,csa);
Selector sel2 = SelectorNHardest(3);
JetMedianBackgroundEstimator bge2(sel2,csa);

//bge.set_particles(input_particles);
double rho = bge.rho();
cout << "rho = " << rho << endl;

cout << warnings.summary() << endl;
//myfile << "GGGG" << endl;
//myfile.close();
}

