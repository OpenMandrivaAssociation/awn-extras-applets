%define rel 1
%define bzr 0

%if %bzr
%define srcname		%{name}-%{bzr}
%define distname	%{name}
%define release		%mkrel 0.%{bzr}.%{rel}
%else
%define srcname		%{name}-%{version}
%define distname	%{name}-%{version}
%define release		%mkrel %{rel}
%endif

%define library_name	awn-extras
%define major		0
%define libname		%mklibname %library_name %major
%define develname	%mklibname %library_name -d

%define schemas switcher trash filebrowser awnsystemmonitor awn-notification-daemon

Summary:	Applets for Avant Window Navigator
Name:		awn-extras-applets
Version:	0.2.6
Release:	%{release}
Source0:	%{srcname}.tar.gz
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		https://launchpad.net/awn-extras
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gnome-common
BuildRequires:	libGConf2-devel
BuildRequires:	intltool
BuildRequires:	libgtk+2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgnome-desktop-2-devel
BuildRequires:	libwnck-devel
BuildRequires:	libnotify-devel
BuildRequires:	awn-devel
BuildRequires:	gnome-menus-devel
BuildRequires:	librsvg-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	libsexy-devel
BuildRequires:	vte-devel
BuildRequires:	gstreamer0.10-python
BuildRequires:	gnome-python-gtkmozembed
BuildRequires:	gnome-python-applet
BuildRequires:	gnome-python-gnomevfs
BuildRequires:	python-alsaaudio
BuildRequires:	python-feedparser
BuildRequires:	python-gnome-menus
BuildRequires:	avant-window-navigator >= 0.2.6
Requires:	avant-window-navigator >= 0.2.6
Requires:	notification-daemon
Requires:	gstreamer0.10-python
Requires:	gnome-python-gtkmozembed
Requires:	gnome-python-applet
Requires:	gnome-python-gnomevfs
Requires:	python-alsaaudio
Requires:	python-feedparser
Requires:	python-gnome-menus

%description
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. This package contains optional applets for
avant-window-navigator, including a notification daemon, system monitor,
battery monitor, trash applet, volume control, weather applet and more.

%package -n %{libname}
Group: System/Libraries
Summary: Shared library for awn-extras

%description -n %{libname}
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. awn-extras-applets contains optional applets for
avant-window-navigator, including a notification daemon, system monitor,
battery monitor, trash applet, volume control, weather applet and more.
This package contains the shared library for awn-extras-applets.

%package -n %{develname}
Group: Development/C
Summary: Development library for awn-extras
Requires: %{libname} = %{version}
Provides: %{library_name}-devel = %{version}-%{release}

%description -n %{develname}
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. awn-extras-applets contains optional applets for
avant-window-navigator, including a notification daemon, system monitor,
battery monitor, trash applet, volume control, weather applet and more.
This package contains the development library for awn-extras-applets.

%prep
%setup -q -n %{distname}

%build
%if %bzr
./autogen.sh -V
%endif
%configure --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %name

%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/awn/applets/*
%{_datadir}/%{name}/*
%{_datadir}/avant-window-navigator/applets/icons/*.svg
%{_datadir}/avant-window-navigator/defs/*.defs
%{_iconsdir}/hicolor/*/*/*.*
%{_bindir}/affinity-preferences
%{py_platsitedir}/awn/extras

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.*a
%{_libdir}/*.so
%{_includedir}/lib%{library_name}
