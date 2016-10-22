#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  bnm.py
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


import pdb
import sqlite3


def unmarcxml(registro_inicial,
              limite,
              url_base='http://www.bnm.me.gov.ar/catalogo/Record/'):
    import requests
    import os

    clave_xml = '/Export?style=MARCXML'
    lista_registros_bnm = []
    tag_name = 'datafield'
    attribute_name = 'tag'
    attribute_value = '856'

    directory = 'xml/' + url_base.split('/')[2]
    if not os.path.exists(directory):
        os.makedirs(directory)

    db_file = 'registro.db'
    db_connection = sqlite3.connect(directory + "/" + db_file)
    db_cursor = db_connection.cursor()
    db_cursor.execute(''' CREATE TABLE IF NOT EXISTS records
                          (id int,
                           server_response bool,
                           reg_exists bool,
                           reg_saved bool )''')

    while registro_inicial <= limite:
        url_final = '%s%09d%s' % (url_base, registro_inicial, clave_xml)
        print('descargando ' + url_final, end=' ')
        registro_bnm = requests.get(url_final)
        status = registro_bnm.status_code
        print(status, end=' ')
        if status == requests.codes.ok:
            # ejecutar si código de respuesta OK
            if FindAttribute(registro_bnm.text,
                             tag_name,
                             attribute_name,
                             attribute_value):
                with open('%s/%09d.xml' % (directory, registro_inicial),
                          'xb') as f:
                    f.write(registro_bnm.content)
                lista_registros_bnm.append(registro_bnm)
                print('Guardado')
        else:
            print()
        registro_inicial += 1

    return lista_registros_bnm


def FindAttribute(document, tag_name, attribute_name, attribute_value):
    import xml
    from xml.dom.minidom import parseString
    #pdb.set_trace()
    try:
        document = xml.dom.minidom.parseString(document)
        for tag in document.getElementsByTagName(tag_name):
            if tag.getAttribute(attribute_name) == attribute_value:
                return True
        # imprime descartado si condición no se cumple en ninguna iteración:
        print('Descartado')
    except xml.parsers.expat.ExpatError:
        print('Inexistente')


def main(args):
    if len(args) == 4:
        unmarcxml(int(args[1]), int(args[2]), args[3])
    elif len(args) == 3:
        unmarcxml(int(args[1]), int(args[2]))
    else:
        print("Usage: " + args[0] + " registro_inicial(int) limite(int) [url]")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
