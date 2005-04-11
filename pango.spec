#
# Conditional build:
%bcond_with	xlibs	# use pkgconfig to find libX11 CFLAGS
#
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Name:		pango
Version:	1.8.1
Release:	2
Epoch:		1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.8/%{name}-%{version}.tar.bz2
# Source0-md5:	88aa6bf1876766db6864f3b93577887c
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-xlibs.patch
URL:		http://www.pango.org/
%{!?with_xlibs:BuildRequires:	XFree86-devel}
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.7
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1.0.1
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	glib2-devel >= 1:2.6.0-2
BuildRequires:	gtk-doc >= 1.0
%{?with_xlibs:BuildRequires:	libX11-devel}
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	xft-devel >= 2.1.0
Requires(post,postun):	/sbin/ldconfig
Requires:	freetype >= 2.1.7
Requires:	glib2 >= 1:2.6.0-2
Obsoletes:	libpango24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
System for layout and rendering of internationalized text.

%description -l pl
System obs�ugi i renderowania mi�dzynarodowego tekstu.

%description -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%package devel
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs�ugi i renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{!?with_xlibs:Requires:	XFree86-devel}
Requires:	freetype-devel >= 2.1.7
Requires:	glib2-devel >= 1:2.6.0-2
Requires:	gtk-doc-common
%{?with_xlibs:Requires:	libX11-devel}
Requires:	xft-devel >= 2.1.0
Obsoletes:	libpango24-devel

%description devel
Developer files for pango.

%description devel -l pl
Pliki developerskie pango.

%description devel -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%package static
Summary:	Static pango libraries
Summary(pl):	Biblioteki statyczne pango
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static pango libraries.

%description static -l pl
Biblioteki statyczne pango.

%description static -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%package modules
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs�ugi i renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description modules
System for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pl
System obs�ugi i renderowania mi�dzynarodowego tekstu.

Pakiet zawiera modu�y pango dla j�zyk�w: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%prep
%setup -q
%patch0 -p1
%{?with_xlibs:%patch1 -p1}

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-fribidi \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-static \
	--enable-debug=%{?debug:yes}%{!?debug:minimum} \
	--enable-man
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.4.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ldconfig_post
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%postun
%ldconfig_postun

%post modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%postun modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README examples/HELLO.utf8
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.4.0
%dir %{_libdir}/pango/1.4.0/modules
%attr(755,root,root) %{_libdir}/pango/1.4.0/modules/*basic*.so
%dir %{_sysconfdir}/pango
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pango/pangox.aliases
%ghost %{_sysconfdir}/pango/pango.modules
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog TODO
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
%attr(755,root,root) %{_libdir}/pango/1.4.0/modules/*.so
%exclude %{_libdir}/pango/1.4.0/modules/*basic*.so
