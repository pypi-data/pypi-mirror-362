# fastjet/example/Makefile

# include the Makefile in the top directory, which has the bits and pieces
# needed to get CGAL working
include ../Makefile
# make sure we use the pedantic flags here (defined in ../Makefile)
CXXFLAGS += $(CXXPEDANTIC)

FASTJET_INCLUDE = -I../include
INCLUDE += $(FASTJET_INCLUDE)
LDFLAGS += -L../lib -lfastjet

CXXFLAGS += -Woverloaded-virtual

# plugin includes here are temporary and subject to change...
PLUGIN_INCLUDE = -I../plugins/CDFCones  -I../plugins/SISCone
PLUGIN_LIBRARY = -L../plugins/CDFCones  -L../plugins/SISCone -lCDFConesPlugin  -lSISConePlugin
PLUGIN77_INCLUDE = $(PLUGIN_INCLUDE) -I../plugins/PxCone
PLUGIN77_LIBRARY = $(PLUGIN_LIBRARY) -L../plugins/PxCone -lPxConePlugin  $(F77LIB)

INCLUDE += $(PLUGIN77_INCLUDE)

# Gavin sometimes likes to compile with google's tcmalloc and profiler
# libraries: tcmalloc gives a faster malloc (about 10% speed
# gain on the CGAL based algorithms), while the profiler is useful
# for a faithful estimation of where the time is being spent
#ifeq ($(shell whoami),salam)
#  LDFLAGS += -L/ada1/lpthe/salam/software/local/lib -ltcmalloc -lprofiler
#endif

SRCS = voronoi-square-problem.cc
OBJS = $(patsubst %.cc,%.o,$(SRCS))

voronoi-square-problem: voronoi-square-problem.o  ../lib/libfastjet.a
	$(CXX)  -o voronoi-square-problem voronoi-square-problem.o  $(LDFLAGS)

clean: 
	rm -f *.o

realclean: clean
	rm -f  fastjet_example fastjet_timing ktjet_example ktjet_timing

depend:
	makedepend $(FASTJET_INCLUDE) -Y -- -- $(SRCS)
# DO NOT DELETE

voronoi-square-problem.o: ../include/fastjet/ClusterSequenceArea.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequenceAreaBase.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequence.hh
voronoi-square-problem.o: ../include/fastjet/internal/DynamicNearestNeighbours.hh
voronoi-square-problem.o: ../include/fastjet/internal/numconsts.hh
voronoi-square-problem.o: ../include/fastjet/internal/base.hh
voronoi-square-problem.o: ../include/fastjet/PseudoJet.hh
voronoi-square-problem.o: ../include/fastjet/Error.hh
voronoi-square-problem.o: ../include/fastjet/JetDefinition.hh
voronoi-square-problem.o: ../include/fastjet/internal/LimitedWarning.hh
voronoi-square-problem.o: ../include/fastjet/RangeDefinition.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequenceActiveArea.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequenceActiveAreaExplicitGhosts.hh
voronoi-square-problem.o: ../include/fastjet/GhostedAreaSpec.hh
voronoi-square-problem.o: ../include/fastjet/internal/BasicRandom.hh
voronoi-square-problem.o: ../include/fastjet/ActiveAreaSpec.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequenceWithArea.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequencePassiveArea.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequence1GhostPassiveArea.hh
voronoi-square-problem.o: ../include/fastjet/ClusterSequenceVoronoiArea.hh
voronoi-square-problem.o: ../include/fastjet/AreaDefinition.hh
