%define plymouthdaemon_execdir %{_sbindir}
%define plymouthclient_execdir %{_bindir}
%define plymouth_libdir %{_libdir}
%define plymouth_initrd_file /boot/initrd-plymouth.img

Name:           plymouth
#Version:        %{tarversion}_git%{patchversion}
Version:        0.8.6.1
Release:        0
License:        GPL-2.0+
Summary:        Graphical Boot Animation and Logger
Url:            http://freedesktop.org/software/plymouth/releases
Group:          System/Base
Source0:        %{name}-%{version}.tar.bz2
Source1:        boot-duration
# PATCH-OPENSUSE -- Add line numbers to tracing output
Patch2:         plymouth-trace-lines
# PATCH-OPENSUSE -- Handle correctly multiple displays with different sizes
Patch3:         plymouth-fix-window-size
# PATCH-OPENSUSE -- Ensure graphical.target is conflicting with plymouth-wait-quit.service
Patch4:         stop-graphical.patch
# PATCH-FIX-UPSTREAM -- Create targets for plymouth systemd services
Patch6:         plymouth-systemd-target.patch
# PATCH-OPENSUSE -- Change udevadm path
Patch7:         plymouth-udevadm-path.patch
# PATCH-OPENSUSE -- Remove tag not understood by systemd v44
Patch8:         systemd-no-warning.patch
# PATCH-FIX-UPSTREAM -- Recognize quotes often used in sysconfig-style files
Patch9:         0001-ply-text-progress-bar-strip-quotes-if-present.patch
# PATCH-FIX-UPSTREAM -- Fix systemd service file
Patch11:        plymouth-fix-systemd-service.patch
Patch12:        tizen.patch
Patch13:        systemd_path.patch
BuildRequires:  automake
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  xz
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(systemd)
%ifarch %ix86 x86_64
BuildRequires:  pkgconfig(libdrm_intel)
%endif
BuildRequires:  pkgconfig(libkms)
Requires:       systemd >= 44
Requires(post): plymouth-scripts
Requires(post): dracut

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package -n libply-boot-client
Summary:        Plymouth core library
Group:          Development/Libraries/C and C++

%description -n libply-boot-client
This package contains the libply-boot-client library used by Plymouth.

%package -n libply-splash-core
Summary:        Plymouth core library
Group:          Development/Libraries/C and C++

%description -n libply-splash-core
This package contains the libply-splash-core library
used by graphical Plymouth splashes.

%package -n libply-splash-graphics
Summary:        Plymouth graphics libraries
Group:          Development/Libraries/C and C++
BuildRequires:  libpng-devel

%description -n libply-splash-graphics
This package contains the libply-splash-graphics library
used by graphical Plymouth splashes.

%package -n libply
Summary:        Plymouth core library
Group:          Development/Libraries/C and C++
Requires:       libply-boot-client = %{version}

%description -n libply
This package contains the libply library used by Plymouth.

%package devel
Summary:        Libraries and headers for writing Plymouth splash plugins
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       %{name}-x11-renderer = %{version}
Requires:       libply = %{version}
Requires:       libply-boot-client = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}
Requires:       pkgconfig

%description devel
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package x11-renderer
Summary:        Plymouth X11 renderer
Group:          System/Base
Requires:       %{name} = %{version}

%description x11-renderer
This package provides the X11 renderer which allows to test plymouth
behavior on environments with a valid DISPLAY.

%package scripts
Summary:        Plymouth related scripts
Group:          System/Base
Requires:       coreutils
Requires:       cpio
Requires:       findutils
Requires:       gzip
Requires:       plymouth
BuildArch:      noarch

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Summary:        Plymouth label plugin
Group:          System/Base
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango) >= 1.21.0
Requires:       libply-splash-core = %{version}

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Summary:        Plymouth "Fade-Throbber" plugin
Group:          System/Base
Requires:       libply = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package plugin-throbgress
Summary:        Plymouth "Throbgress" plugin
Group:          System/Base
Requires:       %{name}-plugin-label = %{version}
Requires:       libply = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package plugin-space-flares
Summary:        Plymouth "space-flares" plugin
Group:          System/Base
Requires:       %{name}-plugin-label = %{version}
Requires:       libply = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package plugin-two-step
Summary:        Plymouth "two-step" plugin
Group:          System/Base
Requires:       libply = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}
Requires:       plymouth-plugin-label

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package plugin-script
Summary:        Plymouth "script" plugin
Group:          System/Base
Requires:       libply = %{version}
Requires:       libply-splash-core = %{version}
Requires:       libply-splash-graphics = %{version}

%description plugin-script
This package contains the "script" boot splash plugin for
Plymouth. It features an extensible, scriptable boot splash
language that simplifies the process of designing custom
boot splash themes.

%package theme-fade-in
Summary:        Plymouth "Fade-In" theme
Group:          System/Base
Requires:       %{name}-plugin-fade-throbber = %{version}
Requires:       plymouth-plugin-label
BuildArch:      noarch
Requires(post): %{name}-scripts

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package theme-spinfinity
Summary:        Plymouth "Spinfinity" theme
Group:          System/Base
Requires:       %{name}-plugin-throbgress = %{version}
BuildArch:      noarch
Requires(pre):  %{name}
Requires(post): %{name}-scripts

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package theme-spinner
Summary:        Plymouth "Spinner" theme
Group:          System/Base
Requires:       %{name}-plugin-two-step = %{version}
BuildArch:      noarch
Requires(post): %{name}-scripts

%description theme-spinner
This package contains the "spinner" boot splash theme for
Plymouth.

%package theme-solar
Summary:        Plymouth "Solar" theme
Group:          System/Base
Requires:       %{name}-plugin-space-flares = %{version}
BuildArch:      noarch
Requires(post): %{name}-scripts

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package theme-script
Summary:        Plymouth "Script" plugin
Group:          System/Base
Requires:       %{name}-plugin-script = %{version}
BuildArch:      noarch
Requires(post): %{name}-scripts

%description theme-script
This package contains the "script" boot splash theme for
Plymouth. It it is a simple example theme the uses the "script"
plugin.

%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch11 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch12 -p1
%patch13 -p1

# replace builddate with patch0date
sed -i "s/__DATE__/\"$(stat -c %y %{_sourcedir}/%{name}.changes)\"/" src/main.c

# Change the default theme
sed -i -e 's/fade-in/openSUSE/g' src/plymouthd.defaults

%build
autoreconf -fiv
%configure --disable-static                                      \
	   --disable-gtk \
           --enable-systemd-integration                          \
           --enable-tracing --disable-tests                      \
           --with-background-start-color-stop=0x1A3D1F           \
           --with-background-end-color-stop=0x4EA65C             \
           --with-background-color=0x3391cd                      \
           --disable-gdm-transition                              \
           --without-system-root-install                         \
           --without-rhgb-compat-link                            \
           --with-boot-tty=/dev/tty7                             \
           --with-shutdown-tty=/dev/tty1                         \
           --without-gdm-autostart-file                          \
           --with-release-file=/etc/os-release

make %{?_smp_mflags}

%install

%make_install
rm -f %{buildroot}/%{_bindir}/rhgb-client
#rm -f %{buildroot}%{_libexecdir}/plymouth/plymouth-generate-initrd
#rm -f %{buildroot}%{_libexecdir}/plymouth/plymouth-populate-initrd

# Glow isn't quite ready for primetime
rm -rf %{buildroot}%{_datadir}/plymouth/glow/
rm -rf %{buildroot}%{_datadir}/plymouth/themes/glow/
rm -f %{buildroot}%{_libdir}/plymouth/glow.so
#mv %{buildroot}/%{_lib}/systemd %{buildroot}/%{_libdir}

mkdir -p %{buildroot}%{_localstatedir}/lib/plymouth
mkdir -p %{buildroot}%{_localstatedir}/run/plymouth
cp $RPM_SOURCE_DIR/boot-duration %{buildroot}%{_datadir}/plymouth/default-boot-duration
cp $RPM_SOURCE_DIR/boot-duration %{buildroot}%{_localstatedir}/lib/plymouth
cp %{buildroot}/%{_datadir}/plymouth/plymouthd.defaults %{buildroot}/%{_sysconfdir}/plymouth/plymouth.conf

%post
if [ ! -e /.buildenv ]; then
   [ -f %{_localstatedir}/lib/plymouth/boot-duration ] || cp -f %{_datadir}/plymouth/default-boot-duration %{_localstatedir}/lib/plymouth/boot-duration
   %{_libexecdir}/plymouth/plymouth-update-initrd
fi
[ -x /bin/systemctl ] && /bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
    rm -f /boot/initrd-plymouth.img
    [ -x /bin/systemctl ] && /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post scripts  -p /sbin/ldconfig

%postun scripts  -p /sbin/ldconfig

%post -n libply-boot-client -p /sbin/ldconfig

%postun -n libply-boot-client -p /sbin/ldconfig

%post -n libply-splash-core -p /sbin/ldconfig

%postun -n libply-splash-core -p /sbin/ldconfig

%post -n libply-splash-graphics -p /sbin/ldconfig

%postun -n libply-splash-graphics -p /sbin/ldconfig

%post -n libply -p /sbin/ldconfig

%postun -n libply -p /sbin/ldconfig

%post theme-spinfinity
if [ $1 -eq 1 -a ! -e /.buildenv ]; then
   export LIB=%{_libdir}
   if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "text" ]; then
      %{_sbindir}/plymouth-set-default-theme -R spinfinity
   fi
fi

%postun theme-spinfinity
if [ $1 -eq 0 ]; then
    export LIB=%{_libdir}
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "spinfinity" ]; then
        %{_sbindir}/plymouth-set-default-theme -R --reset
    fi
fi

%post theme-fade-in
if [ $1 -eq 1 -a ! -e /.buildenv ]; then
   export LIB=%{_libdir}
   if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "text" ]; then
      %{_sbindir}/plymouth-set-default-theme -R fade-in
   fi
fi

%postun theme-fade-in
if [ $1 -eq 0 ]; then
    export LIB=%{_libdir}
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "fade-in" ]; then
        %{_sbindir}/plymouth-set-default-theme -R --reset
    fi
fi

%post theme-solar
if [ $1 -eq 1 -a ! -e /.buildenv ]; then
   export LIB=%{_libdir}
   if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "text" ]; then
      %{_sbindir}/plymouth-set-default-theme -R solar
   fi
fi

%postun theme-solar
if [ $1 -eq 0 ]; then
    export LIB=%{_libdir}
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme -R --reset
    fi
fi


%docs_package

%files
%defattr(-, root, root)
%{_libexecdir}/plymouth/*
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_sysconfdir}/plymouth
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%config(noreplace) %{_sysconfdir}/plymouth/plymouth.conf
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*
%{_datadir}/plymouth/default-boot-duration
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_datadir}/plymouth/bizcom.png
%ghost %{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%ghost %{_localstatedir}/lib/plymouth/boot-duration
%{_unitdir}/*

%files devel
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{plymouth_libdir}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/pkgconfig/ply-splash-core.pc
%{_libdir}/pkgconfig/ply-splash-graphics.pc
%{_libdir}/pkgconfig/ply-boot-client.pc
%{_includedir}/plymouth-1

%files -n libply-boot-client
%defattr(-, root, root)
%{_libdir}/libply-boot-client.so.2*

%files -n libply-splash-core
%defattr(-, root, root)
%{plymouth_libdir}/libply-splash-core.so.2*

%files -n libply-splash-graphics
%defattr(-, root, root)
%{_libdir}/libply-splash-graphics.so.2*

%files -n libply
%defattr(-, root, root)
%{plymouth_libdir}/libply.so.2*

%files scripts
%defattr(-, root, root)
%dir %{_libexecdir}/plymouth
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
#/lib/mkinitrd/scripts/boot-plymouth.sh
#/lib/mkinitrd/scripts/boot-plymouth.chroot.sh
#/lib/mkinitrd/scripts/setup-plymouth.sh


%files x11-renderer
#%defattr(-,root,root,-)
#%{_libdir}/plymouth/renderers/x11*

%files plugin-label
%defattr(-, root, root)
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%defattr(-, root, root)
%{_libdir}/plymouth/fade-throbber.so

%files theme-fade-in
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/fade-in
%{_datadir}/plymouth/themes/fade-in/bullet.png
%{_datadir}/plymouth/themes/fade-in/entry.png
%{_datadir}/plymouth/themes/fade-in/lock.png
%{_datadir}/plymouth/themes/fade-in/star.png
%{_datadir}/plymouth/themes/fade-in/fade-in.plymouth

%files plugin-throbgress
%defattr(-, root, root)
%{_libdir}/plymouth/throbgress.so

%files theme-spinfinity
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/spinfinity
%{_datadir}/plymouth/themes/spinfinity/box.png
%{_datadir}/plymouth/themes/spinfinity/bullet.png
%{_datadir}/plymouth/themes/spinfinity/entry.png
%{_datadir}/plymouth/themes/spinfinity/lock.png
%{_datadir}/plymouth/themes/spinfinity/throbber-[0-3][0-9].png
%{_datadir}/plymouth/themes/spinfinity/spinfinity.plymouth

%files plugin-space-flares
%defattr(-, root, root)
%{_libdir}/plymouth/space-flares.so

%files theme-spinner
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/spinner
%{_datadir}/plymouth/themes/spinner/*.*

%files theme-solar
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/solar
%{_datadir}/plymouth/themes/solar/*.png
%{_datadir}/plymouth/themes/solar/solar.plymouth

%files plugin-two-step
%defattr(-, root, root)
%{_libdir}/plymouth/two-step.so

%files plugin-script
%defattr(-, root, root)
%{_libdir}/plymouth/script.so

%files theme-script
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/script/
%{_datadir}/plymouth/themes/script/*.png
%{_datadir}/plymouth/themes/script/script.script
%{_datadir}/plymouth/themes/script/script.plymouth

%changelog
