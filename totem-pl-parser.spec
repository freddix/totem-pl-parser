Summary:	Totem Playlist Parser library
Name:		totem-pl-parser
Version:	3.10.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/totem-pl-parser/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	e2c29a68f783e92bd2cb55c4d8916758
URL:		http://www.gnome.org/projects/totem/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	gmime-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libarchive-devel >= 3.1.2
BuildRequires:	libsoup-gnome-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library to parse and save playlists, as used in music and movie
players.

%package devel
Summary:	Header files for totem-pl-parser library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmime-devel

%description devel
Header files for totem-pl-parser library.

%package apidocs
Summary:	totem-pl-parser library API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
totem-pl-parser library API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e '/GNOME_CODE_COVERAGE/d'		\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac
%{__sed} -i -e '/@GNOME_CODE_COVERAGE_RULES@/d' plparse/Makefile.am

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--enable-introspection	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libtotem*.so.??
%attr(755,root,root) %{_libdir}/libtotem*.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtotem-*.so
%{_includedir}/totem-pl-parser
%{_pkgconfigdir}/totem*.pc
%{_datadir}/gir-1.0/TotemPlParser-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/totem-pl-parser

