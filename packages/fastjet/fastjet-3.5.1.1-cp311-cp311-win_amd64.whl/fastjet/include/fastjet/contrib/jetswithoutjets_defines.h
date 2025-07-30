// Required definitions for exporting static variables in windows builds.
// This is only needed for static data variables since we use
// the CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON automation when building with cmake.
// That automation handles all member functions.
// So, when making a static variable please add in the beginning of a variable
// definition, like a keyword. It is very important to use the windll export/import
// relevant to the library you are working in, see below for possibilities!
// e.g.: NSUBJETTINESS_WINDLL static bool verbosity; // inside a SomeClass.h, for instance
// Similarly for declarations you must prefix the appropriate WINDLL
// e.g. NSUBJETTINESS_WINDLL static bool SomeClass::verbosity = true; // in SomeClass.cc
#ifdef _WIN32
    #if defined(jetswithoutjets_EXPORTS) || defined(fastjetcontrib_EXPORTS)
        #define JETSWITHOUTJETS_WINDLL __declspec(dllexport) // Export when building the DLL
    #else
        #define JETSWITHOUTJETS_WINDLL __declspec(dllimport) // Import when using the DLL
    #endif
#else
    // For Linux/macOS
    #define JETSWITHOUTJETS_WINDLL
#endif
