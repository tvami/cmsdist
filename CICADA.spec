### RPM external CICADA 1.0.0
Source: https://github.com/cms-hls4ml/%{n}/archive/refs/tags/v%{realversion}.tar.gz
Requires: hls4mlEmulatorExtras
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT}

%install
make PREFIX=%{i} install EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT}

