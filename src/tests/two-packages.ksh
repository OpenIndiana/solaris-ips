#!/bin/ksh -px
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END

# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.

eval `pkgsend open library/libc@0.1-1`
if [ $? != 0 ]; then
	echo \*\* script aborted:  couldn\'t open library/libc
	exit 1
fi

echo $PKG_TRANS_ID
pkgsend add dir mode=0755 owner=root group=bin path=/lib
pkgsend add file /lib/libc.so.1 mode=0555 owner=root group=bin path=/lib/libc.so.1
pkgsend add link path=/lib/libc.so target=/lib/libc.so.1
pkgsend close

eval `pkgsend open application/cat@0.1-1`
if [ $? != 0 ]; then
	echo \*\* script aborted:  couldn\'t open application/cat
	exit 1
fi

echo $PKG_TRANS_ID
pkgsend add depend type=require fmri=pkg:/library/libc@0.1-1
pkgsend add dir mode=0755 owner=root group=bin path=/usr
pkgsend add dir mode=0755 owner=root group=bin path=/usr/bin
pkgsend add file /usr/bin/cat mode=0555 owner=root group=bin path=/usr/bin/cat
pkgsend close
