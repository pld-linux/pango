Summary:	System for layout and rendering of internationalized text
Name:		pango
Version:	0.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.pango.org/download/%{name}-%{version}.tar.gz
URL:		http://www.pango.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME

%description
System for layout and rendering of internationalized text.

%package devel
Summary:	System for layout and rendering of internationalized text
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	libunicode-devel
Requires:	fribidi-devel
Requires:	XFree86-devel
Requires:	%{name} = %{version}

%description devel

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README AUTHORS ChangeLog TODO examples/HELLO.utf8
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/pango-querymodules /usr/lib/pango/modules/*.so > /var/lib/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz examples/*gz
%attr(755,root,root) %{_libdir}/lib*.so
%{_bindir}/pango-querymodules
%{_bindir}/pango-viewer
%{_libdir}/pango/modules/*
%config %{_sysconfdir}/pango/pangox_aliases

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_bindir}/pango-config
%{_libdir}/libpango*.a
%{_includedir}/*
