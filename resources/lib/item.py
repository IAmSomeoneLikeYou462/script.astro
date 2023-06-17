# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2022 Alfa-Addon & Balandro: Modified by Someone Like You
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
#
# Thanks to Alfa-Addon & Balandro Addon
# Alfa - https://github.com/alfa-addon
# Balandro Addon - https://github.com/balandro-tk
# ----------------------------------------------------------------------

import base64
import copy
import os
import json
import sys


PY3 = sys.version_info[0] >= 3
if PY3:
    unicode = str
    from urllib.parse import quote, unquote_plus, unquote
    from html.parser import unescape
else:
    from urllib import quote, unquote_plus, unquote
    from HTMLParser import HTMLParser
    unescape = HTMLParser().unescape


class Item(object):
    def __init__(self, **kwargs):
        """
        Inicializacion del item
        """

        if "parentContent" in kwargs:
            self.set_parent_content(kwargs["parentContent"])
            del kwargs["parentContent"]

        kw = copy.copy(kwargs)
        for k in kw:
            if k in ["contentTitle", "contentPlot", "contentSerieName", "show", "contentType", "contentEpisodeTitle",
                     "contentSeason", "contentEpisodeNumber", "contentThumbnail", "plot", "duration", "contentQuality",
                     "quality"]:
                self.__setattr__(k, kw[k])
                del kwargs[k]

        self.__dict__.update(kwargs)
        self.__dict__ = self.toutf8(self.__dict__)

    def __contains__(self, m):
        """
        Comprueba si un atributo existe en el item
        """
        return m in self.__dict__

    def __setattr__(self, name, value):
        """
        Función llamada al modificar cualquier atributo del item, modifica algunos atributos en función de los datos
        modificados.
        """
        if PY3:
            name = self.toutf8(name)
        value = self.toutf8(value)
        if name == "__dict__":
            for key in value:
                self.__setattr__(key, value[key])
            return

        # Descodificamos los HTML entities

        if name in ["title", "plot", "fulltitle", "contentPlot", "contentTitle"]:
            value = self.decode_html(value)

        elif name == "viewcontent" and value not in ["files", "movies", "tvshows", "seasons", "episodes"]:
            super(Item, self).__setattr__("viewcontent", "files")

        if not isinstance(name, str):
            name = name.decode("utf-8", "strict")
        else:
            super(Item, self).__setattr__(name, value)

    def __getattr__(self, name):
        """
        Devuelve los valores por defecto en caso de que el atributo solicitado no exista en el item
        """
        if name.startswith("__"):
            return super(Item, self).__getattribute__(name)

        # valor por defecto para folder
        if name == "folder":
            return True

        # valor por defecto para contentChannel
        elif name == "contentChannel":
            return "list"

        # valor por defecto para viewcontent
        elif name == "viewcontent":
            viewcontent = "files"

            self.__dict__["viewcontent"] = viewcontent
            return viewcontent

        # valor por defecto para el resto de atributos
        else:
            return ""

    def __str__(self):
        return '\r\t' + self.tostring('\r\t')

    def set_parent_content(self, parentContent):
        """
        Rellena los campos contentDetails con la informacion del item "padre"
        @param parentContent: item padre
        @type parentContent: item
        """
        # Comprueba que parentContent sea un Item
        if not type(parentContent) == type(self):
            return
        for attr in parentContent.__dict__:
            if attr.startswith("content"):
                self.__setattr__(attr, parentContent.__dict__[attr])

    def tostring(self, separator=", "):
        """
        Genera una cadena de texto con los datos del item para el log
        @param separator: cadena que se usará como separador
        @type separator: str
        '"""
        dic = self.__dict__.copy()

        # Añadimos los campos content... si tienen algun valor
        for key in ["contentTitle", "contentPlot", "contentSerieName", "contentEpisodeTitle",
                    "contentSeason", "contentEpisodeNumber", "contentThumbnail"]:
            value = self.__getattr__(key)
            if value:
                dic[key] = value

        ls = []
        for var in sorted(dic):
            if isinstance(dic[var], str):
                valor = "'%s'" % dic[var]
            elif PY3 and isinstance(dic[var], bytes):
                valor = "'%s'" % dic[var].decode('utf-8')

            else:
                valor = str(dic[var])
            if PY3 and isinstance(var, bytes):
                var = var.decode('utf-8')
            ls.append(var + "= " + valor)

        return separator.join(ls)

    def tourl(self):
        """
        Genera una cadena de texto con los datos del item para crear una url, para volver generar el Item usar
        item.fromurl().

        Uso: url = item.tourl()
        """
        try:
            dump = json.dumps(self.__dict__).encode("utf8")
        except:
            dump = json.dumps(self.__dict__)
        # if empty dict
        if not dump:
            # set a str to avoid b64encode fails
            dump = "".encode("utf8")
        # return quote(base64.b64encode(dump))
        return str(quote(base64.b64encode(dump)))

    def fromurl(self, url):
        """
        Genera un item a partir de una cadena de texto.
        Uso: item.fromurl("cadena")

        @param url: url
        @type url: str
        """
        if "?" in url:
            url = url.split("?")[1]
        decoded = False
        try:
            if 'action=' not in url:  # Si tiene action= es que no está b64encodeado
                str_item = base64.b64decode(unquote(url))
                json_item = json.loads(str_item, object_hook=self.toutf8)
                if json_item is not None and len(json_item) > 0:
                    self.__dict__.update(json_item)
                    decoded = True
        except:
            pass

        if not decoded:
            url = unquote_plus(url)
            dct = dict([[param.split("=")[0], param.split("=")[1]]
                       for param in url.split("&") if "=" in param])
            self.__dict__.update(dct)
            self.__dict__ = self.toutf8(self.__dict__)

        return self

    def tojson(self, path=""):
        """
        Crea un JSON a partir del item, para guardar archivos de favoritos, lista de descargas, etc...
        Si se especifica un path, te lo guarda en la ruta especificada, si no, devuelve la cadena json
        Usos: item.tojson(path="ruta\archivo\json.json")
              file.write(item.tojson())

        @param path: ruta
        @type path: str
        """
        if path:
            open(path, "wb").write(json.dumps(self.__dict__))
        else:
            return json.dumps(self.__dict__)

    def fromjson(self, json_item=None, path=""):
        """
        Genera un item a partir de un archivo JSON
        Si se especifica un path, lee directamente el archivo, si no, lee la cadena de texto pasada.
        Usos: item = Item().fromjson(path="ruta\archivo\json.json")
              item = Item().fromjson("Cadena de texto json")

        @param json_item: item
        @type json_item: json
        @param path: ruta
        @type path: str
        """
        if path:
            if os.path.exists(path):
                json_item = open(path, "rb").read()
            else:
                json_item = {}

        if json_item is None:
            json_item = {}

        item = json.loads(json_item, object_hook=self.toutf8)
        self.__dict__.update(item)

        return self

    def clone(self, **kwargs):
        """
        Genera un nuevo item clonando el item actual
        Usos: NuevoItem = item.clone()
              NuevoItem = item.clone(title="Nuevo Titulo", action = "Nueva Accion")
        """
        newitem = copy.deepcopy(self)
        for kw in kwargs:
            newitem.__setattr__(kw, kwargs[kw])
        newitem.__dict__ = newitem.toutf8(newitem.__dict__)

        return newitem

    @staticmethod
    def decode_html(value):
        """
        Descodifica las HTML entities
        @param value: valor a decodificar
        @type value: str
        """
        try:
            unicode_title = unicode(value, "utf8", "ignore")
            return unescape(unicode_title).encode("utf8")
        except:
            if PY3:
                if isinstance(value, bytes):
                    value = value.decode("utf8")
            return value

    def toutf8(self, *args):
        """
        Pasa el item a utf8
        """
        if len(args) > 0:
            value = args[0]
        else:
            value = self.__dict__

        if isinstance(value, unicode):
            value = value.encode("utf8")
            if PY3:
                value = value.decode("utf8")
            return value

        elif not PY3 and isinstance(value, str):
            return unicode(value, "utf8", "ignore").encode("utf8")

        elif PY3 and isinstance(value, bytes):
            return value.decode("utf8")

        elif isinstance(value, list):
            for x, key in enumerate(value):
                value[x] = self.toutf8(value[x])
            return value

        elif isinstance(value, dict):
            newdct = {}
            for key in value:
                value_unc = self.toutf8(value[key])
                key_unc = self.toutf8(key)
                # if isinstance(key, unicode):
                #    key = key.encode("utf8")

                newdct[key_unc] = value_unc

            if len(args) > 0:
                return newdct

        else:
            return value
