Installation procedure:
=======================

You have two options to install the SISCone jet finder:
1. 
2. use the autotools configure/make/make install technique (recommended)
3. use the 'old-fashionned' Makefile

Installation through cmake
--------------------------

Since version 3.1.0, SISCone can be installed with CMake. 

For compilation in a build/ directory and subsequent installation, do 
```sh
cmake -S . -B build 
cmake --build build -j
cmake --install build
```

Additional options for the first step include:

- `-DCMAKE_INSTALL_PREFIX=<your-preferred-prefix>`, to change the
  default installation prefix
- `-DCMAKE_BUILD_TYPE=TYPE` where TYPE is one of `Debug`, `Release`,
  `MinSizeRel` and `RelWithDebInfo`. The default is `Release`.

Installation through autotools configure/make/make install
----------------------------------------------------------

This was the recommended method for installing the SISCone library,
headers and programs until the end of the 3.0.x series and will continue
to be supported at least throughout the 3.1.x series. 

For an 'autotools' installation process, do
```sh
./configure [--prefix=...]
make
make install
```

In short, 'configure' checks if your system has the required tools to
build SISCone, 'make' actually does the build and 'make install'
installs everything in the correct directories.

Notes:

- If you're using an svn version of SISCone, you first need to issue
  `./autogen.sh`
  (to which you can pass configure's options, see below for details)
  in order to generate the configure script from svn files. 

- The SISCone library is installed in `${prefix}/lib`, the SISCone
  development headers in `${prefix}/include/siscone` and the useful
  programs in `${prefix}/bin`. The default prefix is `/usr/local` but
  this can be changed by passing the `--prefix=<your_preferred_prefix>` 
  to the 'configure' script. Note that if you do not have sufficiently
  write access you may need to issue 'make install' as root.
  Also, if you install SISCone in a non standard location (e.g.
  /usr/local/SISCone), do not forget to append `${prefix}/lib` to your 
  LD_LIBARY_PATH.

- By default, both shared (libsiscone.so) and static (libsiscone.a)
  libraries are built and installed. You can disable one of them by
  passing `--disable-shared` or `--disable-static` to 'configure'.


Installation using the Makefiles
----------------------------------------

If you do not feel comfortable with the suggested installation
procedure, it is still possible to install it using the old-fashionned
'make' method. For that, you just need to tell 'make' to use
makefile.static as a main Makefile. This is done typing
$ make -f makefile.static

This will build the siscone library as src/libsiscone.a and the
various example programs in examples/ :
- 'siscone'  an application with options to tune it from the command line
             (see main.cpp and options.h/cpp) 
- 'sample'   another example (used in the html documentation (see doc/html))
- 'test'     a testing program (see src/test.cpp)
- 'times'    computes execution times and various statistics for 1 <= N <= 1000
- mem_check  a shell script for checking memory usage as a function of the
             number of particles (requires google perftools).
You also have access to the SISCone headers in the src folder.
