#! /bin/sh
### BEGIN INIT INFO
# Provides:          mountnfs-bootclean
# Required-Start:    $local_fs mountnfs
# Required-Stop:
# Default-Start:     S
# Default-Stop:
# Short-Description: bootclean after mountnfs.
# Description:       Clean temporary filesystems after
#                    network filesystems have been mounted.
### END INIT INFO

## We don't need this on SLP platform
[ -e /etc/init.d/.slp ] && exit 0

case "$1" in
  start|"")
	# Clean /tmp, /var/lock, /var/run
	. /lib/init/bootclean.sh
	;;
  restart|reload|force-reload)
	echo "Error: argument '$1' not supported" >&2
	exit 3
	;;
  stop)
	# No-op
	;;
  *)
	echo "Usage: mountnfs-bootclean.sh [start|stop]" >&2
	exit 3
	;;
esac

:
