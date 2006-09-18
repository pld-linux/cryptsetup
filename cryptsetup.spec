#
# Conditonal build:
%bcond_with	static	# link cryptsetup statically
#
Summary:	LUKS for dm-crypt implemented in cryptsetup
Summary(pl):	LUKS dla dm-crypta zaimplementowany w cryptsetup
Name:		cryptsetup-luks
Version:	1.0.3
Release:	1
License:	GPL
Group:		Base
Source0:	http://luks.endorphin.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	e134b82b4706a28ba1d73b9176d5ad0c
Patch0:		%{name}-sepol.patch
Patch1:		%{name}-nostatic.patch
URL:		http://luks.endorphin.org/about
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
BuildRequires:	gettext-devel
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
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
Provides:	cryptsetup = 0.2-1.pre1.8
Obsoletes:	cryptsetup
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

%description -l pl
LUKS to nadchodz±cy standard linuksowego szyfrowania twardego dysku.
Dostarczaj±c standardowy format danych na dysku nie tylko u³atwia
utrzymanie kompatybilno¶ci miêdzy dystrybucjami, ale tak¿e dostarcza
bezpieczne zarz±dzanie wieloma has³ami u¿ytkowników. W przeciwieñstwie
do istniej±cego rozwi±zania LUKS przechowuje wszystkie potrzebne
informacje o konfiguracji w nag³ówku partycji, pozwalaj±c
u¿ytkownikowi przenosiæ lub migrowaæ dane w sposób przezroczysty.

Ten pakiet zawiera implementacjê LUKS dla dm-crytpa zaimplementowan± w
cryptsetup.

%package devel
Summary:	Header files for cryptsetup library
Summary(pl):	Pliki nag³ówkowe biblioteki cryptsetup
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	device-mapper-devel
Requires:	libgcrypt-devel >= 1.1.42
Provides:	cryptsetup-devel
Obsoletes:	cryptsetup-devel

%description devel
Header files for cryptsetup library.

%description devel -l pl
Pliki nag³ówkowe biblioteki cryptsetup.

%package static
Summary:	Static cryptsetup library
Summary(pl):	Statyczna biblioteka cryptsetup
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	cryptsetup-static
Obsoletes:	cryptsetup-static

%description static
Static version of cryptsetup library.

%description static -l pl
Statyczna wersja biblioteki cryptsetup.

%prep
%setup -q
%patch0 -p1
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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
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
