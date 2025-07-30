#ifndef __TESTRECOMBINERS_HH__
#define __TESTRECOMBINERS_HH__

#include "TestBase.hh"
#include "fastjet/JetDefinition.hh"

class FlavourRecombiner : public  DefRecomb {
public:
  FlavourRecombiner(RecombinationScheme recomb_scheme = E_scheme) : 
    DefRecomb(recomb_scheme) {};

  virtual std::string description() const {
    return DefRecomb::description()+" (with user index addition)";}

  /// recombine pa and pb and put result into pab
  virtual void recombine(const PseudoJet & pa, const PseudoJet & pb, 
                         PseudoJet & pab) const {
    DefRecomb::recombine(pa,pb,pab);
    // Note: see the above discussion for the fact that we consider
    // negative user indices as "0"
    pab.set_user_index(max(pa.user_index(),0) + max(pb.user_index(),0));
  }
};


/// class to test some things that happen with Groomers and Recombiners
/// put together
class TestRecombiners : public TestBase {
  std::string short_name()  const {return "TestRecombiners";}

  virtual bool run_test () {
    double R = 1.0;
    JetDefinition jd1(antikt_algorithm, R);

    PseudoJet a = PtYPhiM(100.0, 0, 0,    1.0);
    PseudoJet b = PtYPhiM(50.0,  0, pi/4, 1.0);
    
    jd1.set_recombination_scheme(BIpt_scheme);
    PseudoJet c;
    jd1.recombiner()->recombine(a, b, c);
    verify_almost_equal(c.phi(), pi/12.0, "BIpt_scheme phi");
    verify_equal(c.user_index(), -1, "default user index");

    // now test copying of default recombiner
    JetDefinition jd2(antikt_algorithm, R/2);
    jd2.set_recombiner(jd1);

    verify_equal(jd1.recombination_scheme(), jd2.recombination_scheme(), 
                 "copy of recombination scheme");
    
    // and then try a new recombiner
    jd1.set_recombiner(new FlavourRecombiner);
    jd1.delete_recombiner_when_unused();
    a.set_user_index(3);
    b.set_user_index(2);
    jd2.set_recombiner(jd1);
    jd2.recombiner()->recombine(a, b, c);
    verify_equal(c.user_index(), 5, "FlavourRecombiner (copied) user index");

    // additional tests of the WTA recombination schemes
    jd1.set_recombination_scheme(WTA_pt_scheme);
    a = PtYPhiM(100.0, 0, pi/4, 1.0);
    b = PtYPhiM( 50.0, 0,    0, 2.0);
    jd1.recombiner()->recombine(a, b, c);
    verify_almost_equal(c.pt(),  150.0, "WTA_pt_scheme pt");
    verify_almost_equal(c.rap(),   0.0, "WTA_pt_scheme y");
    verify_almost_equal(c.phi(),  pi/4, "WTA_pt_scheme phi");
    verify_almost_equal(c.m(),     1.0, "WTA_pt_scheme m");

    a.reset_momentum(120.0, 50.0,  0.0, 200.0);
    b.reset_momentum( 40.0,  0.0, 30.0,  60.0);

    //jd1.set_recombination_scheme(WTA_E_scheme);
    //jd1.recombiner()->recombine(a, b, c);
    //verify_almost_equal(c.E(),   260.0,   "WTA_E_scheme pt");
    //verify_almost_equal(c.eta(), a.eta(), "WTA_E_scheme y");
    //verify_almost_equal(c.phi(), a.phi(), "WTA_E_scheme phi");
    //verify_almost_equal(c.m(),   a.m(),   "WTA_E_scheme m");

    jd1.set_recombination_scheme(WTA_modp_scheme);
    jd1.recombiner()->recombine(a, b, c);
    verify_almost_equal(c.modp(),180.0,   "WTA_modp_scheme pt");
    verify_almost_equal(c.eta(), a.eta(), "WTA_modp_scheme y");
    verify_almost_equal(c.phi(), a.phi(), "WTA_modp_scheme phi");
    verify_almost_equal(c.m(),   a.m(),   "WTA_modp_scheme m");

    return _pass_test;
  }
};
#endif // __TESTRECOMBINERS_HH__
