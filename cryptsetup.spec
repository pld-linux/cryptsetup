#
# Conditonal build:
%bcond_with	static	# link cryptsetup statically
#
%define	_realname	cryptsetup
Summary:	LUKS for dm-crypt implemented in cryptsetup
Summary(pl.UTF-8):	LUKS dla dm-crypta zaimplementowany w cryptsetup
Name:		cryptsetup-luks
Version:	1.0.5
Release:	2
License:	GPL
Group:		Base
Source0:	http://luks.endorphin.org/source/%{_realname}-%{version}.tar.bz2
# Source0-md5:	0aa2f94c39123f1a0352983e5366179c
Patch1:		%{name}-nostatic.patch
URL:		http://luks.endorphin.org/about
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
%if %{with static}
BuildRequires:	device-mapper-static >= 1.02.07
BuildRequires:	libgcrypt-static >= 1.1.42
BuildRequires:	libgpg-error-static
BuildRequires:	libselinux-static
BuildRequires:	libsepol-static
BuildRequires:	libuuid-static
BuildRequires:	popt-static
%endif
Provides:	cryptsetup = 1.0.5
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

%prep
%setup -q -n %{_realname}-%{version}
%patch1 -p1

%build
%{__gettextize}
%{__autoheader}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-static \
	%{?with_static:--enable-static-cryptsetup}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so.*.*.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib}; echo libcryptsetup.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcryptsetup.so

%find_lang %{_realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_sbindir}/cryptsetup
%attr(755,root,root) /%{_lib}/libcryptsetup.so.*.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptsetup.so
%{_libdir}/libcryptsetup.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcryptsetup.a
