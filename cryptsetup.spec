#
# Conditonal build:
%bcond_without	initrd		# don't build initrd version
%bcond_without	dietlibc	# build initrd version with static glibc instead of dietlibc

%define		realname	cryptsetup
Summary:	LUKS for dm-crypt implemented in cryptsetup
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup
Name:		cryptsetup-luks
Version:	1.1.3
Release:	1
License:	GPL v2
Group:		Base
Source0:	http://cryptsetup.googlecode.com/files/%{realname}-%{version}.tar.bz2
# Source0-md5:	318a64470861ea5b92a52f2014f1e7c1
Source1:	%{name}-initramfs-root-conf
Source2:	%{name}-initramfs-root-hook
Source3:	%{name}-initramfs-root-local-top
Source4:	%{name}-initramfs-passdev-hook
Source5:	%{name}-initramfs-README
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-diet.patch
URL:		http://code.google.com/p/cryptsetup/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	device-mapper-devel >= 1.02.03
BuildRequires:	gettext-devel >= 0.15
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	popt-devel >= 1.7
%if %{with initrd}
BuildRequires:	libgpg-error-static
	%if %{with dietlibc}
BuildRequires:	device-mapper-dietlibc
BuildRequires:  dietlibc-static
BuildRequires:	libgcrypt-dietlibc
BuildRequires:	libuuid-dietlibc
BuildRequires:	popt-dietlibc
	%else
BuildRequires:	device-mapper-static >= 1.02.07
BuildRequires:	libgcrypt-static >= 1.1.42
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
BuildRequires:	libuuid-static
BuildRequires:	popt-static
	%endif
%endif
Requires:	popt >= 1.7
Provides:	cryptsetup = %{version}
Obsoletes:	cryptsetup
Conflicts:	udev < 1:118-1
Conflicts:	udev-core < 1:115
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
LUKS is the upcoming standard for Linux hard disk encryption. By
providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS
stores all setup necessary setup information in the partition header,
enabling the user to transport or migrate his data seamlessly.

This package contains implementation of LUKS for dm-crypt implemented
in cryptsetup.

%description -l pl.UTF-8
LUKS to nadchodzący standard linuksowego szyfrowania twardego dysku.
Dostarczając standardowy format danych na dysku nie tylko ułatwia
utrzymanie kompatybilności między dystrybucjami, ale także dostarcza
bezpieczne zarządzanie wieloma hasłami użytkowników. W przeciwieństwie
do istniejącego rozwiązania LUKS przechowuje wszystkie potrzebne
informacje o konfiguracji w nagłówku partycji, pozwalając
użytkownikowi przenosić lub migrować dane w sposób przezroczysty.

Ten pakiet zawiera implementację LUKS dla dm-crytpa zaimplementowaną w
cryptsetup.

%package devel
Summary:	Header files for cryptsetup library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cryptsetup
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	device-mapper-devel
Requires:	libgcrypt-devel >= 1.1.42
Obsoletes:	cryptsetup-devel

%description devel
Header files for cryptsetup library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cryptsetup.

%package static
Summary:	Static cryptsetup library
Summary(pl.UTF-8):	Statyczna biblioteka cryptsetup
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	cryptsetup-static

%description static
Static version of cryptsetup library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki cryptsetup.

%package initrd
Summary:	LUKS for dm-crypt implemented in cryptsetup - initrd version
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup - wersja initrd
Group:		Base
Requires:	udev-initrd >= 1:115
Conflicts:	geninitrd < 10000.10

%description initrd
This package contains implementation of LUKS for dm-crypt implemented
in cryptsetup - statically linked for initrd.

%description initrd -l pl.UTF-8
Ten pakiet zawiera implementację LUKS dla dm-crypta zaimplementowaną
w cryptsetup - wersję statycznie zlinkowaną dla initrd.

%package initramfs
Summary:	LUKS for dm-crypt implemented in cryptsetup - support scripts for initramfs-tools
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup - skrypty dla initramfs-tools
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	initramfs-tools

%description initramfs
LUKS for dm-crypt implemented in cryptsetup - support scripts
for initramfs-tools.

%description initramfs -l pl.UTF-8
LUKS dla dm-crypta zaimplementowany w cryptsetup - skrypty dla
initramfs-tools.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1

cp -a %{SOURCE5} README.initramfs

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%if %{with initrd}
CC="%{__cc}"
%configure \
%if %{with dietlibc}
%configure \
	CC="diet ${CC#ccache } %{rpmcflags} %{rpmldflags} -Os" \
	ac_cv_lib_popt_poptConfigFileToString=yes \
	ac_cv_lib_sepol_sepol_bool_set=no \
	ac_cv_lib_selinux_is_selinux_enabled=no \
%endif
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-initrd.cache \
%endif
	--disable-shared-library \
	--enable-static \
	--enable-static-cryptsetup \
	--disable-nls

%{__make} -C luks
%{__make} -C lib

%if %{with dietlibc}
# we have to do it by hand cause libtool "know better" and forces
# static libs from /usr/lib
CC="%{__cc}"
diet ${CC#ccache } %{rpmcflags} %{rpmldflags} -Os -I. -I./lib -static \
	-o cryptsetup-initrd src/cryptsetup.c ./lib/.libs/libcryptsetup.a \
	-lpopt -lgcrypt -lgpg-error -ldevmapper -luuid -lcompat
%else
%{__make} -C src
mv src/cryptsetup cryptsetup-initrd
%endif

%{__make} clean
%endif

%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/{conf-hooks.d,hooks,scripts/local-top}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcryptsetup.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install -p cryptsetup-initrd $RPM_BUILD_ROOT%{_libdir}/initrd/cryptsetup
%endif

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/conf-hooks.d/cryptsetup
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/hooks/cryptroot
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/local-top/cryptroot
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/hooks/cryptpassdev

%find_lang %{realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_sbindir}/cryptsetup
%attr(755,root,root) /%{_lib}/libcryptsetup.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libcryptsetup.so.1
%{_mandir}/man8/cryptsetup.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptsetup.so
%{_libdir}/libcryptsetup.la
%{_includedir}/libcryptsetup.h
%{_pkgconfigdir}/libcryptsetup.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcryptsetup.a

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/cryptsetup
%endif

%files initramfs
%defattr(644,root,root,755)
%doc README.initramfs
%attr(755,root,root) %{_datadir}/initramfs-tools/conf-hooks.d/cryptsetup
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/cryptroot
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/cryptpassdev
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-top/cryptroot
