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
from modals.librarymodal import LibraryModal
from modals.developermodal import DeveloperModal


def main():
    if not databasetools.checkFileExists():
        databasetools.initialiseDatabaseFile()
    if get_setting('dev_mode'):
        window = DeveloperModal('{} - {}'.format(TITLE, 'Developer Mode'))
        window.doModal()
        del window
        return

    window = LibraryModal(TITLE)
    window.doModal()
    del window


if __name__ == '__main__':
    main()
