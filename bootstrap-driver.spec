### RPM external bootstrap-driver 40.0
## NOCOMPILER
Requires: rpm
BuildRequires: cms-common fakesystem

#danger! cms-common version is now hardwired below (and in bootstrap.file)

%prep
%build
%install
packageList=""
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            toolversion=$(eval echo $`echo ${toolcap}_VERSION`)
            toolrevision=$(eval echo $`echo ${toolcap}_REVISION`)
            echo $toolversion $toolrevision
            packageList="$packageList external+${tool}+${toolversion}-1-${toolrevision}.%cmsplatf.rpm"
        ;;
    esac
done

additionalProvides=""
##############################
# Packages to seed for runtime
##############################
platformSeeds="bash tcsh bzip2-libs glibc nspr nss nss-util popt zlib glibc-devel openssl openssl-devel openssl-libs krb5-libs
               libcom_err libX11 libXext libXft libXpm libglvnd-glx libglvnd-opengl mesa-libGLU"
# Needed by python runtime
platformSeeds+=" readline ncurses-libs tcl tk"
# Seed packages which provides these
packagesWithProvides="/usr/bin/python3 /usr/bin/perl /usr/bin/env /usr/bin/uname"

##############################
#Packages to seed for build
##############################
platformBuildSeeds="git patch perl make zip unzip bzip2 java-1.8.0-openjdk-devel libcom_err-devel which libXpm-devel libXft-devel mesa-libGLU-devel rsync"
#Needed by autotools,go and lcov
platformBuildSeeds+=" perl-Carp perl-PathTools perl-Data-Dumper perl-Exporter perl-File-Path perl-PathTools perl-File-Temp perl-Getopt-Long perl-Text-ParseWords
                      perl-constant perl-PathTools perl-PathTools perl-Digest-MD5 perl-File-Path perl-PathTools perl-File-Temp perl-Getopt-Long"
#needed by python build
platformBuildSeeds+=" readline-devel ncurses-devel tcl-devel tk-devel"
packagesWithBuildProvides=""

case %cmsplatf in
*_aarch64_* )
  ;;
*)
  # Needed by oracle
  platformSeeds+=" libaio"
  ;;
esac

case %cmsplatf in
cc* )
  platformSeeds+=" libxcrypt perl-IO perl-Memoize perl-libnet perl-Term-ANSIColor perl-libs"
  ;;
slc*)
  platformSeeds+=" perl-Switch"
  ;;
esac

defaultPkgs="cms+cms-common+1.0 cms+fakesystem+1.0"

mkdir -p %{i}/etc/profile.d
(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"\""; \
 echo "unsupportedSeeds=\"\""; \
 echo "%{cmsos}_platformSeeds=\"$platformSeeds\""; \
 echo "%{cmsos}_platformBuildSeeds=\"$platformBuildSeeds\""; \
 echo "%{cmsos}_packagesWithProvides=\"$packagesWithProvides\""; \
 echo "%{cmsos}_packagesWithBuildProvides=\"$packagesWithBuildProvides\""; \
 echo "packageList=\"$packageList\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt

cp %{i}/%{cmsplatf}-driver.txt %{i}/%{cmsplatf}-driver-comp.txt
