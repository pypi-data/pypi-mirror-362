#ifndef __TESTGRIDS_HH__
#define __TESTGRIDS_HH__

#include "TestBase.hh"
#include "fastjet/tools/GridMedianBackgroundEstimator.hh"
#include "fastjet/GridJetPlugin.hh"


/// class to test some things that happen with Groomers and Grids
/// put together
class TestGrids : public TestBase {
  std::string short_name()  const {return "TestGrids";}

  virtual bool run_test () {
    
    RectangularGrid grid;
    VERIFY_THROWS(GridMedianBackgroundEstimator gmbge1(grid), "GMBGE constructor with default (uninitialised) grid throws");
    VERIFY_THROWS(GridJetPlugin gridjet(grid), "GridJetPlugin constructor with default (uninitialised) grid throws");

    grid = RectangularGrid(2.0, 5.0, 0.5, twopi/12.0, !SelectorRapRange(3.0,4.0));
    verify_equal(grid.n_tiles(), 72, "total number of grid tiles");
    verify_equal(grid.n_good_tiles(), 48, "number of good grid tiles");
    
    // now test the grid jet plugin
    GridJetPlugin gridjet(grid);
    JetDefinition gridjetdef(&gridjet);
    vector<PseudoJet> particles;
    particles.push_back(PtYPhiM( 8.0,0.1,0.1));

    particles.push_back(PtYPhiM( 9.0,2.1,6.0));
    particles.push_back(PtYPhiM(11.0,2.2,6.0));

    particles.push_back(PtYPhiM(12.0,3.5,1.0));

    particles.push_back(PtYPhiM(14.0,4.4,1.0));

    vector<PseudoJet> jets = gridjetdef(particles);
    verify_equal(int(jets.size()), 2, "number of grid jets");
    verify_almost_equal(jets[0].pt(), 20.0, "jet 1 pt = 20 GeV", 0.01);
    verify_almost_equal(jets[1].pt(), 14.0, "jet 2 pt = 14 GeV", 0.01);

    // test the GridMedianBackgroundEstimator with RectangularGrid assignments
    GridMedianBackgroundEstimator gmbge(2.0, 5.0, 0.5, twopi/12.0, !SelectorRapRange(3.0,4.0));
    verify_equal(gmbge.n_tiles(), grid.n_tiles(), "total # of grid tiles in GMBGE & RG");
    verify_equal(gmbge.n_good_tiles(), grid.n_good_tiles(), "total # of good grid tiles in GMBGE & RG");
    verify_equal(gmbge.dphi(), grid.dphi(), "phi spacing in GMBGE & RG");
    verify_equal(gmbge.drap(), grid.drap(), "rap spacing in GMBGE & RG");
    
    return _pass_test;
  }
};
#endif // __TESTGRIDS_HH__
