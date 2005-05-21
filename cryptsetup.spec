#
# todo:
# - static library
#
Summary:	LUKS for dm-crypt implemented in cryptsetup
Name:		cryptsetup-luks
Version:	1.0
Release:	0.2
License:	GPL
Group:		Base
Source0:	http://luks.endorphin.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	62c4bff081e470fb2c9a0f2cb890e613
URL:		http://luks.endorphin.org/about
BuildRequires:	device-mapper-devel
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libuuid-devel
BuildRequires:	popt-devel
Obsoletes:	cryptsetup
Provides:	cryptsetup
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

%package devel
Summary:	Header files for cryptsetup library
Summary(pl):	Pliki nag³ówkowe biblioteki cryptsetup
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	device-mapper-devel
Requires:	libgcrypt-devel >= 1.1.42
Obsoletes:	cryptsetup-devel
Provides:	cryptsetup-devel

%description devel
Header files for cryptsetup library.

%description devel -l pl
Pliki nag³ówkowe biblioteki cryptsetup.

%package static
Summary:	Static cryptsetup library
Summary(pl):	Statyczna biblioteka cryptsetup
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of cryptsetup library.

%description static -l pl
Statyczna wersja biblioteki cryptsetup.

%prep
%setup -q

%build
%configure
#	--enable-static
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
#%{_libdir}/libcryptsetup.a
