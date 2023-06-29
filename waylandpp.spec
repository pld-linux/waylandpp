#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API documentation

Summary:	Wayland C++ bindings
Name:		waylandpp
Version:	1.0.0
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://github.com/NilsBrause/waylandpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2b0892152599210e9797a0651a119f65
Patch0:		gcc-13.patch
URL:		https://nilsbrause.github.io/waylandpp_docs/
BuildRequires:	cmake >= 3.4
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	pkgconfig
BuildRequires:	pugixml-devel >= 1.4
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	wayland-devel >= 1.11.0
BuildRequires:	wayland-egl-devel
Requires:	wayland >= 1.11.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# project claims missing symbols are intentional and even tries to
# remove -Wl,--no-undefined from linker flags
%define		no_install_post_check_so	1

%description
The goal of this library is to create such a C++ binding for Wayland
using the most modern C++ technology currently available, providing an
easy to use C++ API to Wayland.

%package devel
Summary:	Header files for Waylandpp libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pugixml >= 1.4
Requires:	wayland-devel >= 1.11.0
Requires:	wayland-egl-devel

%description devel
Header files for Waylandpp libraries.

%package apidocs
Summary:	Waylandpp API documentation
Group:		Documentation
BuildArch:	noarch

%description apidocs
Waylandpp API documentation.

%prep
%setup -q
%patch0 -p1

%build
%cmake -B build \
	%{cmake_on_off apidocs BUILD_DOCUMENTATION}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libwayland-client++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-client++.so.1
%attr(755,root,root) %{_libdir}/libwayland-client-extra++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-client-extra++.so.1
%attr(755,root,root) %{_libdir}/libwayland-client-unstable++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-client-unstable++.so.1
%attr(755,root,root) %{_libdir}/libwayland-cursor++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-cursor++.so.1
%attr(755,root,root) %{_libdir}/libwayland-egl++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-egl++.so.1
%attr(755,root,root) %{_libdir}/libwayland-server++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-server++.so.1
%attr(755,root,root) %{_libdir}/libwayland-server-extra++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-server-extra++.so.1
%attr(755,root,root) %{_libdir}/libwayland-server-unstable++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-server-unstable++.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wayland-scanner++
%attr(755,root,root) %{_libdir}/libwayland-client++.so
%attr(755,root,root) %{_libdir}/libwayland-client-extra++.so
%attr(755,root,root) %{_libdir}/libwayland-client-unstable++.so
%attr(755,root,root) %{_libdir}/libwayland-cursor++.so
%attr(755,root,root) %{_libdir}/libwayland-egl++.so
%attr(755,root,root) %{_libdir}/libwayland-server++.so
%attr(755,root,root) %{_libdir}/libwayland-server-extra++.so
%attr(755,root,root) %{_libdir}/libwayland-server-unstable++.so
%dir %{_datadir}/waylandpp
%dir %{_datadir}/waylandpp/protocols
%{_datadir}/waylandpp/protocols/*.xml
%{_includedir}/wayland-client*.hpp
%{_includedir}/wayland-cursor.hpp
%{_includedir}/wayland-egl.hpp
%{_includedir}/wayland-server*.hpp
%{_includedir}/wayland-util.hpp
%{_includedir}/wayland-version.hpp
%{_libdir}/cmake/waylandpp
%{_pkgconfigdir}/wayland-client++.pc
%{_pkgconfigdir}/wayland-client-extra++.pc
%{_pkgconfigdir}/wayland-client-unstable++.pc
%{_pkgconfigdir}/wayland-cursor++.pc
%{_pkgconfigdir}/wayland-egl++.pc
%{_pkgconfigdir}/wayland-scanner++.pc
%{_pkgconfigdir}/wayland-server++.pc
%{_pkgconfigdir}/wayland-server-extra++.pc
%{_pkgconfigdir}/wayland-server-unstable++.pc
%if %{with apidocs}
%{_mandir}/man3/wayland_*.3*
%{_mandir}/man3/wayland-client.hpp.3*
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html
%endif
