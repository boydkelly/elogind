%global commit 2a7eaf306d6910c270212b65a2b6a950986d398c
%global shortcommit %(c=%{commit}; echo ${c:0:7}) 

Name:     elogind
Version:  241
Release:  1 
Summary:  The systemd project's "logind", extracted to a standalone package
Group:    System/Configuration/Boot and Init
License:  GPL2, LGPL2.1
URL:      https://github.com/elogind/elogind
Packager: Boyd Kelly 

Source0:  https://github.com/boydkelly/elogind-fedora-crouton-wayland/archive/%{commit}/%{name}-%{shortcommit}.tar.gz  
#Source1: elogind-dbus-helper
#Source2: elogind.init
#Source3: elogind.sysconfig
#Source4: pam_elogind.control
#Source5: libelogind-preload.control

Conflicts: systemd
Conflicts: systemd-services

BuildRequires: gcc 
BuildRequires: m4
BuildRequires: cmake
BuildRequires: meson
BuildRequires: gettext
BuildRequires: libcap-devel
BuildRequires: dbus-devel
BuildRequires: pam-devel
BuildRequires: ninja-build
BuildRequires: kexec-tools
BuildRequires: gperf
BuildRequires: libxslt 
BuildRequires: docbook-xsl
BuildRequires: libacl-devel
BuildRequires: audit-libs-devel
BuildRequires: libblkid-devel
BuildRequires: libcap-devel
BuildRequires: keyutils-libs-devel
BuildRequires: libmount-devel
BuildRequires: pam-devel
BuildRequires: polkit-devel
BuildRequires: systemd-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: libudev-devel

%define _unpackaged_files_terminate_build 1

%description
Elogind is the systemd project's "logind", extracted out to be a
standalone daemon.  It integrates with PAM to know the set of users
that are logged in to a system and whether they are logged in
graphically, on the console, or remotely.

%package -n lib%name
Summary:  The %name library
Group:    System/Libraries

%description -n lib%name
This library provides access to %name session management.

%package -n lib%name-devel
Summary:  Development libraries for elogind
Group:    Development/C

Obsoletes: elogind-devel
Provides:  elogind-devel = %version-%release

%description -n lib%name-devel
Header and Library files for doing development with the elogind.

%package -n lib%name-devel-docs
Summary:  Development documentation for elogind
Group:    Development/C

Conflicts: libsystemd-devel

%description -n lib%name-devel-docs
Development documentation for elogind.

%package -n lib%name-devel-static
Summary:  Development static libraries for elogind
Group:    Development/C

Obsoletes: elogind-devel-static
Provides:  elogind-devel-static = %version-%release

%description -n lib%name-devel-static
Header and Static Library files for doing development with the elogind.

%package -n bash-completion-%name
Summary: Bash completion for %name utils
Group: Shells
BuildArch: noarch
Requires: bash-completion
Requires: %name = %version-%release

%description -n bash-completion-%name
Bash completion for %name.

%prep
%setup

%build
%meson \
-Drootlibdir=/%_lib \
-Dpamlibdir=/%_lib/security \
-Dcgroup-controller=%name \
-Ddefault-hierarchy=hybrid \
-Ddefault-kill-user-processes=false \
-Dtty-gid=5 \
-Dsystem-uid-max=499 \
-Dsystem-gid-max=499 \
-Dsplit-usr=true \
-Dman=true \
-Dutmp=true \
-Dpolkit=true \
-Dacl=true \
-Daudit=true \
-Dpam=true \
-Dselinux=true \
-Dsmack=true \
-Dhalt-path=/sbin/halt \
-Dreboot-path=/sbin/reboot \
-Dstatic-libelogind=pic \
-Dtests=false \
#

%meson_build

%install
%meson_install

%find_lang %name

rm -rf -- \
%buildroot/%_datadir/zsh \
%buildroot/%_datadir/factory \
%buildroot/%_datadir/doc

for f in %buildroot/lib/udev/rules.d/*.rules; do
n="${f##*/}"
mv -f -- "$f" "${f%%/*}/${n%%%%-*}-elogind-${n#*-}"
done

for f in \
%_bindir/busctl /bin/loginctl; do 
n="${f##*/}"
d="${f%%/*}"

mv -f -- "%buildroot/$f" "%buildroot/$d/e$n"
ln -s -- "e$n" "%buildroot/$f"

sed -i \
-e "s#/$n#/e$n#g" \
%buildroot/lib/udev/rules.d/*.rules
done

sed -i \
-e '/^complete -F _loginctl loginctl/a \
complete -F _loginctl eloginctl' \
%buildroot/%_datadir/bash-completion/completions/loginctl
ln -s loginctl %buildroot/%_datadir/bash-completion/completions/eloginctl

%pre_control pam_elogind
%pre_control libelogind-preload

%post
%post_control -s enabled pam_elogind
%post_control -s enabled libelogind-preload

%files -f %name.lang
%_initdir/elogind
/bin/elogind-inhibit
/bin/loginctl
/bin/eloginctl
%_bindir/busctl
%_bindir/ebusctl
/lib64/%name
/lib/udev/rules.d/*.rules
/%_lib/security/pam_elogind.so
%_datadir/dbus-1/system-services/org.freedesktop.login1.service
%_datadir/dbus-1/system.d/org.freedesktop.login1.conf
%_datadir/polkit-1/actions/org.freedesktop.login1.policy
%_man1dir/*
%_man5dir/*
%_man7dir/*
%_man8dir/*

%files -n lib%name
/%_lib/*.so.*

%files -n lib%name-devel
%_includedir/%name
/%_lib/*.so
%_pkgconfigdir/libelogind.pc

%files -n lib%name-devel-static
/%_lib/*.a

%files -n lib%name-devel-docs
%_man3dir/*

%files -n bash-completion-%name
%_datadir/bash-completion/completions/*

%changelog
