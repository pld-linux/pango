Summary:	System for layout and rendering of internationalized text
Summary(pl):	System renderowania miêdzynarodowego tekstu
Name:		pango
Version:	1.0.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gtk.org/pub/gtk/v2.0/%{name}-%{version}.tar.bz2
Patch0:		%{name}-am_ac.patch
URL:		http://www.pango.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	glib2-devel >= 2.0.0
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

%package devel
Summary:	System for layout and rendering of internationalized text
Summary(pl):	System obs³ugi i renderowania miêdzynarodowego tekstu
Group:		Development/Libraries
Requires:	%{name} = %{version}
Obsoletes:	libpango24-devel

%description devel
Developer files for pango.

%description devel -l pl
Pliki developerskie pango.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static %{name} libraries.

%description static -l pl
Biblioteki statyczne %{name}.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing acinclude.m4
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
%configure \
	--with-fribidi \
	--enable-gtk-doc=no \
	--enable-static
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
umask 022
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz examples/*gz
%attr(755,root,root) %{_bindir}/pango-querymodules
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/pango
%dir %{_libdir}/pango/%{version}
%dir %{_libdir}/pango/%{version}/modules
%attr(755,root,root) %{_libdir}/pango/%{version}/modules/*.so
%attr(755,root,root) %{_libdir}/pango/%{version}/modules/*.la
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
