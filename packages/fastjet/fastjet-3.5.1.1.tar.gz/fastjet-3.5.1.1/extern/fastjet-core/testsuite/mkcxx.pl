#!/usr/bin/perl -w
#
# Usage .../scripts/mkmk.pl [-v VPATH1[:VPATH2[:...]]] [-f] [-c]
#
#    -v  specify a VPATH
#    -g  replace g++ with the specified compiler
#    -c  compile with the CmdLine library
#    -f  compile with the FastJet library
#    -L  compile with the LHAPDF library
#    -H  compile with the HOPPET library
#    -r  compile with the root libraries
#    -m  compile with the mpfr/gmp libraries
#    -b  compile with the boost libraries
#    -q  compile with the QD library
#    -A  compile with ARPREC library
#    -s  compile with gsl
#    -i  add what follows as include flags
#    -d  add what follows as a define flag
#    -l  add what follows as link flags
#    -e  add extra bit (from file) to the Makefile
#    -3  force 32 bit
#    -p  add google profiling lib
#    -t  add google tcmalloc lib
#    -1  tell compiler to use c++11
#    -4  tell compiler to use c++14
#    -7  tell compiler to use c++17
#    -a name   
#        make the library archive libname.a from the non-main contents
#
# if there is a .fastjet file, it will be used to set the location
# for fastjet

#use File::Glob ':bsd_glob';
use File::Glob ':globally';
use Getopt::Std;

# try to establish the directory contaning common things etc.
#($common=$0)=~ s/\/mkmk.pl//;

$cmdline = "$0 '".join("' '",@ARGV)."'";

@info = ();

# get options
%options=();
getopts("v:a:l:i:g:d:e:fcrmsbqA3ptHL147",\%options);
if (defined($options{"v"})) {
  $VPATH = $options{"v"};
  @PATH = split(":",$VPATH);
} else {
  $VPATH = '';
  @PATH  = ();
}

$postlib='';
if (defined($options{"l"})) {
  $postlib = $options{"l"};
}

$postincl='';
if (defined($options{"i"})) {
  $postincl = $options{"i"};
}

if (defined($options{"a"})) {
  $libname = "lib".$options{"a"}.".a";
} else {
  $libname = "";
}

# set up default paths for certain things
# see if .cmdline is there
if (-e ".cmdline") {
  $cmdlinedir=`cat .cmdline`;
  chomp($cmdlinedir);
} else {
  $cmdlinedir=$ENV{"HOME"}."/utils/CmdLine";
}


$cxx='g++';  # for macs - otherwise get c++ = clang
if (defined($options{"g"})) {
  $cxx = $options{"g"};
}

# get a decent header
$makefile="
# Makefile generated automatically by $cmdline
# run 'make make' to update it if you add new files

CXX = $cxx
CXXFLAGS = -Wall -g -O2

# also arrange for fortran support
FC = gfortran
FFLAGS = -Wall -O2
";

# work around sone strange defines from Intel compiler stuff
$user=getpwuid $<;
if ($user eq 'gsoyez') {
    $makefile .= "INCLUDE=\nLIBRARIES=\n";
}

# now sort out some of the options
if (defined($options{"d"})) {
  $makefile .= "CXXFLAGS += ".$options{"d"}."\n";
}

# now sort out some of the options
if (defined($options{"3"})) {
  $makefile .= "CXXFLAGS += -m32\n";
  $makefile .= "LDFLAGS += -m32\n";
}

$cppversion="";
if    (defined($options{"1"})) {$cppversion="11";}
elsif (defined($options{"4"})) {$cppversion="14";}
elsif (defined($options{"7"})) {$cppversion="17";}
if ($cppversion) {
  # maybe also include -stdlib=libc++??? for clang?
  $makefile .= "CXXFLAGS += -std=c++$cppversion\n";
  $makefile .= "LDFLAGS += -std=c++$cppversion\n";
  # the following was needed on old versions of clang
  # but now (2021-06) things should be OK?
  # $clangcheck= `$cxx -v 2>&1| grep clang`;
  # chomp $clangcheck;
  # if ($clangcheck) {
  #   print "Detected clang compiler: $clangcheck\n";
  #   print "Adding -stdlib=libc++ \n";
  #   $makefile .= "CXXFLAGS += -stdlib=libc++\n";
  #   $makefile .= "LDFLAGS += -stdlib=libc++\n";
  # }
}


if (defined($options{"f"})) {
  # see if .fastjet is there -- if so, use it to indicate
  # which version to use
  if (-e ".fastjet") {
    $fastjetconfig=`cat .fastjet`;
    chomp($fastjetconfig);
    $fastjetconfig.="/bin/fastjet-config";
    print "Taking FastJet via $fastjetconfig\n";
  } else {
    $fastjetconfig="fastjet-config";
    print "Taking FastJet via $fastjetconfig in user's path\n";
  }
  push(@info, "FastJet config is $fastjetconfig");
  $makefile.="
FJCONFIG = $fastjetconfig
INCLUDE += `\$(FJCONFIG) --cxxflags`
LIBRARIES  += `\$(FJCONFIG) --libs --plugins`
";
}

if (defined($options{"A"})) {
    print "Taking ARPREC via arprec-config\n";
  $makefile.="
APCONFIG = arprec-config
INCLUDE += `\$(APCONFIG) --cxxflags`
LIBRARIES  += `\$(APCONFIG) --fclibs`
";
}

if (defined($options{"q"})) {
    print "Taking QD via qd-config\n";
  $makefile.="
QDCONFIG = qd-config
INCLUDE += `\$(QDCONFIG) --cxxflags`
LIBRARIES  += `\$(QDCONFIG) --libs`
";
}

if (defined($options{"H"})) {
  print "Taking HOPPET via hoppet-config\n";
  $makefile.="
HOPPETCONFIG = hoppet-config
INCLUDE += `\$(HOPPETCONFIG) --cxxflags`
LIBRARIES  += `\$(HOPPETCONFIG) --libs ` -lgfortran
";
}

if (defined($options{"L"})) {
  print "Taking LHAPDF via lhapdf-config\n";
  $makefile.="
LHAPDFCONFIG = lhapdf-config
INCLUDE += `\$(LHAPDFCONFIG) --cppflags`
LIBRARIES  += `\$(LHAPDFCONFIG) --ldflags ` -lgfortran
";
}

if (defined($options{"c"})) {
  push(@info, "command-line library");
  $makefile.="
INCLUDE += -I$cmdlinedir
LIBRARIES  += -L$cmdlinedir -lCmdLine
";
}

if (defined($options{"m"})) {
  push(@info, "gmp/mpfr");
  $makefile.="
LIBRARIES  +=  -lgmpxx -lgmp -lmpfr
";
}

if (defined($options{"b"})) {
  push(@info, "parts of boost");
  # include some boost stuff, but not all???
  $user=getpwuid $<;
  if ($user eq 'monni') {
    $makefile.="
LIBRARIES += -L/opt/local/lib -lboost_iostreams-mt -lboost_regex-mt -L/opt/local/lib/libgcc -lquadmath
";
  } elsif ($user eq 'gsoyez'){
    # looks like I need pthread on the cluster
    $makefile.="
LIBRARIES +=  -lboost_iostreams -lboost_regex -lpthread
";
}else {
    $makefile.="
#LIBRARIES +=  -lboost_iostreams -lboost_regex -lboost_program_options 
LIBRARIES +=  -lboost_iostreams -lboost_regex 
";
  }
}

if (defined($options{"s"})) {
  push(@info, "gsl");
  $gsllib=`gsl-config --libs`;
  $makefile .= "LIBRARIES += $gsllib\n";
  $gslinc=`gsl-config --cflags`;
  $makefile .= "INCLUDE += $gslinc\n";
  
#   $makefile.="
# #LIBRARIES  +=  -lgsl -lgslcblas  -lblas
# LIBRARIES  +=  -lgsl -lgslcblas 
#";
}

if (defined($options{"r"})) {
  push(@info, "root");
  $makefile.="
INCLUDE += `root-config --cflags`
LIBRARIES  += `root-config --libs`
";
}

# google options
if (defined($options{"p"})) {$makefile .= "LIBRARIES += -lprofiler\n";}
if (defined($options{"t"})) {$makefile .= "LIBRARIES += -ltcmalloc\n";}


# give some info to user...
if ($#info>=0) {print "Including ",join(", ",@info),"\n";}

if ($VPATH) {
  $makefile .= "\nVPATH = $VPATH\n";
  $makefile .= "LCLINCLUDE += -I".join(" -I",@PATH)."\n";
}

$makefile .= 'INCLUDE += $(LCLINCLUDE)'."\n";

# get the list of files
@src = <*.cc>;
push @src, <*.cpp>;
push @src, <*.f>;
push @src, <*.f90>;
push @src, <*.c>;
push @src, <*.C>;
foreach $path (@PATH) {
  push @src, <$path/*.cc>;
  push @src, <$path/*.cpp>;
  push @src, <$path/*.f>;
  push @src, <$path/*.f90>;
  push @src, <$path/*.c>;
  push @src, <$path/*.C>;
}
@progsrc = ();
@commonsrc = ();
@progobj = ();
@commonobj = ();
$doFortran=0;
foreach $name (@src) {
  if ($name =~ /\.f(90)?$/) {$doFortran = 1;}
  ($obj = $name) =~ s/\.[a-z]+$/.o/i;
  if (has_main($name)) {
    push @progsrc, $name;
    push @progobj, $obj;
  }
  else {
    push @commonsrc, $name;
    push @commonobj, $obj;
  }
}

if ($doFortran) {
  $makefile .= "\nLDFLAGS += -lgfortran\n\n";
}

# # get the ones in the VPATH too
# foreach $path (@PATH) {
#   @subsrc = <$path/*.cc>;
#   push @subsrc, <$path/*.cpp>;
#   foreach $sub (@subsrc) {
#     ($ssub = $sub);# =~ s:$path/::;
#     if (has_main($sub)) { push @progsrc, $ssub;}
#     else                { push @commonsrc, $ssub;}
#     push @src, $ssub;
#   }
# }

#--- add that list to the Makefile
$makefile .= "
COMMONSRC = ".join(" ",@commonsrc).'
F77SRC = 
COMMONOBJ = '.join(" ",@commonobj).'

PROGSRC = '.join(" ",@progsrc).'
PROGOBJ = '.join(" ",@progobj)."

INCLUDE += $postincl
LIBRARIES += $postlib
\n\n"; 

# get a make all
$proglist = '';
foreach $progsrc (@progsrc) {
  $progname = $progsrc;
  $progname =~ s/.cc$//;
  $progname =~ s/.cpp$//;
  $proglist .= " $progname"
}
$makefile .= "all: $proglist $libname\n\n";

# now put in pieces for making each prog
foreach $progsrc (@progsrc) {
  ($progname = $progsrc) =~ s/.(cc|cpp)$//;
  ($progobj  = $progsrc) =~ s/.(cc|cpp)$/.o/;
  $makefile .= "
$progname: $progobj ".' $(COMMONOBJ)
	$(CXX) $(LDFLAGS) -o $@ $@.o $(COMMONOBJ) $(LIBRARIES)
';

}
# and for the library
if ($libname) {
  $makefile .= "
$libname: ".'$(COMMONOBJ)'."
	ar cru $libname ".'$(COMMONOBJ)'."
	ranlib $libname
";
}

# add in any fixed extra bits to the Makefile
if (defined($options{"e"})) {
  open(EXTRA, "<".$options{"e"}) || die "Could not open ".$options{"e"};
  foreach $line (<EXTRA>) {$makefile .= $line;}
}


#-- tail end
$makefile .= '

make:
	'.$cmdline.'

clean:
	rm -vf $(COMMONOBJ) $(PROGOBJ)

realclean: clean
	rm -vf '.$proglist.' '.$libname.'

.cc.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.cpp.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.C.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.f.o:         $<
	$(FC) $(FFLAGS) -c $< -o $@
.f90.o:         $<
	$(FC) $(FFLAGS) -c $< -o $@


depend:
	makedepend  $(INCLUDE) -Y --   -- $(COMMONSRC) $(PROGSRC)
';

open(MAKE, "> Makefile") || die "Could not write to Makefile";
print MAKE $makefile;
close (MAKE);

system("make depend 2>&1 | grep -v -e warning -e 'not in' -e /usr/include/boost -e expecting ");




#-------------
# returns true if the program has a main block
sub has_main {
  ($name) = @_;
  my $regexp='^ *int +main[ \(]';
  my $n=`grep -E '$regexp' $name | wc -l`;
  return ($n == 1);
}
