%define srcname	awn-extras

%define libname		%mklibname awn-extras 0
%define develname	%mklibname awn-extras -d

Summary:	Applets for Avant Window Navigator
Name:		awn-extras-applets
Version:	0.4.0
Release:	%mkrel 3
Source0:	%{srcname}-%{version}.tar.gz
Patch0:		awn-extras-applets-0.4.0-python_dir.patch
Patch1:		awn-extras-applets-0.4.0-fix-cairo-menu.patch
Patch2:		awn-extras-0.4.0-libnotify.patch
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		https://launchpad.net/awn-extras
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#BuildRequires:	gnome-common
#BuildRequires:	libGConf2-devel
#BuildRequires:	libgtk+2-devel
#BuildRequires:	libgnome2-devel
#BuildRequires:	libgnomeui2-devel
#BuildRequires:	librsvg-devel
#BuildRequires:	libgtop2.0-devel
#BuildRequires:	libsexy-devel
#BuildRequires:	gnome-python-gtkmozembed
#BuildRequires:	gnome-python-applet
#BuildRequires:	gnome-python-gnomevfs
#BuildRequires:	python-alsaaudio
#BuildRequires:	python-cairo-devel
#BuildRequires:	pygtk2.0-devel
#BuildRequires:	libglade2-devel
#BuildRequires:	tracker-devel
#BuildRequires:	libbeagle-devel
BuildRequires:	intltool
BuildRequires:	libgnome-desktop-2-devel
BuildRequires:	libwnck-devel
BuildRequires:	libnotify-devel
BuildRequires:	awn-devel >= 0.4.0
BuildRequires:	gnome-menus-devel
BuildRequires:	gnome-python-desktop
BuildRequires:	gnome-python-gconf
BuildRequires:	vte-devel
BuildRequires:	gstreamer0.10-python
BuildRequires:	python-notify
BuildRequires:	python-feedparser
BuildRequires:	python-gnome-menus
BuildRequires:	python-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	python-dateutil
BuildRequires:	python-gdata
BuildRequires:	python-vobject
BuildRequires:	webkitgtk-devel
BuildRequires:	vala
Requires:	avant-window-navigator >= 0.4.0
#Requires:	gnome-python-gtkmozembed
Requires:	gnome-python-applet
Requires:	gnome-python-gnomevfs
Requires:	gnome-python-gconf
#Requires:	python-alsaaudio
Requires:	python-libgmail
Requires:	pygtk2.0
Requires:	python-notify
Requires:	python-feedparser
Requires:	python-gnome-menus
Requires:	gstreamer0.10-python
Requires:	python-cairo
Requires:	gnome-menus
Requires:	pygtk2.0-libglade
Obsoletes:	%libname < 0.4.0 %develname < 0.4.0

%description
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. This package contains optional applets for
avant-window-navigator, including a notification daemon, system monitor,
battery monitor, trash applet, volume control, weather applet and more.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p0 -b .python
%patch1 -p0 -b .cairo-menu
%patch2 -p0 -b .libnotify

%build
./autogen.sh -V
%configure2_5x --disable-static \
	--with-webkit \
	--disable-static \
	--enable-shave \
	--with-gnu-ld
%make

%install
rm -rf %{buildroot}

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

%find_lang %{srcname}

# don't ship .a or .la files:
find %{buildroot} -name '*.*a' -exec rm {} \;

%clean
rm -rf %{buildroot}

%files -f %{srcname}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_sysconfdir}/gconf/schemas/*
%{python_sitearch}/awn/extras
%{_libdir}/awn/applets
%dir %{_datadir}/avant-window-navigator
%{_datadir}/avant-window-navigator/applets
%{_datadir}/avant-window-navigator/schemas
%{_iconsdir}/hicolor/*/*/*.*
