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
from item import Item
from tools import *
import databasetools
import servicetools
import plugintools


def menu(item):
    itemlist = list()
    if not item.sectionId:
        item.sectionId = 0
    folders = databasetools.executeSQL(
        'SELECT * FROM astro_folders WHERE subFolderId == {}'.format(item.sectionId))
    actions = databasetools.executeSQL(
        'SELECT * FROM astro_actions WHERE keepFolderId == {}'.format(item.sectionId))
    if get_setting('sort_items_alphabetically'):
        folders = sorted(folders, key=lambda item: item[2])
        actions = sorted(actions, key=lambda act: act[1])
    if get_setting('dev_mode') and bool(item.mainmenu):
        itemlist.append(item.clone(
                        title='[COLOR orange]Astro[/COLOR] - %s' % (
                            getLocalizedString(32001)),
                        thumbnail=ICON,
                        fanart=FANART,
                        action='open_developer_modal'
                        ))
    for id, sectionId, name, thumbnail, subFolderId, onClick, backFolderId in folders:
        item.mainmenu = False
        itemlist.append(item.clone(
                        id=id,
                        title=name,
                        thumbnail=prepareThumbnail(thumbnail),
                        fanart=FANART,
                        sectionId=sectionId,
                        subFolderId=subFolderId,
                        action='menu'
                        ))
    for action in actions:
        id, label, folder, path, filename, thumbnail, \
            icon, fanart, window, isplayable, isfolder, \
            file, isstream, description, hasVideo, picture, onClick, keepFolderId = action
        item.mainmenu = False
        itemlist.append(item.clone(
                        id=id,
                        title=label,
                        thumbnail=prepareThumbnail(thumbnail),
                        fanart=FANART,
                        path=path,
                        url=path,
                        action='runPlugin'
                        ))

    return itemlist


def open_developer_modal(item):
    from modals.developermodal import DeveloperModal
    window = DeveloperModal(TITLE)
    window.doModal()
    del window


def run_customize_modal(item):
    from modals.customizemodal import CustomizeModal
    window = CustomizeModal(TITLE)
    window.doModal()
    del window


def set_admin_password(item):
    return plugintools.set_admin_password()


def runPlugin(item):
    xbmc.executebuiltin('Dialog.Close(all,true)')
    xbmc.executebuiltin(
        'ActivateWindow(10025, "%s")' % (item.path))


def moveElement(item):
    return plugintools.moveElement(item)


def renameSQL(item):
    return plugintools.renameSQL(item)


def deleteSQL(item):
    return plugintools.deleteSQL(item)


def changeIcon(item):
    return plugintools.changeIcon(item)


def run(item):
    itemlist = list()
    if not item.action:
        logger('Item sin acci\xc3\xb3n')
        return
    itemlist = eval(item.action)(item)
    if itemlist is not None:
        if not len(itemlist):
            itemlist.append(Item(
                title='[COLOR orange]Sin resultados[/COLOR]', thumbnail=ICON, fanart=FANART))

    if itemlist:
        render_items(itemlist, item)


if __name__ == '__main__':
    from updater import Updater
    try:
        Updater().checkAvailableVersion(silent=False)
    except Exception as e:
        logger("Ha ocurrido un error leyendo la última versión de Astro")
        logger(f"ERROR: {e}")
    if not databasetools.checkFileExists():
        databasetools.initialiseDatabaseFile()

    try:
        servicetools.updateAstroRemoteConfig()
    except Exception as e:
        logger("Ha ocurrido un error leyendo la última versión de los datos")
        logger(f"ERROR: {e}")
    if sys.argv[2]:
        item = Item().fromurl(sys.argv[2])
    else:
        item = Item(action='menu', mainmenu=True)
    run(item)
