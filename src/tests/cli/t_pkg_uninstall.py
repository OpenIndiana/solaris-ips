#!/usr/bin/python
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
#

# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.

import testutils
if __name__ == "__main__":
        testutils.setup_environment("../../../proto")

import os
import unittest

class TestCommandLine(testutils.SingleDepotTestCase):
        # Only start/stop the depot once (instead of for every test)
        persistent_depot = True

        def test_pkg_bogus_opts(self):
                """ pkg bogus option checks """

                # create a image to avoid non-existant image messages
                durl = self.dc.get_depot_url()
                self.image_create(durl)

                self.pkg("uninstall -@ foo", exit=2)
                self.pkg("uninstall -vq foo", exit=2)
                self.pkg("uninstall", exit=2)
                self.pkg("uninstall foo@x.y", exit=1)
                self.pkg("uninstall pkg:/foo@bar.baz", exit=1)
                self.image_destroy()

        foo12 = """
            open foo@1.2,5.11-0
            add dir path=/tmp mode=0755 owner=root group=bin
            close """

        def test_rmdir_cwd(self):
                """Remove a package containing a directory that's our cwd."""

                durl = self.dc.get_depot_url()
                self.pkgsend_bulk(durl, self.foo12)
                self.image_create(durl)

                self.pkg("install foo")
                os.chdir(os.path.join(self.get_img_path(), "tmp"))
                self.pkg("uninstall foo")
                self.image_destroy()

        foob20 = """
            open foob@2.0,5.11-0
            add depend type=require fmri=barb@2.0
            close """

        barb20 = """
            open barb@2.0,5.11-0
            add depend type=require fmri=foob@2.0
            close """

        bazb20 = """
            open bazb@2.0,5.11-0
            add depend type=require fmri=foob@2.0
            close """

        def test_dependencies(self):
                """This code tests for:
                  1) uninstall is blocked if dependencies are found
                  2) packages w/ circular dependencies can be uninstalled
                  3) if all dependencies are to be deleted, uninstall works."""
                durl = self.dc.get_depot_url()
                self.pkgsend_bulk(durl, self.foob20)
                self.pkgsend_bulk(durl, self.barb20)
                self.pkgsend_bulk(durl, self.bazb20)
                self.image_create(durl)
                self.pkg("install bazb")
                self.pkg("verify")
                self.pkg("uninstall foob", exit=1)
                self.pkg("uninstall bazb foob barb")
                self.pkg("verify")
                self.image_destroy()

        quux10 = """
            open quux@1.0,5.11-0
            close """

        renamed10 = """
            open renamed@1.0,5.11-0
            add set name=pkg.renamed value=true
            add depend type=require fmri=quux@1.0
            close """

        def test_uninstalled_state(self):
                """Uninstalling a package that is no longer known should result
                in its removal from the output of pkg list -a, even if it has
                been renamed, etc.""" 

                durl = self.dc.get_depot_url()
                self.pkgsend_bulk(durl, self.quux10 + self.renamed10)
                self.image_create(durl)
                self.pkg("install -v renamed")
                self.pkg("verify")
                self.pkg("set-publisher -P -g %s bogus" % durl)
                self.pkg("unset-publisher test")
                self.pkg("info quux@1.0 renamed@1.0")
                self.pkg("uninstall renamed")
                self.pkg("list -a renamed@1.0", exit=1)
                self.pkg("uninstall quux")
                self.pkg("list -a quux@1.0", exit=1)
                self.image_destroy()


if __name__ == "__main__":
        unittest.main()
