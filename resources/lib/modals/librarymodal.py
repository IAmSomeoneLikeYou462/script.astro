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
import librarytools
import databasetools
from tools import *

params = librarytools.getCurrentParams()


class LibraryModal(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(LibraryModal, self).__init__(title)
        self.setGeometry(700, 450, 9, 4)
        self.items = list()
        self.backIdHistory = list()
        self.subFolderIdsList = list()
        self.set_controls()
        self.set_navigation()
        self.prepareList()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def prepareList(self):
        self.prepareItems(0)
        self.subFolderIdsList.append(0)
        self.backIdHistory.append(0)
        self.connect(self.list, lambda: self.onClickList(
            self.list.getSelectedPosition()))
        self.connectEventList([pyxbmct.ACTION_MOVE_DOWN, pyxbmct.ACTION_MOVE_UP, pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
                              pyxbmct.ACTION_MOUSE_WHEEL_UP, pyxbmct.ACTION_MOUSE_MOVE], self.list_update)

    def set_controls(self):
        self.list = pyxbmct.List()
        self.placeControl(self.list, 0, 1, 9, 3)
        self.image = pyxbmct.Image(ICON)
        self.placeControl(self.image, 2, 0, 4, 1)
        self.addButton = pyxbmct.Button(getLocalizedString(32038))
        self.placeControl(self.addButton, 6, 0, 1, 1)
        self.connect(self.addButton, self.addSection)
        self.closeButton = pyxbmct.Button(getLocalizedString(32039))
        self.placeControl(self.closeButton, 7, 0, 1, 1)
        self.connect(self.closeButton, self.close)

    def addSection(self):
        global params
        if not params or len(params) == 0:
            return
        if librarytools.checkCompleteAddon(params):
            params = librarytools.completeAddonParams(params)
        keepFolderId = self.subFolderIdsList[-1]
        insertSeq = 'INSERT INTO astro_actions (%s, keepFolderId) VALUES (%s, %s)' % (
            ', '.join(params.keys()),
            ', '.join(['"%s"' % str(v).replace('"', "'")
                      for v in params.values()]),
            keepFolderId
        )
        databasetools.commitSQL(insertSeq)
        xbmcgui.Dialog().notification(
            TITLE, '{} added to Astro'.format(params['label']), ICON)
        self.prepareItems(keepFolderId)

    def onClickList(self, position):
        global sectionId
        item = self.items[position]
        # Check if list element is to go back or add new element
        if item[2] == getLocalizedString(32005):
            name = xbmcgui.Dialog().input(TITLE, '', xbmcgui.INPUT_ALPHANUM)
            sectionId = databasetools.getSectionId()
            if name == '':
                return
            insertSeq = 'INSERT INTO astro_folders (sectionID, name, thumb, subFolderId, onClick, backFolderID) VALUES (?, ?, ?, ?, ?, ?)'
            dataSeq = (sectionId, name,
                       'ICON', self.subFolderIdsList[-1], 1, self.subFolderIdsList[-1])
            databasetools.commitSQL(insertSeq, dataSeq)
            xbmcgui.Dialog().notification(TITLE, name, ICON)
            self.subFolderIdsList.append(sectionId)
            self.prepareItems(sectionId)

        elif item[2] == getLocalizedString(32006):
            if len(self.backIdHistory) > 0:
                sectionId = self.backIdHistory[-1]
                if int(sectionId) != 0:
                    self.backIdHistory.pop(-1)
                self.subFolderIdsList.append(sectionId)
                self.prepareItems(sectionId)
        else:
            if not bool(item[-2]):  # Skip if item is not an onClick item (action)
                xbmcgui.Dialog().notification(TITLE, 'Item is an action!', ICON)
                return
            if item[-1] != '0':
                self.backIdHistory.append(item[-1])
            self.subFolderIdsList.append(int(item[1]))
            self.prepareItems(item[1])

    def prepareItems(self, sectionId):
        self.list.reset()
        sections = list()
        if not sectionId == 0 and len(self.backIdHistory) > 0:
            sections.append([0, 0, getLocalizedString(32006), 'ICON', True])
        sections.append(
            [0, sectionId, getLocalizedString(32005), 'ICON', True])
        for folder in databasetools.executeSQL(
                'SELECT * FROM astro_folders WHERE subFolderId == {}'.format(sectionId)):
            sections.append(list(folder))
        for action in databasetools.executeSQL(
                'SELECT * FROM astro_actions WHERE keepFolderId == {}'.format(sectionId)):
            action = self.prepareItemAction(action)
            sections.append(list(action))
        self.items = sections
        self.list.addItems(list(sec[2]
                                for sec in sections))

    def list_update(self):
        if self.getFocus() == self.list:
            listPosition = self.list.getSelectedPosition()
            if listPosition == 0:
                self.image.setImage(ICON)
            if listPosition > 0:
                thumb = self.items[listPosition][3]
                if not thumb or thumb == 'ICON' and (not thumb.startswith('http') and not thumb.startswith('special://')):
                    thumb = ICON
                self.image.setImage(thumb)

    def prepareItemAction(self, actionElement):
        id, label, folder, path, filename, thumb, \
            icon, fanart, window, isplayable, isfolder, \
            file, isstream, description, hasVideo, picture, onClick, keepFolderId = actionElement
        name = '[COLOR {}]{}[/COLOR]'.format(get_setting('color_customize', 'orange'),
                                             remove_format(label)) if get_setting('differentiate_elements_window') else label
        return [id, id,
                name,
                thumb, bool(onClick), '-']

    def set_navigation(self):
        self.list.controlRight(self.addButton)
        self.list.controlLeft(self.addButton)
        self.closeButton.controlRight(self.list)
        self.closeButton.controlLeft(self.list)
        self.addButton.controlRight(self.list)
        self.addButton.controlLeft(self.list)
        self.addButton.controlDown(self.closeButton)
        self.addButton.controlUp(self.closeButton)
        self.closeButton.controlDown(self.addButton)
        self.closeButton.controlUp(self.addButton)
        self.setFocus(self.addButton)
