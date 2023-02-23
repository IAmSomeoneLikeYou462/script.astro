# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2022 Someone Like You
#
# This file is part of Astro.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from tools import *
from developertools import *

def set_admin_password():
    passwordInput = xbmcgui.Dialog().input(f"{TITLE} - {getLocalizedString(32027)}", "", xbmcgui.INPUT_ALPHANUM)
    if passwordInput:
        passwordFin = str(hashlib.md5(str(passwordInput).encode()).hexdigest())
        set_setting("astro_admin_password", passwordFin)

def updateAstroRemoteConfig():
    astroRemoteUrl = get_setting('astro_remote_url')
    if astroRemoteUrl != "" and astroRemoteUrl is not None:
        from urllib import request
        req = request.Request(astroRemoteUrl)
        response = request.urlopen(req)
        data = response.read()
        jdata = json.loads(data)
        remoteAdminPassword = jdata.get('adminPassword')
        if get_setting('admin_password') != "" and get_setting('admin_password') is not None and get_setting('admin_password') == remoteAdminPassword:
            return xbmcgui.Dialog().notification(TITLE, "Admin detected, ignore remote update", ICON)
        if get_setting('astro_remote_hash') != jdata.get('hash'):
            convertJsonToDB(jdata=jdata, override=True)