Summary: X.Org X11 xkb utilities
Name: xorg-x11-xkb-utils
Version: 7.7
Release: 1
License: MIT
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# use the macro so the doc dir is changed automagically
#%define xkbutils_version 1.0.3
#Source0: ftp://ftp.x.org/pub/individual/app/xkbutils-%{xkbutils_version}.tar.bz2
#Source1: ftp://ftp.x.org/pub/individual/app/xkbcomp-1.2.4.tar.bz2
#Source2: ftp://ftp.x.org/pub/individual/app/xkbevd-1.1.3.tar.bz2
#Source3: ftp://ftp.x.org/pub/individual/app/xkbprint-1.0.3.tar.bz2
#Source4: ftp://ftp.x.org/pub/individual/app/setxkbmap-1.3.0.tar.bz2

Source: %{name}-%{version}.tar.gz

BuildRequires: pkgconfig
BuildRequires: byacc
BuildRequires: xorg-x11-proto-input
BuildRequires: libxkbfile-devel
BuildRequires: libX11-devel
BuildRequires: libXaw-devel
BuildRequires: libXt-devel
# FIXME: xkbvleds requires libXext, but autotools doesn't check/require it:
# gcc  -O2 -g -march=i386 -mcpu=i686   -o xkbvleds  xkbvleds-xkbvleds.o
# xkbvleds-LED.o xkbvleds-utils.o -lXaw7 -lXmu -lXt -lSM -lICE -lXext -lXpm -lX11 -ldl
# /usr/bin/ld: cannot find -lXext
# libXext-devel needed for xkbutils (from above error)
BuildRequires: libXext-devel
# FIXME: xkbvleds requires libXext, but autotools doesn't check/require it:
# gcc  -O2 -g -march=i386 -mcpu=i686   -o xkbvleds  xkbvleds-xkbvleds.o
# xkbvleds-LED.o xkbvleds-utils.o -lXaw7 -lXmu -lXt -lSM -lICE -lXext -lXpm -lX11 -ldl
# /usr/bin/ld: cannot find -lXpm
# libXpm-devel needed for xkbutils (from above error)
BuildRequires: libXpm-devel

Provides: setxkbmap xkbcomp
Obsoletes: XFree86 xorg-x11

%package devel
Summary:        X.Org X11 xkb utilities development package.
Group:          Development/Libraries
Requires:       pkgconfig
%description devel
X.Org X11 xkb utilities development files.

%package -n xorg-x11-xkb-extras
Summary: X.Org X11 xkb gadgets
Provides: xkbevd xkbprint xkbutils

%description
X.Org X11 xkb core utilities

%description -n xorg-x11-xkb-extras
X.Org X11 xkb gadgets

%prep
%setup -q
#%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4

%build
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS -DHAVE_STRCASECMP -Os"
for pkg in xkbutils setxkbmap xkbcomp xkbevd xkbprint ; do
    pushd $pkg*
    [ $pkg == xkbcomp ] && rm xkbparse.c # force regen
    %configure --prefix=/usr --datadir=/etc
    make %{?jobs:-j%jobs} V=1
    popd
done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
cp -af COPYING %{buildroot}/usr/share/license/xorg-x11-xkb-extras
for pkg in xkbutils setxkbmap xkbcomp xkbevd xkbprint ; do
    pushd $pkg*
    make install DESTDIR=$RPM_BUILD_ROOT
    popd
done

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/share/license/%{name}
%{_bindir}/setxkbmap
%{_bindir}/xkbcomp
#%{_mandir}/man1/setxkbmap.1*
#%{_mandir}/man1/xkbcomp.1*

%files -n xorg-x11-xkb-extras
%defattr(-,root,root,-)
/usr/share/license/xorg-x11-xkb-extras
#%doc xkbutils-%{xkbutils_version}/COPYING
#%doc xkbutils-%{xkbutils_version}/README
%{_bindir}/xkbbell
%{_bindir}/xkbevd
%{_bindir}/xkbprint
%{_bindir}/xkbvleds
%{_bindir}/xkbwatch
#%{_mandir}/man1/xkbbell.1*
#%{_mandir}/man1/xkbevd.1*
#%{_mandir}/man1/xkbprint.1*
#%{_mandir}/man1/xkbvleds.*
#%{_mandir}/man1/xkbwatch.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/xkbcomp.pc
