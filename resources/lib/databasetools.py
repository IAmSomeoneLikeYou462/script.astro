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

import sqlite3
from tools import *


def checkFileExists(): return os.path.isfile(DBFILE)


def executeSQL(sql):
    connection = sqlite3.connect(DBFILE)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return data


def commitSQL(sql, dataSeq=None):
    connection = sqlite3.connect(DBFILE)
    cursor = connection.cursor()
    if dataSeq is not None:
        cursor.execute(sql, dataSeq)
    else:
        cursor.execute(sql)
    connection.commit()
    connection.close()
    return True


def createDatabaseFile():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE "astro_folders" (
            "id"	INTEGER,
            "sectionID"	INTEGER,
            "name"	TEXT,
            "thumb"	TEXT,
            "subFolderId"	INTEGER DEFAULT NULL,
            "onClick"	BOOLEAN DEFAULT 1,
            "backFolderID"	TEXT DEFAULT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        )''')
    c.execute('''CREATE TABLE "astro_actions" (
            "id"	INTEGER,
            "label"	TEXT,
            "folder"	TEXT,
            "path"	TEXT,
            "filename"	TEXT,
            "thumb"	TEXT,
            "icon"	TEXT,
            "fanart"	TEXT,
            "window"	INTEGER,
            "isplayable"	BOOLEAN,
            "isfolder"	BOOLEAN,
            "file"	TEXT,
            "isstream"	BOOLEAN,
            "description"	TEXT,
            "hasVideo"	BOOLEAN,
            "picture"	TEXT,
            "onClick"	BOOLEAN DEFAULT 0,
            "keepFolderId"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        )''')
    conn.commit()
    conn.close()


def initializeDatabaseFile():
    createDatabaseFile()
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute(
        '''INSERT INTO astro_folders (sectionID, name, thumb) VALUES (?, ?, ?)''', (0, 'root', 'ICON'))
    conn.commit()
    conn.close()


def getSectionId():
    from functools import reduce
    nums = list(filter(lambda num: num is not None,
                       [number[0] for number in executeSQL(
                           '''SELECT sectionID FROM astro_folders''')]))
    if len(nums) == 0:
        return 1

    def custom_max(x, y):
        try:
            int(x)
            int(y)
        except:
            return -1
        if x < y:
            return y
        else:
            return x
    maxNumber = reduce(custom_max, nums)
    if isinstance(maxNumber, tuple):
        maxNumber = maxNumber[0]
    return maxNumber + 1
