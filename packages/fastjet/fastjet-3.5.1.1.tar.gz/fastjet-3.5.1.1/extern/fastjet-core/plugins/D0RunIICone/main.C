#include <list>
#include "ILConeAlgorithm.hpp"
#include "HepEntity.h"

#include <fastjet/internal/base.hh>

FASTJET_BEGIN_NAMESPACE

namespace d0{

using namespace std;

int main() {

  
  HepEntity el;
  list<const HepEntity*> *ensemble = new list<const HepEntity*>;
  //list<const HepEntity*> ensemble;

  //fill with E, px, py, pz
  el.Fill(100., 25., 25., 25., 0);
  ensemble->push_back(new HepEntity(el));
  el.Fill(105., 20., 30., 30., 1);
  ensemble->push_back(new HepEntity(el));
  el.Fill(60., 20., 20., 20., 2);
  ensemble->push_back(new HepEntity(el));
  el.Fill(95., 65., 10., 20., 3);
  ensemble->push_back(new HepEntity(el));
  
  el.Fill(110., 25., -25., -25., 4);
  ensemble->push_back(new HepEntity(el));
  el.Fill(100., 23., -25., -25., 5);
  ensemble->push_back(new HepEntity(el));
  el.Fill(101., 25., -20., -25., 6);
  ensemble->push_back(new HepEntity(el));
  el.Fill(102., 25., -25., -23., 7);
  ensemble->push_back(new HepEntity(el));
  

  
  cout << "list->size()=" << ensemble->size() << endl;
  int i=1;
  for (list<const HepEntity*>::iterator it = ensemble->begin(); it != ensemble->end(); ++it) {
    cout << "4-vector " << i++ << " : E=" << (*it)->E << " pT=" << (*it)->pT() << " y=" << (*it)->y() << " phi=" << (*it)->phi() << endl; 
    cout << (*it) << endl;
  }

  
  float cone_radius = 0.5;
  float min_jet_Et = 8.0;
  float split_ratio = 0.5;

  //the parameters below have been found to be set to the values given below 
  //in the original implementation, shouldn't be altered
  float far_ratio=0.5;
  float Et_min_ratio=0.5;
  bool kill_duplicate=true;
  float duplicate_dR=0.005; 
  float duplicate_dPT=0.01; 
  float search_factor=1.0; 
  float pT_min_leading_protojet=0.; 
  float pT_min_second_protojet=0.;
  int merge_max=10000; 
  float pT_min_nomerge=0.;

  ILConeAlgorithm<HepEntity> 
    ilegac(cone_radius, min_jet_Et, split_ratio,
	   far_ratio, Et_min_ratio, kill_duplicate, duplicate_dR, 
	   duplicate_dPT, search_factor, pT_min_leading_protojet, 
	   pT_min_second_protojet, merge_max, pT_min_nomerge);
 
  float Item_ET_Threshold = 0.;
  float Zvertex = 0.;

  float* Item_ET_Threshold_ptr = &Item_ET_Threshold;


  list<HepEntity> jets;
  ilegac.makeClusters(jets, *ensemble, Item_ET_Threshold);


  list<HepEntity>::iterator it;
  cout << "Number of jets = " << jets.size() << endl;
  for (it=jets.begin(); it!=jets.end(); ++it) {
    cout << "jet: E=" << (*it).E << " pT=" << (*it).pT() << " y=" << (*it).y() << " phi=" << (*it).phi() << endl; 
  }

  //delete elements of the ensemble particle list
  //relevant to prevent memory leakage when running over many events
  for (list<const HepEntity*>::iterator it = ensemble->begin(); it != ensemble->end(); ++it) {
    delete *it;
  }
  delete ensemble;

  return 0;

}

}  // namespace d0


FASTJET_END_NAMESPACE
