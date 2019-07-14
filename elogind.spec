%global commit 95ddd43cdde907e7439cd7e85bf32837112770d7
%global shortcommit %(c=%{commit}; echo ${c:0:7}) 
%global gittag v241.1

Name:     elogind
Version:  241.1
Release:  1%{dist} 
Summary:  The systemd project's "logind", extracted to a standalone package
License:  GPL2, LGPL2.1
URL:      https://github.com/elogind/elogind
 
Source0:  https://github.com/elogind/elogind/archive/%{gittag}/%{name}-%{version}.tar.gz  

BuildRequires: git 
BuildRequires: gcc 
BuildRequires: m4
BuildRequires: cmake
BuildRequires: meson
BuildRequires: gettext
BuildRequires: libcap-devel
BuildRequires: dbus-devel
BuildRequires: pam-devel
BuildRequires: glib2
BuildRequires: glib2-devel
BuildRequires: pcre2-devel
BuildRequires: ninja-build
BuildRequires: kexec-tools
BuildRequires: gperf
BuildRequires: libxslt-devel 
BuildRequires: docbook-style-xsl
BuildRequires: libacl-devel
BuildRequires: polkit-devel
BuildRequires: libacl-devel
BuildRequires: audit-libs-devel
BuildRequires: libblkid-devel
BuildRequires: libcap-devel
BuildRequires: keyutils-libs-devel
BuildRequires: libmount-devel
BuildRequires: pam-devel
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
%description -n lib%name
This library provides access to %name session management.

%package -n lib%name-devel
Summary:  Development libraries for elogind
Provides:  elogind-devel = %version-%release
%description -n lib%name-devel
Header and Library files for doing development with the elogind.

%package -n bash-completion-%name
Summary: Bash completion for %name utils
BuildArch: noarch
Requires: bash-completion
Requires: %name = %version-%release

%description -n bash-completion-%name
Bash completion for %name.

%prep

%autosetup -n elogind-fedora-crouton-wayland-%{commit}

%build
%meson \
-Dpamlibdir=/%_libdir/security \
-Dcgroup-controller=%name \
-Ddefault-hierarchy=hybrid \
-Ddefault-kill-user-processes=false \
-Dtty-gid=5 \
-Dsystem-uid-max=499 \
-Dsystem-gid-max=499 \
-Dsplit-usr=auto \
-Dman=true \
-Dutmp=true \
-Dpolkit=true \
-Dacl=true \
-Daudit=true \
-Dpam=true \
-Dselinux=true \
-Dsmack=true \
-Dstatic-libelogind=pic \
-Dtests=false \

%meson_build

%install
%meson_install

%find_lang %name

%post

%files -f %name.lang
/%_bindir/*
/%_libdir/lib%{name}.so.*
/%_libdir/libelogind.a
/%_prefix/lib/elogind/*
/%_prefix/lib/udev/rules.d/*.rules
/%_libdir/security/pam_elogind.so
/%{_sysconfdir}/pam.d/*
/%{_sysconfdir}/elogind/*
/%_datadir/dbus-1/system-services/org.freedesktop.login1.service
/%_datadir/dbus-1/system.d/org.freedesktop.login1.conf
/%_datadir/polkit-1/actions/org.freedesktop.login1.policy
/%_datadir/factory/etc/pam.d/*
/%_datadir/zsh/*
/%_mandir/*
/%_docdir/*

%files -n lib%name
/%_libdir/*.so.*

%files -n lib%name-devel
/%_includedir/%name
/%_libdir/*.so
/%_libdir/pkgconfig/libelogind.pc
/%_mandir/*

%files -n bash-completion-%name
/%_datadir/bash-completion/completions/*

%changelog
* Sun Jul 14 2019 Boyd Kelly <bkelly@coastsystems.net> - 241.1
- Initial version of elogind for Fedora and fedora-crouton-wayland 
