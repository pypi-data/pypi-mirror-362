/* config-cmake.hh.in -- manually adapted from the config.h.in generated from configure.ac by autoheader. */

//----------------------------------------------------------------------------
// basic information
//----------------------------------------------------------------------------

// Name of package
#undef FASTJET_PACKAGE

// Define to the address where bug reports for this package should be sent
#undef FASTJET_PACKAGE_BUGREPORT

// Define to the full name of this package
#define FASTJET_PACKAGE_NAME "FastJet"

// Define to the full name and version of this package
#undef FASTJET_PACKAGE_STRING

// Define to the one symbol short name of this package
#undef FASTJET_PACKAGE_TARNAME

// Define to the home page for this package
#undef FASTJET_PACKAGE_URL


//----------------------------------------------------------------------------
// version information
//----------------------------------------------------------------------------

// Define to the version of this package
#define FASTJET_PACKAGE_VERSION "3.5.1"

// Version number of package
#define FASTJET_VERSION "3.5.1"

// Major version of this package
#define FASTJET_VERSION_MAJOR 3

// Minor version of this package
#define FASTJET_VERSION_MINOR 5

// Patch version of this package
#define FASTJET_VERSION_PATCHLEVEL 1

// Pre-release version of this package
#define FASTJET_VERSION_PRERELEASE 

// Version of the package under the form XYYZZ (instead of X.Y.Z)
#define FASTJET_VERSION_NUMBER 30501


//----------------------------------------------------------------------------
// available plugins
//----------------------------------------------------------------------------

// Defined if the ATLASCone plugin is enabled
#define FASTJET_ENABLE_PLUGIN_ATLASCONE

// Defined if the CDFCones plugin is enabled
#define FASTJET_ENABLE_PLUGIN_CDFCONES

// Defined if the CMSIterativeCone plugin is enabled
#define FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE

// Defined if the D0RunICone plugin is enabled
#define FASTJET_ENABLE_PLUGIN_D0RUNICONE

// Defined if the D0RunIICone plugin is enabled
#define FASTJET_ENABLE_PLUGIN_D0RUNIICONE

// Defined if the EECambridge plugin is enabled
#define FASTJET_ENABLE_PLUGIN_EECAMBRIDGE

// Defined if the GridJet plugin is enabled
#define FASTJET_ENABLE_PLUGIN_GRIDJET

// Defined if the Jade plugin is enabled
#define FASTJET_ENABLE_PLUGIN_JADE

// Defined if the NestedDefs plugin is enabled
#define FASTJET_ENABLE_PLUGIN_NESTEDDEFS

// Defined if the PxCone plugin is enabled
/* #undef FASTJET_ENABLE_PLUGIN_PXCONE */

// Defined if the SISCone plugin is enabled
#define FASTJET_ENABLE_PLUGIN_SISCONE

// Defined if the TrackJet plugin is enabled
#define FASTJET_ENABLE_PLUGIN_TRACKJET

//----------------------------------------------------------------------------
// mais switches for specific support
//----------------------------------------------------------------------------

// defined if FastJet is built with CGAL support
#define FASTJET_ENABLE_CGAL

// compilation uses DROP_CGAL if CGAL is not used
#ifndef FASTJET_ENABLE_CGAL
#define DROP_CGAL
#endif

// defined if limited thread-safety has been enabled
#define FASTJET_HAVE_LIMITED_THREAD_SAFETY

// defined if thread-safety has been enabled
#define FASTJET_HAVE_THREAD_SAFETY

//----------------------------------------------------------------------------
// compilation flags
//----------------------------------------------------------------------------

// whether debugging info is built or not
/* #undef FASTJET_ENABLE_DEBUG */

// defined if auto_ptr  is allowed (deprecated => off by default)
/* #undef FASTJET_HAVE_AUTO_PTR_INTERFACE */

// compiler supports c++14 deprecated keyword
#define FASTJET_HAVE_CXX14_DEPRECATED

// compiler supports GNU c++ deprecated attribute
/* #undef FASTJET_HAVE_GNUCXX_DEPRECATED */

// compiler supports the "override" keyword
#define FASTJET_HAVE_OVERRIDE

// compiler supports "explicit" for operators in class
#define FASTJET_HAVE_EXPLICIT_FOR_OPERATORS

// Define to 1 if you have the <execinfo.h> header file
#define FASTJET_HAVE_EXECINFO_H

// defined if demangling is enabled at configure time
// and is supported through the GNU C++ ABI
#define FASTJET_HAVE_DEMANGLING_SUPPORT

