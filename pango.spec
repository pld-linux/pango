#
# Conditional build:
%bcond_without	apidocs		# gi documentation
%bcond_without	libthai		# thai-lang module
%bcond_without	static_libs	# static libraries
%bcond_with	sysprof		# sysprof tracing support

Summary:	System for layout and rendering of internationalized text
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu
Summary(pt_BR.UTF-8):	Sistema para layout e renderização de texto internacionalizado
Name:		pango
Version:	1.56.4
Release:	1
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/pango/1.56/%{name}-%{version}.tar.xz
# Source0-md5:	3db267bc07bfd96615c652e9187b85b5
URL:		https://gnome.pages.gitlab.gnome.org/pango/Pango/
# cairo-ft cairo-pdf cairo-png cairo-ps cairo-xlib
BuildRequires:	cairo-devel >= 1.18.0
BuildRequires:	cairo-gobject-devel >= 1.18.0
%{?with_apidocs:BuildRequires:	docutils >= 0.13.1}
BuildRequires:	fontconfig-devel >= 1:2.15.0
BuildRequires:	freetype-devel >= 2.1.7
BuildRequires:	fribidi-devel >= 1.0.6
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.82
BuildRequires:	gobject-introspection-devel >= 1.83.2
BuildRequires:	harfbuzz-devel >= 8.4.0
BuildRequires:	harfbuzz-gobject-devel >= 8.4.0
%{?with_libthai:BuildRequires:	libthai-devel >= 0.1.9}
BuildRequires:	meson >= 1.2.0
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1.0
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
Requires:	cairo >= 1.18.0
Requires:	fontconfig-libs >= 1:2.15.0
Requires:	freetype >= 2.1.7
Requires:	fribidi >= 1.0.6
Requires:	glib2 >= 1:2.82
Requires:	harfbuzz >= 8.4.0
Obsoletes:	libpango24 < 1
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
# "gm convert" optionally used in pango-view
Suggests:	GraphicsMagick
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
Requires:	cairo-devel >= 1.18.0
Requires:	fontconfig-devel >= 1:2.15.0
Requires:	freetype-devel >= 2.1.7
Requires:	fribidi-devel >= 1.0.6
Requires:	glib2-devel >= 1:2.82
Requires:	harfbuzz-devel >= 8.4.0
%{?with_libthai:Requires:	libthai-devel >= 0.1.9}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXft-devel >= 2.1.0
Obsoletes:	libpango24-devel < 1

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

%package apidocs
Summary:	Pango API documentation
Summary(pl.UTF-8):	Dokumentacja API pango
Group:		Documentation
BuildArch:	noarch

%description apidocs
Pango API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API pango.

%package examples
Summary:	pango - example programs
Summary(pl.UTF-8):	pango - przykładowe programy
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
pango - example programs.

%description examples -l pl.UTF-8
pango - przykładowe programy.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Ddocumentation=%{__true_false apidocs} \
	-Dintrospection=enabled \
	-Dman-pages=%{__true_false apidocs} \
	%{?with_sysprof:-Dsysprof=enabled}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/Pango* $RPM_BUILD_ROOT%{_gidocdir}
%endif

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
%{_libdir}/girepository-1.0/PangoFc-1.0.typelib
%{_libdir}/girepository-1.0/PangoOT-1.0.typelib
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pango-list
%attr(755,root,root) %{_bindir}/pango-segmentation
%attr(755,root,root) %{_bindir}/pango-view
%if %{with apidocs}
%{_mandir}/man1/pango-list.1*
%{_mandir}/man1/pango-segmentation.1*
%{_mandir}/man1/pango-view.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango-1.0.so
%attr(755,root,root) %{_libdir}/libpangocairo-1.0.so
%attr(755,root,root) %{_libdir}/libpangoft2-1.0.so
%attr(755,root,root) %{_libdir}/libpangoxft-1.0.so
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir
%{_datadir}/gir-1.0/PangoFc-1.0.gir
%{_datadir}/gir-1.0/PangoOT-1.0.gir
%{_datadir}/gir-1.0/PangoXft-1.0.gir
%{_includedir}/pango-1.0
%{_pkgconfigdir}/pango.pc
%{_pkgconfigdir}/pangocairo.pc
%{_pkgconfigdir}/pangofc.pc
%{_pkgconfigdir}/pangoft2.pc
%{_pkgconfigdir}/pangoot.pc
%{_pkgconfigdir}/pangoxft.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpango-1.0.a
%{_libdir}/libpangocairo-1.0.a
%{_libdir}/libpangoft2-1.0.a
%{_libdir}/libpangoxft-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/Pango
%{_gidocdir}/PangoCairo
%{_gidocdir}/PangoFT2
%{_gidocdir}/PangoFc
%{_gidocdir}/PangoOT
%{_gidocdir}/PangoXft
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
