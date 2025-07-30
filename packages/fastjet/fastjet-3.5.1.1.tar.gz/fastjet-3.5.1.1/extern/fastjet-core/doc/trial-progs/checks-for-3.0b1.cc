#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/MassDropTagger.hh"
#include "fastjet/tools/JetMedianBackgroundEstimator.hh"
#include <iostream>
#include <fastjet/tools/Boost.hh>
#include <fastjet/Selector.hh>
#include <fastjet/SISConePlugin.hh>
#include <fastjet/tools/CASubJetTagger.hh>
using namespace std;
using namespace fastjet;

//----------------------------------------------------------------------
class SimpleFilterStructure;
class SimpleFilterWrappedStructure;

class SimpleFilter: public Transformer {
public:
  SimpleFilter(const JetDefinition & subjet_def, const Selector & selector) :
    _subjet_def(subjet_def), _selector(selector) {}

  virtual std::string description() const {
    return "Filter that finds subjets with "+_subjet_def.description()+
      ", using a ("+_selector.description() + ") selector" ;
  }

  virtual PseudoJet result(const PseudoJet & jet) const;

  // CompositeJetStructure is the structural type associated with the 
  // join operation that we use shall use to create the returned jet
  //typedef CompositeJetStructure StructureType;
  //typedef SimpleFilterStructure StructureType;
  typedef SimpleFilterWrappedStructure StructureType;

private:
  JetDefinition _subjet_def;
  Selector      _selector;
};


// PseudoJet SimpleFilter::result(const PseudoJet & jet) const {
//   // get the subjets
//   ClusterSequence * cs = new ClusterSequence(jet.constituents(), _subjet_def);
//   vector<PseudoJet> subjets = cs->inclusive_jets();
//   
//   // indicate that the cluster sequence should delete itself when
//   // there are no longer any of its (sub)jets in scope anywhere
//   cs->delete_self_when_unused();
//   
//   // get the selected subjets 
//   vector<PseudoJet> selected_subjets = _selector(subjets);
//   // join them using the same recombiner as was used in the subjet_def
//   PseudoJet result = join(selected_subjets, *_subjet_def.recombiner());
//   return result;
// }

/// solution #1 to getting a SimpleFilter Structure
class SimpleFilterStructure: public CompositeJetStructure {
public:
  SimpleFilterStructure(const std::vector<PseudoJet> & pieces, 
		  const JetDefinition::Recombiner *recombiner = 0) :
    CompositeJetStructure(pieces, recombiner) {}

  const vector<PseudoJet> & rejected() const {return _rejected;}
private:
  vector<PseudoJet> _rejected;
  friend class SimpleFilter;
};

/// solution #2 to getting a SimpleFilter Structure
class SimpleFilterWrappedStructure: public WrappedStructure {
public:
  SimpleFilterWrappedStructure(
      const SharedPtr<PseudoJetStructureBase> & to_be_wrapped,
      const vector<PseudoJet> & rejected_pieces) :
    WrappedStructure(to_be_wrapped), _rejected(rejected_pieces) {}

  const vector<PseudoJet> & rejected() const {return _rejected;}
private:
  vector<PseudoJet> _rejected;
};


// PseudoJet SimpleFilter::result(const PseudoJet & jet) const {
//   // get the subjets
//   ClusterSequence * cs = new ClusterSequence(jet.constituents(), _subjet_def);
//   vector<PseudoJet> subjets = cs->inclusive_jets();
//   
//   // indicate that the cluster sequence should delete itself when
//   // there are no longer any of its (sub)jets in scope anywhere
//   cs->delete_self_when_unused();
//   
//   // get the selected subjets 
//   vector<PseudoJet> selected_subjets, rejected_subjets;
//   _selector.sift(subjets, selected_subjets, rejected_subjets);
//   // join them using the same recombiner as was used in the subjet_def
//   PseudoJet result = join<SimpleFilterStructure>(selected_subjets, *_subjet_def.recombiner());
//   SimpleFilterStructure * structure = dynamic_cast<SimpleFilterStructure *>(result.structure_non_const_ptr());
//   structure->_rejected = rejected_subjets;
//   return result;
// }

PseudoJet SimpleFilter::result(const PseudoJet & jet) const {
  // get the subjets
  ClusterSequence * cs = new ClusterSequence(jet.constituents(), _subjet_def);
  vector<PseudoJet> subjets = cs->inclusive_jets();
  
  // indicate that the cluster sequence should delete itself when
  // there are no longer any of its (sub)jets in scope anywhere
  cs->delete_self_when_unused();
  
  // get the selected subjets 
  vector<PseudoJet> selected_subjets, rejected_subjets;
  _selector.sift(subjets, selected_subjets, rejected_subjets);
  // join them using the same recombiner as was used in the subjet_def
  PseudoJet result = join(selected_subjets, *_subjet_def.recombiner());
  SharedPtr<PseudoJetStructureBase> structure(new
     SimpleFilterWrappedStructure(result.structure_shared_ptr(), 
				  rejected_subjets));
  result.set_structure_shared_ptr(structure);
  return result;
}




int main() {
  
  vector<PseudoJet> particles;
  particles.push_back(PtYPhiM(100.0, 0.10, 0.0, 0.0));
  particles.push_back(PtYPhiM(101.0,-0.90, 0.0, 0.0));
  particles.push_back(PtYPhiM(  1.0,-0.89, 0.0, 0.0));
  particles.push_back(PtYPhiM(201.0,-1.10, 0.0, 0.0));

  JetDefinition jet_def(kt_algorithm, 0.6);
  
  AreaDefinition area_def(active_area, GhostedAreaSpec(3.0));
  ClusterSequenceArea * csa = new ClusterSequenceArea(particles, jet_def, area_def);
  vector<PseudoJet> jets = sorted_by_pt(csa->inclusive_jets());
  cout << jets[0].perp() << " " << jets[0].area() << endl;
  
  cout << jets[1].pieces().size() << endl;

  PseudoJet joined = join(jets[0],jets[1]);
  cout << joined.perp() << " " << joined.area() << endl;
  cout << joined.has_area() << endl;

  cout << particles[0].has_area() << endl;

  PseudoJet filtered = Filter(0.1,SelectorNHardest(2))(joined);
  cout << filtered.perp() << " " << filtered.has_structure_of<Filter>() << endl;

  PseudoJet higgs = MassDropTagger()(jets[0]);
  cout << "may be higgs: " << (higgs != 0) << " " << higgs.perp() << endl;
  
  // //FunctionOfPseudoJet<double> * bgrescale = new 
  // BackgroundRescalingYPolynomial bgrescale(1,0.0,-0.5);
  // Selector sel =  bgrescale > 0.5;
  // Selector sel = BackgroundRescalingYPolynomial(1,0.0,-0.5) > 0.5;
  // cout << sel.pass(PtYPhiM(100,0,0,0)) << endl;
  // cout << sel.pass(PtYPhiM(100,2.0,0,0)) << endl;
  
  vector<PseudoJet> excl_jets = csa->exclusive_jets(3);
  cout << excl_jets.size() << endl;

  vector<PseudoJet> excl_subjets = jets[0].exclusive_subjets_up_to(5);
  cout << excl_subjets.size() << endl;

  excl_subjets = csa->exclusive_subjets_up_to(jets[0], 3);
  cout << excl_subjets.size() << endl;

  cout <<  jets[0].area() << endl;
  ClusterSequence cs;
  FunctionOfPseudoJet<PseudoJet> * unboost = new Unboost(jets[0]);
  cs.transfer_from_sequence(*csa, unboost);
  cout <<  jets[1].perp() << " " << jets[1].m() << endl;
  //cs.transfer_from_sequence(csa);
  cout << cs.inclusive_jets()[1].perp()  << " " << cs.inclusive_jets()[1].m() << endl;

  
  JetDefinition siscone = new SISConePlugin(0.5,0.75);
  ClusterSequence cs_siscone(particles, siscone);
  jets = sorted_by_pt(cs_siscone.inclusive_jets());
  
  const fastjet::SISConeExtras * extras = 
             dynamic_cast<const fastjet::SISConeExtras *>(cs_siscone.extras());
  int pass = extras->pass(jets[0]);
  cout << jets[0].perp() << " " << pass << " " << endl;

  cout << "----------- filtering -----------\n";
  SimpleFilter filter(JetDefinition(antikt_algorithm, 0.1), SelectorNHardest(1));
  cout << filter.description() << endl;
  PseudoJet filtered_jet = filter(jets[0]);
  cout << filtered_jet.perp() << " " << filtered_jet.pieces().size() 
       << " " << filtered_jet.constituents().size() << endl;
  cout << filtered_jet.structure_of<SimpleFilter>().rejected().size() << endl;
}
