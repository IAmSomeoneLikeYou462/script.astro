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

JSONFILE = os.path.join(translatePath(PROFILE), 'astro.json')


def getPrefix():
    """Created by jmooremcc, spoyser from the project plugin.program.super.favourtites"""
    try:
        return 'Container(%d).' % int(xbmc.getInfoLabel('System.CurrentControlId'))
    except:
        return ''


def getDescription():
    """Created by jmooremcc, spoyser from the project plugin.program.super.favourtites"""
    prefix = getPrefix()

    labels = []
    labels.append('%sListItem.Plot' % prefix)
    labels.append('%sListItem.AddonDescription' % prefix)
    labels.append('%sListItem.AddonSummary' % prefix)
    labels.append('%sListItem.Property(Artist_Description)' % prefix)
    labels.append('%sListItem.Property(Album_Description)' % prefix)
    labels.append('%sListItem.Artist' % prefix)
    labels.append('%sListItem.Comment' % prefix)

    for label in labels:
        desc = xbmc.getInfoLabel(label)
        if len(desc) > 0:
            return desc

    return ''


def getCurrentParams():
    """Created by jmooremcc, spoyser from the project plugin.program.super.favourites"""
    prefix = getPrefix()

    window = xbmcgui.getCurrentWindowId()
    folder = xbmc.getInfoLabel('Container.FolderPath')
    path = xbmc.getInfoLabel('%sListItem.FolderPath' % prefix)
    label = xbmc.getInfoLabel('%sListItem.Label' % prefix)
    filename = xbmc.getInfoLabel('%sListItem.FilenameAndPath' % prefix)
    thumb = xbmc.getInfoLabel('%sListItem.Thumb' % prefix)
    icon = xbmc.getInfoLabel('%sListItem.ActualIcon' % prefix)
    # thumb   = xbmc.getInfoLabel('%sListItem.Art(thumb)' % prefix)
    playable = xbmc.getInfoLabel(
        '%sListItem.Property(IsPlayable)' % prefix).lower() == 'true'
    # fanart  = xbmc.getInfoLabel('%sListItem.Property(Fanart_Image)' % prefix)
    fanart = xbmc.getInfoLabel('%sListItem.Art(fanart)' % prefix)
    isFolder = xbmc.getCondVisibility('%sListItem.IsFolder' % prefix) == 1
    hasVideo = xbmc.getCondVisibility('Player.HasVideo') == 1
    picture = xbmc.getInfoLabel('%sListItem.PicturePath' % prefix)

    desc = getDescription()

    if not thumb or not thumb.startswith('http'):
        if not icon or not icon.startswith('http'):
            thumb = icon
        else:
            thumb = IMAGES_URL['ICON']

    if not fanart or not fanart.startswith('http'):
        fanart = IMAGES_URL['FANART']

    try:
        file = xbmc.Player().getPlayingFile()
    except:
        file = None

    isStream = xbmc.getCondVisibility('Player.IsInternetStream') == 1

    # if file:
    #    isStream = file.startswith('http')

    if window == 10003:  # filemanager
        try:
            id = int(xbmc.getInfoLabel('System.CurrentControlId'))
        except:
            id = 0

        if id not in [20, 21]:
            return None

        folder = path.replace(filename, '')

        import os
        if path.endswith(os.sep):
            path = path[:-1]  # .rsplit(os.sep, 1)[0]

        isFolder = True
        thumb = 'DefaultFolder.png'

    if isFolder:
        path = path.replace('\\', '\\\\')
        filename = filename.replace('\\', '\\\\')

    params = {}
    params['label'] = label
    params['folder'] = folder
    params['path'] = path
    params['filename'] = filename
    params['thumb'] = thumb
    params['icon'] = icon
    params['fanart'] = fanart
    params['window'] = window
    params['isplayable'] = playable
    params['isfolder'] = isFolder
    params['file'] = file
    params['isstream'] = isStream
    params['description'] = desc
    params['hasVideo'] = hasVideo
    params['picture'] = picture

    return params


def completeAddonParams(params):
    from xml.etree import ElementTree
    path = params.get('path')
    if path.endswith('/'):
        path = path[:-1]
    pluginDirName = path.split('/')[-1]
    pluginDir = os.path.join(ADDONS_DIR, pluginDirName)
    if not os.path.exists(pluginDir):
        return params
    addonXml = os.path.join(translatePath(pluginDir), 'addon.xml')
    if not os.path.isfile(addonXml):
        return params
    data = open(addonXml, 'rb').read()
    dataXml = ElementTree.fromstring(data)
    metadata = list(filter(
        lambda extension: extension.attrib['point'] == "xbmc.addon.metadata", dataXml.findall('extension')))[0]
    assets = metadata.find('assets')
    assetsTag = ['icon', 'fanart']
    for tag in assetsTag:
        tagValue = assets.find(tag)
        if tagValue == None: continue
        image = f"{ADDONS_DIR_NAME}{pluginDirName}/{tagValue.text}"
        if tag == 'icon':
            tag = 'thumb'
        params[tag] = image
    return params


def checkCompleteAddon(params): return params.get(
    'path').startswith('addons://') or params.get('path').startswith('plugin://')


def checkItemLibStructure(params): 
    from item import Item
    decoded_params = Item().fromurl(params.get('path'))
    if 'thumbnail' in decoded_params:
        params['thumb'] = decoded_params.thumbnail
    return params
