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


class FirstRunModal(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(FirstRunModal, self).__init__(title)
        self.setGeometry(850, 600, 17, 8)
        self.step = 0
        self.nextStepButton = None
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        if self.step == 0:
            self.fanartImage = pyxbmct.Image(FANART, aspectRatio=1)
            self.placeControl(self.fanartImage, 0, 0, 6, 8)
            self.welcomeText = pyxbmct.Label(
                f'[COLOR gold][B]{getLocalizedString(32019)}[/B][/COLOR]', font='font15')
            self.placeControl(self.welcomeText, 6, 3, 6, 8)
            self.descriptionText = pyxbmct.TextBox(font='font12')
            self.descriptionText.setText(
                '%s\n%s\n%s' % (getLocalizedString(32020),
                                getLocalizedString(32021),
                                getLocalizedString(32022))
            )
            self.descriptionText.autoScroll(1000, 1000, 1000)
            self.placeControl(self.descriptionText, 8, 0, 6, 8)
            self.welcomeToNewAgeText = pyxbmct.Label(
                f'[COLOR gold][B]{getLocalizedString(32023)}[/B][/COLOR]', font='font15')
            self.placeControl(self.welcomeToNewAgeText, 11, 3, 6, 8)
            self.worldText = pyxbmct.Label(
                f'[COLOR gold][B]{getLocalizedString(32024)}[/B][/COLOR]', font='font15')
            self.placeControl(self.worldText, 12, 3, 6, 8)
        if self.nextStepButton is None:
            self.nextStepButton = pyxbmct.Button(getLocalizedString(32025))
            self.placeControl(self.nextStepButton, 15, 3, 2, 2)
            self.connect(self.nextStepButton, self.nextStep)

    def nextStep(self):
        self.step += 1
        if self.step == 1:
            self.welcomeText.setVisible(False)
            self.descriptionText.setVisible(False)
            self.welcomeText.setVisible(False)
            self.welcomeToNewAgeText.setVisible(False)
            self.worldText.setVisible(False)
        elif self.step == 2:
            self.close()
        self.nextStepButton.setLabel(getLocalizedString(32026))
        self.set_controls()
        self.set_navigation()

    def set_navigation(self):
        self.setFocus(self.nextStepButton)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                              ('WindowClose', 'effect=fade start=100 end=0 time=500',)])
