#
# Conditional build:
%bcond_with	xlibs	# use pkgconfig to find libX11 CFLAGS
#
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Name:		pango
%define		_major_ver	1.5
%define		_minor_ver	2
Version:	%{_major_ver}.%{_minor_ver}
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/%{_major_ver}/%{name}-%{version}.tar.bz2
# Source0-md5:	39868e0da250fd4c00b2970e4eb84389
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-xlibs.patch
URL:		http://www.pango.org/
%{!?with_xlibs:BuildRequires:	XFree86-devel}
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1.7
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	glib2-devel >= 1:2.4.0
BuildRequires:	gtk-doc >= 1.0
%{?with_xlibs:BuildRequires:	libX11-devel}
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.1-8.2
BuildRequires:	xft-devel >= 2.1.2
Requires(post):	/sbin/ldconfig
Requires:	freetype >= 2.1.7
Requires:	glib2 >= 1:2.4.0
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
Requires:	%{name} = %{version}-%{release}
%{!?with_xlibs:Requires:	XFree86-devel}
Requires:	freetype-devel >= 2.1.7
Requires:	glib2-devel >= 1:2.4.0
Requires:	gtk-doc-common
%{?with_xlibs:Requires:	libX11-devel}
Requires:	xft-devel >= 2.1.2
Obsoletes:	libpango24-devel

%description devel
Developer files for pango.

%description devel -l pl
Pliki developerskie pango.

%description devel -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} libraries.

%description static -l pl
Biblioteki statyczne %{name}.

%description static -l pt_BR
Pango � um sistema para layout e renderiza��o de texto
internacionalizado.

%package modules
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs�ugi i renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

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
gtkdocize --copy
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
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules
exit 0

%postun -p /sbin/ldconfig

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
