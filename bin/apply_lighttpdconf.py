#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Karesansui.
#
# Copyright (C) 2009-2010 HDE, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

import os
import os.path
import sys
import logging
from optparse import OptionParser

from ksscommand import KssCommand, KssCommandException, KssCommandOptException

import __cmd__

try:
    import karesansui
    from karesansui import __version__
    from karesansui.lib.utils import load_locale, copy_file, remove_file
    from karesansui.lib.const import LIGHTTPD_CONF_TEMP_DIR,\
        LIGHTTPD_PORT_CONFIG, LIGHTTPD_ACCESS_CONFIG, LIGHTTPD_SSL_CONFIG

except ImportError:
    print >>sys.stderr, "[Error] karesansui package was not found."
    sys.exit(1)

_ = load_locale()

usage = '%prog [options]'

def getopts():
    opts = OptionParser(usage=usage, version=__version__)
    opts.add_option('-d', '--dest', dest='dest', help=('copy destination directory'))
    opts.add_option('-p', '--port', dest='tmp_port_conf', help=('port.conf temporary file path'))
    opts.add_option('-s', '--ssl', dest='tmp_ssl_conf', help=('ssl.conf temporary file path'))
    opts.add_option('-a', '--access', dest='tmp_access_conf', help=('access.conf temporary file path'))
    return opts.parse_args()

def chkopts(opts):
    # option check
    if not opts.dest:
        raise KssCommandOptException('ERROR: -d or --dest option is required.')
    elif not opts.tmp_port_conf:
        raise KssCommandOptException('ERROR: -p or --port option is required.')
    elif not opts.tmp_ssl_conf:
        raise KssCommandOptException('ERROR: -s or --ssl option is required.')
    elif not opts.tmp_access_conf:
        raise KssCommandOptException('ERROR: -a or --access option is required.')

    # exist check
    if os.path.isdir(opts.dest) is False:
        raise KssCommandOptException('ERROR: Not directory dest=%s' % opts.dest)
    elif os.path.isfile(opts.tmp_port_conf) is False:
        raise KssCommandOptException('ERROR: Not exist temporary file tmp_port_conf=%s' % opts.tmp_port_conf)
    elif os.path.isfile(opts.tmp_ssl_conf) is False:
        raise KssCommandOptException('ERROR: Not exist temporary file tmp_ssl_conf=%s' % opts.tmp_ssl_conf)
    elif os.path.isfile(opts.tmp_access_conf) is False:
        raise KssCommandOptException('ERROR: Not exist temporary file tmp_access_conf=%s' % opts.tmp_access_conf)

class LighttpdConfigFile(KssCommand):

    def process(self):
        (opts, args) = getopts()
        chkopts(opts)
        opts.dest = opts.dest.rstrip('/')
        self.up_progress(10)

        tmp_configfiles = {
            LIGHTTPD_PORT_CONFIG : opts.tmp_port_conf,
            LIGHTTPD_SSL_CONFIG : opts.tmp_ssl_conf,
            LIGHTTPD_ACCESS_CONFIG : opts.tmp_access_conf
        }
        self.up_progress(10)

        for srcfile in tmp_configfiles.values():
            if os.path.isfile(srcfile) is False:
                raise KssCommandException(
                    'Temporary config file is not found. -path=%s' % srcfile)

        self.up_progress(20)
        try:
            for dest, src in tmp_configfiles.items():
                copy_file(src, opts.dest + '/' + dest)
                remove_file(src)

            self.up_progress(40)
        except:
            raise KssCommandException('Failed to copy config file -src=%s dest=%s' % (src, dest))

        self.logger.info('Applied lighttpd settings.')
        print >>sys.stdout, _('Applied lighttpd settings.')

        return True

if __name__ == "__main__":
    target = LighttpdConfigFile()
    sys.exit(target.run())
