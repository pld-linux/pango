#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	libthai		# don't build thai-lang module

Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.44.2
Release:	0.1
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.44/%{name}-%{version}.tar.xz
# Source0-md5:	d79534bf001e657250f60cbd9ab96390
URL:		http://www.pango.org/
# cairo-ft cairo-pdf cairo-png cairo-ps cairo-xlib
BuildRequires:	cairo-devel >= 1.12.10
BuildRequires:	cairo-gobject-devel >= 1.12.10
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel >= 1:2.11.91
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	fribidi-devel >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.59.2
BuildRequires:	gobject-introspection-devel >= 0.9.5
%if %{with apidocs}
BuildRequires:	gtk-doc >= 1.15
%endif
BuildRequires:	harfbuzz-devel >= 2.0.0
%{?with_libthai:BuildRequires:	libthai-devel >= 0.1.9}
BuildRequires:	meson >= 0.48.0
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1.0
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
Requires:	cairo >= 1.12.10
Requires:	fontconfig-libs >= 1:2.11.91
Requires:	freetype >= 2.1.7
Requires:	fribidi >= 0.19.7
Requires:	glib2 >= 1:2.59.2
Requires:	harfbuzz >= 2.0.0
Obsoletes:	libpango24
Obsoletes:	pango-modules < 1:1.38.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
System for layout and rendering of internationalized text.

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu.

%description -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%package tools
Summary:	Pango tools
Summary(pl.UTF-8):	Narzędzia pango
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	pango-view < 1:1.42.2

%description tools
Pango tools:
- text viewer
- list availabe fonts

%description tools -l pl.UTF-8
Narzędzia pango:
- przeglądarka tekstu
- wyświetlanie dostępnych fontów

%package devel
Summary:	Header files for Pango libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Pango
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	cairo-devel >= 1.12.10
Requires:	fontconfig-devel >= 1:2.11.91
Requires:	freetype-devel >= 2.1.7
Requires:	fribidi-devel >= 0.19.7
Requires:	glib2-devel >= 1:2.59.2
Requires:	harfbuzz-devel >= 2.0.0
%{?with_libthai:Requires:	libthai-devel >= 0.1.9}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXft-devel >= 2.1.0
Obsoletes:	libpango24-devel

%description devel
Header files for Pango libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Pango.

%package static
Summary:	Static pango libraries
Summary(pl.UTF-8):	Biblioteki statyczne pango
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static pango libraries.

%description static -l pl.UTF-8
Biblioteki statyczne pango.

%package modules
Summary:	Pango modules for various scripts
Summary(pl.UTF-8):	Moduły Pango dla różnych systemów pisma
Group:		X11/Development/Libraries
Requires(post,postun):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_libthai:Requires:	libthai >= 0.1.9}

%description modules
Pango is a system for layout and rendering of internationalized text.

This package contains pango modules for: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%description modules -l pl.UTF-8
Pango to system obsługi i renderowania międzynarodowego tekstu.

Pakiet zawiera moduły pango dla języków: arabic, bengali, devanagari,
gujarati, gurmukhi, hangul, hebrew, indic, myanmar, tamil, thai.

%package apidocs
Summary:	Pango API documentation
Summary(pl.UTF-8):	Dokumentacja API pango
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Pango API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API pango.

%package examples
Summary:	pango - example programs
Summary(pl.UTF-8):	pango - przykładowe programy
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
pango - example programs.

%description examples -l pl.UTF-8
pango - przykładowe programy.

%prep
%setup -q

%build
%meson build \
	-Dgtk_doc=%{__true_false apidocs}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%ninja_install -C build

cp examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md THANKS
%attr(755,root,root) %{_libdir}/libpango-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpango-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangocairo-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangoft2-1.0.so.0
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangoxft-1.0.so.0
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pango-list
%attr(755,root,root) %{_bindir}/pango-view
%{_mandir}/man1/pango-view.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango-1.0.so
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir
%{_datadir}/gir-1.0/PangoXft-1.0.gir
%{_includedir}/pango-1.0
%{_pkgconfigdir}/pango.pc
%{_pkgconfigdir}/pangocairo.pc
%{_pkgconfigdir}/pangoft2.pc
%{_pkgconfigdir}/pangoxft.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango-1.0.a
%{_libdir}/libpangocairo-1.0.a
%{_libdir}/libpangoft2-1.0.a
%{_libdir}/libpangoxft-1.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pango
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
