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


#import pdb
import sqlite3


class RegistrosDB():

    def __init__(self, database):
        self._connect_db(database)
        self._create_table()

    def _connect_db(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def _create_table(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS records
                        (id INTEGER PRIMARY KEY,
                        server_response BOOLEAN NOT NULL,
                        reg_exists BOOLEAN NOT NULL,
                        reg_saved BOOLEAN NOT NULL )''')

    def disconnect_db(self):
        self.connection.close()

    def get_record(self, record):
        record = (record,)  # creamos una tupla de un elemento
        self.cursor.execute('SELECT server_response, reg_exists, reg_saved FROM records WHERE id =?', record)
        return(self.cursor.fetchone())

    def save_record(self, record, server_response, reg_exists, reg_saved):
        db_insert = (record, server_response, reg_exists, reg_saved)
        self.cursor.execute('INSERT INTO records VALUES (?, ?, ?, ?)',
                            db_insert)
        self.connection.commit()


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
    registro_actual = registro_inicial

    directory = 'xml/' + url_base.split('/')[2]
    if not os.path.exists(directory):
        os.makedirs(directory)

    db_file = directory + "/" + 'registro.sqlite'
    database = RegistrosDB(db_file)

    while registro_actual <= limite:
        db_response = database.get_record(registro_actual)
        url_final = '%s%09d%s' % (url_base, registro_actual, clave_xml)
        if db_response is None:
            print('descargando ' + url_final, end=' ')
            registro_bnm = requests.get(url_final)
            status = registro_bnm.status_code
            print(status, end=' ')
            # Asumimos que todos los estados son false
            server_response = 0
            reg_exists = 0
            reg_saved = 0

            if status == requests.codes.ok:
                # ejecutar si código de respuesta OK
                server_response = 1
                find_attribute_return = findAttribute(registro_bnm.text,
                                                      tag_name,
                                                      attribute_name,
                                                      attribute_value)
                if find_attribute_return == "Guardo":
                    reg_exists = 1
                    reg_saved = 1
                    with open('%s/%09d.xml' % (directory, registro_actual),
                              'xb') as f:
                        f.write(registro_bnm.content)
                    lista_registros_bnm.append(registro_bnm)
                    print('Guardado')
                elif find_attribute_return == "Descarto":
                    reg_exists = 1
            else:
                print()
            database.save_record(registro_actual,
                                 server_response,
                                 reg_exists,
                                 reg_saved)
        else:
            print(url_final + ' ya se intentó; sigo a la siguiente...')

        registro_actual += 1
    database.disconnect_db()

    return lista_registros_bnm


def findAttribute(document, tag_name, attribute_name, attribute_value):
    import xml
    from xml.dom.minidom import parseString
    try:
        #document = xml.dom.minidom.parseString(document)
        document = parseString(document)
        for tag in document.getElementsByTagName(tag_name):
            if tag.getAttribute(attribute_name) == attribute_value:
                return "Guardo"
        # imprime descartado si condición no se cumple en ninguna iteración:
        print('Descartado')
        return "Descarto"
    except xml.parsers.expat.ExpatError:
        print('Inexistente')
        return "Error"


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
