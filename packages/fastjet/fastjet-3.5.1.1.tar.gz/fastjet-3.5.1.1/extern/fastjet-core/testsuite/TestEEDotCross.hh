#ifndef __TESTEEDOTCROSS_HH__
#define __TESTEEDOTCROSS_HH__

#include "TestBase.hh"
#include "fastjet/tools/GridMedianBackgroundEstimator.hh"
#include "fastjet/GridJetPlugin.hh"


/// class to test how well we are doing on the evaluation of distances 
/// in the e+e- algorithms
class TestEEDotCross : public TestBase {
  std::string short_name()  const {return "TestEEDotCross";}

  virtual bool run_test () {


    // use a jet radius of pi/2 so that 1/(1-cosR) term in normalisation
    // is just one.
    // NB: these tests must be run with the N2PlainEEAccurate strategy
    // so as to ensure that distance calculations are carried out appropriately
    //JetDefinition jd(fastjet::ee_genkt_algorithm, pi/2, 0.0, E_scheme, N2PlainEEAccurate);
    JetDefinition jd(fastjet::ee_kt_algorithm, E_scheme, N2PlainEEAccurate);
    double norm = 2.0;

    // prepare some rotation matrices for use below
    double phi = 0.95, theta = 0.78;
    vector<vector<double> > rotmat_phi = {{ cos(phi), -sin(phi), 0},
                                          { sin(phi),  cos(phi), 0},
                                          {0, 0, 1}};
    vector<vector<double> > rotmat_theta = {{1,0,0},
                                            {0, cos(theta),-sin(theta)},
                                            {0, sin(theta), cos(theta)}};

    for (int i = 2; i < 11; i++) {
      
      // we will explore a range of small angles 
      double dtheta = pow(10,-i);

      // construct an event (and do the clustering) in a way that will
      // give a certain expected value for dtheta
      double expected_rtdij = sqrt(norm * 2*pow(sin(dtheta/2),2));
      PseudoJet j1 = PtYPhiM(1.0, 0.0, 0.0);
      PseudoJet j2 = PtYPhiM(1.0, 0.0, dtheta);
      vector<PseudoJet> event_a{j1,j2};
      ClusterSequence cs_a(event_a, jd);

      // when one of the momenta is aligned along an axis, as above,
      // then we should expect to have a relative rounding error that is
      // never larger than sqrt(epsilon) (this largest error occurs when
      // dmerge is of order sqrt(epsilon)). We include a margin factor
      // of 10 for safety.
      constexpr double epsilon = std::numeric_limits<double>::epsilon();
      double local_tolerance = 10 * sqrt(epsilon) * dtheta;

      // run the check
      verify_almost_equal(expected_rtdij, sqrt(cs_a.exclusive_dmerge(1)), 
                          "unrotated rtdmerge(1) check", local_tolerance);

      // now rotate the event so that we are not in a situation with
      // things aligned along any specific axes 
      vector<PseudoJet> event_b;
      for (const auto & j: event_a) {
        event_b.push_back(rotate(rotmat_theta,rotate(rotmat_phi,j)));
        //const auto & rj = event_b.back();
        //std::cout <<  j.px() << " " <<  j.py() << " " <<  j.pz() << " " <<  j.E() << std::endl;
        //std::cout << rj.px() << " " << rj.py() << " " << rj.pz() << " " << rj.E() << std::endl;
      }
      ClusterSequence cs_b(event_b, jd);


      // here, with momenta pointing arbitrarily in x,y,z, we design a
      // tolerance where we want to be accurate to within sqrt(epsilon)
      // times the value of the angle, but keeping in mind that we can
      // be no better than absolute epsilon (from the cross-product
      // evaluation of the distance); include a factor of 10 margin wrt
      // normal epsilon
      local_tolerance = 10 * std::max(epsilon, sqrt(epsilon) * dtheta);
      verify_almost_equal(expected_rtdij, sqrt(cs_b.exclusive_dmerge(1)), 
                          "rotated rtdmerge(1) check", local_tolerance);
    
    }
  
    
    return _pass_test;
  }

  PseudoJet rotate(const vector<vector<double>> & matrix, const PseudoJet & jet_in) const {
    vector<double> vec_out(4,0);
    for (unsigned i = 0; i < 3; i++) {
      for (unsigned j = 0; j < 3; j++) {
        vec_out[i] += matrix[i][j] * jet_in[j];
      }
    }
    vec_out[3] = jet_in.E();
    return PseudoJet(vec_out);
  }

};
#endif // __TESTEEDOTCROSS_HH__
