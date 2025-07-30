#ifndef __TESTBASE_HH__
#define __TESTBASE_HH__

#include "fastjet/PseudoJet.hh"
#include "fastjet/internal/BasicRandom.hh"
#include <iostream>
#include <sstream>
#include <fstream>

using namespace std;
using namespace fastjet;

//FASTJET_BEGIN_NAMESPACE      // defined in fastjet/internal/base.hh

//----------------------------------------------------------------------
/// Base class setting out the basic functionality that any test needs
/// to provide, and also including some helper functions
class TestBase {
public:
  TestBase() : _pass_test(true), _quiet_OK(false) {}
  virtual ~TestBase() {}

  virtual std::string description() const {return short_name();}
  virtual std::string short_name()  const = 0;
  virtual bool run_test() = 0;
  /// repeat the test multiple times
  virtual bool run_test(unsigned int n) {
    bool outcome = true;
    for (unsigned i = 0; i < n; i++) outcome &= run_test();
    return outcome;
  };

  /// a helper function to verify equality to within some specified
  /// tolerance, with the tolerance defined as a relative tolerance
  /// for large numbers (>>1) and an absolute tolerance for small
  /// numbers (<<1).
  bool almost_equal(double a, double b, double tol = -1.0) const {
    double local_tol = tol >= 0 ? tol : default_tolerance();
    return abs(a-b) <= local_tol*(1+max(abs(a),abs(b)));
  }

  /// verifies equality of two integers and registers failure if appropriate
  template<class T> bool verify_equal(const T & a, const T & b, const string & testname) {
    if (! (a == b)) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": " << a << " != " << b;
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }

  template<class T> bool verify_null(const T * a, const string & testname) {
    if (a != 0) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": " << a << " != null";
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }

  template<class T> bool verify_null(const T & a, const string & testname) {
    if (a != 0) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": " << a << " != null";
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }

  /// verify that a jet is 0 (though not necessarily equal to PseudoJet())
  bool verify_null(const PseudoJet & j, const string & testname) {
    if (j != 0) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": jet " << " != 0";
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }

  // /// verifies equality of two integers and registers failure if appropriate
  // void verify_equal(const void * a, const void * b, const string & testname) {
  //   if (a != b) {
  //     _pass_test = false;
  //     std::ostringstream ostr;
  //     ostr << testname << ": " << a << " != " << b;
  //     _failure_testnames.push_back(ostr.str());
  //   } else if (!_quiet_OK) {
  //     _OK_testnames.push_back(testname);
  //   }
  // }

  /// verifies equality of two integers and registers failure if appropriate
  template<class T> bool verify_different(const T & a, const T & b, const string & testname) {
    if (a == b) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": " << a << " == " << b;
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }


  /// verifies two things are equal within tolerance; if not it
  /// registers failure in the _pass_test
  bool verify_almost_equal(double a, double b, const string & testname, double tol = -1.0, 
                           bool dummy_ignore_structure = false) {
    if (!almost_equal(a,b,tol)) {
      _pass_test = false;
      std::ostringstream ostr;
      ostr << testname << ": " << a << " != " << b << " (within tol = " << tol << ")";
      _failure_testnames.push_back(ostr.str());
      return false;
    } else if (!_quiet_OK) {
      _OK_testnames.push_back(testname);
    }
    return true;
  }


  /// verifies two PseudoJets are equal within tolerance; if not it
  /// registers failure in the _pass_test
  bool verify_almost_equal(const PseudoJet & a, const PseudoJet b, 
			   const string & testname, double tol = -1.0,
			   bool ignore_structure = false) {

    // don't record all the individual tests below unless they fail
    _quiet_OK = true;

    bool pass = true;
    pass &= verify_almost_equal(a.px(), b.px(), testname+" (x)", tol);
    pass &= verify_almost_equal(a.py(), b.py(), testname+" (y)", tol);
    pass &= verify_almost_equal(a.pz(), b.pz(), testname+" (z)", tol);
    pass &= verify_almost_equal(a.E (), b.E (), testname+" (E)", tol);

    pass &= verify_almost_equal(a.perp(), b.perp(),  testname+"(pt )", tol);
    pass &= verify_almost_equal(a.rap() , b.rap() ,  testname+"(rap)", tol);
    pass &= verify_almost_equal(a.eta() , b.eta() ,  testname+"(eta)", tol);
    pass &= verify_almost_equal(a.phi() , b.phi() ,  testname+"(phi)", tol);
    pass &= verify_almost_equal(a.m2()  , b.m2()  ,  testname+"(m2 )", tol);

    pass &= verify_equal(a.user_index(), b.user_index(), testname+"(user index)");
    pass &= verify_equal(a.user_info_ptr(), b.user_info_ptr(), testname+"(user info ptr)");
    if (!ignore_structure) {
      pass &= verify_equal(a.cluster_hist_index(), b.cluster_hist_index(), testname+"(cluster hist index)");
      pass &= verify_equal(a.structure_ptr(), b.structure_ptr(), testname+"(structure ptr)");
    }
    _quiet_OK = false;
    if (pass) _OK_testnames.push_back(testname);
    return pass;
  }

  /// verifies two things are equal within tolerance; if not it
  /// registers failure in the _pass_test
  bool verify_equal(const PseudoJet & a, const PseudoJet b, const string & testname,
		    bool ignore_structure = false) {
    return verify_almost_equal(a,b,testname, 0.0, ignore_structure);
  }


  /// print a list of all the failures
  void print_failures(std::ostream & ostr = std::cout, unsigned max_print = 5) {
    for (unsigned i=0; i < min((unsigned int) _failure_testnames.size(), max_print); i++) {
      ostr << "           " << _failure_testnames[i] << endl;
    }
    if (_failure_testnames.size() > max_print) {
      ostr << "           ... and " << _failure_testnames.size() - max_print 
	   << " more failures ... " << endl;
    }
  }

  void print_OK(std::ostream & ostr = std::cout, unsigned max_print = 4000000000U) {
    for (unsigned i=0; i < min((unsigned int) _OK_testnames.size(), max_print); i++) {
      ostr << "           " << _OK_testnames[i] << endl;
    }
    if (_OK_testnames.size() > max_print) {
      ostr << "           ... and " << _OK_testnames.size() - max_print 
	   << " more OKs ... " << endl;
    }
  }

  /// a default tolerance to use when tolerances are not specified
  virtual double default_tolerance() const {
    return 1e-10;
  }


  /// return a random number in the range xmin to xmax
  double uniform_random(double xmin, double xmax) {return xmin + (xmax-xmin)*random();}

  /// return a sensible random PseudoJet
  PseudoJet random_PtYPhiM(double m = -1.0) {
    
    // range of pt values chosen affects choice for tolerance below
    double pt = uniform_random(1.0, 10.0);
    double rap = uniform_random(-5.0, 5.0);
    double phi = uniform_random(0.0, twopi);

    if (m < 0) m = uniform_random(40.0,10.0);
    return PtYPhiM(pt, rap, phi, m);
  }

  /// returns the event corresponding to the given filename
  vector<PseudoJet> get_event(const string & filename) const {
    ifstream istr(filename.c_str());
    double px, py , pz, E;
    vector<PseudoJet> input_particles;
    while (istr >> px >> py >> pz >> E) {
      // create a fastjet::PseudoJet with these components and put it onto
      // back of the input_particles vector
      input_particles.push_back(fastjet::PseudoJet(px,py,pz,E)); 
      input_particles.back().set_user_index(input_particles.size()-1);
    }
    return input_particles;
  }
  
  //----------------------------------------------------
  vector<PseudoJet> default_event() const {
    return get_event("../example/data/single-event.dat");
  }

protected:
  BasicRandom<double> random;
  
  bool _pass_test;
  std::vector<std::string> _failure_testnames;
  std::vector<std::string> _OK_testnames;
  bool _quiet_OK;
};


#define VERIFY_THROWS(CODE, MSG) {		\
    bool check = false;				\
    Error::set_print_errors(false);		\
    try {					\
      CODE ;					\
    } catch (const fastjet::Error & err) {	\
      check = true;				\
    }						\
    verify_equal(check, true, MSG );		\
    Error::set_print_errors(true);		\
  }


#define VERIFY_RUNS(CODE, MSG) {          \
  bool check = true;                      \
  try {                                   \
    CODE ;                                \
  } catch (const fastjet::Error & err) {  \
    check = false;                        \
  }                                       \
  verify_equal(check, true, MSG );	  \
  }

//FASTJET_END_NAMESPACE

#endif // __TESTBASE_HH__
