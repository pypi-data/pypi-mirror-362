#ifndef INC_ENERGYCLUSTERCOLLECTION
#define INC_ENERGYCLUSTERCOLLECTION
///////////////////////////////////////////////////////////////////////////////
// File: EnergyClusterCollection.hpp
// 
// Purpose:   Container of energy clusters
//            an energy cluster is a list of labels with
//            4-vector and em energy
//            you can create the container giving it a list
//            of energy clusters or create it empty and fill
//            it one cluster at a time.
//            Only reconstructors inheriting AbsEnergyClusterReco
//            can modify contents of an existing collection.
//
// Created:   10-FEB-1998  Serban Protopopescu
// History:   add removeCluster(), allows deletion of last cluster
//          15-Sep-2009 Lars Sonnenschein
//          extracted from D0 software framework and modified to remove subsequent dependencies
///////////////////////////////////////////////////////////////////////////////
// Dependencies (#includes)

#include <iostream>
#include "energycluster/EnergyCluster.hpp"

///////////////////////////////////////////////////////////////////////////////

namespace edm{class AbsChunk;}

namespace d0runi {

template <class T>
class EnergyClusterCollection{

friend class EnergyClusterReco;

public:
    
  // Constructors
  EnergyClusterCollection();
  EnergyClusterCollection(std::vector<EnergyCluster<T> > &ecv);

  // destructor
  ~EnergyClusterCollection();

  //  return number of clusters in collection
  int nclusters()const;
#ifndef __CINT__
  // return vector of clusters
  void getClusters(std::vector<const EnergyCluster<T>*> &ecv) const;

  // return list of clusters
  void getClusters(std::list<const EnergyCluster<T>*> &ecl) const;

  // return refernce to a cluster given the index
  const EnergyCluster<T>& at(int index)const;
#endif
  int collectionID() const;

  void print(std::ostream &os) const;

  void doLinks(const edm::AbsChunk* c)const;

private:

  //  create an empty cluster and add to collection
  //  cluster should be filled using method EnergyCluster::addItem
   void createCluster(EnergyCluster<T>* &ptec);
  // use to allocate memory for vector (if known size)
  void reserve(int nsize);
  // add an existing cluster
  void addCluster(EnergyCluster<T> &t);
  // remove last cluster
  void removeCluster();

  std::vector<EnergyCluster<T> > _ecvector;
  int _nclusters;

};

template<class T>
inline
EnergyClusterCollection<T>::EnergyClusterCollection():_nclusters(0){;}

template<class T>
inline
EnergyClusterCollection<T>::
EnergyClusterCollection(std::vector<EnergyCluster<T> > &ecv){
  _ecvector=ecv;
  _nclusters=_ecvector.size();
}

template<class T>
inline
EnergyClusterCollection<T>::~EnergyClusterCollection(){;}

template<class T>
inline
const EnergyCluster<T>& EnergyClusterCollection<T>::
at(int index)const{
  return _ecvector[index];
}

template<class T>
inline
int EnergyClusterCollection<T>::nclusters()const{
  return _nclusters;
}

#ifndef __CINT__
template<class T>
inline
void EnergyClusterCollection<T>::getClusters(
			      std::vector<const EnergyCluster<T>*> &ecv)const{
  for(int i=0; i<_nclusters; i++){
    ecv.push_back(&_ecvector[i]);
  }
}

template<class T>
inline
void EnergyClusterCollection<T>::getClusters(
				std::list<const EnergyCluster<T>*> &ecl)const{
  for(int i=0; i<_nclusters; i++){
    ecl.push_back(&_ecvector[i]);
  }
}

////template<class T>
////inline
////void EnergyClusterCollection<T>::doLinks(const edm::AbsChunk* c)const{
////  for(int i=0; i<_nclusters; i++){
////    _ecvector[i].setLinkIndex(c->chunkID(),i);
////    _ecvector[i].completeLinks(c);
////  }
////}

#endif

//  private methods, must use reconstructor


template<class T>
inline
void EnergyClusterCollection<T>::reserve(int nsize){
  _ecvector.reserve(nsize);
}

template<class T>
inline
void EnergyClusterCollection<T>::createCluster(EnergyCluster<T>* &ptec){
  _ecvector.push_back(EnergyCluster<T>());
  ptec=&_ecvector[_nclusters];
  _nclusters++;
}

template<class T>
inline
void EnergyClusterCollection<T>::addCluster(EnergyCluster<T> &ec){
  _ecvector.push_back(ec);
  _nclusters++;
}

template<class T>
inline
void EnergyClusterCollection<T>::removeCluster(){
  _ecvector.pop_back();
  _nclusters--;
}

template<class T>
inline
void EnergyClusterCollection<T>::print(std::ostream &os) const{
  os<<std::endl<<"              Energy Cluster Collection "<<std::endl;
  for(int i=0; i<_nclusters; i++){
    _ecvector[i].print(os);
  }
}
#endif // INC_ENERGYCLUSTERCOLLECTION

} //namespace d0runi
