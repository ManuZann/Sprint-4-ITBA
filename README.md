# Sprint-4-ITBA
Esta entrega es la relacionada al 4to Sprint.

# Consigna
El objetivo de este proyecto es desarrollar un script de Python llamadolistado_cheques.py que permita procesar y consultar información de cheques bancarios almacenados en un archivo CSV.
El script debe permitir a los usuarios filtrar y visualizar los datos de los cheques emitidos y depositados por un cliente específico, considerando diferentes criterios de filtrado, como el estado del cheque y el rango de fechas.
Además, se debe gestionar la exportación de datos aun archivo CSV si es necesario.

## Ejecutar
Antes de ejecutar el archivo verificar si tiene instalado Python en la PC.
Ir a la consola de su preferencia y ejecutar el comando:
```py --version```
De caso contrario instalarlo:
``` https://www.python.org/downloads/ ```
Para ejecutar el archivo utilizar el siguiente comando (Antes de ejecutar posicionar el Path en la ubicacion de dicho archivo):
```python listado_cheques.py```
Luego, este nos pedirá ingresar el nombre del .csv que tengamos (si no se encuentra, se creará uno vacío)

Ahora el usuario debe navegar a traves de la aplicación usando el menú y las opciones proporcionadas

## Consideraciones:
*No contemplamos que el campo "valor" sea de tipo flotante o decimal, si se quisiese hacerlo solo habría que agregar una función que separe por "." y valide tanto la parte entera como la decimal para que sean números.
*Usamos un menu para que el usuario pueda navegar entre las opciones y funcionalidades, y que asi sea más amigable con nuevos clientes
