### RPM external classlib-full 3.1.3
%define tag 9226fd576b0d01417b4bc618577b8d8e32ea3606
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/classlib.git?obj=%{branch}/%{tag}&export=classlib-%{realversion}&output=/classlib-%{realversion}.tgz

Requires: bz2lib 
Requires: pcre 
Requires: xz
Requires: zlib 

%prep
%setup -n classlib-%realversion

%build
# Update to get aarch64 and ppc64le
rm -f ./cfg/config.{sub,guess}
%get_config_guess ./cfg/config.guess
%get_config_sub ./cfg/config.sub
chmod +x ./cfg/config.{sub,guess}

./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-lzma-includes=$XZ_ROOT/include         \
  --with-lzma-libraries=$XZ_ROOT/lib

perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses CXXFLAGS="-Wno-error=extra -ansi -pedantic -W -Wall -Wno-long-long -Werror"

%install
make %makeprocesses install
