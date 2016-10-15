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

def unmarcxml(registro_inicial, limite, url_base = 'http://www.bnm.me.gov.ar/catalogo/Record/'):
    import requests
    import os

    clave_xml           = '/Export?style=MARCXML'
    lista_registros_bnm = []
    tag_name            = 'datafield'
    attribute_name      = 'tag'
    attribute_value     = '856'

    directory = url_base.split('/')[2]
    if not os.path.exists(directory):
        os.makedirs(directory)

    while registro_inicial <= limite:
        url_final    = '%s%09d%s' % (url_base, registro_inicial, clave_xml)
        print('descargando ' + url_final, end=' ')
        registro_bnm = requests.get(url_final)
        status = registro_bnm.status_code
        print(status, end=' ')
        if status == requests.codes.ok:
            if FindAttribute(registro_bnm.text, tag_name, attribute_name, attribute_value):
                with open('%09d.xml' % registro_inicial, 'xb') as f:
                    f.write(registro_bnm.content)
                lista_registros_bnm.append(registro_bnm)
                print('Guardado')
            else:
                print('Descartado')
        else:
            print()
        registro_inicial += 1

    return lista_registros_bnm

def FindAttribute(document, tag_name, attribute_name, attribute_value):
    from xml.dom.minidom import parseString
    document = parseString(document)
    for tag in document.getElementsByTagName(tag_name):
        if tag.getAttribute(attribute_name) == attribute_value:
            return True
    return False

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
