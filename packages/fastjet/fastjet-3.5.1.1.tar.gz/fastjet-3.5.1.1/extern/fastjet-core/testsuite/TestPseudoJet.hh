#ifndef __TESTPSEUDOJET_HH__
#define __TESTPSEUDOJET_HH__

/// \file TestPseudoJet.hh 
/// Provides a series of tests of PseudoJets

#include "TestBase.hh"
#include "fastjet/ClusterSequence.hh"


//----------------------------------------------------------------------
/// Class to test that assignments via PtYPhiM are being performed
/// correctly
class TestPtYPhiM : public TestBase {
  std::string short_name()  const {return "TestPtYPhiM";}

  bool run_test () {
    for (unsigned i = 0; i < 10; i++) {
      // range of pt values chosen affects choice for tolerance below
      double pt = uniform_random(1.0, 10.0);
      double rap = uniform_random(-5.0, 5.0);
      double phi = uniform_random(0.0, twopi);

      PseudoJet p = PtYPhiM(pt, rap, phi);
      verify_almost_equal(pt , p.perp(),  "pt test (m=0)");
      verify_almost_equal(rap, p.rap() ,  "rap test (m=0)");
      verify_almost_equal(phi, p.phi() ,  "phi test (m=0)");
      verify_almost_equal(0  , p.m()   ,  "m test (m=0)", 1e-5); // lower tolerance

      p += PseudoJet(1e-100,1e-100,1e-100,1e-100);
      verify_almost_equal(pt , p.perp(),  "2nd pt test (m=0)");
      verify_almost_equal(rap, p.rap() ,  "2nd rap test (m=0)");
      verify_almost_equal(phi, p.phi() ,  "2nd phi test (m=0)");
      verify_almost_equal(0  , p.m()   ,  "2nd m test (m=0)", 1e-5); // lower tolerance

      PseudoJet pp = p;
      pp = pp + PseudoJet(1e-100,1e-100,1e-100,1e-100);
      verify_almost_equal(p,pp, "usual addition");

      double m = uniform_random(1.0,10.0);
      p = PtYPhiM(pt, rap, phi, m); 
      verify_almost_equal(pt , p.perp(),  "pt test");
      verify_almost_equal(rap, p.rap() ,  "rap test");
      verify_almost_equal(phi, p.phi() ,  "phi test");
      verify_almost_equal(m  , p.m()   ,  "m test", 1e-5); // lower tolerance

      p += PseudoJet(1e-100,1e-100,1e-100,1e-100);
      verify_almost_equal(pt , p.perp(),  "2nd pt test");
      verify_almost_equal(rap, p.rap() ,  "2nd rap test");
      verify_almost_equal(phi, p.phi() ,  "2nd phi test");
      verify_almost_equal(m  , p.m()   ,  "2nd m test", 1e-5); // lower tolerance
    }
    return _pass_test;
  }
};

//----------------------------------------------------------------------
/// class to test that addition, etc. are all working sensibly
class TestPJOperations : public TestBase {
  std::string short_name()  const {return "TestPJOperations";}
  bool run_test () {
    for (unsigned i = 0; i < 10; i++) {
      // range of pt values chosen affects choice for tolerance below
      double pt1  = uniform_random(1.0, 10.0);
      double rap1 = uniform_random(-5.0, 5.0);
      double phi1 = uniform_random(0.0, twopi);
      double m1   = uniform_random(0.0, 5.0);

      double pt2  = uniform_random(1.0, 10.0);
      double rap2 = uniform_random(-5.0, 5.0);
      double phi2 = uniform_random(0.0, twopi);
      double m2   = uniform_random(0.0, 5.0);

      double factor = uniform_random(0.5, 1.5);

      // first check additions (and dot_product)
      PseudoJet p1 = PtYPhiM(pt1, rap1, phi1, m1);
      PseudoJet p2 = PtYPhiM(pt2, rap2, phi2, m2);

      PseudoJet p12_a = p1 + p2;
      PseudoJet p12_b = p1; p12_b += p2;
      verify_almost_equal(p12_a, p12_b, "+= v. +");
      verify_almost_equal(p12_a.m2(), p1.m2() + p2.m2() + 2*dot_product(p1,p2),
                          "(p1+p2).m2() v. explicit calculation of m2 with dot products");

      // then try subtractions
      p12_a = p1 - p2;
      p12_b = p1; p12_b -= p2;
      verify_almost_equal(p12_a, p12_b, "-= v. -");
      //p12_a = p1 + (-p2); // unary minus not supported...
      //verify_almost_equal(p12_a, p12_b, "p1 += p2 v. p1 + (-p2)");
      verify_almost_equal(p12_a.m2(), p1.m2() + p2.m2() - 2*dot_product(p1,p2),
                          "(p1-p2).m2() v. explicit calculation of m2 with dot products");
      
      // then multiplication
      PseudoJet pfact_a, pfact_b;
      pfact_a = factor * p1;
      pfact_b = p1; pfact_b *= factor;
      verify_almost_equal(pfact_a, pfact_b, "*= v. factor*p1");
      pfact_a = p1 * factor;
      verify_almost_equal(pfact_a, pfact_b, "*= v. p1*factor");
      verify_almost_equal(pfact_a.pt(), p1.pt()*factor, "(p1*factor).pt() == p1.pt()*factor");

      // then division
      pfact_a = p1 / factor;
      pfact_b = p1; pfact_b /= factor;
      verify_almost_equal(pfact_a, pfact_b, "/= v. p1/factor");
      verify_almost_equal(pfact_a.pt(), p1.pt()/factor, "(p1/factor).pt() == p1.pt()/factor");

      // then boost (& unboost)?
      PseudoJet p1copy = p1;
      p1copy.boost(p2);
      p1copy.unboost(p2);
      // this operation seems to need a looser tolerance (specifically for m2)
      verify_almost_equal(p1copy, p1, "p1copy.boost(p2).unboost(p2) == p1", 1e-6);

      // and check that rapidity comes out sensible with a longitudinal boost
      double delta_y = 2.0;
      PseudoJet myboost = PtYPhiM(0.0,delta_y,0.0,1.0);
      PseudoJet p1boost = p1; p1boost.boost(myboost);
      verify_almost_equal(p1boost.rap(), p1.rap()+delta_y, "p1boost.rap() == p1.rap() + delta_y");
      
    }
    
    return _pass_test;
  }
};

//----------------------------------------------------------------------
class Info : public PseudoJet::UserInfoBase {
public:
  Info() : pdg(21) {}
  int pdg;
};

//----------------------------------------------------------------------
class MyPseudoJet : public PseudoJet {
public:
  MyPseudoJet() {set_user_info(new Info());}
  MyPseudoJet(const PseudoJet & in) {
    reset(in);
    if (dynamic_cast<const Info *>(user_info_ptr()) == 0) {
      set_user_info(new Info());
    }
  }
  
  // NB dangerous if reset(...) has been called...
  int pdg_id() const {return user_info<Info>().pdg;}
};

//----------------------------------------------------------------------
/// Tests of assignments and resets of PseudoJets
class TestPJAssignment : public TestBase {
 std::string short_name()  const {return "TestPJAssignment";}
 std::string description()  const {return "Tests of assignments, resets and zero-tests of PseudoJets";}

  bool run_test () {
    
    PseudoJet a = random_PtYPhiM();

    // check default indices
    verify_equal(a.user_index(),         -1, "default user index");
    verify_equal(a.cluster_hist_index(), -1, "default cluster index");
    verify_null(a.user_info_ptr(), "default user_info");
    verify_null(a.structure_ptr(), "default structure");

    PseudoJet b = a;
    verify_equal(a == b, true, "PJ internal equality test");

    // set indices -- we'll check them again later
    a.set_user_index(10);
    verify_equal(a != b, true, "PJ internal inequality test (because of user index)");

    b = a;
    a.set_cluster_hist_index(11);
    verify_equal(a != b, true, "PJ internal equality test (because of cluster history index)");

    // check assignments and resets
    b = a;
    verify_equal(a, b, "assignment from PJ");
    b.reset(a);
    verify_equal(a, b, "reset from PJ");

    double p[4];
    p[0] = a.px();
    p[1] = a.py();
    p[2] = a.pz();
    p[3] = a.E();

    // checks assignemnts and resets from 4-vectors
    PseudoJet c(p);
    verify_equal(a, b, "assignment from 4-vector");
    PseudoJet d;
    d.reset(p);
    verify_equal(a, b, "reset from 4-vector");

    MyPseudoJet particle(a);
    verify_equal(particle.pdg_id(), 21 , "default pdg ID");

    // checks that assignments and resets from MyPJ -> PJ -> MyPJ behave sensibly
    b = particle; // remember b is a PseudoJet
    MyPseudoJet particle2(b);
    verify_almost_equal(particle, particle2, "MyPJ -> PJ -> MyPJ (via assignment)");
    MyPseudoJet particle3;
    particle3.reset(b);
    verify_almost_equal(particle, particle3, "MyPJ -> PJ -> MyPJ (via reset)");
    
    // NB these values were set earlier
    verify_equal(b.user_index(),         10, "remembering modified user index");
    verify_equal(b.cluster_hist_index(), 11, "remembering modified cluster index");

    // make sure that reset with simple 4-component vector also resets everything else
    MyPseudoJet particle4;
    particle4.reset(b.px(), b.py(), b.pz(), b.E());

    verify_different(particle.user_info_ptr(), particle4.user_info_ptr(), "user info reset");
    verify_equal(particle4.user_index(),         -1, "default user index on reset from 4-mom");
    verify_equal(particle4.cluster_hist_index(), -1, "default clust index on reset from 4-mom");
    verify_null(particle4.user_info_ptr(), "default user_info");
    verify_null(particle4.structure_ptr(), "default structure");

    // now run some tests 
    verify_equal(particle4==particle, false, "PJ inequality because of meta-info");

    // now check null v. non-null things
    PseudoJet null_vector;
    verify_equal(null_vector == 0, true,  "PJ zero test");
    verify_equal(0 == null_vector, true,  "PJ reversed zero test");
    verify_equal(particle    == 0, false, "PJ non-zero test");
    verify_equal(0 == particle,    false, "PJ reversed non-zero test");

    // tests related to the bug discovered on 2023-02-14
    // first set up pj1 and make sure its phi is evaluated & cached
    PseudoJet pj1(3.0, 4.0, 0.0, 5.0);
    //double phi1 = pj1.phi();
    // now set up pj2 with phi not yet cached
    PseudoJet pj2(1,0,0,1);
    double phi2 = pj2.phi();
    // transfer momentum from pj1 to pj2
    pj2.reset_momentum(pj1);
    // similar test but with the assignment operator
    PseudoJet pj3(1,0,0,1);
    double phi3 = pj3.phi();
    verify_equal(phi2, phi3, "dummy test to avoid compiler warnings");
    // transfer momentum from pj1 to pj3
    pj3 = pj1;
    verify_equal(pj2.phi(), pj1.phi(), "phi after reset_momentum");
    verify_equal(pj3.phi(), pj1.phi(), "phi after assignment");

    return _pass_test;
  }
};


//----------------------------------------------------------------------
/// Tests of assignments and resets of PseudoJets
class TestPJCSaccess : public TestBase {
  virtual std::string description() const {return "Tests of the PseudoJet structure calls";}
  virtual std::string short_name()  const {return "TestPJStructure";}

  virtual bool run_test() {
    vector<PseudoJet> event = default_event();
    double R = 0.5;
    JetDefinition jet_def(antikt_algorithm, R);
    ClusterSequence * cs = new ClusterSequence(event, jet_def);
    vector<PseudoJet> jets = sorted_by_pt(cs->inclusive_jets());

    PseudoJet dummy1, dummy2;

    // test an uninitialised particle
    PseudoJet empty;
    verify_equal(empty.has_associated_cluster_sequence(), false,
		 "empty PseudoJet has no cluster sequence (=false)");
    verify_equal<const ClusterSequence*>(empty.associated_cluster_sequence(), NULL,
		 "empty PseudoJet associated cluster sequence (=NULL)");
    verify_equal(empty.has_valid_cluster_sequence(), false,
		 "empty PseudoJet has no valid cluster sequence (=throws)");
    VERIFY_THROWS(empty.validated_cs(),
		  "empty PseudoJet validated cluster sequence (=throws)");
    verify_equal(empty.has_constituents(), false,
		 "empty PseudoJet has no constituents (=false)");
    VERIFY_THROWS(empty.constituents(),
		 "empty PseudoJet constituents (=throws)");
    verify_equal(empty.has_pieces(), false,
		 "empty PseudoJet has no pieces (=false)");
    VERIFY_THROWS(empty.pieces(),
		  "empty PseudoJet pieces (=throws)");
    VERIFY_THROWS(empty.has_parents(dummy1, dummy2),
		  "empty PseudoJet parents (=false)");
    VERIFY_THROWS(empty.has_child(dummy1),
		  "empty PseudoJet child (=false)");
    verify_equal(empty.has_structure_of<ClusterSequence>(), false,
		 "empty PseudoJet has not the structure of a ClusterSequence (=false)");


    // test an input particle
    verify_equal(event[0].has_associated_cluster_sequence(), false, 
		 "input particle has no cluster sequence");
    verify_equal<const ClusterSequence*>(event[0].associated_cluster_sequence(), 
		 NULL, "input particle associated cluster sequence (=NULL)");
    verify_equal(event[0].has_valid_cluster_sequence(), false, 
		 "input particle has no valid cluster sequence");
    VERIFY_THROWS(event[0].validated_cs(),
		  "input particle validated cluster sequence (=throws)");
    verify_equal(event[0].has_constituents(), false, 
		 "input particle has no constituents");
    VERIFY_THROWS(event[0].constituents(),
		 "input particle constituents (=throws)");
    verify_equal(event[0].has_pieces(), false, 
		 "input particle has no pieces");
    VERIFY_THROWS(event[0].pieces(),
		  "input particle pieces (=throws)");
    VERIFY_THROWS(event[0].has_parents(dummy1, dummy2),
		  "input particle parents (=throws)");
    VERIFY_THROWS(event[0].has_child(dummy1),
		  "input particle child (=throws)");
    verify_equal(event[0].has_structure_of<ClusterSequence>(), false,
		 "input particle has the structure of a ClusterSequence (=false)");

    // test a jet
    verify_equal(jets[0].has_associated_cluster_sequence(), true, 
		 "jet has cluster sequence");
    verify_equal<const ClusterSequence*>(jets[0].associated_cluster_sequence(),
		 cs, "jet associated cluster sequence (=CS)");
    verify_equal(jets[0].has_valid_cluster_sequence(), true, 
		 "jet has valid cluster sequence");
    verify_equal<const ClusterSequence*>(jets[0].validated_cs(), cs, 
		 "jet validated cluster sequence (=CS)");
    verify_equal(jets[0].has_constituents(), true, 
		 "jet has constituents");
    verify_equal((unsigned int) jets[0].constituents().size(), 31U, 
    		 "jet has 31 constituents"); // hard coded # of constit is ugly
    verify_equal(jets[0].has_pieces(), true, 
		 "jet has pieces");
    verify_equal((unsigned int) jets[0].pieces().size(), 2U,
		 "jet has 2 pieces");
    verify_equal(jets[0].has_parents(dummy1, dummy2), true,
		 "jet parents");
    verify_equal(jets[0].has_child(dummy1), false,
		 "jet child (=false)");
    verify_equal(jets[0].has_structure_of<ClusterSequence>(), true,
		 "jet has the structure of a ClusterSequence (=true)");

    // test a jet's constituent
    PseudoJet constituent = jets[0].constituents()[0];
    verify_equal(constituent.has_associated_cluster_sequence(), true, 
		 "jet constituent has cluster sequence");
    verify_equal<const ClusterSequence*>(constituent.associated_cluster_sequence(),
                 cs, "jet constituent associated cluster sequence (=CS)");
    verify_equal(constituent.has_valid_cluster_sequence(), true, 
		 "jet constituent has valid cluster sequence");
    verify_equal<const ClusterSequence*>(constituent.validated_cs(), cs, 
		 "jet constituent validated cluster sequence (=CS)");
    verify_equal(constituent.has_constituents(), true, 
		 "jet constituent has constituents");
    verify_equal(constituent.constituents()[0], constituent, 
    		 "jet constituent has itself as a constituents"); 
    verify_equal(constituent.has_pieces(), false, 
		 "jet constituent has no pieces");
    verify_equal((unsigned int) constituent.pieces().size(), 0U,
		  "jet constituent pieces (=0)");
    verify_equal(constituent.has_parents(dummy1, dummy2), false,
		 "jet constituent has no parents");
    verify_equal(constituent.has_child(dummy1), true,
		 "jet constituent child (=true)");
    verify_equal(constituent.has_structure_of<ClusterSequence>(), true,
		 "jet constituent has the structure of a ClusterSequence (=true)");

    // test a composite jet (from input particles)
    PseudoJet composite1 = join(event[0], event[1]);
    verify_equal(composite1.has_associated_cluster_sequence(), false, 
		 "composite (2 inputs) has no cluster sequence");
    verify_equal<const ClusterSequence*>(composite1.associated_cluster_sequence(),
                 NULL, "composite (2 inputs) associated cluster sequence (=NULL)");
    verify_equal(composite1.has_valid_cluster_sequence(), false, 
		 "composite (2 inputs) has valid cluster sequence");
    VERIFY_THROWS(composite1.validated_cs(), 
		  "composite (2 inputs) validated cluster sequence (=throws)");
    verify_equal(composite1.has_constituents(), true, 
		 "composite (2 inputs) has constituents");
    verify_equal((unsigned int) composite1.constituents().size(), 2U, 
    		 "composite (2 inputs) has 2 constituents"); 
    verify_equal(composite1.has_pieces(), true, 
		 "composite (2 inputs) has pieces");
    verify_equal((unsigned int) composite1.pieces().size(), 2U,
		  "composite (2 inputs) has 2 pieces");
    VERIFY_THROWS(composite1.has_parents(dummy1, dummy2),
		  "composite (2 inputs) parents (=throws)");
    VERIFY_THROWS(composite1.has_child(dummy1),
		  "composite (2 inputs) child (=throws)");
    verify_equal(composite1.has_structure_of<ClusterSequence>(), false,
		 "composite (2 inputs) has not the structure of a ClusterSequence (=false)");

    // test a composite jet (from CS jets)
    PseudoJet composite2 = join(jets[0], jets[1]);
    verify_equal(composite2.has_associated_cluster_sequence(), false, 
		 "composite (2 jets) has no cluster sequence");
    verify_equal<const ClusterSequence*>(composite2.associated_cluster_sequence(),
                 NULL, "composite (2 jets) associated cluster sequence (=NULL)");
    verify_equal(composite2.has_valid_cluster_sequence(), false, 
		 "composite (2 jets) has valid cluster sequence");
    VERIFY_THROWS(composite2.validated_cs(), 
		  "composite (2 jets) validated cluster sequence (=throws)");
    verify_equal(composite2.has_constituents(), true, 
		 "composite (2 jets) has constituents");
    verify_equal((unsigned int) composite2.constituents().size(), 
		 (unsigned int) (jets[0].constituents().size() + jets[1].constituents().size()),
    		 "composite (2 jets) has itself as a constituents"); 
    verify_equal(composite2.has_pieces(), true, 
		 "composite (2 jets) has pieces");
    verify_equal((unsigned int) composite2.pieces().size(), 2U,
		  "composite (2 jets) has 2 pieces");
    VERIFY_THROWS(composite2.has_parents(dummy1, dummy2),
		  "composite (2 jets) parents (=throws)");
    VERIFY_THROWS(composite2.has_child(dummy1),
		  "composite (2 jets) child (=throws)");
    verify_equal(composite2.has_structure_of<ClusterSequence>(), false,
		 "composite (2 jets) has not the structure of a ClusterSequence (=false)");


    // test a jet (after CS deletion)
    delete cs;

    verify_equal(jets[0].has_associated_cluster_sequence(), true, 
		 "post CS-deletion, jet has cluster sequence");
    verify_equal<const ClusterSequence*>(jets[0].associated_cluster_sequence(),
		 NULL, "post CS-deletion, jet associated cluster sequence (=NULL)");
    verify_equal(jets[0].has_valid_cluster_sequence(), false, 
		 "post CS-deletion, jet has no valid cluster sequence");
    VERIFY_THROWS(jets[0].validated_cs(),
		 "post CS-deletion, jet validated cluster sequence (=throws)");
    verify_equal(jets[0].has_constituents(), true, 
		 "post CS-deletion, jet has constituents");
    VERIFY_THROWS(jets[0].constituents().size(),
		  "post CS-deletion, jet has constituents (=throws)");
    VERIFY_THROWS(jets[0].has_pieces(),
		  "post CS-deletion, jet has pieces (=throws)");
    VERIFY_THROWS(jets[0].pieces().size(),
		 "post CS-deletion, jet has 2 pieces (=throws)");
    VERIFY_THROWS(jets[0].has_parents(dummy1, dummy2),
		 "post CS-deletion, jet parents (=throws)");
    VERIFY_THROWS(jets[0].has_child(dummy1),
		 "post CS-deletion, jet child (=throws)");
    verify_equal(jets[0].has_structure_of<ClusterSequence>(), true,
		 "post CS-deletion jet has the structure of a ClusterSequence (=true)");
    
    
//     cout << jets[0].perp() << endl;
//     cout << jets[0].has_associated_cluster_sequence() << endl;
//     cout << jets[0].has_constituents() << endl;
//     cout << jets[0].constituents().size() << endl;
// 
    return _pass_test;
  }
};

#endif // __TESTPSEUDOJET_HH__
