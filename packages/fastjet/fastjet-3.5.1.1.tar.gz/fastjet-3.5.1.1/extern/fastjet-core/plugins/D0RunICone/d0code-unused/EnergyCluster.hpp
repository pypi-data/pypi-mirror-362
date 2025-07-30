#ifndef INC_ENERGYCLUSTER
#define INC_ENERGYCLUSTER
//////////////////////////////////////////////////////////////////////
//  File: EnergyCluster.hpp
//
//  Purpose: contains a list of adresses to items collected as a cluster
//           and the sum of their 4-momenta and em Energy
//  All methods of this class are inline
//  Only EnergyClusterCollection can give an id to an EnergyCluster object
//
//  Created: 3-APR-1998  Serban Protopopescu
//  Modified: 6-Nov-1998 use AnglesUtil
//             6-SEP-1999 use LinkIndex
//             4-NOV-1999 store members in vector rather than list
//            23-JAN-2001 add isolation members, they do not contribute to 4-momenta
//            15-Sep-2009 Lars Sonnenschein
//            extracted from D0 software framework and modified to remove subsequent dependencies
//
//////////////////////////////////////////////////////////////////////  
#include <vector>
#include <list>
//#include "kinem_util/AnglesUtil.hpp"
//#include "edm/LinkIndex.hpp"
//#include "edm/LinkIndexUtils.hpp"
#include <iostream>

#include "../inline_maths.h"

namespace d0runi {

template <class T> class EnergyClusterCollection;
template <class T> class EnergyCluster;

template <class T>
std::ostream& operator<< (std::ostream& os, const EnergyCluster<T> &y);


template <class T>
class EnergyCluster{

  friend class EnergyClusterReco;
  friend class EnergyClusterCollection<T>;

 public:

  EnergyCluster();

  // construct energy cluster in one step
  // note that isolation must be added with addIsoItem
  EnergyCluster(const std::list<T> &tl, float sump[4], float sumEmE);
  EnergyCluster(const std::vector<T> &tl, float sump[4], float sumEmE);

  ~EnergyCluster();

  //   access methods


  float E() const;

  float emE() const;

  float isoE() const;

  float emisoE() const;

  float pT() const; 
 
  float phi() const;

  float eta() const;

  float theta() const;

  float p() const;

  //  return 4-momenta as an array
  void p4vec(float p[4]) const;

  //  returns members of cluster in a list container
  void members(std::list<T> &members)const;
  
  //  access vector of cluster members 
  const std::vector<T>& members()const;

  //  access vector of cluster isolation members 
  const std::vector<T>& isomembers()const;

  //  return cluster address (ie location in EnergyClusterCollection)
  int address()const;

  ////edm::LinkIndex<EnergyCluster<T> > index()const;

  ////void setLinkIndex(edm::ChunkID cid, int indx)const;

  // complete all Links
  ////void completeLinks(const edm::AbsChunk* c) const;

  //               output operator  
  friend std::ostream& operator<< <> (std::ostream& os, const EnergyCluster<T> &y);

  // I/O
  void print(std::ostream &os) const;

 private:

  //  private method addItem accessible via friend classes

  //  construction methods
  void addItem(T &t, const float p[4], const float &emE);

  //  construction methods
  void addIsoItem(T &t, const float &isoE, const float &emisoE);

  //   attributes
  float _E;
  float _px;
  float _py;
  float _pz;
  float _emE;
  std::vector<T> _members;
  float _isoE;
  float _emisoE;
  std::vector<T> _isomembers;
  ////#ifndef __CINT__
  ////mutable bool linksDone; //! not persistent
  ////mutable edm::LinkIndex<EnergyCluster<T> > _index; // ! not persistent
  ////#endif

};

//  inline implementation of methods
template <class T>
inline std::ostream&
operator<<(std::ostream& os, const EnergyCluster<T> &y){
  os<<" id (4-mom) (emE) = "<<y._index.id()<<" ("
    <<y._px<<", "<<y._py<<", "<<y._pz<<", "<<y._E<<")"<<"("<<y._emE<<")"
    <<std::endl<<" isolation (E, emE) =  ("<<y._isoE<<", "<<y._emisoE<<")"
    <<std::endl;
  return os;
}

template <class T>
inline
EnergyCluster<T>::EnergyCluster():
 _E(0), _px(0), _py(0), _pz(0), _emE(0), _isoE(0),_emisoE(0), _isomembers(){;}

template <class T>
inline
EnergyCluster<T>::
EnergyCluster(const std::vector<T> &tl, float sump[4], float sumEmE):
  _E(sump[3]), _px(sump[0]), _py(sump[1]), _pz(sump[2]), _emE(sumEmE),
  _members(tl), 
  _isoE(0),_emisoE(0), _isomembers(){;}

template <class T>
inline
EnergyCluster<T>::
EnergyCluster(const std::list<T> &tl, float sump[4], float sumEmE):
  _E(sump[3]), _px(sump[0]), _py(sump[1]), _pz(sump[2]), _emE(sumEmE),
  _isoE(0),_emisoE(0), _isomembers()
{

  typename std::list<T>::const_iterator iter;
  for(iter = tl.begin(); iter != tl.end(); ++iter){
    _members.push_back(*iter);
  }

}

template <class T>
inline
EnergyCluster<T>::~EnergyCluster(){;}

template <class T>
inline
float EnergyCluster<T>::E() const
{
  return _E;
}

template <class T>
inline
float EnergyCluster<T>::emE() const
{
  return _emE;
}

template <class T>
inline
float EnergyCluster<T>::isoE() const
{
  return _isoE;
}

template <class T>
inline
float EnergyCluster<T>::emisoE() const
{
  return _emisoE;
}

template <class T>
inline
float EnergyCluster<T>::pT() const
{
  return sqrt(_px*_px+_py*_py);
}

template <class T>
inline
float EnergyCluster<T>::phi() const
{
  //return kinem::phi(_px,_py);
  return inline_maths::phi(_px,_py);
} 

template <class T>
inline 
float EnergyCluster<T>::eta() const
{
  //return kinem::eta(_px,_py,_pz);
  return inline_maths::eta(_px,_py,_pz);
}

template <class T>
inline
float EnergyCluster<T>::theta() const
{
  //return kinem::theta(_px,_py,_pz);
  return inline_maths::theta(_px,_py,_pz);
}

template <class T>
inline
float EnergyCluster<T>::p() const
{
  return sqrt(_px*_px+_py*_py+_pz*_pz);
}

template <class T>
inline
void EnergyCluster<T>::p4vec(float p4v[4]) const
{
  p4v[0]=_px;
  p4v[1]=_py;
  p4v[2]=_pz;
  p4v[3]=_E;
}

////template <class T>
////inline
////edm::LinkIndex<EnergyCluster<T> > EnergyCluster<T>::index()const{
////  return _index;
////}

////template <class T>
////inline
////int EnergyCluster<T>::address()const{
////  return _index.id().index();
////}

template <class T>
inline
const std::vector<T>& EnergyCluster<T>::members()const{
    return _members;
}

template <class T>
inline
const std::vector<T>& EnergyCluster<T>::isomembers()const{
    return _isomembers;
}

template <class T>
inline
void EnergyCluster<T>::members(std::list<T> &members)const{
  typename std::vector<T>::const_iterator iter;
  for(iter = _members.begin(); iter != _members.end(); ++iter){
    members.push_back(*iter);
  }
}

////template <class T>
////inline
////void EnergyCluster<T>::setLinkIndex(edm::ChunkID cid, int indx)const{
////  _index=edm::LinkIndex<EnergyCluster<T> >(this,cid,indx);
////}

template <class T>
inline
void EnergyCluster<T>::print(std::ostream &os) const{

  os<<std::endl << " id (4-mom) (emE) = "////<<_index.id()
    <<" ("
    <<_px<<", "<<_py<<", "<<_pz<<", "<<_E<<")"<<"("<<_emE<<")"
    <<std::endl<<" isolation (E, emE) =  ("<<_isoE<<", "<<_emisoE<<")"
    <<std::endl;
    os<<" members= ";
  typename std::vector<T>::const_iterator i;
  for( i=_members.begin(); i != _members.end(); ++i){
    os<<(*i)<<" ";
  }
  os<<std::endl<<" isolation members= ";
  typename std::vector<T>::const_iterator iso;
  for( iso=_isomembers.begin(); iso != _isomembers.end(); ++iso){
    os<<(*iso)<<" ";
  }
  os<<std::endl;
}

//   private methods

template <class T>
inline
void EnergyCluster<T>::addItem(T &t, const float p4v[4], const float &emE){

  _members.push_back(t);
  _px+=p4v[0];
  _py+=p4v[1];
  _pz+=p4v[2];
  _E+=p4v[3];
  _emE+=emE;
}

template <class T>
inline
void EnergyCluster<T>::addIsoItem(T &t, const float &isoE, const float &emisoE){

  _isomembers.push_back(t);
  _isoE+=isoE;
  _emisoE+=emisoE;
}

////template <class T>
////inline
////void EnergyCluster<T>::completeLinks(const edm::AbsChunk* c) const{
////  finishUpLink(_index,c);
////}

#endif // INC_ENERGYCLUSTER

} //namespace d0runi
