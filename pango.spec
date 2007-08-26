#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.18.0
Release:	1
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.18/%{name}-%{version}.tar.bz2
# Source0-md5:	5a3cbda73be7277a20d97f2bc89b0737
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-arch_confdir.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.4.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1:2.4.0
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	glib2-devel >= 1:2.14.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.8}
BuildRequires:	gtk-doc-automake >= 1.8
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1.0
Requires:	cairo >= 1.4.0
Requires:	freetype >= 2.1.7
Requires:	glib2 >= 1:2.14.0
Obsoletes:	libpango24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		_sysconfdir	/etc/%{name}64
%else
%define		_sysconfdir	/etc/%{name}
%endif

%description
System for layout and rendering of internationalized text.

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu.

%description -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package devel
Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System obsługi i renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	cairo-devel >= 1.4.0
Requires:	freetype-devel >= 2.1.7
Requires:	glib2-devel >= 1:2.14.0
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXft-devel >= 2.1.0
Obsoletes:	libpango24-devel

%description devel
Developer files for pango.

%description devel -l pl.UTF-8
Pliki developerskie pango.

%description devel -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package static
Summary:	Static pango libraries
Summary(pl.UTF-8):	Biblioteki statyczne pango
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static pango libraries.

%description static -l pl.UTF-8
Biblioteki statyczne pango.

%description static -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package modules
Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System obsługi i renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description modules
System for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu.

Pakiet zawiera moduły pango dla języków: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package apidocs
Summary:	Pango API documentation
Summary(pl.UTF-8):	Dokumentacja API pango
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Pango API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API pango.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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

> $RPM_BUILD_ROOT%{_sysconfdir}/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.6.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango.modules
exit 0

%postun -p /sbin/ldconfig

%post modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango.modules
exit 0

%postun modules
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango.modules
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README THANKS
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_bindir}/pango-view
%attr(755,root,root) %{_libdir}/libpango-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangox-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so.*.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.6.0
%dir %{_libdir}/pango/1.6.0/modules
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-basic-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-basic-x.so
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pangox.aliases
%ghost %{_sysconfdir}/pango.modules
%{_mandir}/man1/pango-querymodules.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango-1.0.so
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so
%attr(755,root,root) %{_libdir}/libpangox-1.0.so
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so
%{_libdir}/libpango-1.0.la
%{_libdir}/libpangocairo-1.0.la
%{_libdir}/libpangoft2-1.0.la
%{_libdir}/libpangox-1.0.la
%{_libdir}/libpangoxft-1.0.la
%{_pkgconfigdir}/pango.pc
%{_pkgconfigdir}/pangocairo.pc
%{_pkgconfigdir}/pangoft2.pc
%{_pkgconfigdir}/pangox.pc
%{_pkgconfigdir}/pangoxft.pc
%{_includedir}/pango-1.0

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpango-1.0.a
%{_libdir}/libpangocairo-1.0.a
%{_libdir}/libpangoft2-1.0.a
%{_libdir}/libpangox-1.0.a
%{_libdir}/libpangoxft-1.0.a
%endif

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-arabic-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-arabic-lang.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-hangul-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-hebrew-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-indic-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-indic-lang.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-khmer-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-syriac-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-thai-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-tibetan-fc.so
%exclude %{_libdir}/pango/1.6.0/modules/pango-basic-fc.so
%exclude %{_libdir}/pango/1.6.0/modules/pango-basic-x.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango
%endif
