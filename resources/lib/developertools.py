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
import databasetools

DEVELOPER_OPTIONS = [getLocalizedString(
    32007), getLocalizedString(32011), getLocalizedString(32027), getLocalizedString(32000)]


def convertDbJson(tableName, json_str=False):
    import sqlite3
    conn = sqlite3.connect(DBFILE)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    rows = db.execute('SELECT * from {}'.format(tableName)).fetchall()

    conn.commit()
    conn.close()

    data = [dict(ix) for ix in rows]

    if json_str:
        return json.dumps(data)

    return data


def convertJsonToDB(astroRemoteLink=None, jdata=None, override=False):
    if jdata is None:
        from urllib import request
        req = request.Request(astroRemoteLink)
        response = request.urlopen(req)
        data = response.read()
        jdata = json.loads(data)
        if not data or len(data) == 0:
            xbmcgui.Dialog().notification(TITLE, getLocalizedString(32014), ICON)
            return
    folders = databasetools.executeSQL(
        'SELECT * FROM astro_folders WHERE sectionID != 0')
    actions = databasetools.executeSQL('SELECT * FROM astro_actions')
    if not override:
        if len(folders) > 0 or len(actions) > 0:
            overrideRemote = xbmcgui.Dialog().yesno(TITLE, getLocalizedString(32015) %
                                                    ('[COLOR orange]{}[/COLOR]'.format(str(len(folders))),
                                                    '[COLOR orange]{}[/COLOR]'.format(str(len(actions)))))
            if overrideRemote:
                # Let's create a security copy of the Astro existing local data
                os.rename(DBFILE, translatePath(
                    os.path.join(PROFILE, 'astro-SecurityCopy-{}.db'.format(
                        time.strftime('%m-%d-%Y %H-%M-%S')))))
    if not databasetools.checkFileExists():
        databasetools.createDatabaseFile()

    folders = jdata['data'][0]['astro_folders']
    actions = jdata['data'][0]['astro_actions']
    if len(folders) > 0 and len(actions) > 0:
        databasetools.commitSQL("DELETE FROM astro_actions")
        databasetools.commitSQL("DELETE FROM astro_folders")
    for action in actions:
        insertSeqAct = 'INSERT OR REPLACE INTO astro_actions (%s) VALUES (%s)' % (
            ', '.join(actions[0].keys()),
            ', '.join(['"%s"' % str(v).replace('"', "'")
                       for v in action.values()]))
        databasetools.commitSQL(insertSeqAct)
    for folder in folders:
        insertSeqFolders = 'INSERT OR REPLACE INTO astro_folders (%s) VALUES (%s)' % (
            ', '.join(folders[0].keys()),
            ', '.join(['"%s"' % str(v).replace('"', "'")
                       for v in folder.values()])
        )
        databasetools.commitSQL(insertSeqFolders)
    set_setting('astro_remote_hash', jdata['hash'])
