#ifndef __TESTTHREADSBASE_HH__
#define __TESTTHREADSBASE_HH__
#include <thread>
#include <sstream>
#include "TestBase.hh"
#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/Pruner.hh"
#include "fastjet/tools/GridMedianBackgroundEstimator.hh"
#include "fastjet/tools/JetMedianBackgroundEstimator.hh"
#include "fastjet/tools/Subtractor.hh"

using namespace std;
using namespace fastjet;



template<class R>
void thread_run_test(R * test, unsigned itest) {
  test->run_test_i(itest);
}

/// a class to help with thread tests;
///
/// It is to be templated with a subclass of ThreadedTestBase, creates
/// two copies of the template class, one which executes a series of
/// tests sequentially, the other which executes them in a set of
/// threads. It then compares the results.
template<class R>
class TestThread : public TestBase {

public:
  // allow this class to pass parameters to the constructor
  // of the underlying R class, via pack expansion
  template<class ... Types>
  TestThread(Types... args_R) : sequential(args_R...), threaded(args_R...) {}
  /// descriptions are taken from the template class
  std::string description() const {return threaded.description();}
  std::string short_name()  const {return threaded.short_name();}

  bool run_test() {
    
    bool outcome = true;


    unsigned i_round = 0;
    cout << " " << flush;
    while (true) {

      // first establish if we will run this round
      bool thr_OK = threaded  .prepare_round(i_round);
      bool seq_OK = sequential.prepare_round(i_round);
      assert(seq_OK == thr_OK);
      if (not seq_OK) break;

      threaded  .reset_result();
      sequential.reset_result();

      // then figure out how many threads we will want
      unsigned n = sequential.n_threads();

      // first do the threaded part
      cout << "t" << flush;
      vector<unique_ptr<thread>> threads;
      for (unsigned i = 0; i < n; i++) {
        threads.emplace_back(make_unique<thread>(thread_run_test<R>, &threaded, i));
      }
      for (unsigned i = 0; i < n; i++) {
        threads[i]->join();
      }

      // then run the sequential test
      cout << "s" << flush;
      for (unsigned i = 0; i < n; i++) {
        thread_run_test<R>(&sequential, i);
      }

      // finally check the results are in agreement
      cout << "v" << flush;
      for (unsigned i = 0; i < n; i++) {
        ostringstream ostr;
        ostr << short_name() << ": size of result from thread " << i;
        outcome &= verify_equal(sequential.result()[i].size(), 
                                threaded.result()[i].size(), ostr.str());
        for (unsigned j = 0; j < sequential.result()[i].size(); j++) {
          ostringstream ostr2;
          ostr2 << ostr.str() << ", value " << j;
          // last argument (true) tells verify_almost_equal to ignore 
          // structure info in its test
          outcome &= verify_almost_equal(sequential.result()[i][j], 
                        threaded.result()[i][j], ostr2.str(), -1 , true);
        }
      }
      i_round += 1;
    }
    return outcome;
  }

protected:
  R sequential;
  R threaded;
  /// stores the result of running in a thread-safe manner
  vector<vector<R> > _result;
  int _nrepeat = 1;
};

//--------------------------------------------------------------------
/// Base class for threaded tests; it provides
///
/// - tools to load events
/// - a function run_test_i(i) to run test i
///   (the TestThread class will run this sequentially on one 
///   copy of the class and in parallel on the other copy)
/// - storage for the outcome of the test (_result)
///
/// The class is templated according to the type of the underlying
/// results, and that type should be supported by the TestThread class
/// (double or PseudoJet) 
template<class S>
class ThreadedTestBase {
public:
  ThreadedTestBase(unsigned n = 0) {_result.resize(n);}
  void set_n_threads(unsigned n) {_result.resize(n);}
  virtual ~ThreadedTestBase() {}

  /// this is the critical part that the user needs to implement
  /// (together with the constructor))
  virtual void run_test_i(unsigned i) = 0;

  /// The TestThread class will try things on increasing rounds
  /// (each with an incremented index j) until this function
  /// returns false. Many classes won't need to overload this and
  /// will run a single round. But it provides the functionality
  /// for multiple rounds where needed...
  virtual bool prepare_round(unsigned j) {return j == 0;}

  /// empty out the results vector. Intended for use ahead of each new round
  void reset_result() {
    for (vector<S> & r: _result) {r.resize(0);}
  }

  /// default short name is the class name (this will take on the
  /// derived class name, albeit in its mangled form)
  virtual std::string short_name()  const {return typeid(*this).name();}
  /// one can include a more detailed description
  virtual std::string description() const {return short_name();}

  /// the number of threads that this is meant to be run across
  unsigned int n_threads() const {return result().size();}

  /// access to the results
  const vector<vector<S> > & result() const {return _result;}

  /// returns the event corresponding to the given filename
  void load_event(const string & filename) {
    ifstream istr(filename.c_str());
    double px, py , pz, E;
    vector<PseudoJet> input_particles;
    while (istr >> px >> py >> pz >> E) {
      // create a fastjet::PseudoJet with these components and put it onto
      // back of the input_particles vector
      input_particles.push_back(fastjet::PseudoJet(px,py,pz,E)); 
      input_particles.back().set_user_index(input_particles.size()-1);
    }
    _events.push_back(input_particles);
  }

  /// loads up to max events from filename
  void load_events(const string & filename, int max=-1) {
    ifstream istr(filename.c_str());
    vector<PseudoJet> input_particles;
    string line;
    int iev = 0;
    double px, py , pz, E;
    while (getline(istr,line)) {
      if (line =="#END") {
        _events.push_back(input_particles);
        input_particles.resize(0);
        ++iev;
        if (iev == max) return;
      }
      if (line.substr(0,1) == "#") {continue;}
      istringstream linestream(line);
      linestream >> px >> py >> pz >> E;
      input_particles.push_back(fastjet::PseudoJet(px,py,pz,E)); 
      input_particles.back().set_user_index(input_particles.size()-1);
    }
    if (input_particles.size() > 0) _events.push_back(input_particles);
  }


  //----------------------------------------------------
  void load_default_event() {
    return load_event("../example/data/single-event.dat");
  }

  /// loads the default 10 events
  void load_default_10events() {
    return load_events("../example/data/Pythia-PtMin1000-LHC-10ev.dat");
  }


protected:
  vector<vector<S> > _result;
  vector<vector<PseudoJet>> _events;
};


//-------------------------------------------------------------
/// just generates a banner; we can't explicitly test the outcome
/// of this, but when running the code we'll look to see
/// how many times the banner comes out...
class ThreadedBanner : public ThreadedTestBase<double> {
public:
  ThreadedBanner() : ThreadedTestBase<double>(8) {
  }

  //std::string short_name() const {return typeid(*this).name();}

  void run_test_i(unsigned i) {
    ClusterSequence::print_banner();
  }
};


//-------------------------------------------------------------

/// check thread-safety of warnings output;
///
/// There are two aspects to testing this:
///
///     1. that it does not crash
///     2. that the output comes out identical
///
/// Unfortunately, 2 isn't the case, because the "(LAST SUCH WARNING)"
/// text does not come out in the same location
class ThreadedWarning : public ThreadedTestBase<string> {
public:
  ThreadedWarning() : ThreadedTestBase<string>(8) {
    // send output to a place that we ignore (at least for now)
    // (but you can replace _ostr with _cerr to see what the 
    // output looks like)
#ifdef FASTJET_HAVE_LIMITED_THREAD_SAFETY
    LimitedWarning::set_default_stream_and_mutex(&_ostr, &_mutex);
#endif
  }

  //std::string short_name() const {return typeid(*this).name();}

  void run_test_i(unsigned i) {
    _warning.warn("test warning for threading tests");
  }  

  std::ostringstream _ostr;
  LimitedWarning _warning;
#ifdef FASTJET_HAVE_LIMITED_THREAD_SAFETY
  std::mutex _mutex;
#endif
};

class ThreadedError : public ThreadedTestBase<string> {
public:
  ThreadedError() : ThreadedTestBase<string>(8) {
    // send output to a place that we ignore (at least for now)
    // (but you can replace _ostr with _cerr to see what the 
    // output looks like)
#ifdef FASTJET_HAVE_LIMITED_THREAD_SAFETY
    Error::set_default_stream_and_mutex(&_ostr, &_mutex);    
#endif
  }

  void run_test_i(unsigned i) {
    try {
      throw Error("test error for threading checks");
    } catch (const Error & error) {}
  }  

  std::ostringstream _ostr;
  Error _error;
#ifdef FASTJET_HAVE_LIMITED_THREAD_SAFETY
  std::mutex _mutex;
#endif
};


//-------------------------------------------------------------
/// since rap and phi have cached calculations, this test
/// checks that if we evaluate them in separate threads 
/// we get the same answers
class ThreadedTestPhiRap : public ThreadedTestBase<double> {
public:

  ThreadedTestPhiRap() : ThreadedTestBase<double>(8) {
    load_default_10events();
  }

  bool prepare_round(unsigned j) override {
    if (j >= _events.size()) return false;
    _event = &_events[j];
    return true;
  }

  void run_test_i(unsigned i) override {
    _result[i].reserve(_event->size() * 4);
    for (const auto & j: *_event) {
      _result[i].push_back(j.phi());
      _result[i].push_back(j.rap());
      _result[i].push_back(j.phi());
      _result[i].push_back(j.rap()); 
    }
  } 
protected:
  const vector<PseudoJet> * _event;
};


//-------------------------------------------------------------
/// relative to ThreadedTestPhiRap alternative order
/// of rap and phi extractions
class ThreadedTestRapPhi : public ThreadedTestPhiRap {
public:

  void run_test_i(unsigned i) override {
    _result[i].reserve(_event->size() * 4);
    for (const auto & j: *_event) {
      _result[i].push_back(j.rap()); 
      _result[i].push_back(j.phi());
      _result[i].push_back(j.rap());
      _result[i].push_back(j.phi());
    }
  } 
};

//-------------------------------------------------------------
/// Test clustering with multiple jet definitions on one original event
class ThreadedClustering1EvManyR : public ThreadedTestBase<PseudoJet> {
public:

  ThreadedClustering1EvManyR() : _R_values{0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0} {
    set_n_threads(_R_values.size());
    load_default_event();
  }

  void run_test_i(unsigned i) {
    JetDefinition jet_def(antikt_algorithm, _R_values[i]);
    ClusterSequence cs(_events[0], jet_def);
    _result[i] = cs.inclusive_jets();
  } 

protected:
  vector<double> _R_values;
};

// //-------------------------------------------------------------
// /// Test clustering with each thread extracting jets from a common
// /// underlying ClusterSequence, which should automatically delete
// /// itself
// class ThreadedClustering1EvCommonCS : public ThreadedTestBase<PseudoJet> {
// public:
// 
//   ThreadedClustering1EvCommonCS() {
//     set_n_threads(3);
//     load_default_event();
//     JetDefinition jet_def(antikt_algorithm, 0.4);
//     _jets = jet_def(_events[0]);
//     //cs.reset(new ClusterSequence(_events[0], jet_def));
//   }
// 
//   void run_test_i(unsigned i) {
//     //_result[i] = cs->inclusive_jets();
//     _result[i] = _jets;
//   } 
// 
// protected:
//   
//   vector<PseudoJet> _jets;
//   //unique_ptr<ClusterSequence> cs;
// };


//-------------------------------------------------------------
/// Test clustering with each thread extracting jets from a common
/// underlying ClusterSequence, which should automatically delete
/// itself; this one seems to work non non-thread-safe versions, whereas
/// the logically similar  parallel groomer below fails.
class ThreadedClustering1EvCommonCS : public ThreadedTestBase<double> {
public:

  ThreadedClustering1EvCommonCS() {
    set_n_threads(8);
    load_default_10events();
    //load_default_event();
    //JetDefinition jet_def(antikt_algorithm, 0.4);
    //vector<PseudoJet> jets = jet_def(_events[0]);
    //_jets.resize(n_threads());
    //for (unsigned i = 0; i < n_threads(); i++) {
    //  _jets[i] = jets;
    //}
    //cs.reset(new ClusterSequence(_events[0], jet_def));
  }

  bool prepare_round(unsigned j) override {
    if (j >= _events.size()) return false;

    JetDefinition jet_def(antikt_algorithm, 0.4);
    vector<PseudoJet> jets = jet_def(_events[j]);
    _jets.resize(n_threads());
    for (unsigned i = 0; i < n_threads(); i++) {
      _jets[i] = jets;
    }
    return true;
  }

  void run_test_i(unsigned i) override {
    //_result[i] = cs->inclusive_jets();
    for (const PseudoJet & j: _jets[i]) {
      _result[i].push_back(j.pt());
    }
    _jets[i].resize(0);
  } 

protected:
  
  vector<vector<PseudoJet>> _jets;
  //unique_ptr<ClusterSequence> cs;
};


//-------------------------------------------------------------
/// Test clutering with the same jet definition across many events
class ThreadedClustering10Ev : public ThreadedTestBase<PseudoJet> {
public:

  ThreadedClustering10Ev()  {
    load_default_10events();
    set_n_threads(_events.size());
  }

  void run_test_i(unsigned i) {
    ClusterSequence cs(_events[i], _jet_def);
    _result[i] = cs.inclusive_jets();
  } 

  JetDefinition _jet_def{antikt_algorithm, 0.4};

protected:
};

//-------------------------------------------------------------
/// Test clutering with the same jet definition across many events
/// and get ghosted areas
class ThreadedClustering10EvAreas : public ThreadedTestBase<double> {
public:

  ThreadedClustering10EvAreas(AreaDefinition area_def) : _area_def(area_def) {
    load_default_10events();
    //load_default_event();
    set_n_threads(_events.size());
  }

  std::string short_name()  const override {
    string area_desc = _area_def.description();
    size_t max_len = 15;
    string short_area_desc = area_desc.substr(0,min(max_len,area_desc.size()));
    return string(typeid(*this).name())
     + " "+ short_area_desc + "...";
  }


  void run_test_i(unsigned i) override {
#ifdef FASTJET_HAVE_THREAD_SAFETY
    vector<int> seed{int(12345+i), int(67890-i*i)};
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def.with_fixed_seed(seed));
#else
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def);
#endif 
    auto jets = sorted_by_pt(cs.inclusive_jets());
    for (const auto & jet: jets) {
      _result[i].push_back(jet.area());
    }
  } 

protected:

  JetDefinition _jet_def{antikt_algorithm, 0.4};
  AreaDefinition _area_def;

};

///-------------------------------------------------------------
/// Test clutering with the same jet definition across many events
/// and get ghosted areas: in this "Alt" case we are mainly testing
/// that the default area usage (with the global random number
/// generator) is safe, in that it doesn't cause hangs or crashes; for
/// the area results themselves, we simply take the two hardest jets and
/// look at the nearest integer to area/(pi R^2)
class ThreadedClustering10EvAreasGlobalRand : public ThreadedClustering10EvAreas {
public:

  ThreadedClustering10EvAreasGlobalRand(AreaDefinition area_def) : ThreadedClustering10EvAreas(area_def) {}


  void run_test_i(unsigned i) {
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def);
    auto jets = SelectorNHardest(2)(sorted_by_pt(cs.inclusive_jets()));
    for (const auto & jet: jets) {
      int int_area_result = int( jet.area()/ (pi*pow(_jet_def.R(),2)) + 0.5);
      _result[i].push_back(int_area_result);
    }
  } 

protected:

  JetDefinition _jet_def{antikt_algorithm, 0.4};
  AreaDefinition _area_def;

};


//---------------------------------------------------------
/// this is intended to carry out the same test as supplied
/// by Chris Delitzsch and ATLAS colleagues; note that it 
/// does not always crash: there is some system-based
/// randomness
class ThreadedClusteringPrllGroomers : public ThreadedTestBase<double> {

public:
  ThreadedClusteringPrllGroomers() {
    double Rfilt = 0.3;
    unsigned int nfilt = 3;
    _groomers.emplace_back(std::make_unique<Filter>(JetDefinition(cambridge_algorithm, Rfilt), 
                                                    SelectorNHardest(nfilt) ) );

    double Rtrim = 0.2;
    double ptfrac = 0.03;
    _groomers.emplace_back(std::make_unique<Filter>(JetDefinition(kt_algorithm, Rtrim), 
                                                    SelectorPtFractionMin(ptfrac) ) );

    double zcut = 0.1;
    double rcut_factor = 0.5;
    _groomers.emplace_back(std::make_unique<Pruner>(cambridge_algorithm, zcut, rcut_factor));
    
    set_n_threads(_groomers.size());
    //load_default_event();
    //_jets = jet_def(_events[0]);
    //cs.reset(new ClusterSequence(_events[0], jet_def));
    load_default_10events();
    JetDefinition jet_def(antikt_algorithm, 1.0);
    for (const auto & event: _events) {
      vector<PseudoJet> jets = jet_def(event);
      for (const PseudoJet & j: jets) {_jets.push_back(j);}
    }
  }

  void run_test_i(unsigned i) {
    //_result[i] = cs->inclusive_jets();
    for (const PseudoJet & j: _jets) {
      auto groomed = (*_groomers[i])(j);
      _result[i].push_back(groomed.pt());
    }
  } 

protected:
  vector<PseudoJet> _jets;
  vector<unique_ptr<Transformer> > _groomers;
};

/// class to try out GridMedianBGE, taking a copy for local use within
/// the thread
class ThreadedGMBGE : public ThreadedTestBase<PseudoJet> {
public:
  ThreadedGMBGE() {
    load_default_10events();
    set_n_threads(_events.size());
  }

  void run_test_i(unsigned i) {
#ifdef FASTJET_HAVE_THREAD_SAFETY
    vector<int> seed{int(12345+i), int(67890-i*i)};
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def.with_fixed_seed(seed));
#else
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def);
#endif 
    vector<PseudoJet> jets = cs.inclusive_jets();
    GridMedianBackgroundEstimator gmbge(_gmbge);
    gmbge.set_particles(_events[i]);
    Subtractor subtractor(&gmbge);
    subtractor.set_use_rho_m(true);
    vector<PseudoJet> subtracted_jets = subtractor(jets);
    _result[i] = subtracted_jets;
  } 

private:
  JetDefinition  _jet_def{cambridge_algorithm, 1.0};
  AreaDefinition _area_def{active_area_explicit_ghosts};
  GridMedianBackgroundEstimator _gmbge{-5.0, 5.0, 1.0, 1.0};
};

/// class to try out JetMedianBGE, taking a copy for local use within
/// the thread
class ThreadedJMBGE : public ThreadedTestBase<PseudoJet> {
public:
  ThreadedJMBGE() {
    load_default_10events();
    set_n_threads(_events.size());
  }

  void run_test_i(unsigned i) {
#ifdef FASTJET_HAVE_THREAD_SAFETY
    vector<int> seed{int(12345+i), int(67890-i*i)};
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def.with_fixed_seed(seed));
#else
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def);
#endif 
    // only examine jets up to c. 4 to avoid warnings with jets
    // outside the region where rho can be estimated reliably (since our
    // JMBGE definition uses a dynamic selector to choose the set of jets)
    vector<PseudoJet> jets = SelectorAbsRapMax(4.0)(cs.inclusive_jets());
    // use a copy of the jmbge
    JetMedianBackgroundEstimator jmbge(_jmbge);
    jmbge.set_cluster_sequence(cs);
    Subtractor subtractor(&jmbge);
    subtractor.set_use_rho_m(true);
    //for (const PseudoJet & j: jets) {
    //  cout << j.rap() << " " << jmbge.rho(j) << endl;
    //}
    vector<PseudoJet> subtracted_jets = subtractor(jets);
    _result[i] = subtracted_jets;
  } 

private:
  JetDefinition  _jet_def{cambridge_algorithm, 0.5};
  AreaDefinition _area_def{active_area_explicit_ghosts};
  JetMedianBackgroundEstimator _jmbge{SelectorStrip(1.5)};
};


/// class to try out JetMedianBGE, taking a copy for local use within
/// the thread
class ThreadedBGEBase : public ThreadedTestBase<PseudoJet> {
public:
  ThreadedBGEBase(BackgroundEstimatorBase * bge) : _bge(bge) {
    load_default_10events();
    set_n_threads(_events.size());
  }

  virtual std::string short_name()  const {
    return string(typeid(*this).name())+"+"+string(typeid(*_bge).name());
  }

  void run_test_i(unsigned i) {
#ifdef FASTJET_HAVE_THREAD_SAFETY
    unique_ptr<BackgroundEstimatorBase> bge(_bge->copy());
    vector<int> seed{int(12345+i), int(67890-i*i)};  
    bge->set_particles_with_seed(_events[i], seed);
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def.with_fixed_seed(seed));
#else
    BackgroundEstimatorBase * bge = _bge;
    bge->set_particles(_events[i]);
    ClusterSequenceArea cs(_events[i], _jet_def, _area_def);
#endif 
    // only examine jets up to c. 4 to avoid warnings with jets
    // outside the region where rho can be estimated reliably (since our
    // JMBGE definition uses a dynamic selector to choose the set of jets)
    vector<PseudoJet> jets = SelectorAbsRapMax(4.0)(cs.inclusive_jets());
    // use a copy of the jmbge
    Subtractor subtractor(&*bge);
    subtractor.set_use_rho_m(true);
    //for (const PseudoJet & j: jets) {
    //  cout << j.rap() << " " << jmbge.rho(j) << endl;
    //}
    vector<PseudoJet> subtracted_jets = subtractor(jets);
    _result[i] = subtracted_jets;
  } 

private:
  BackgroundEstimatorBase * _bge;
  JetDefinition  _jet_def{cambridge_algorithm, 0.5};
  AreaDefinition _area_def{active_area_explicit_ghosts};
  JetMedianBackgroundEstimator _jmbge{SelectorStrip(1.5)};
};


/// class to try out JetMedianBGE, taking a copy for local use within
/// the thread
class ThreadedJMBGECommonEvent : public ThreadedTestBase<PseudoJet> {
public:
  ThreadedJMBGECommonEvent() : _subtractor(&_jmbge) {
    load_default_10events();
    set_n_threads(8);
    _subtractor.set_use_rho_m(true);
  }

  virtual bool prepare_round(unsigned j) {
    if (j >= _events.size()) return false;
#ifdef FASTJET_HAVE_THREAD_SAFETY
    vector<int> seed{int(12345+j), int(67890-j*j)};
    _cs.reset(new ClusterSequenceArea(_events[j], _jet_def, _area_def.with_fixed_seed(seed)));
#else 
    _cs.reset(new ClusterSequenceArea(_events[j], _jet_def, _area_def));
#endif
    _jmbge.set_cluster_sequence(*_cs);
    _jets = SelectorAbsRapMax(4.0)(_cs->inclusive_jets());
    return true;
  }

  void run_test_i(unsigned i) {
    _result[i] = _subtractor(_jets);
  } 

private:
  vector<PseudoJet> _jets;
  unique_ptr<ClusterSequenceArea> _cs;
  JetDefinition  _jet_def{cambridge_algorithm, 0.5};
  AreaDefinition _area_def{active_area_explicit_ghosts};
  JetMedianBackgroundEstimator _jmbge{SelectorStrip(1.5)};
  //JetMedianBackgroundEstimator _jmbge{SelectorAbsRapMax(2.5)};
  Subtractor _subtractor;
};


//-------------------------------------------------------------
/// Test PseudoJet reset_momentum
///
/// Test designed to check caching of phi in PseudoJet after
/// reset_momentum (specifically the bug discovered on 2023-02-14 where
/// the cached status of phi was not updated after reset_momentum when
/// threading was enabled)
class ThreadedPseudoJetResetMomB : public ThreadedTestBase<double> {
public:
  ThreadedPseudoJetResetMomB()
    : _nthreads(10) {
    set_n_threads(_nthreads);
  }

  bool prepare_round(unsigned j) FASTJET_OVERRIDE {
    if (j < _nrounds) {
      _pj_ptr.reset(new PseudoJet(3,4,0,5));
      return true;
    } else {
      return false;
    }
  }

  std::string short_name()  const override {
    return "PseudoJetResetMomB";
  }

  void run_test_i(unsigned i) override {
    if (i==_nthreads-1){
      _result[i] = {_pj_ptr->phi()};
      return;
    }
    PseudoJet j(1,0,0,1);
    // force evaluation of j's phi (put into result[i] to
    // minimise change of compiler warning)
    //_result[i] = {j.phi()};
    if (i%2 == 0) _result[i] = {j.phi()};
    j.reset_momentum(*_pj_ptr);  //< this is the operation we want to test
    _result[i] = {j.phi()};
  } 

protected:
  const unsigned int _nthreads;
  const unsigned int _nrounds = 300;
  std::unique_ptr<PseudoJet> _pj_ptr;
};

//-------------------------------------------------------------
/// Test PseudoJet assignment
///
/// Test designed to check PseudoJet phi evaluation after assignment,
/// specifically the bug discovered on 2023-02-14 where the status of
/// the phi calculation could be copied as being in progress, which
/// would then lead to an infinite loop in the copy's phi evaluation
class ThreadedPseudoJetAssignment : public ThreadedPseudoJetResetMomB  {
public:
  ThreadedPseudoJetAssignment() : ThreadedPseudoJetResetMomB() {}

  std::string short_name()  const override {
    return "PseudoJetAssignment";
  }

  void run_test_i(unsigned i) override {
    if (i==0){
      _result[0] = {_pj_ptr->phi()};
      return;
    }
    // create a new PseudoJet 
    PseudoJet j(1,0,0,1);
    if (i%2 == 0) _result[i] = {j.phi()};
    j = *_pj_ptr; //< this is the operation we want to test
    _result[i] = {j.phi()};
  } 
};


#endif // __TESTTHREADSBASE_HH__
