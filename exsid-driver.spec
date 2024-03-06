#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Simple I/O library for exSID USB
Summary(pl.UTF-8):	Prosta biblioteka we/wy do przystawki exSID USB
Name:		exsid-driver
Version:	2.1
Release:	1
License:	GPL v2
Group:		Libraries
#Source0Download: https://github.com/libsidplayfp/exsid-driver/tags
Source0:	https://github.com/libsidplayfp/exsid-driver/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4025bdcccd6c430594b8abbd655abda9
#Patch0:	%{name}-what.patch
URL:		https://github.com/libsidplayfp/exsid-driver
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%if %{with apidocs}
BuildRequires:	doxygen
%endif
BuildRequires:	libftdi1-devel >= 1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple I/O library for exSID USB.

%description -l pl.UTF-8
Prosta biblioteka we/wy do przystawki exSID USB.

%package devel
Summary:	Header files for exsid library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki exsid
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for exsid library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki exsid.

%package static
Summary:	Static exsid library
Summary(pl.UTF-8):	Statyczna biblioteka exsid
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static exsid library.

%description static -l pl.UTF-8
Statyczna biblioteka exsid.

%package apidocs
Summary:	API documentation for exsid library
Summary(pl.UTF-8):	Dokumentacja API biblioteki exsid
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for exsid library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki exsid.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libexsid.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libexsid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexsid.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexsid.so
%{_includedir}/exSID.h
%{_pkgconfigdir}/libexsid.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexsid.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*.{css,html,js,png}
%endif
