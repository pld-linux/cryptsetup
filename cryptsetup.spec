#
# Conditonal build:
%bcond_with	initrd		# don't build initrd version
%bcond_with	dietlibc	# build initrd version with static glibc instead of dietlibc
%bcond_with	passwdqc	# password quality checking via libpasswdqc [conflicts with pwquality]
%bcond_with	pwquality	# password quality checking via libpwquality [conflicts with passwdqc]
%bcond_without	python		# Python binding
%bcond_without	tests		# "make check" run

Summary:	LUKS for dm-crypt implemented in cryptsetup
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup
Name:		cryptsetup
Version:	1.7.3
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://www.kernel.org/pub/linux/utils/cryptsetup/v1.7/%{name}-%{version}.tar.xz
# Source0-md5:	7e3fdb1a1cd055cb9c5f847b15230d81
Patch0:		diet.patch
URL:		https://gitlab.com/cryptsetup/cryptsetup
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake >= 1:1.12
BuildRequires:	device-mapper-devel >= 1.02.27
BuildRequires:	gettext-tools >= 0.15
BuildRequires:	libgcrypt-devel >= 1.6.1
BuildRequires:	libgpg-error-devel
%{?with_pwquality:BuildRequires:	libpwquality-devel >= 1.0.0}
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libuuid-devel
%{?with_passwdqc:BuildRequires:	passwdqc-devel}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.7
%if %{with python}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with initrd}
BuildRequires:	libgpg-error-static
	%if %{with dietlibc}
BuildRequires:	device-mapper-dietlibc >= 1.02.27
BuildRequires:	dietlibc-static
BuildRequires:	libgcrypt-dietlibc >= 1.6.1
BuildRequires:	libuuid-dietlibc
BuildRequires:	popt-dietlibc
	%else
BuildRequires:	device-mapper-static >= 1.02.27
BuildRequires:	libgcrypt-static >= 1.6.1
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
BuildRequires:	libuuid-static
BuildRequires:	popt-static
BuildRequires:	udev-static
	%endif
%endif
Requires:	libgcrypt >= 1.6.1
%{?with_pwquality:Requires:	libpwquality >= 1.0.0}
Requires:	popt >= 1.7
Provides:	cryptsetup-luks = %{version}-%{release}
Obsoletes:	cryptsetup-luks < 1.4.1-2
%{!?with_initrd:Obsoletes:	cryptsetup-initrd < %{version}-%{release}}
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
Requires:	device-mapper-devel >= 1.02.27
Requires:	libgcrypt-devel >= 1.6.1
Provides:	cryptsetup-luks-devel = %{version}-%{release}
Obsoletes:	cryptsetup-luks-devel < 1.4.1-2

%description devel
Header files for cryptsetup library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cryptsetup.

%package static
Summary:	Static cryptsetup library
Summary(pl.UTF-8):	Statyczna biblioteka cryptsetup
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	cryptsetup-luks-static = %{version}-%{release}
Obsoletes:	cryptsetup-luks-static < 1.4.1-2

%description static
Static version of cryptsetup library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki cryptsetup.

%package -n python-pycryptsetup
Summary:	Python binding for cryptsetup library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki cryptsetup
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-pycryptsetup
Python binding for cryptsetup library.

%description -n python-pycryptsetup -l pl.UTF-8
Wiązanie Pythona do biblioteki cryptsetup.

%package initrd
Summary:	LUKS for dm-crypt implemented in cryptsetup - initrd version
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup - wersja initrd
Group:		Base
Requires:	udev-initrd >= 1:115
Provides:	cryptsetup-luks-initrd = %{version}-%{release}
Obsoletes:	cryptsetup-luks-initrd < 1.4.1-2
Conflicts:	geninitrd < 10000.10

%description initrd
This package contains implementation of LUKS for dm-crypt implemented
in cryptsetup - statically linked for initrd.

%description initrd -l pl.UTF-8
Ten pakiet zawiera implementację LUKS dla dm-crypta zaimplementowaną w
cryptsetup - wersję statycznie zlinkowaną dla initrd.

%prep
%setup -q
%{?with_diet:%patch0 -p1}

%{__rm} po/stamp-po

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
	CC="diet ${CC#ccache } %{rpmcppflags} %{rpmcflags} %{rpmldflags} -Os" \
	LIBS="-lcompat" \
	ac_cv_lib_popt_poptConfigFileToString=yes \
	ac_cv_lib_sepol_sepol_bool_set=no \
	ac_cv_lib_selinux_is_selinux_enabled=no \
%endif
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-initrd.cache \
%endif
	--disable-nls \
	--disable-silent-rules \
	--disable-shared \
	--enable-static \
	--enable-static-cryptsetup

%{__make} -C lib

%if %{with dietlibc}
# we have to do it by hand cause libtool "know better" and forces
# static libs from /usr/lib
CC="%{__cc}"
diet ${CC#ccache } %{rpmcppflags} %{rpmcflags} %{rpmldflags} -Os -I. -I./lib -static \
	-o cryptsetup-initrd src/cryptsetup.c ./lib/.libs/libcryptsetup.a \
	-lpopt -lgcrypt -lgpg-error -ldevmapper -luuid -lcompat
%else
%{__make} -C src
mv src/cryptsetup cryptsetup-initrd
%endif

%{__make} clean
%endif

%configure \
	--enable-udev \
	--disable-silent-rules \
	--enable-static \
	%{?with_passwdqc:--enable-passwdqc=/etc/passwdqc.conf} \
	%{?with_pwquality:--enable-pwquality} \
	%{?with_python:--enable-python}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

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

%{?with_python:%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/pycryptsetup.la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ README TODO docs/{ChangeLog.old,v*-ReleaseNotes,on-disk-format.pdf}
%attr(755,root,root) %{_sbindir}/cryptsetup
%attr(755,root,root) %{_sbindir}/veritysetup
%attr(755,root,root) /%{_lib}/libcryptsetup.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libcryptsetup.so.4
%{_mandir}/man8/cryptsetup.8*
%{_mandir}/man8/veritysetup.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptsetup.so
%{_libdir}/libcryptsetup.la
%{_includedir}/libcryptsetup.h
%{_pkgconfigdir}/libcryptsetup.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcryptsetup.a

%if %{with python}
%files -n python-pycryptsetup
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pycryptsetup.so
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/cryptsetup
%endif
