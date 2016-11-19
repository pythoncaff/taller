# TODO:

* Nombres para los parametros
* Archivo de configuracion
* Registro de corrida // ¿revisar el tema de la cantidad de registros totales? o parar si recibimos más de 20 (ej) registros inexistentes consecutivos
* Consultar db para ver qué hacemos
* Actualización de registros en db según el caso
~~Manejar excepciones con archivos existentes~~
* Manejar las no respuestas del servidor: que no se cuelgue el programa; si servidor no responde, por ejemplo podemos reintentar un número predefinido de veces antes de salir
* Hacer solicitudes al servidor en paralelo (conexiones simultáneas), varias solicitudes por proceso. Sería deseable que siempre por ejemplo 5 requests en curso. Otra alternativa (menos deseable?) es largar 5 en paralelo, y no seguir con las siguientes 5 hasta que todas las anteriores hayan respondido.
* Explorar y parsear los xml de un directorio, y extraer los valores de los tags que se pasen como argumentos de la función junto al directorio. Esto se guarda en un archivo (csv, sqlite, json) para acceder al él y al menos descargar los contenidos después; la info parseada también nos podría servir por un lado para armar una estructura de directorios y nombrar los pdf bajados o generados, y alimentar el sitio dominiopublico. Decidimos programarlo como un módulo separado (en vez de ir parseando a medida que descargamos los xml) para poder trabajar con los xml descargados offline.
* Armar el programa que explora la lista de metadatos de los xml y descarga el pdf si existe, o las imágenes si no.
* Si no hay pdf y sólo hay ebook (imágenes), en teoría podríamos usar el número de inventario para ir al directorio indexable (el árbol expuesto: http://www.bnm.me.gov.ar/giga1/) y bajar todas las imágenes del directorio (en vez de ir página por página en el reader). Pero, queremos explorar el reader como usuarios en cambio (página por página), para poder usarlo en otras bibliotecas que no tengan el árbol de directorios así expuesto.
