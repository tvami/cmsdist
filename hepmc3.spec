### RPM external hepmc3 3.2.5

Source: https://gitlab.cern.ch/hepmc/HepMC3/-/archive/3.2.5/HepMC3-%{realversion}.tar.gz

BuildRequires: cmake

%define drop_files %i/share

%prep
%setup -q -n HepMC3-%{realversion}

%build
sed 's/SOVERSION 3//' < CMakeLists.txt > tmpsed.txt
mv tmpsed.txt CMakeLists.txt
cd search
sed 's/SOVERSION 4//' < CMakeLists.txt > tmpsed.txt
mv tmpsed.txt CMakeLists.txt
cd ..
rm -rf ../build
mkdir ../build
cd ../build

cmake ../HepMC3-%{realversion} \
  -DHEPMC3_ENABLE_ROOTIO:BOOL=OFF -DHEPMC3_ENABLE_TEST:BOOL=OFF \
  -DHEPMC3_INSTALL_INTERFACES:BOOL=ON -DHEPMC3_ENABLE_PYTHON:BOOL=OFF \
  -DHEPMC3_BUILD_STATIC_LIBS:BOOL=OFF -DHEPMC3_BUILD_DOCS:BOOL=OFF \
  -DCMAKE_INSTALL_PREFIX:PATH="%i"

make %{makeprocesses}

%install
cd ../build
make install
