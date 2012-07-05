Name:           xorg-x11-xkb-utils
Version:        7.6
Release:        8
License:        MIT/X11
Summary:        X11 XKB utilities
Url:            http://www.x.org
Group:          User Interface/X
Source:         %{name}-%{version}.tar.gz
Source1001:     packaging/xorg-x11-xkb-utils.manifest

BuildRequires:  byacc
BuildRequires:  pkgconfig(inputproto)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xorg-macros)

%define DEF_SUBDIRS setxkbmap xkbcomp xkbevd xkbprint xkbutils

Provides:       %{DEF_SUBDIRS}

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
cp %{SOURCE1001} .
# Build all apps
{
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        autoreconf -i -v -f
        %configure  --datadir=/etc
        make
        popd
    done
}

%install
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
%make_install
      popd
   done
}

%docs_package

%files
%manifest xorg-x11-xkb-utils.manifest
%{_bindir}/*
