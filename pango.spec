Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania miêdzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.0.3
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	ftp://ftp.gtk.org/pub/gtk/v2.0/%{name}-%{version}.tar.bz2
Patch0:		%{name}-am_ac.patch
URL:		http://www.pango.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	glib2-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libpango24

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

# pango is not GNOME-specific
%define		_sysconfdir	/etc/X11

%description
System for layout and rendering of internationalized text.

%description -l pl
System obs³ugi i renderowania miêdzynarodowego tekstu.

%description -l pt_BR
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package devel
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs³ugi i renderowania miêdzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Obsoletes:	libpango24-devel

%description devel
Developer files for pango.

%description devel -l pl
Pliki developerskie pango.

%description devel -l pt_BR
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Summary(pt_BR):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static %{name} libraries.

%description static -l pl
Biblioteki statyczne %{name}.

%description static -l pt_BR
Pango é um sistema para layout e renderização de texto
internacionalizado.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing acinclude.m4
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
%configure \
	--with-fribidi \
	--enable-gtk-doc=no \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog TODO examples/HELLO.utf8
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.0.0
%dir %{_libdir}/pango/1.0.0/modules
%attr(755,root,root) %{_libdir}/pango/1.0.0/modules/*.so
%attr(755,root,root) %{_libdir}/pango/1.0.0/modules/*.la
%dir %{_sysconfdir}/pango
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pango/pangox.aliases
%ghost %{_sysconfdir}/pango/pango.modules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango*.so
%attr(755,root,root) %{_libdir}/libpango*.la
%{_pkgconfigdir}/*
%{_includedir}/*
%{_datadir}/gtk-doc/html/pango

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango*.a
