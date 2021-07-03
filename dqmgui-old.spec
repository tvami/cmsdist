### RPM cms dqmgui-old 9.6.0
## INITENV +PATH PATH %i/xbin
## INITENV +PATH %{dynamic_path_var} %i/xlib
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON27PATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON27PATH $ROOT_ROOT/lib

%define tag 367e291d35a6b872a8c336327fcbca4a821732c6
%define branch main

%define github_user cms-sw
Source0: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source1: svn://rotoglup-scratchpad.googlecode.com/svn/trunk/rtgu/image?module=image&revision=10&scheme=http&output=/rtgu.tar.gz
Source2: http://opensource.adobe.com/wiki/download/attachments/3866769/numeric.tar.gz
Patch0: dqmgui-rtgu

Requires: python yui extjs gmake pcre boost root rootjs libpng libjpeg-turbo rotatelogs py2-pycurl py2-python-cjson libuuid d3 protobuf py2-argparse py2-pytest py2-nose jemalloc
Requires: py2-CherryPy py2-Cheetah classlib-full

%prep
# Unpack sources.
%setup -c -D -T -a 1 -n stuff/rtgu
%patch0 -p1
%setup -c -D -T -a 2 -n stuff/boost/gil/extension
perl -p -i -e '/#include/ && s|\.\./\.\./|boost/gil/|' $(find . -name *.hpp)
chmod 644 $(find . -name *.hpp)

%setup -T -b 0 -n %{n}-%{realversion}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/*/conf.py
# Adapt CMSSW sources to our build.
cp -pr %_builddir/stuff/{rtgu,boost} src/cpp
# Generate makefile fragment for externals.
libs=". %i/128/xlib %i/128/lib"
incs=". %i/128/xinclude %i/128/include"
dirs="$CLASSLIB_FULL_ROOT $BOOST_ROOT $PYTHON_ROOT $ROOT_ROOT
      $ZLIB_ROOT $PCRE_ROOT $LIBPNG_ROOT $LIBJPEG_TURBO_ROOT $PROTOBUF_ROOT $JEMALLOC_ROOT"
for d in $dirs; do
  if [ -e $d/lib ] ; then libs="$libs $d/lib" ; fi
  if [ -e $d/lib64 ] ; then libs="$libs $d/lib64" ; fi
  case $d in
    $PYTHON_ROOT )
      incs="$incs $d/include/python2.7" ;;
    * )
      incs="$incs $d/include" ;;
  esac
done

cat > etc/makefile.ext <<- EOF
 INCLUDE_DIRS = $incs
 LIBRARY_DIRS = $libs
EOF

# Build
%build
python setup.py -v build_system -s DQM -d

# Install
%install
mkdir -p %i/{128,}/etc/profile.d %i/128/{x,}{bin,lib,include,data} %i/128/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s DQM --prefix=%i/128
find %i/128 -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/128/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/128/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export YUI_ROOT EXTJS_ROOT D3_ROOT ROOTJS_ROOT;"
 echo "export DQMGUI_VERSION='%{realversion}';" # for visDQMUpload
 echo "export LD_PRELOAD=$JEMALLOC_ROOT/lib/libjemalloc.so.`jemalloc-config --revision`"
 echo "export MONITOR_ROOT='%i';") > %i/128/etc/profile.d/env.sh

%post
%{relocateConfig}/128/etc/makefile.ext
%{relocateConfig}/128/etc/profile.d/{env,dep*}.*sh
cp $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.*sh $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d
perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/128|g" $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d/env.*sh
perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/128|g" $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d/init.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/128/doc
