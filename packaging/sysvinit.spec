Summary: Programs which control basic system processes
Name: sysvinit
Version: 2.87
Release: 1
License: GPLv2+
Group: System/Base
Url: http://savannah.nongnu.org/projects/sysvinit

Requires: /bin/cp

Source: %{name}-%{version}dsf.tar.gz
Source1: inittab
Source2: update-rc.d
Source3: service

Patch0: 21_ifdown_kfreebsd.patch
Patch1: 50_bootlogd_devsubdir.patch
Patch2: 54_bootlogd_findptyfail.patch
Patch3: 55_bootlogd_flush.patch
Patch4: 60_init_selinux_ifdef.patch
Patch5: 62_init_freebsdterm.patch
Patch6: 63_init_keep_utf8_ttyflag.patch
Patch7: 70_compiler_warnings.patch
Patch8: 91_sulogin_lockedpw.patch
Patch9: 94_fstab-decode.patch
Patch10: 96_shutdown_acctoff.patch
Patch11: 97_init_starttest.patch
Patch12: 98_installtarget.patch
Patch13: startpar.patch
Patch14: always_use_lcrypt.patch
Patch15: dont_set_ownership.patch
Patch16: add_initscripts.patch
Patch17: add_sysvrc.patch
Patch18: 64_init_add_cmd_for_reboot.dpatch
Patch19: 0001-Fixing-syntax-error-in-start-stop-daemon.c.patch

%description
The sysvinit package contains a group of processes that control
the very basic functions of your system. sysvinit includes the init
program, the first program started by the Linux kernel when the
system boots. Init then controls the startup, running, and shutdown
of all other programs.

%package utils
Summary: System-V-like utilities
Group: System/Base
Provides: /usr/sbin/service
Provides: /bin/pidof

%description utils
 This package contains the important System-V-like utilities.
 Specifically, this package includes:
 killall5, last, lastb, mesg, pidof, service, sulogin

%package -n sysv-rc
Summary: System-V-like runlevel change mechanism
Group: System/Base
Requires: sysvinit-utils

%description -n sysv-rc
 This package provides support for the System-V like system
 for booting, changing runlevels, and shutting down,
 configured through symbolic links in /etc/rc?.d/.

%package -n initscripts
Summary: scripts for initializing the system
Group: System/Base
Requires: /lib/lsb/init-functions
Requires: /usr/sbin/update-rc.d

%description -n initscripts
 scripts for initializing and shutting down the system
 The scripts in this package initialize a system at boot time
 and shut it down at halt or reboot time.

%doc_package

%prep
%setup -q -n %{name}-%{version}dsf

%patch0 -p1 -b .ifdown_kfreebsd
%patch1 -p1 -b .bootlogd_devsubdir
%patch2 -p1 -b .bootlogd_findptyfail
%patch3 -p1 -b .bootlogd_flush
%patch4 -p1 -b .init_selinux_ifdef
%patch5 -p1 -b .init_freebsdterm
%patch6 -p1 -b .init_keep_utf8_ttyflag
%patch7 -p1 -b .compiler_warnings
%patch8 -p1 -b .sulogin_lockedpw
%patch9 -p1 -b .fstab-decode
%patch10 -p1 -b .shutdown_acctoff
%patch11 -p1 -b .init_starttest
%patch12 -p1 -b .installtarget
%patch13 -p1 -b .startpar
%patch14 -p1 -b .always_use_lcrypt
%patch15 -p1 -b .dont_set_ownership
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%build
make -C src
make -C startpar

export CFLAGS='-ansi -W -Wall -O2 -fomit-frame-pointer -D_GNU_SOURCE'
export LDFLAGS='-s'
gcc $LDFLAGS -o start-stop-daemon contrib/start-stop-daemon.c

%install
make -C src ROOT=$RPM_BUILD_ROOT install
make -C startpar DESTDIR=$RPM_BUILD_ROOT install
make -C initscripts DESTDIR=$RPM_BUILD_ROOT install
make -C sysv-rc DESTDIR=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install %SOURCE2 $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install %SOURCE3 $RPM_BUILD_ROOT/usr/sbin/

install start-stop-daemon $RPM_BUILD_ROOT/usr/sbin/

rm -f $RPM_BUILD_ROOT/usr/bin/wall
rm -f $RPM_BUILD_ROOT/usr/bin/lastb
rm -f $RPM_BUILD_ROOT/usr/bin/utmpdump
rm -f $RPM_BUILD_ROOT/usr/share/man/man1/wall.1*

rm -rf %{buildroot}/%{_docdir}

%post
echo ".... sysvinit post ....."
[ -f /etc/inittab ] || /bin/cp -p /usr/share/sysvinit/inittab /etc/inittab
exit 0

%post -n initscripts

set -e
umask 022
#
# Initialize rcS default file.
#
if [ ! -f /etc/default/rcS ]
then
	cp -p /usr/share/initscripts/default.rcS /etc/default/rcS
fi

#
# In 2.86.ds1-7 the "single" script was moved.
# We have to remove the old links _before_ we install new ones.
#
update-rc.d -f single remove >/dev/null

# In 2.86.ds1-16, the mtab.sh and hostname.sh scripts were moved.
update-rc.d -f mtab.sh remove >/dev/null
update-rc.d -f hostname.sh remove >/dev/null

# In 2.86.ds1-21, the sendsigs script were moved, and in 2.86.ds1-35
# it was moved back.
update-rc.d -f sendsigs remove >/dev/null

#
# In 2.87dsf-2 the "mountoverflowtmp" script was dropped
# from runlevels 0 and 6.
# We have to remove the old links _before_ we install new ones.
#
update-rc.d -f mountoverflowtmp remove >/dev/null

#
# Okay, we could do this with update-rc.d, but that would probably
# be pretty slow. This way we win some speed.
# DO NOT FOLLOW THIS EXAMPLE IN OTHER PACKAGES.
#
# Links in runlevel S
#
update-rc.d mountkernfs.sh         start 02 S . >/dev/null || exit $?
update-rc.d hostname.sh            start 02 S . >/dev/null || exit $?
update-rc.d mountdevsubfs.sh       start 04 S . >/dev/null || exit $?
update-rc.d bootlogd               start 05 S . >/dev/null || exit $?
update-rc.d checkroot.sh           start 10 S . >/dev/null || exit $?
update-rc.d mtab.sh                start 12 S . >/dev/null || exit $?
update-rc.d checkfs.sh             start 30 S . >/dev/null || exit $?
update-rc.d mountall.sh            start 35 S . >/dev/null || exit $?
update-rc.d mountall-bootclean.sh  start 36 S . >/dev/null || exit $?
update-rc.d mountoverflowtmp       start 37 S . >/dev/null || exit $?
update-rc.d mountnfs.sh            start 45 S . >/dev/null || exit $?
update-rc.d mountnfs-bootclean.sh  start 46 S . >/dev/null || exit $?
update-rc.d bootmisc.sh            start 55 S . >/dev/null || exit $?
update-rc.d urandom                start 55 S . start 30 0 6 . >/dev/null || exit $?
#
# Links in runlevels other than S
#
update-rc.d halt                   start 90 0 . >/dev/null || exit $?
update-rc.d reboot                 start 90 6 . >/dev/null || exit $?
update-rc.d umountroot             start 60 0 6 . >/dev/null || exit $?
update-rc.d umountfs               start 40 0 6 . >/dev/null || exit $?
update-rc.d umountnfs.sh           start 31 0 6 . >/dev/null || exit $?
update-rc.d sendsigs               start 20 0 6 . >/dev/null || exit $?

update-rc.d killprocs              start 30 1 . >/dev/null || exit $?
update-rc.d single                 start 90 1 . >/dev/null || exit $?
update-rc.d bootlogs               start 70 1 2 3 4 5 . >/dev/null || exit $?
update-rc.d rc.local               start 99 2 3 4 5 . >/dev/null || exit $?
update-rc.d rmnologin              start 99 2 3 4 5 . >/dev/null || exit $?
update-rc.d stop-bootlogd-single   start 99 S . >/dev/null || exit $?
update-rc.d stop-bootlogd          start 99 2 3 4 5 . >/dev/null || exit $?

#
# Remove scripts that were left behind by older glibc (<< 2.3.2.ds1-12)
# versions. We have the same functionality in mount{kern,devsub}fs.sh 
#
#
# In 2.86.ds1-10 the "mountvirtfs" script was replaced by
# mountkernfs.sh and mountdevsubfs.sh.  It was removed completely in
# 2.86.ds1-16.
#
for F in mountkernfs devpts.sh mountvirtfs
do
	rm -f /etc/init.d/$F
	update-rc.d $F remove >/dev/null
done

#
# When installing for the first time or upgrading from version before
# 2.86.ds1-27, a reboot is needed to make the /lib/init/rw/ tmpfs
# available.  Flag this using notify-reboot-required.  Not mounting it
# here as it creates problem for debootstrap, vservers, pbuilder and
# cowbuilder.
#
if [ -x /usr/share/update-notifier/notify-reboot-required ]; then
	/usr/share/update-notifier/notify-reboot-required
fi

#
# Create initial log files
#
for F in /var/log/dmesg /var/log/boot /var/log/fsck/checkroot /var/log/fsck/checkfs
do
	if [ ! -f "$F" ] && touch "$F" >/dev/null 2>&1
	then
		echo "(Nothing has been logged yet.)" >| "$F"
		# root UID is 0, adm GID is ordinary 4
		chown 0:4 "$F"
		chmod 640 "$F"
	fi
done

#
# Set up nologin symlink so that dynamic-login-disabling will work
# (when DELAYLOGIN is set to "yes")
#
if [ ! -L /etc/nologin ] && [ ! -e /etc/nologin ]
then
	rm -f /var/lib/initscripts/nologin
	ln -s /var/lib/initscripts/nologin /etc/nologin
fi

#
# Set up motd stuff, putting variable file in /var/run/
#
if [ ! -f /etc/motd.tail ]
then
	if [ -f /etc/motd ]
	then
		sed 1d /etc/motd > /etc/motd.tail
		[ -s /etc/motd.tail ] || rm -f /etc/motd.tail
	fi
fi
if [ ! -f /var/run/motd ]
then
	if [ -f /etc/motd ]
	then
		cat /etc/motd > /var/run/motd
	else
		:>/var/run/motd
	fi
fi
if [ ! -L /etc/motd ]
then
	[ -f /etc/default/rcS ] && . /etc/default/rcS
	if [ "$EDITMOTD" = no ]
	then
		cat /var/run/motd > /etc/motd.static
		ln -sf motd.static /etc/motd
	else
		ln -sf /var/run/motd /etc/motd
	fi
fi

#
# Mount kernel virtual filesystems...not.
# This causes problems in pbuilder.
#
#
#if [ -x /etc/init.d/mountkernfs.sh ]
#then
#	if which invoke-rc.d >/dev/null 2>&1
#	then
#		invoke-rc.d mountkernfs.sh start || :
#	else
#		/etc/init.d/mountkernfs.sh start
#	fi
#fi

#
# Create /dev/pts, /dev/shm directories
#
if [ "$(uname -s)" = Linux ]
then
	#
	# Only create /dev/{pts,shm} if /dev is on the
	# root file system. If some package has mounted a
	# seperate /dev (ramfs from udev, devfs) it is
	# responsible for the presence of those subdirs.
	# (it is OK for these to fail under fakechroot)
	#
	if ! mountpoint -q /dev
	then
		# root UID is 0
		[ -d /dev/pts ] || { mkdir --mode=755 /dev/pts ; chown 0:0 /dev/pts || [ "$FAKECHROOT" = true ]; }
		[ -d /dev/shm ] || { mkdir --mode=755 /dev/shm ; chown 0:0 /dev/shm || [ "$FAKECHROOT" = true ]; }
	fi
fi

#
# Create /etc/rc.local on first time install and when upgrading from
# versions before "2.86.ds1-16"
#
if [ ! -e /etc/rc.local ]; then
	cat << EOF > /etc/rc.local
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

exit 0
EOF
		# make sure it's enabled by default.
		chmod 755 /etc/rc.local
fi


%clean
rm -rf $RPM_BUILD_ROOT


%docs_package

%files
%defattr(-,root,root)
/sbin/init
/sbin/halt
/sbin/runlevel
/sbin/shutdown
/sbin/poweroff
/sbin/reboot
/sbin/telinit
%{_datadir}/%{name}/inittab
%{_datadir}/%{name}/update-rc.d
%{_includedir}/initreq.h

%files utils
/bin/pidof
/sbin/bootlogd
/sbin/fstab-decode
/sbin/killall5
/sbin/sulogin
/sbin/startpar
/usr/sbin/start-stop-daemon
%attr(755,root,root)/usr/sbin/service
/usr/bin/last
/usr/bin/mesg

%files -n sysv-rc
%doc %{_sysconfdir}/rc0.d/README
%doc %{_sysconfdir}/rc1.d/README
%{_sysconfdir}/rc2.d/README
%{_sysconfdir}/rc3.d/README
%{_sysconfdir}/rc4.d/README
%{_sysconfdir}/rc5.d/README
%{_sysconfdir}/rc6.d/README
%{_sysconfdir}/rcS.d/README
/usr/sbin/invoke-rc.d
/usr/sbin/update-rc.d
%{_datadir}/sysv-rc/saveconfig


%files -n initscripts
%{_sysconfdir}/init.d/*
%{_sysconfdir}/init.d/.slp
%{_sysconfdir}/default/*
%{_datadir}/initscripts/default.rcS
/etc/network/if-up.d/mountnfs
/sbin/fsck.nfs
/lib/init/*
/bin/mountpoint

