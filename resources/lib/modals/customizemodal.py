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
from tools import *
from developertools import *


class CustomizeModal(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(CustomizeModal, self).__init__(title)
        self.setGeometry(500, 450, 9, 2)
        self.set_controls()
        self.set_navigation()
        self.colors = getKodiColors()
        self.prepareList()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        self.closeButton = pyxbmct.Button('Cerrar')
        self.placeControl(self.closeButton, 8, 0, 1, 2)
        self.connect(self.closeButton, self.close)
        self.list = pyxbmct.List()
        self.placeControl(self.list, 0, 0, 8, 2)

    def prepareList(self):
        self.list.addItems(
            [f'[COLOR {color}]ASTRO EXAMPLE ITEM[/COLOR] - {color}' for color in self.colors])
        self.connect(self.list, lambda: self.setColor(
            self.list.getSelectedPosition()))

    def setColor(self, position):
        selectedColor = self.colors[position]
        set_setting('color_customize', selectedColor)
        xbmcgui.Dialog().notification(TITLE, getLocalizedString(32018) %
                                      (f'[COLOR {selectedColor}]{selectedColor}[/COLOR]'), ICON)
        self.close()

    def set_navigation(self):
        self.list.controlUp(self.closeButton)
        self.list.controlDown(self.closeButton)
        self.closeButton.controlUp(self.list)
        self.closeButton.controlDown(self.list)
        self.setFocus(self.closeButton)
