Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania miêdzynarodowego tekstu
Name:		pango
Version:	0.21
Release:	1
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	âÉÂÌÉÏÔÅËÉ
Group(uk):	â¦ÂÌ¦ÏÔÅËÉ
Source0:	ftp://ftp.gtk.org/pub/gtk/v1.3/%{name}-%{version}.tar.gz
Patch0:		%{name}-am_ac.patch
URL:		http://www.pango.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	glib2-devel >= 1.3.10
BuildRequires:	fribidi-devel
BuildRequires:	pkgconfig
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

# pango is not GNOME-specific
%define		_sysconfdir	/etc/X11
%define		_pkgconfig	%{_libdir}/pkgconfig

%description
System for layout and rendering of internationalized text.

%description -l pl
System obs³ugi i renderowania miêdzynarodowego tekstu.

%package devel
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs³ugi i renderowania miêdzynarodowego tekstu
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name} = %{version}
Requires:	libunicode-devel

%description devel
Developer files for pango.

%description -l pl devel
Pliki developerskie pango.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name}-devel = %{version}

%description static
Static %{name} libraries.

%description -l pl static
Biblioteki statyczne %{name}.

%package X11
Summary:	System for layout and rendering of internationalized text - X11 version
Summary(pl):	System renderowania miêdzynarodowego tekstu - wersja X11
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	âÉÂÌÉÏÔÅËÉ
Group(uk):	â¦ÂÌ¦ÏÔÅËÉ

%description X11
System for layout and rendering of internationalized text - X11
version.

%description -l pl X11
System renderowania miêdzynarodowego tekstu - wersja X11.

%package freetype
Summary:	System for layout and rendering of internationalized text - FreeType version
Summary(pl):	System renderowania miêdzynarodowego tekstu - wersja FreeType
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	âÉÂÌÉÏÔÅËÉ
Group(uk):	â¦ÂÌ¦ÏÔÅËÉ

%description freetype
System for layout and rendering of internationalized text - FreeType
version.

%description -l pl freetype
System renderowania miêdzynarodowego tekstu - wersja FreeType.

%package XRender
Summary:	System for layout and rendering of internationalized text - X11 version with XRender support
Summary(pl):	System renderowania miêdzynarodowego tekstu - wersja X11 z obs³ug± XRender
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	âÉÂÌÉÏÔÅËÉ
Group(uk):	â¦ÂÌ¦ÏÔÅËÉ

%description XRender
System for layout and rendering of internationalized text - X11
version with XRender support.

%description -l pl XRender
System renderowania miêdzynarodowego tekstu - wersja X11 z obs³ug±
XRender.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing acinclude.m4
libtoolize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--with-fribidi
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# avoid relinking
for lafile in pango/*.la; do
  mv ${lafile} ${lafile}.old
  grep -v "^relink_command" ${lafile}.old > ${lafile}
done

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

> $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

gzip -9nf README AUTHORS ChangeLog TODO examples/HELLO.utf8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz examples/*gz
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_libdir}/libpango-*.so
%dir %{_libdir}/pango
%dir %{_libdir}/pango/modules
%dir %{_sysconfdir}/pango
%ghost %{_sysconfdir}/pango/pango.modules

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpangox-*.so
%attr(755,root,root) %{_libdir}/pango/modules/*-x.so
%attr(755,root,root) %{_libdir}/pango/modules/*-x.la
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pango/pangox.aliases

%files XRender
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpangoxft-*.so
%attr(755,root,root) %{_libdir}/pango/modules/*-xft.so
%attr(755,root,root) %{_libdir}/pango/modules/*-xft.la

%files freetype
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpangoft2-*.so
%attr(755,root,root) %{_libdir}/pango/modules/*-ft2.so
%attr(755,root,root) %{_libdir}/pango/modules/*-ft2.la

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpango.so
%attr(755,root,root) %{_libdir}/libpangox.so
%attr(755,root,root) %{_libdir}/libpangoxft.so
%attr(755,root,root) %{_libdir}/libpangoft2.so
%attr(755,root,root) %{_libdir}/libpango*.la
%{_pkgconfigdir}/*
%{_includedir}/*
%{_datadir}/gtk-doc/html/pango

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango*.a
