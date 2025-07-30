#!/bin/zsh
# create a tar archive

# deduce version automatically from the appropriate include file
version=`grep 'fastjet_version = ' include/fastjet/version.hh | sed 's/.* = \"//' | sed 's/\".*//'`

origdir=`pwd | sed 's/.*\///'`
echo "Will make an archive of $origdir/"
dirhere=fastjet-release
dirtar=fastjet-$version
tarname=$dirtar.tgz
tmptarname=tmp-$tarname

# make sure we have Makefile with use CGAL=no

if [[ -e ../$tarname ]]
then
  echo "Tarfile $tarname already exists. Not proceeding."
elif [[ -e /tmp/$dirtar ]]
then
  echo "/tmp/$dirtar already exists, not proceeding"
else
  echo "Moving original Makefile out of way to make a copy with USE_CGAL = no"
  mv -v Makefile Makefile.orig
  cat Makefile.orig | sed 's/^USE_CGAL *= *yes/USE_CGAL = no/' > Makefile
  pushd ..

  echo "Creating tmp-$tarname"
  tar --exclude '.svn*' --exclude '*~' -zcf $tmptarname \
                      $dirhere/(src|include|example|plugins|)/**/*.(f90|f|h|hh|alg|c|cc|C|tex|eps|cpp) \
                      $dirhere/doc/*.(tex|eps|sty) \
                      $dirhere/(src|include|example|doc|plugins)/**/Makefile \
                      $dirhere/Makefile \
                      $dirhere/example/data/*.dat \
                      $dirhere/plugins/usage_examples/data \
                      $dirhere/include/* \
                      $dirhere/**/(README|INSTALL|Doxyfile|ReleaseNotes|COPYING) \
                      $dirhere/plugins/SISCone/siscone/doc/html/*.html \
                      $dirhere/plugins/SISCone/siscone/ChangeLog \
                      $dirhere/plugins/SISCone/siscone/examples/events/single-event.dat \
                      $dirhere/test-script.sh $dirhere/lib/.dummy \
                      $dirhere/test-script-output-orig.txt
  
  fulltarloc=`pwd`
  pushd /tmp
  echo "Unpacking it as /tmp/$dirhere"
  tar zxf $fulltarloc/$tmptarname
  mv -v /tmp/$dirhere /tmp/$dirtar
  echo "Repacking it with directory name $dirtar"
  tar zcvf $fulltarloc/$tarname $dirtar
  echo 
  echo "Removing /tmp/$dirhere"
  rm -rf $dirtar
  popd
  rm -v $tmptarname

  echo ""
    # if it's gavin running this then automatically copy the tarfile
    # to the web-space
  webdir=~salam/www/repository/software/fastjet/
  if [[ $USER = salam && -e $webdir ]]
      then
      echo "Copying .tgz file to web-site"
      cp -vp $tarname $webdir
      echo "************   Remember to edit web page **********"
  fi

  popd
  echo "Putting original Makefile back"
  mv -v Makefile.orig Makefile

  # reminders about what to do for svn
  URL=`svn info | grep URL | sed 's/^.*URL: //'`
  tagURL=`echo $URL | sed "s/trunk\/fastjet-release/tags\/fastjet-$version/"`
  echo "Remember to tag the version:"
  echo "svn mkdir $tagURL -m 'made directory for tag of release $version' "
  echo "svn copy  -m 'tagged release of release $version' $URL $tagURL/"
fi

#tar zcf $tarname


