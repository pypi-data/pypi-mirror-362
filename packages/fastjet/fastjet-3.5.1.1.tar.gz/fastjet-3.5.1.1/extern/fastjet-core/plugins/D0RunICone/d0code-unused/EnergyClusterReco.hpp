#ifndef INC_ENERGYCLUSTERRECO
#define INC_ENERGYCLUSTERRECO
///////////////////////////////////////////////////////////////////////////////
// File: EnergyClusterReco.hpp
//
// Purpose:   Base class for EnergyCluster reconstructors
//
// Created:    3-APR-1998  Serban Protopopescu
//
//   This class must be inherited by any reconstructor that makes
//   energy clusters. Its methods provide the only access to fill
//   EnergyCluster and EnergyClusterCollection objects inside an
//   energy cluster Chunk.
//   Reconstructor is expected to create a chunk C and then use:
//
//   EnergyClusterCollection<T>* createClusterCollection(C* ptr);
//   to create an energy cluster collection in C
//
//   EnergyCluster<T>* createCluster(EnergyClusterCollection<T>* ptr);     
//   to create an energy cluster in the collection      
//
//   addClusterItem(EnergyCluster<T> *cluster, A address,float *p, float emE);
//   to add information to a cluster
//
//   If a cluster is created outside the collection one can add it by
//   addCluster(EnergyClusterCollection<T> *collection,	
//              EnergyCluster<T> &cluster);
//
//   
// History:
//   15-Sep-2009 Lars Sonnenschein
//   extracted from D0 software framework and modified to remove subsequent dependencies

///////////////////////////////////////////////////////////////////////////////

// Dependencies (#includes)
#include "energycluster/EnergyClusterCollection.hpp"

using namespace edm;
using namespace std;
///////////////////////////////////////////////////////////////////////////////

namespace d0runi {

class EnergyClusterReco {
//class AbsEnergyClusterReco{

public:

// Constructors
// Reconstructors are instantiated by using an RCP object to fill in
// member data.
  EnergyClusterReco(){;}

// Execute method: generates chunks and puts in the Event
// must be implemented by derived class (pure virtual in AbsReco)
//void execute(Event& event) const;

// Returns list of chunks made in this reconstructor 
// empty of data, but not of ID info 
// must be implemented by derived class (pure virtual in AbsReco)
// std::list<RCPtr<AbsChunk> > creates() const;

// Returns true if chunks in list satisfy all keys in reconstructor
// must be implemented by derived class (pure virtual in AbsReco)
// bool satisfied(list<RCPtr<AbsChunk> > chlist) const;

// Destructor
  ~EnergyClusterReco(){;}

public:

  //  add one cluster item to an energy cluster
template<class T>
void addClusterItem(EnergyCluster<T> *cluster, T &item, const float *p, 
const float &emE)const;

  //  add one isolation item to an energy cluster
template<class T>
void addClusterIsoItem(EnergyCluster<T> *cluster, T &item, const float &E,
		       const float &emE)const;

  // add one energy cluster to an energy cluster collection
template<class T>
void addCluster(EnergyClusterCollection<T> *ptcol,
	EnergyCluster<T> &cluster)const;

  // interface to create an energy cluster collection in chunk C
template<class T, class C>
void createClusterCollection(C* ptC, EnergyClusterCollection<T>* &ptcol)const;

  // interface to create an energy cluster in a collection
template<class T>
void createCluster(EnergyClusterCollection<T>* ptcol, EnergyCluster<T>* &ptec)
const;

  // interface to remove an energy cluster in a collection
template<class T>
void removeCluster(EnergyClusterCollection<T>* ptcol)const;

private:
};

template<class T>
inline
void  EnergyClusterReco::addClusterItem(EnergyCluster<T>* ptec, 
	T &item, const float *p, const float &emE)const{
  ptec->addItem(item, p, emE);
}

template<class T>
inline
void  EnergyClusterReco::addClusterIsoItem(EnergyCluster<T>* ptec, 
	T &item, const float &E, const float &emE)const{
  ptec->addIsoItem(item, E, emE);
}

template<class T>
inline
void EnergyClusterReco::addCluster(EnergyClusterCollection<T> *ptcol,
	EnergyCluster<T> &cluster)const{
  ptcol->addCluster(cluster);
}

template<class T>
inline
void EnergyClusterReco::
createCluster(EnergyClusterCollection<T>* ptcol, EnergyCluster<T>* &ptec)const{
  ptcol->createCluster(ptec);
}

template<class T>
inline
void EnergyClusterReco::
removeCluster(EnergyClusterCollection<T>* ptcol)const{
  ptcol->removeCluster();
}


template<class T, class C>
inline 
void EnergyClusterReco::
createClusterCollection(C* ptC, EnergyClusterCollection<T>* &ptcol)const{
  ptC->createClusterCollection(ptcol);
}
								     

#endif // INC_ENERGYCLUSTERRECO

} //namespace d0runi
