#!/bin/bash
# Run this to generate all the initial makefiles, etc.
#

# This script automatically runs configure with whatever command-line
# options are passed. If you don't like this, run it with
#
# NOCONFIGURE=true ./autogen.sh
#
#
# NB: you are advised to have recent versions of autoconf, libtool and
# automake; if you run into problems; first download and compile all
# the recent versions of the autotools programs, and then try again...
#
# Earliest version that have been found to work are:
#   automake: 1.9.2
#   autoconf: 2.59
#   libtool:  1.5.6
# (i.e. SLC4 on lxplus)
#

srcdir=`dirname $0`
PKG_NAME="FastJet"

DIE=0

# set the libtool program to be used
LIBTOOL=libtool
LIBTOOLIZE=libtoolize

# change executable names when running on Macs
# if test x`uname` = xDarwin; then
if [ `uname` == "Darwin" ]; then
  echo "Detected Mac OSX"
  if [ x$(which glibtool) == "x" ]; then    
    echo ""
    echo "On Mac OSX, $0 requires the GNU libtool and libtoolize scripts,"
    echo "renamed glibtol and glibtoolize respectively by Apple to avoid"
    echo "conflict with Apple-provided libtool."
    echo ""
    echo "They should be already installed, together with Apple developer tools,"
    echo "in /usr/bin. If you see this message, they are not."
    echo ""
    echo "The GNU version can be retrieved from http://ftp.gnu.org/gnu/libtool/."
    echo "If they are (re)installed from sources in a different location,"
    echo "autogen.sh should then be modified accordingly."
    exit
  fi
  LIBTOOL=glibtool
  LIBTOOLIZE=glibtoolize
fi

# check that all utilities needed by configure.ac are present
(autoconf --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: You must have \`autoconf' installed."
  echo "Download the appropriate package for your distribution,"
  echo "or get the source tarball at ftp://ftp.gnu.org/pub/gnu/"
  DIE=1
}

(grep "^AC_PROG_LIBTOOL" $srcdir/configure.ac >/dev/null) && {
  ($LIBTOOLIZE --version) < /dev/null > /dev/null 2>&1 || {
    echo
    echo "**Error**: You must have \`libtool' installed."
    echo "Get ftp://ftp.gnu.org/pub/gnu/libtool-1.2d.tar.gz"
    echo "(or a newer version if it is available)"
    DIE=1
  }
}

grep "^AM_GNU_GETTEXT" $srcdir/configure.ac >/dev/null && {
  grep "sed.*POTFILES" $srcdir/configure.ac >/dev/null || \
  (gettext --version) < /dev/null > /dev/null 2>&1 || {
    echo
    echo "**Error**: You must have \`gettext' installed."
    echo "Get ftp://alpha.gnu.org/gnu/gettext-0.10.35.tar.gz"
    echo "(or a newer version if it is available)"
    DIE=1
  }
}

(automake --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: You must have \`automake' installed."
  echo "Get ftp://ftp.gnu.org/pub/gnu/automake-1.3.tar.gz"
  echo "(or a newer version if it is available)"
  DIE=1
  NO_AUTOMAKE=yes
}


# if no automake, don't bother testing for aclocal
test -n "$NO_AUTOMAKE" || (aclocal --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: Missing \`aclocal'.  The version of \`automake'"
  echo "installed doesn't appear recent enough."
  echo "Get ftp://ftp.gnu.org/pub/gnu/automake-1.3.tar.gz"
  echo "(or a newer version if it is available)"
  DIE=1
}

# if something is missing, quit
if test "$DIE" -eq 1; then
  exit 1
fi

# check for the command line arguments and warn if none is present
if test -z "$*" && test x$NOCONFIGURE == x; then
  echo "**Warning**: I am going to run \`configure' with no arguments."
  echo "If you wish to pass any to it, please specify them on the"
  echo \`$0\'" command line."
  echo
fi

case $CC in
xlc )
  am_opt=--include-deps;;
esac

# recursively generate configure & makefile.in for all configure.ac found
#
# alternative where SISCone is built directly from the FastJet build systen
# for coin in $srcdir
for coin in $srcdir `find $srcdir/plugins -name configure.ac -print`
do 
  dr=`dirname $coin`
  if test -f $dr/NO-AUTO-GEN; then
    echo skipping $dr -- flagged as no auto-gen
  else
    echo processing $dr
    #macrodirs=`sed -n -e 's,AM_ACLOCAL_INCLUDE(\(.*\)),\1,gp' < $coin`
    macrodirs="m4"
    ( cd $dr
      aclocalinclude="$ACLOCAL_FLAGS"
      for k in $macrodirs; do
  	if test -d $k; then
          aclocalinclude="$aclocalinclude -I $k"
  	##else 
	##  echo "**Warning**: No such directory \`$k'.  Ignored."
        fi
      done
      if grep "^AM_GNU_GETTEXT" configure.ac >/dev/null; then
	if grep "sed.*POTFILES" configure.ac >/dev/null; then
	  : do nothing -- we still have an old unmodified configure.ac
	else
	  echo "Creating $dr/aclocal.m4 ..."
	  test -r $dr/aclocal.m4 || touch $dr/aclocal.m4
	  echo "Running gettextize...  Ignore non-fatal messages."
	  echo "no" | gettextize --force --copy
	  echo "Making $dr/aclocal.m4 writable ..."
	  test -r $dr/aclocal.m4 && chmod u+w $dr/aclocal.m4
        fi
      fi
      if grep "^AM_GNOME_GETTEXT" configure.ac >/dev/null; then
	echo "Creating $dr/aclocal.m4 ..."
	test -r $dr/aclocal.m4 || touch $dr/aclocal.m4
	echo "Running gettextize...  Ignore non-fatal messages."
	echo "no" | gettextize --force --copy
	echo "Making $dr/aclocal.m4 writable ..."
	test -r $dr/aclocal.m4 && chmod u+w $dr/aclocal.m4
      fi
      if grep "^AC_PROG_LIBTOOL" configure.ac >/dev/null; then
	echo "Running libtoolize..."
	$LIBTOOLIZE --force --copy
      fi
      echo "Running aclocal $aclocalinclude ..."
      aclocal $aclocalinclude
      #if grep "^AM_CONFIG_HEADER" configure.ac >/dev/null; then
      #	echo "Running autoheader..."
      #  autoheader
      #fi
      echo "Running automake --gnu $am_opt ..."
      automake --add-missing --gnu $am_opt
      echo "Running autoconf ..."
      autoconf
    )
  fi
done

#conf_flags="--enable-maintainer-mode --enable-compile-warnings" #--enable-iso-c

# run configure
if test x$NOCONFIGURE = x; then
  echo Running $srcdir/configure $conf_flags "$@" ...
  $srcdir/configure $conf_flags "$@" \
  && echo Now type \`make\' to compile $PKG_NAME
else
  echo Skipping configure process.
fi
