#ifndef  D0RunIIconeJets_HepEntity_class
#define  D0RunIIconeJets_HepEntity_class

#include "inline_maths.h"

//Author: Lars Sonnenschein 28/Mar/2007
//This is an example class fulfilling the minimal requirements needed by the
//D0 RunII cone jet algorithm implementation, which is an inlined template class

class HepEntity {

 public:

  HepEntity() {
    E=0.;
    px=0.;
    py=0.;
    pz=0.;
    return;
  }


  HepEntity(double E_in, double px_in, double py_in, double pz_in) : 
    E(E_in), px(px_in), py(py_in), pz(pz_in) {
    return;
  }


  HepEntity(const HepEntity& in) : E(in.E), px(in.px), py(in.py), pz(in.pz) {
    return;
  }

  
  inline double y() const {
    return inline_maths::y(E,pz);
  }


  inline double phi() const {
     return inline_maths::phi(px,py);
  }


  inline double pT() const {
     return sqrt(inline_maths::sqr(px)+inline_maths::sqr(py));
  }


  inline void p4vec(float* p) const {
    p[0] = px;
    p[1] = py;
    p[2] = pz;
    p[3] = E;
    return;
  }

  inline void Add(const HepEntity el) {
    E += el.E;
    px += el.px;
    py += el.py;
    pz += el.pz;
    return;
  }

  inline void Fill(double E_in, double px_in, double py_in, double pz_in) {
    E = E_in;
    px = px_in;
    py = py_in;
    pz = pz_in;
    return;
  }


  double E;
  double px;
  double py;
  double pz;

 private:



};
//end of class HepEntity;

#endif
