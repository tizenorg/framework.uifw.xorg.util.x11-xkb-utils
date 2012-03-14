Summary: X11 XKB utilities
Name: xorg-x11-xkb-utils
Version: 7.6
Release: 8
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source: %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(xorg-macros)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xaw7)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(inputproto)
BuildRequires: byacc

%define DEF_SUBDIRS setxkbmap xkbcomp xkbevd xkbprint xkbutils

Provides: %{DEF_SUBDIRS}

%description
xkbutils contains a number of client-side utilities for XKB, the X11 keyboard extension.
setxkbmap is a tool to query and change the current XKB map.
xkbbell generates a bell event through the keyboard.
xkbcomp is a tool to compile XKB definitions into map files the server can use.
xkbevd is an experimental tool to listen for certain XKB events and execute defined triggers when actions occur.
xkbprint is a tool to generate an image with the physical representation of the keyboard as XKB sees it.
xkbvleds shows the changing status of keyboard LEDs.
xkbwatch shows the changing status of modifiers and LEDs.

%prep
%setup -q

%build
# Build all apps
{
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        autoreconf -i -v -f
        ./configure --prefix=/usr --mandir=/usr/share/man \
                    --infodir=/usr/share/info \
                    --datadir=/opt/etc 
        make
        popd
    done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%docs_package

%files
%{_bindir}/*
