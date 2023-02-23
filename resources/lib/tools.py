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

import os
import sys
import re
import time
import json
import glob
import hashlib

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

__base_url = sys.argv[0]
PY3 = sys.version_info[0] >= 3
translatePath = xbmc.translatePath if not PY3 else xbmcvfs.translatePath
LOGNOTICE = xbmc.LOGINFO if PY3 else xbmc.LOGNOTICE
ADDON = xbmcaddon.Addon()
HOME = translatePath(ADDON.getAddonInfo('Path'))
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PROFILE = translatePath(ADDON.getAddonInfo('Profile'))
TITLE = '{NAME} - {VERSION}'.format(
        NAME=ADDON.getAddonInfo('name'), VERSION=ADDON.getAddonInfo('version'))
if not os.path.exists(PROFILE):
    os.makedirs(PROFILE)
DBFILE = translatePath(os.path.join(PROFILE, 'astro.db'))
IMAGES_URL = {
    "ICON": "https://p4.wallpaperbetter.com/wallpaper/235/979/748/the-sky-stars-the-universe-spiral-wallpaper-preview.jpg",
    "FANART": "https://images.wallpapersden.com/image/download/watching-the-universe_a2dnbmeUmZqaraWkpJRmbmdlrWZlbWU.jpg"
}

def build_url(item):
    return __base_url + '?' + item.tourl()


def create_RunPlugin(item):
    return 'RunPlugin(%s?%s)' % (__base_url, item.tourl())


def getLocalizedString(code):
    return ADDON.getLocalizedString(code)


def encode_log(message=""):

    # Unicode to utf8
    if isinstance(message, str):
        message = message.encode("utf8")
        if PY3:
            message = message.decode("utf8")

    # All encodings to utf8
    elif not PY3 and isinstance(message, str):
        message = str(message, "utf8", errors="replace").encode("utf8")

    # Bytes encodings to utf8
    elif PY3 and isinstance(message, bytes):
        message = message.decode("utf8")

    # Objects to string
    else:
        message = str(message)

    return message


def logger(message, level=None):

    texto = '[%s] %s' % (xbmcaddon.Addon().getAddonInfo(
        'id'), encode_log(message))

    try:
        if level == 'info':
            xbmc.log(texto, LOGNOTICE)
        elif level == 'error':
            xbmc.log("######## ERROR #########", xbmc.LOGERROR)
            xbmc.log(texto, xbmc.LOGERROR)
        else:
            xbmc.log("######## DEBUG #########", LOGNOTICE)
            xbmc.log(texto, LOGNOTICE)
    except:
        xbmc.log(str([texto]), LOGNOTICE)


def itemlist_refresh():
    xbmc.executebuiltin("Container.Refresh")


def set_context_commands(item):
    """    Función para generar los menus contextuales.    """
    context_commands = []
    # Rename Folder
    if item.path is None or not item.path:
        context_commands.append(('[COLOR orange]Astro[/COLOR] - %s' % (getLocalizedString(32008)),
                                 create_RunPlugin(
                                     item.clone(
                                         action='renameSQL',
                                         id=item.id,
                                         columnName='name',
                                         sqlTable='astro_folders'
                                     ))))
    else:
        context_commands.append(('[COLOR orange]Astro[/COLOR] - %s' % (getLocalizedString(32009)),
                                 create_RunPlugin(
                                     item.clone(
                                         action='renameSQL',
                                         id=item.id,
                                         columnName='label',
                                         sqlTable='astro_actions'
                                     ))))
    return context_commands


def render_items(itemlist, parent_item):

    for item in itemlist:
        listitem = xbmcgui.ListItem(item.title)
        listitem.setInfo(
            'video', {'title': item.title, 'mediatype': 'video'})

        listitem.setArt({'icon': "DefaultFolder.png" if item.folder else "DefaultVideo.png",
                         'thumb': item.thumbnail,
                         'poster': item.thumbnail, 'fanart': item.fanart})
        if item.plot:
            listitem.setInfo('video', {'plot': item.plot})

        if item.isPlayable:
            listitem.setProperty('IsPlayable', 'true')
            isFolder = False

        elif isinstance(item.isFolder, bool):
            isFolder = item.isFolder

        elif not item.action:
            isFolder = False

        else:
            isFolder = True

        listitem.addContextMenuItems(set_context_commands(item))

        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url='%s?%s' % (sys.argv[0], item.tourl()),
            listitem=listitem,
            isFolder=isFolder,
            totalItems=len(itemlist)
        )

    xbmcplugin.addSortMethod(handle=int(
        sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)


def get_setting(name, default=None):
    value = ADDON.getSetting(name)
    if not value:
        return default

    # Translate Path if start with "special://"
    if value.startswith("special://"):
        value = translatePath(value)

    # hack para devolver el tipo correspondiente
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        return value


def set_setting(name, value):
    try:
        if isinstance(value, bool):
            if value:
                value = "true"
            else:
                value = "false"

        elif isinstance(value, int):
            value = str(value)

        ADDON.setSetting(name, value)

    except Exception as ex:
        logger(
            "'%s' could not be stored, code error: %s" % (name, ex))
        return None

    return value


def remove_format(string):
    string = string.rstrip()
    string = re.sub(r'(\[|\[\/)(?:color|COLOR|b|B|i|I).*?\]', '', string)
    string = re.sub(r'\:|\.|\-|\_|\,|\¿|\?|\¡|\!|\"|\'|\&', ' ', string)
    string = re.sub(r'\(.*?\).*|\[.*?\].*', ' ', string)
    string = re.sub(r'\s+', ' ', string).strip()
    return string


def getKodiColors():
    from xml.etree import ElementTree
    from urllib import request
    req = request.Request(
        'https://raw.githubusercontent.com/xbmc/xbmc/Matrix/system/colors.xml')
    response = request.urlopen(req)
    data = response.read()
    xml = ElementTree.fromstring(data)
    colors = [color.get('name') for color in xml.findall('color')]
    return colors


def prepareThumbnail(thumbnail):
    return thumbnail if thumbnail.startswith('http') else ICON
