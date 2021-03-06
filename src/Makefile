#
# Makefile	Makefile for the systemV init suite.
#		Targets:   all      compiles everything
#		           install  installs the binaries (not the scripts)
#                          clean    cleans up object files
#			   clobber  really cleans up
#
# Version:	@(#)Makefile  2.85-13  23-Mar-2004  miquels@cistron.nl
#

CC	= gcc
CFLAGS	= -ansi -W -Wall -O2 -fomit-frame-pointer -D_GNU_SOURCE
LDFLAGS	= -s
STATIC	=

# For some known distributions we do not build all programs, otherwise we do.
BIN	=
SBIN	= init halt shutdown runlevel killall5
USRBIN	= last mesg

MAN1	= last.1 lastb.1 mesg.1
MAN5	= initscript.5 inittab.5
MAN8	= halt.8 init.8 killall5.8 pidof.8 poweroff.8 reboot.8 runlevel.8
MAN8	+= shutdown.8 telinit.8

ifeq ($(DISTRO),)
BIN	+= mountpoint
SBIN	+= sulogin bootlogd
USRBIN	+= utmpdump wall
MAN1	+= mountpoint.1 wall.1
MAN8	+= sulogin.8 bootlogd.8
endif

ifeq ($(DISTRO),Debian)
BIN	+= mountpoint
SBIN	+= sulogin bootlogd
MAN1	+= mountpoint.1
MAN8	+= sulogin.8 bootlogd.8
endif

ifeq ($(DISTRO),Owl)
USRBIN	+= wall
MAN1	+= wall.1
endif

BIN_OWNER	= root
BIN_GROUP	= root
BIN_COMBO	= $(BIN_OWNER):$(BIN_GROUP)
STRIP		= strip -s -R .comment
INSTALL_EXEC	= install -o $(BIN_OWNER) -g $(BIN_GROUP) -m 755
INSTALL_DATA	= install -o $(BIN_OWNER) -g $(BIN_GROUP) -m 644
MANDIR		= /usr/share/man

ifeq ($(WITH_SELINUX),yes)
  SELINUX_DEF=-DWITH_SELINUX
  INIT_SELIBS=-lsepol -lselinux
  SULOGIN_SELIBS=-lselinux	
else
  SELINUX_DEF=
  INIT_SELIBS=
  SULOGIN_SELIBS=
endif



# Additional libs for GNU libc.
ifneq ($(wildcard /usr/lib/libcrypt.a),)
LCRYPT		= -lcrypt
endif

all:		$(BIN) $(SBIN) $(USRBIN)

init:		init.o init_utmp.o
		$(CC) $(LDFLAGS) $(STATIC) -o $@ init.o init_utmp.o $(INIT_SELIBS)

halt:		halt.o ifdown.o hddown.o utmp.o reboot.h
		$(CC) $(LDFLAGS) -o $@ halt.o ifdown.o hddown.o utmp.o

last:		last.o oldutmp.h
		$(CC) $(LDFLAGS) -o $@ last.o

mesg:		mesg.o
		$(CC) $(LDFLAGS) -o $@ mesg.o

mountpoint:	mountpoint.o
		$(CC) $(LDFLAGS) -o $@ mountpoint.o

utmpdump:	utmpdump.o
		$(CC) $(LDFLAGS) -o $@ utmpdump.o

runlevel:	runlevel.o
		$(CC) $(LDFLAGS) -o $@ runlevel.o

sulogin:	sulogin.o
		$(CC) $(LDFLAGS) $(STATIC) $(SELINUX_DEF) -o $@ $^ $(LCRYPT) $(SULOGIN_SELIBS)

wall:		dowall.o wall.o
		$(CC) $(LDFLAGS) -o $@ dowall.o wall.o

shutdown:	dowall.o shutdown.o utmp.o reboot.h
		$(CC) $(LDFLAGS) -o $@ dowall.o shutdown.o utmp.o

bootlogd:	bootlogd.o
		$(CC) $(LDFLAGS) -o $@ bootlogd.o -lutil

sulogin.o:	sulogin.c 
		$(CC) -c $(CFLAGS) $(SELINUX_DEF) sulogin.c

init.o:		init.c init.h set.h reboot.h initreq.h
		$(CC) -c $(CFLAGS) $(SELINUX_DEF)  init.c

utmp.o:		utmp.c init.h
		$(CC) -c $(CFLAGS) utmp.c

init_utmp.o:	utmp.c init.h
		$(CC) -c $(CFLAGS) -DINIT_MAIN utmp.c -o init_utmp.o

cleanobjs:
		rm -f *.o *.bak

clean:		cleanobjs
		@echo Type \"make clobber\" to really clean up.

clobber:	cleanobjs
		rm -f $(BIN) $(SBIN) $(USRBIN)

distclean:	clobber

install:
		for i in $(BIN); do \
			$(STRIP) $$i ; \
			$(INSTALL_EXEC) $$i $(ROOT)/bin/ ; \
		done
		for i in $(SBIN); do \
			$(STRIP) $$i ; \
			$(INSTALL_EXEC) $$i $(ROOT)/sbin/ ; \
		done
		for i in $(USRBIN); do \
			$(STRIP) $$i ; \
			$(INSTALL_EXEC) $$i $(ROOT)/usr/bin/ ; \
		done
		# $(INSTALL_EXEC) etc/initscript.sample $(ROOT)/etc/
		ln -sf halt $(ROOT)/sbin/reboot
		ln -sf halt $(ROOT)/sbin/poweroff
		ln -sf init $(ROOT)/sbin/telinit
		ln -sf /sbin/killall5 $(ROOT)/bin/pidof
		if [ ! -f $(ROOT)/usr/bin/lastb ]; then \
			ln -sf last $(ROOT)/usr/bin/lastb; \
		fi
		$(INSTALL_DATA) initreq.h $(ROOT)/usr/include/
		for i in $(MAN1); do \
			$(INSTALL_DATA) ../man/$$i $(ROOT)$(MANDIR)/man1/; \
		done
		for i in $(MAN5); do \
			$(INSTALL_DATA) ../man/$$i $(ROOT)$(MANDIR)/man5/; \
		done
		for i in $(MAN8); do \
			$(INSTALL_DATA) ../man/$$i $(ROOT)$(MANDIR)/man8/; \
		done
ifeq ($(ROOT),)
		#
		# This part is skipped on Debian systems, the
		# debian.preinst script takes care of it.
		@if [ ! -p /dev/initctl ]; then \
		 echo "Creating /dev/initctl"; \
		 rm -f /dev/initctl; \
		 mknod -m 600 /dev/initctl p; fi
endif
