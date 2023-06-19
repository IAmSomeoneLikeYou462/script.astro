# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2023 Someone Like You
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

class Updater(object):
    """This class is used to check if the addon is updated, and if not, update it"""
    def __init__(self):
        self.RELEASES_URL = "https://api.github.com/repos/IAmSomeoneLikeYou462/script.astro/releases?per_page=100&page=1"
        self.REMOTE_DATA = None
        self.LOCAL_VERSION = None
        self.getLocalVersion()

    def getLocalVersion(self):
        """This function read the version from the addon.xml file"""
        with open(os.path.join(translatePath(HOME), 'addon.xml'), 'r') as addonXml:
            data = ElementTree.fromstring(addonXml.read())
            self.LOCAL_VERSION = data.get('version')

    def checkAvailableVersion(self, silent):
        req = request.Request(self.RELEASES_URL)
        response = request.urlopen(req)
        data = response.read()
        self.REMOTE_DATA = data
        releases = json.loads(data)
        self.filtered_releases = list(filter(lambda rls: self.versiontuple(
            rls.get('tag_name')) > self.versiontuple(self.LOCAL_VERSION), releases))

        if len(self.filtered_releases) > 0:
            self.release = self.filtered_releases[0]
            self.downloadRemoteVersion(silent)
            return True
        else:
            return False

    def downloadRemoteVersion(self, silent):
        self.release_url = self.release.get('assets')[0].get('browser_download_url', None)
        dest = os.path.join(PACKAGES_DIR, self.release_url.split('/')[-1])
        self.download_file(self.release_url, dest, silent)
        self.extract_file(dest, ADDONS_DIR, silent)

    def extract_file(self, in_dest, out_dest, silent):
        from zipfile import ZipFile
        dialog = DialogProgress(TITLE, silent)
        with ZipFile(in_dest, 'r') as zip_ref:
            nFiles = float(len(zip_ref.infolist()))
            count = 0
            for item in zip_ref.infolist():
                count += 1
                update = count / nFiles * 100
                dialog.update(int(update), {'line1': 'Extrayendo Astro...'})
                zip_ref.extract(item, out_dest)

    def download_file(self, url, dest, silent):
        dialog = DialogProgress(TITLE, silent)
        request.urlretrieve(
            url, dest, lambda nb, bs, fs: dialog.downloadPercentage(nb, bs, fs, {'line1': 'Descargando Astro...'}))

    def versiontuple(self, vrs):
        """https://stackoverflow.com/a/11887825"""
        return tuple(map(int, (vrs.split("."))))
