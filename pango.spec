#
# TODO:
# - update arch_confdir patch
#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
%bcond_with	arch_confdir	# build with arch-dependant config dir
#
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania mi�dzynarodowego tekstu
Summary(pt_BR):	Sistema para layout e renderiza��o de texto internacionalizado
Name:		pango
Version:	1.14.9
Release:	1
Epoch:		1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.14/%{name}-%{version}.tar.bz2
# Source0-md5:	58766a41693b917fda854b9a41d40834
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-arch_confdir.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.7
BuildRequires:	cairo-devel >= 1.2.4
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1:2.4.0
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	glib2-devel >= 1:2.12.4
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	gtk-doc-automake >= 1.7
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1.0
Requires:	cairo >= 1.2.4
Requires:	freetype >= 2.1.7
Requires:	glib2 >= 1:2.12.4
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
Requires:	cairo-devel >= 1.2.4
Requires:	freetype-devel >= 2.1.7
Requires:	glib2-devel >= 1:2.12.4
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXft-devel >= 2.1.0
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

%package apidocs
Summary:	Pango API documentation
Summary(pl):	Dokumentacja API pango
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Pango API documentation.

%description apidocs -l pl
Dokumentacja API pango.

%prep
%setup -q
%patch0 -p1
%{?with_arch_confdir:%patch1 -p1}

%build
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-fribidi \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}} \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--enable-debug=%{?debug:yes}%{!?debug:minimum} \
	--enable-man
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.5.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules
exit 0

%postun -p /sbin/ldconfig

%post modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules
exit 0

%postun modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README examples/HELLO.utf8
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_bindir}/pango-view
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.5.0
%dir %{_libdir}/pango/1.5.0/modules
%attr(755,root,root) %{_libdir}/pango/1.5.0/modules/*basic*.so
%if %{with arch_confdir}
%dir %{_sysconfdir}/pango-%{_host_cpu}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pango-%{_host_cpu}/pangox.aliases
%ghost %{_sysconfdir}/pango-%{_host_cpu}/pango.modules
%else
%dir %{_sysconfdir}/pango
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pango/pangox.aliases
%ghost %{_sysconfdir}/pango/pango.modules
%endif
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libpango*.so
%{_libdir}/libpango*.la
%{_pkgconfigdir}/*
%{_includedir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpango*.a
%endif

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pango/1.5.0/modules/*.so
%exclude %{_libdir}/pango/1.5.0/modules/*basic*.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango
%endif
