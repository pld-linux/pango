Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania miêdzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.0.5
Release:	2
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.0/%{name}-%{version}.tar.bz2
# Source0-md5:	e300e5c163bc28e180e45c8e20543b4b
Patch0:		%{name}-am_ac.patch
Patch1:		%{name}-gtkdoc.patch
URL:		http://www.pango.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	glib2-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	gtk-doc >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libpango24

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_gtkdocdir	%{_defaultdocdir}/gtk-doc/html

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
Requires:	XFree86-devel
Requires:	freetype-devel
Requires:	glib2-devel
Requires:	gtk-doc-common
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

%package modules
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs³ugi i renderowania miêdzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description modules
System for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pl
System obs³ugi i renderowania miêdzynarodowego tekstu.

Pakiet zawiera modu³y pango dla jêzyków: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pt_BR
Pango é um sistema para layout e renderização de texto
internacionalizado.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	HTML_DIR=%{_gtkdocdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun -p /sbin/ldconfig

%post modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%postun modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%triggerpostun -- pango < 1.05
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%triggerpostun -- pango-modules < 1.05-2
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog TODO examples/HELLO.utf8
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.0.0
%dir %{_libdir}/pango/1.0.0/modules
%attr(755,root,root) %{_libdir}/pango/1.0.0/modules/*basic*.so
%{_libdir}/pango/1.0.0/modules/*basic*.la
%dir %{_sysconfdir}/pango
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pango/pangox.aliases
%ghost %{_sysconfdir}/pango/pango.modules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango*.so
%{_libdir}/libpango*.la
%{_pkgconfigdir}/*
%{_includedir}/*
%{_gtkdocdir}/pango

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango*.a

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pango/1.0.0/modules/*.so
%exclude %{_libdir}/pango/1.0.0/modules/*basic*.so
%{_libdir}/pango/1.0.0/modules/*.la
%exclude %{_libdir}/pango/1.0.0/modules/*basic*.la
