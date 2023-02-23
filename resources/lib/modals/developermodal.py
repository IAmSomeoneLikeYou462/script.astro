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

import pyxbmct
import hashlib
from tools import *
from developertools import *


class DeveloperModal(pyxbmct.AddonDialogWindow):
    def __init__(self, title=TITLE):
        super(DeveloperModal, self).__init__(title)
        self.setGeometry(500, 450, 9, 2)
        self.set_controls()
        self.set_navigation()
        self.prepareList()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        self.closeButton = pyxbmct.Button('Cerrar')
        self.placeControl(self.closeButton, 8, 0, 1, 2)
        self.connect(self.closeButton, self.close)
        self.list = pyxbmct.List()
        self.placeControl(self.list, 0, 0, 8, 2)

    def prepareList(self):
        self.list.addItems(DEVELOPER_OPTIONS)
        self.connect(self.list, lambda: self.onClickList(
            self.list.getSelectedPosition()))

    def getDirectoryJsonFile(self):
        fileName = 'astro-{}.json'.format(
            time.strftime('%m-%d-%Y %H-%M-%S'))
        directory = os.path.join(translatePath(PROFILE),
                                 fileName)
        return fileName, directory

    def onClickList(self, position):
        if DEVELOPER_OPTIONS[position] == getLocalizedString(32007):
            folders = convertDbJson('astro_folders', json_str=False)
            actions = convertDbJson('astro_actions', json_str=False)
            data = [{'astro_folders': folders, 'astro_actions': actions}]
            astroRemoteHash = str(hashlib.md5(str(data).encode()).hexdigest())
            adminPassword = xbmcgui.Dialog().input(f"{TITLE} - {getLocalizedString(32027)}", "", xbmcgui.INPUT_ALPHANUM)
            if not adminPassword or adminPassword == "":
                xbmcgui.Dialog().notification(TITLE, 'You have to set a valid password', ICON)
                return
            fileName, directory = self.getDirectoryJsonFile()
            with open(directory,
                      'w+') as astroFile:
                astroFile.write(json.dumps(
                    {'data': data,
                     'hash': astroRemoteHash,
                     'adminPassword': str(hashlib.md5(str(adminPassword).encode()).hexdigest())}))
            xbmcgui.Dialog().notification(TITLE, '{} File created and stored in [COLOR orange]{}[/COLOR]'.format(
                fileName, translatePath(directory)), ICON)
        elif DEVELOPER_OPTIONS[position] == getLocalizedString(32010):
            # Pastebin does not accept the JSON, TODO: Find another web to upload the file
            globPath = os.path.join(PROFILE, '*.json')
            files = glob.glob(globPath)
            fileNames = [fileName.split('astro-')[1].split('.json')[0]
                         for fileName in files]
            fileNames = sorted(
                fileNames, key=lambda fileName: self.sortJsonFiles(fileName))
            fileSelection = xbmcgui.Dialog().select(TITLE, fileNames)
            if fileSelection == -1:
                xbmcgui.Dialog().notification(
                    '[COLOR red]%s[/COLOR]' % (TITLE), 'Selection canceled', ICON)
                return
            fileSelected = files[fileSelection]
            data = open(os.path.join(PROFILE, fileSelected), 'r').read()
            # uploadPastebin(fileSelected, data)
        elif DEVELOPER_OPTIONS[position] == getLocalizedString(32011):
            inputRemoteUrl = xbmcgui.Dialog().input(
                '{} - {}'.format(TITLE, getLocalizedString(32012)), '', xbmcgui.INPUT_ALPHANUM)
            if not inputRemoteUrl or len(inputRemoteUrl) == 0 or not inputRemoteUrl.startswith('http'):
                xbmcgui.Dialog().notification(TITLE, getLocalizedString(32029), ICON)
                return
            set_setting('astro_remote_url', inputRemoteUrl)
            convertJsonToDB(astroRemoteLink=inputRemoteUrl)
        elif DEVELOPER_OPTIONS[position] == getLocalizedString(32016):
            # TODO: Next Release
            if bool(xbmc.getCondVisibility('System.HasAddon(%s)' % 'plugin.program.super.favourites')):
                SV_PROFILE = translatePath(xbmcaddon.Addon(
                    'plugin.program.super.favourites').getAddonInfo('Profile'))
                SV_FOLDER = translatePath(
                    os.path.join(SV_PROFILE, 'Super Favourites'))
        elif DEVELOPER_OPTIONS[position] == getLocalizedString(32027):
            import servicetools
            servicetools.set_admin_password()
            return
        elif DEVELOPER_OPTIONS[position] == getLocalizedString(32000):
            ADDON.openSettings()
            self.close()
    def sortJsonFiles(self, fileName): return time.strptime(
        fileName, "%m-%d-%Y %H-%M-%S")

    def set_navigation(self):
        self.list.controlUp(self.closeButton)
        self.list.controlDown(self.closeButton)
        self.closeButton.controlUp(self.list)
        self.closeButton.controlDown(self.list)
        self.setFocus(self.closeButton)
