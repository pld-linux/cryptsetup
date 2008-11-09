#
# Conditonal build:
%bcond_without	initrd	# don't build initrd version
#
%define	realname	cryptsetup
Summary:	LUKS for dm-crypt implemented in cryptsetup
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup
Name:		cryptsetup-luks
Version:	1.0.6
Release:	4
License:	GPL v2
Group:		Base
Source0:	http://luks.endorphin.org/source/%{realname}-%{version}.tar.bz2
# Source0-md5:	00d452eb7a76e39f5749545d48934a10
Patch1:		%{name}-nostatic.patch
URL:		http://luks.endorphin.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
BuildRequires:	gettext-devel
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	popt-devel
%if %{with initrd}
BuildRequires:	device-mapper-static >= 1.02.07
BuildRequires:	libgcrypt-static >= 1.1.42
BuildRequires:	libgpg-error-static
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
BuildRequires:	libuuid-static
BuildRequires:	popt-static
%endif
Provides:	cryptsetup = %{version}
Obsoletes:	cryptsetup
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_noautoreqdep	libcryptsetup.so.0

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
Group:		Base

%description initrd
This package contains implementation of LUKS for dm-crypt implemented
in cryptsetup - staticaly linked for initrd.

%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%if %{with initrd}
%configure \
	--enable-static \
	--enable-static-cryptsetup
%{__make}
mv src/cryptsetup cryptsetup-initrd
%{__make} clean
%endif

%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcryptsetup.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so

%if %{with initrd}
install cryptsetup-initrd $RPM_BUILD_ROOT%{_sbindir}
%endif

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
%attr(755,root,root) %ghost /%{_lib}/libcryptsetup.so.0
%{_mandir}/man8/cryptsetup.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptsetup.so
%{_libdir}/libcryptsetup.la
%{_includedir}/libcryptsetup.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcryptsetup.a

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/cryptsetup-initrd
%endif
