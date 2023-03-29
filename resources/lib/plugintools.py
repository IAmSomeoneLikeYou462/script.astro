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
import sys
from item import Item
from tools import *
import databasetools
import servicetools


def set_admin_password(item):
    return servicetools.set_admin_password()


def moveElement(item):
    foldersSQL = databasetools.executeSQL(
        'SELECT id, sectionID, name FROM astro_folders')
    folderNames = [folder[2] for folder in foldersSQL]
    newFolderId = xbmcgui.Dialog().select(TITLE, folderNames)
    if newFolderId != -1:
        columnName = 'subFolderId' if item.sqlTable == 'astro_folders' else 'keepFolderId'
        sqlSeq = "UPDATE {} SET {} = '{}' WHERE id = {};".format(
            item.sqlTable, columnName, foldersSQL[newFolderId][1], item.id)
        databasetools.commitSQL(sqlSeq)
    itemlist_refresh()


def renameSQL(item):
    name = xbmcgui.Dialog().input(TITLE, item.title, xbmcgui.INPUT_ALPHANUM)
    if name:
        sqlSeq = "UPDATE {} SET {} = '{}' WHERE id = {};".format(
            item.sqlTable, item.columnName, name, item.id)
        databasetools.commitSQL(sqlSeq)
    itemlist_refresh()


def deleteSQL(item):
    localizedString = 32034 if item.sqlTable == 'astro_folders' else 32035
    name = xbmcgui.Dialog().yesno(TITLE, getLocalizedString(localizedString) % item.title)
    if name:
        sqlSeq = "DELETE FROM {} WHERE id = {};".format(
            item.sqlTable, item.id)
        databasetools.commitSQL(sqlSeq)
    itemlist_refresh()


def changeIcon(item):
    selectedImage = xbmcgui.Dialog().browse(2, f'{NAME} - {getLocalizedString(32037)}', 'files',
                                            '', True, False, translatePath(SP_HOME))
    if selectedImage:
        selectedImagePath = translatePath(selectedImage)
        specialPath = selectedImagePath.replace(
            translatePath(SP_HOME), SP_HOME)
        sqlSeq = "UPDATE {} SET {} = '{}' WHERE id = {};".format(
            item.sqlTable, 'thumb', specialPath, item.id)
        databasetools.commitSQL(sqlSeq)
    itemlist_refresh()
