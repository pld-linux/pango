Summary:	System for layout and rendering of internationalized text
Name:		pango
Version:	0.12
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.pango.org/download/%{name}-%{version}.tar.gz
URL:		http://www.pango.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libunicode-devel
BuildRequires:	fribidi-devel

%define		_prefix		/usr/X11R6

# pango is not GNOME-specific
# %define		_sysconfdir	/etc/X11/GNOME
%define		_sysconfdir	/etc/X11

%description
System for layout and rendering of internationalized text.

%package devel
Summary:	System for layout and rendering of internationalized text
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Requires:	libunicode-devel
Requires:	fribidi-devel

%description devel

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static %{name} libraries.

%description -l pl static
Biblioteki statyczne %{name}.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

> $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

gzip -9nf README AUTHORS ChangeLog TODO examples/HELLO.utf8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz examples/*gz
%attr(755,root,root) %{_libdir}/libpango-*.so
%attr(755,root,root) %{_libdir}/libpangox-*.so
%attr(755,root,root) %{_bindir}/pango-querymodules
%dir %{_libdir}/pango
%dir %{_libdir}/pango/modules
%attr(755,root,root) %{_libdir}/pango/modules/*.so
%dir %{_sysconfdir}/pango
%config %{_sysconfdir}/pango/pangox.aliases
%ghost %{_sysconfdir}/pango/pango.modules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango.so
%attr(755,root,root) %{_libdir}/libpangox.so
%attr(755,root,root) %{_bindir}/pango-config
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango*.a
%{_libdir}/pango/modules/*.a
