Installation instructions for FastJet with CMake
================================================

## Downloading FastJet

FastJet can be obtained as a tarball (replace `X.Y.Z` with the version number you want)

```
wget https://fastjet.fr/repo/fastjet-X.Y.Z.tar.gz
tar zxvf fastjet-X.Y.Z.tar.gz
cd fastjet-X.Y.Z/
```

or from git

```
git clone --recursive https://gitlab.com/fastjet/fastjet.git
cd fastjet/
```

## Basic build instructions

To configure, build, test and install using a directory called `build/`,
do the following
```
cmake -S . -B build
cmake --build build -j
ctest --test-dir build -V
cmake --install build
```

## CMake build options

The following options can be added to the `cmake -S . -B build` invocation

* `-DCMAKE_INSTALL_PREFIX=/install/path`: sets the installation path

* `-DFASTJET_ENABLE_CGAL=ON`: enables CGAL-based strategies, e.g. NlnN
  strategy for the pp kt algorithm

* `-DFASTJET_ENABLE_PYTHON=ON`: turns on the build of the Python
  interface. In contrast with autotools python support, swig is always
  required, in contrast to the autotools build system, where in standard
  FastJet release tarballs it is optional.

* `-DCMAKE_BUILD_TYPE=TYPE` where TYPE is one of `Debug`, `Release`,
  `MinSizeRel` and `RelWithDebInfo`. The default is `Release`. Note that
  some C++ compilation options get set separately.

* `-DFASTJET_ENABLE_DEBUG=ON/OFF`: sets debug flag separately from CMAKE_BUILD_TYPE

* Individual plugins can be turned on/off with 
  * `-DFASTJET_ENABLE_PLUGIN_EECAMBRIDGE=ON/OFF` (default `ON`)
  * `-DFASTJET_ENABLE_PLUGIN_JADE=ON/OFF` (default `ON`)
  * `-DFASTJET_ENABLE_PLUGIN_NESTEDDEFS=ON/OFF` (default `ON`)
  * `-DFASTJET_ENABLE_PLUGIN_SISCONE=ON/OFF` (default `ON`)
  * `-DFASTJET_ENABLE_PLUGIN_CDFCONES=ON/OFF` (default `ON`)
  * `-DFASTJET_ENABLE_PLUGIN_D0RUNICONE=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_D0RUNIICONE=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_ATLASCONE=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_CMSITERATIVECONE=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_PXCONE=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_TRACKJET=ON/OFF` (default `OFF`)
  * `-DFASTJET_ENABLE_PLUGIN_GRIDJET=ON/OFF` (default `ON`)

* It is also possible to enable all C++ plugins
  `-DFASTJET_ENABLE_ALLCXXPLUGINS=ON` (all plugins except PxCone, which
  is in Fortran), or all plugins with `-DFASTJET_ENABLE_ALLPLUGINS=ON`.

Further options can be explored by running `cmake -LAH -S . -B build`
from the main directory.

## Using FastJet as built with CMake

When building your own code that links with FastJet there are two
recommended ways to access the libraries

### With `fastjet-config`

This is the best if you are building your code with Makefiles or
manually. The `fastjet-config` program should have been installed and
provides access to the include paths, and libraries. E.g., assuming it
is in your path

```
c++ myprog.cc $(fastjet-config --cxxflags --libs --plugins) -o myprog
```

Call `fastjet-config -h` to see further options.

### With `CMake`

If you installed to a standard location, then in your `CMakeLists.txt` file, do the
following

```
find_package(fastjet 3.5.0 REQUIRED)
target_link_libraries(myprog PRIVATE fastjet::fastjet fastjet::fastjettools fastjet::fastjetplugins)
```
and your program `myprog` should automatically get the includes and
libraries needed. 

If you installed to a non-standard location you may need to set the
`CMAKE_PREFIX_PATH` environment variable, e.g.
```
export CMAKE_PREFIX_PATH=$(fastjet-config --prefix)/lib/cmake:$CMAKE_PREFIX_PATH
```