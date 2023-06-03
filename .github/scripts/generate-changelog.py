# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2023 Someone Like You
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

from __future__ import absolute_import, division, unicode_literals

import re
import xml.etree.ElementTree as ET
from datetime import datetime
GIT_URL = "https://github.com/IAmSomeoneLikeYou462/script.astro"
DATE = datetime.today().strftime('%Y-%m-%d')
MARKDOWN_KEYS = {
    'header':{
        'prefix': '#'*2
    },
    'content':{
        'feat': {
            'title': 'Features in this version:',
            'prefix': '#'*3,
            'sort': 1,
        },
        'fix': {
            'title': 'Fixes in this version:',
            'prefix': '#' * 3,
            'sort': 2
        },
        'else': {
            'title': '',
            'prefix': '',
            'sort': 0

        }
    }
}
def write_changelog_file(content):
    print(content)
    with open('CHANGELOG.md', 'a') as file:
        file.write(f"\n\n{content}")

def generate_markdown(version, news):
    content = dict()
    body = list()
    header = f"{MARKDOWN_KEYS['header']['prefix']} [v{version}]({GIT_URL}) ({DATE})"
    contentDict = MARKDOWN_KEYS['content']
    for newsLine in [s.strip() for s in news.splitlines() if s.strip()]:
        contentPattern = r'-\s+([A-Za-z\d*]+):\s+([^\n]+)'
        contentMatch = re.compile(contentPattern).search(newsLine)
        if contentMatch != None:
            key = contentMatch.group(1)
            texts = contentMatch.group(2)
        else:
            key = 'else'
            texts = newsLine
        contentTypeDict = contentDict[key]
        if not key in content:
            content[key] = {
                'texts': [],
                **contentTypeDict}
        content[key]['texts'].append(f"- {texts}" if not texts.startswith('-') else texts)
    for key, value in sorted(content.items(), key=lambda cnt: cnt[1]['sort']):
        contentHeader = f"{value['prefix']} {value['title']}"
        contentBody = "\n".join(value['texts'])
        body.append("\n".join([contentHeader, contentBody]))
    write_changelog_file("\n".join([header, *body]))
if __name__ == '__main__':
    with open('addon.xml', 'r') as f:
        tree = ET.fromstring(f.read())
        addon_info = {
            'id': tree.get('id'),
            'version': tree.get('version'),
            'news': tree.find("./extension[@point='xbmc.addon.metadata']/news").text
        }
    generate_markdown(addon_info['version'], addon_info['news'])
