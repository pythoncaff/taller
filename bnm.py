#!/usr/bin/env python
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
    
    clave_xml           = '/Export?style=MARCXML'
    lista_registros_bnm = []
    
    while registro_inicial <= limite:
        url_final    = '%s%09d%s' % (url_base, registro_inicial, clave_xml)
        registro_bnm = requests.get(url_final)
        with open('%09d.xml' % registro_inicial, 'xb') as f:
            f.write(registro_bnm.content)
        
        lista_registros_bnm.append(registro_bnm)
        registro_inicial += 1
        
    return lista_registros_bnm

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

