%define rel 3
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

%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile     python -c "import compileall; compileall.compile_dir('.')"

Summary:	Applets for Avant Window Navigator
Name:		awn-extras-applets
Version:	0.2.6
Release:	%{release}
Source0:	%{srcname}.tar.gz
# From upstream dev malept: install Python stuff to platsitedir not
# puresitedir - AdamW 2008/02
Patch0:		awn-extras-applets-0.2.6-platsitedir.patch
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
BuildRequires:	python-devel
BuildRequires:	python-cairo-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	libglade2-devel
BuildRequires:	tracker-devel
BuildRequires:	libbeagle-devel
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
Requires:	python-cairo
Requires:	pygtk2.0

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
%patch0 -p1 -b .platsitedir

%build
%if %bzr
./autogen.sh -V
%endif
autoreconf
%configure --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %name

# Pre-generate .pyc and .pyo files as per Python policy.
pushd src
%python_compile_opt
%python_compile
for i in PyClock "arss/Core" arss battery-applet calendar "calendar/google/atom" "calendar/google/gdata" "calendar/google/gdata/apps" "calendar/google/gdata/base" "calendar/google/gdata/calendar" "calendar/google/gdata/docs" "calendar/google/gdata/spreadsheet" comic digitalClock file-browser-launcher lastfm mail media-control media-icon-back media-icon-next media-icon-play mount-applet python-test quit-applet showdesktop stacks volume-control weather; \
do install $i/*.pyc $i/*.pyo %{buildroot}%{_libdir}/awn/applets/$i; \
done
# Grr. Stupid upstream with their non-matching directory names! They
# promise they will fix this.
install pandora/*.pyc pandora/*.pyo %{buildroot}%{_libdir}/awn/applets/awn-pandora
install MiMenu/*.pyc MiMenu/*.pyo %{buildroot}%{_libdir}/awn/applets/mimenu
install tsclient-applet/*.pyc tsclient-applet/*.pyo %{buildroot}%{_libdir}/awn/applets/tsclient-app

# affinity-preferences is a namespace conflict with the original
# affinity. Apparently you can have both installed at once without
# trouble, they'll just share configuration. - AdamW 2008/02
mv %{buildroot}%{_bindir}/affinity-preferences %{buildroot}%{_bindir}/awn-affinity-preferences

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
%{_bindir}/awn-affinity-preferences
%{py_platsitedir}/awn/extras

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.*a
%{_libdir}/*.so
%{_includedir}/lib%{library_name}
