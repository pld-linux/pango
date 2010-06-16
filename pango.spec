#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	libthai		# don't build thai-lang module
%bcond_without	static_libs	# don't build static library
#
Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.28.1
Release:	1
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.28/%{name}-%{version}.tar.bz2
# Source0-md5:	bab5b4eb3fde6b0a5bfe98d25e668741
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-arch_confdir.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.7.6
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1:2.5.0
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.8}
BuildRequires:	gtk-doc-automake >= 1.8
BuildRequires:	libstdc++-devel
%{?with_libthai:BuildRequires:	libthai-devel >= 0.1.9}
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1.0
Requires:	cairo >= 1.7.6
Requires:	freetype >= 2.1.7
Requires:	glib2 >= 1:2.18.0
Obsoletes:	libpango24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		_sysconfdir	/etc/%{name}%{libext}
%define		pqext		-%{libext}
%else
%define		_sysconfdir	/etc/%{name}
%define		pqext		%{nil}
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
Requires:	cairo-devel >= 1.7.6
Requires:	freetype-devel >= 2.1.7
Requires:	glib2-devel >= 1:2.18.0
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
%{?with_libthai:Requires:	libthai:Requires:	libthai >= 0.1.9}

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

%package examples
Summary:	pango - example programs
Summary(pl.UTF-8):	pango - przykładowe programy
Group:		X11/Development/Libraries

%description examples
pango - example programs.

%description examples -l pl.UTF-8
pango - przykładowe programy.

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
	--disable-silent-rules \
	--enable-debug=%{?debug:yes}%{!?debug:minimum} \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--enable-man \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--with-html-dir=%{_gtkdocdir}

# some generator script requires access to newely created .pc files
export PKG_CONFIG_PATH="$PWD"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango.modules

cp examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if "%{_lib}" != "lib"
# We need to have 32-bit and 64-bit pango-querymodules binaries
# as they have hardcoded LIBDIR.
# (needed when multilib is used)
mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules{,%{pqext}}
# fix man page too
mv $RPM_BUILD_ROOT%{_mandir}/man1/pango-querymodules{,%{pqext}}.1
%endif

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.6.0/modules/*.{la,a}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}/pango}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/pango-querymodules%{pqext} > %{_sysconfdir}/pango.modules
exit 0

%postun -p /sbin/ldconfig

%post modules
umask 022
%{_bindir}/pango-querymodules%{pqext} > %{_sysconfdir}/pango.modules
exit 0

%postun modules
umask 022
%{_bindir}/pango-querymodules%{pqext} > %{_sysconfdir}/pango.modules
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README THANKS
%attr(755,root,root) %{_bindir}/pango-querymodules%{pqext}
%attr(755,root,root) %{_bindir}/pango-view
%attr(755,root,root) %{_libdir}/libpango-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpango-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangocairo-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangoft2-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangox-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangox-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangoxft-1.0.so.0
%dir %{_libdir}/pango
%dir %{_libdir}/pango/1.6.0
%dir %{_libdir}/pango/1.6.0/modules
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-basic-fc.so
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-basic-x.so
%{_libdir}/girepository-1.0/Pango*-1.0.typelib
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pangox.aliases
%ghost %{_sysconfdir}/pango.modules
%{_mandir}/man1/pango-querymodules%{pqext}.1*
%{_mandir}/man1/pango-view.1*

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
%{_datadir}/gir-1.0/Pango*-1.0.gir

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
%if %{with libthai}
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-thai-lang.so
%endif
%attr(755,root,root) %{_libdir}/pango/1.6.0/modules/pango-tibetan-fc.so
%exclude %{_libdir}/pango/1.6.0/modules/pango-basic-fc.so
%exclude %{_libdir}/pango/1.6.0/modules/pango-basic-x.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
