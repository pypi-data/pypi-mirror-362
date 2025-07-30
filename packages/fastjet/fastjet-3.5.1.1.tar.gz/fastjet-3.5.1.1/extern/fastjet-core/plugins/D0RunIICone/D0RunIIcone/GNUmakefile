#
#            M A I N
#           =========

info:  	
	@echo Please type: 'main.exe'
	@echo detected host: `hostname`,  os = `uname`

#################################################################
SRC_cc = $(wildcard src/*.cc) 
SRC_C = $(wildcard src/*.C) 
SRC_cpp = $(wildcard src/*.cpp) 
SRC_F = $(wildcard src/*.F)

#ANAOBJ = $(patsubst src/%.cc, obj/%.o, $(ANASRC))
OBJ_cc = $(patsubst src/%.cc, obj/%.o, $(SRC_cc))
OBJ_C = $(patsubst src/%.C, obj/%.o, $(SRC_C))
OBJ_cpp = $(patsubst src/%.cpp, obj/%.o, $(SRC_cpp))
OBJ_F = $(patsubst src/%.F, obj/%.o, $(SRC_F))
ANAOBJ = $(OBJ_cc) $(OBJ_C) $(OBJ_cpp) $(OBJ_F)


OBJ_lib = $(wildcard lib/*.so)
OBJ_lib+= $(wildcard lib/*.a)
LIBStemp = $(patsubst lib/lib%.so, -l%, $(OBJ_lib))
LIBS = -Llib -L.
LIBS += $(patsubst lib/lib%.a, -l%, $(LIBStemp))

#CERNLIB = $(shell cernlib)
CERNLIB = -lmathlib -lkernlib -lpacklib   -lshift -lnsl -lcrypt -ldl
#CERNLIB += -L/cern/pro/lib
#cernlib location from pcth cluster:
CERNLIB +=  -L/afs/cern.ch/sw/lcg/external/cernlib/2005/slc4_ia32_gcc345/lib
#################################################################


#CFLAGS = -O
CFLAGS = -g
#CFLAGS = -O -pg
#FFLAGS = -O
FFLAGS = -g

INC = -Ihh

HOST := $(shell hostname)

ifeq ($(findstring cern, $(HOST)), cern)
  INC += -I/cern/pro/src/cfortran  #CERN	
  LIBS += ${CERNLIB} 	
endif

ifeq ($(HOST),dzero)
  INC += -I/cern/pro/include/cfortran  #BU
  CLHEP = /fnal/ups/clhep/v1_6
  LIBS += -L/fnal/ups/gcc/v2_95_2/lib/gcc-lib/i686-pc-linux-gnu/2.95.2
endif

ifeq ($(findstring clued0,$(HOST)), clued0) #FNAL
  CLHEP = /fnal/ups/clhep/Linux-2-4/v1_8
  LIBS += -L/D0/ups/gcc/Linux-2-4/v3_2_1/lib
endif



#INC += -I${CLHEP}/include/
#LIBS += -lstdhep



SYSTEM:= $(shell uname)

##################################################################
ifeq ($(SYSTEM),SunOS)
  FCOMP = f77
  FFLAGS +=
  CPPCOMP = CC
  CFLAGS += -DOS_SOLARIS_2_5 -DOS_NEW_CHECK -DOS_STL_ASSERT -DOS_NO_WSTRING -DOS_NO_ALLOCATORS 
  INC    += -I/afs/cern.ch/sw/lhcxx/specific/@sys/ObjectSpace/pro \
            -I/afs/cern.ch/sw/lhcxx/specific/@sys/ObjectSpace/pro/ospace/stl \
            -I/afs/cern.ch/sw/lhcxx/specific/@sys/ObjectSpace/pro/ospace/std \
            -I/afs/cern.ch/sw/lhcxx/specific/@sys/CLHEP/pro/include	
  F2CLIB =  -L/usr/lang/SC3.0/lib -lM77 -lF77 -lsunmath
  LINKER = CC -t #-pg	
endif
##################################################################
ifeq ($(SYSTEM),Linux)
  FCOMP = g77
  FFLAGS +=
  #INC += -I/afs/cern.ch/sw/lcg/contrib/gcc/3.4.3/slc3_ia32_gcc343/include/c++/3.4.3/backward
  #INC += -I/afs/cern.ch/sw/lcg/contrib/gcc/3.4.3/slc3_ia64_gcc343/include/c++/3.4.3/backward
  #INC += -I/afs/cern.ch/sw/lcg/contrib/gcc/3.4.3/slc3_amd64_gcc343/include/c++/3.4.3/backward
##  ifeq ($(findstring clued0,$(HOST)), clued0)
#    CPPCOMP = g++ # dont forget to "setup root v3_02_07c -q GCC_2_95_2"
    #CPPCOMP = KCC
    CPPCOMP = gcc #-Wno-deprecated
    #CFLAGS += --exceptions --thread_safe
    #LINKER = KCC --exceptions --thread_safe
    LINKER = gcc #/usr/lib/libstdc++.so.5   #-lstdc++
    #LINKER = gcc -lm -lstdc++
##  else	
##    CPPCOMP = g++
##    CFLAGS += -Df2cFortran -fno-second-underscore \
##              -fno-automatic -fdollar-ok -fno-backslash -finit-local-zero \
##	      -fugly-logint -ftypeless-boz -Wall
##    LINKER = g77 	
##  endif
  F2CLIB = -lg2c
#  FLIBS = -L/D0/ups/cern/2001/lib/ -lpdflib804 -lpacklib -lnsl -lcrypt -lmathlib -lkernlib
#  FLIBS = -L/D0/ups/cern/2001/lib/ -lpdflib804 -lmathlib -lkernlib
  FLIBS =  # ${CERNLIB} -lpdflib804 -lmathlib -lkernlib
endif

#[pcth169] ~/D0RunIIcone/mytest > gcc obj/main.o -L/afs/cern.ch/sw/root/v5.10.00/slc3_gcc3.2.3/root/lib -lCore -lCint -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -pthread -lm -ldl -rdynamic -lMinuit -Llib -L. -lshift -lnsl -lcrypt -ldl -L/usr/local/lib -lshift -lnsl -lcrypt -ldl -lg2c -o main.exe



##################################################################
ifeq ($(SYSTEM),IRIX64)
  FCOMP = f77 
  FFLAGS += -mips3 -n32
  CPPCOMP = KCC
  CFLAGS += -n32 --exceptions --thread_safe
  LINKER = KCC -n32 --exceptions --thread_safe # -v
  F2CLIB += -lm -L/usr/lib32/mips3 -lftn
endif
##################################################################

ROOTCFLAGS := $(shell root-config --cflags)
ROOTLIBS   := $(shell root-config --libs)
ROOTGLIBS  := $(shell root-config --glibs)

ROOTLIBS+= -lMinuit

CFLAGS  += $(ROOTCFLAGS)
RLIBS    = $(ROOTLIBS) $(SYSLIBS)
GLIBS    = $(ROOTGLIBS) $(SYSLIBS)

##################################################################

obj/%.o :: src/%.cc hh/*.h*
	$(CPPCOMP) -c $(CFLAGS) $(INC) $< -o $@

obj/%.o :: src/%.C #hh/*.h*
	$(CPPCOMP) -c $(CFLAGS) $(INC) $< -o $@

obj/%.o :: src/%.cpp #hh/*.h*
	$(CPPCOMP) -c $(CFLAGS) $(INC) $< -o $@

obj/%.o :: src/%.F
	$(FCOMP) -c $(FFLAGS) $< -o $@

#obj/%.o :: $(CLHEP)/CLHEP/Matrix/%.cc hh/*.h*
#	$(CPPCOMP) -c $(CFLAGS) $(INC) $< -o $@


##############################################################
CLHEPLIB=lib/libclhep.a

CLHEPOBJECTS= $(patsubst $(CLHEP)/CLHEP/Matrix/%.cc, \
                lib/%.o, \
                $(wildcard $(CLHEP)/CLHEP/Matrix/*.cc))

lib/%.o :: $(CLHEP)/CLHEP/Matrix/%.cc
	$(CPPCOMP) -c $(CFLAGS) $(INC) $< -o $@


#$(CMSJETLIB) : $(CMSJETLIB)($(CMSJETOBJECTS))
#       rm -f $(CMSJETOBJECTS)

$(CLHEPLIB) : $(CLHEPOBJECTS)
	ar rv $(CLHEPLIB) $(CLHEPOBJECTS)

##############################################################



# main.exe:$(ANAOBJ) $(CLHEPLIB)
main.exe:$(ANAOBJ)
	$(LINKER) $(ANAOBJ) $(RLIBS) $(LIBS) $(FLIBS) $(F2CLIB) \
	-o main.exe


clean:	
	rm -rf obj/*.*
	rm -f *.exe
	rm -f fort.77
	rm -rf ti_files 
	rm -rf Templates.DB

print:
	@echo ANASRC=$(ANASRC)
	@echo ANAOBJ=$(ANAOBJ)
	@echo OBJ_lib=$(OBJ_lib)
	@echo LIBS=$(LIBS)
	@echo CLHEP=$(CLHEP)
	@echo $(CLHEP)/CLHEP/Matrix/*.cc
	@echo INC=$(INC)
	@echo OBJ_cpp=$(OBJ_cpp)


