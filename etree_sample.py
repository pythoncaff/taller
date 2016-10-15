"""script ejemplo con lxml.etree; toma número de registro como argumento e
imprime cuántos elementos "datafield" con tag=856 tiene"""

import requests
from lxml import etree
import sys

base_url = 'http://www.bnm.me.gov.ar/catalogo/Record/'
clave_xml = '/Export?style=MARCXML'

response = requests.get('%s%09d%s' % (base_url, int(sys.argv[1]), clave_xml))
xml = etree.XML(response.content)
ns = {'a': 'http://www.loc.gov/MARC21/slim'}
search = xml.xpath('//a:datafield[@tag="856"]', namespaces=ns)
print(len(search))
