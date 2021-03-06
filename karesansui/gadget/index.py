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

import web
from karesansui.lib.rest import Rest, auth
import karesansui.gadget.host

class Index(Rest):
    @auth
    def _GET(self, *param, **params):
        return True

urls = ('/', karesansui.gadget.host.Host)
