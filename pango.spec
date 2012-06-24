%define prefix /usr

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 0.9
Release: 1
Copyright: LGPL
Group: System Environment/Libraries
Source: http://www.pango.org/download/pango-%{version}.tar.gz
BuildRoot: /var/tmp/pango-%{PACKAGE_VERSION}-root

%description
System for layout and rendering of internationalized text.

%package devel
Summary:  System for layout and rendering of internationalized text
Group: Development/Libraries
Requires: pango = %{PACKAGE_VERSION}
Requires: libunicode-devel
Requires: fribidi-devel
Requires: XFree86-devel

%description devel
The pango-devel package includes the static libraries and header files
for the pango package.

Install pango-devel if you want to develop programs which will use
pango.

%changelog
* Fri Feb 11 2000 Owen Taylor <otaylor@redhat.com>
- Created spec file

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix} --sysconfdir=/etc --localstatedir=/var

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if ! test -d /var/lib/pango ; then
  mkdir -p /var/lib/pango/
fi
/usr/bin/pango-querymodules /usr/lib/pango/modules/*.so > /var/lib/pango/pango.modules

%postun -p /sbin/ldconfig

%files
%doc README AUTHORS COPYING ChangeLog TODO
%doc examples/HELLO.utf8
%{prefix}/lib/libpango*-*.so
%{prefix}/bin/pango-querymodules
%{prefix}/bin/pango-viewer
%{prefix}/lib/pango/modules/*
%config /etc/pango/pangox_aliases

%files devel
%defattr(-, root, root)
%{prefix}/lib/libpango*.so
%{prefix}/bin/pango-config
%{prefix}/lib/libpango*.a
%{prefix}/include/*
