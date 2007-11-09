%define name awn-extras-applets
%define version 0.2.1
%define rel 3
%define bzr 0

%if %bzr
%define srcname %{name}-%{bzr}
%define distname %{name}
%define release %mkrel 0.%{bzr}.%{rel}
%else
%define srcname %{name}-%{version}
%define distname %{name}-%{version}
%define release %mkrel %{rel}
%endif

%define schemas switcher trash filebrowser awnsystemmonitor notification-daemon

Summary:	Applets for Avant Window Navigator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{srcname}.tar
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
BuildRequires:	avant-window-navigator >= 0.2.1
Requires:	avant-window-navigator >= 0.2.1
Conflicts:	notification-daemon
Provides:	virtual-notification-daemon

%description
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. This package contains optional applets for
avant-window-navigator, including a notification daemon, system monitor,
battery monitor, trash applet, volume control, weather applet and more.

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

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/awn/applets/*
%{_datadir}/%{name}/*

