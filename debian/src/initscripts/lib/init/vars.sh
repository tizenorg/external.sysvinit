#
# Set rcS vars
#

[ -f /etc/default/rcS ] && . /etc/default/rcS || true

# check for bootoption 'noswap' and do not activate swap
# partitions/files when it is set.
## Work around Busybox grep not supporting -w switch
#if [ -r /proc/cmdline ] && grep -qw 'noswap' /proc/cmdline ; then
if [ -r /proc/cmdline ] && egrep -q '(^|\W)noswap($|\W)' /proc/cmdline ; then
    NOSWAP=yes
else
    NOSWAP=no
fi

# Accept the same 'quiet' option as the kernel
## Work around Busybox grep not supporting -w switch
#if [ ! -e /proc/cmdline ] || egrep -qw 'quiet' /proc/cmdline ; then
if [ ! -e /proc/cmdline ] || egrep -q '(^|\W)quiet($|\W)' /proc/cmdline ; then
    VERBOSE="no"
fi

# But allow both rcS and the kernel options 'quiet' to be overrided
# when INIT_VERBOSE=yes is used as well.
[ "$INIT_VERBOSE" ] && VERBOSE="$INIT_VERBOSE" || true
