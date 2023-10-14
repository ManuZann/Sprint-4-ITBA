import csv
import os
from datetime import datetime
import time

# ~ el archivo CSV
# ~ archivo_cheques = 'cheques.csv'
archivo_cheques = input("Nombre del archivo CSV que desea consultar (NO es necesario agregar .csv al final) ")+".csv"

# ~ Verifica si el archivo CSV existe y si no existe lo crea
if not os.path.isfile(archivo_cheques):
    with open(archivo_cheques, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NroCheque", "CodigoBanco", "CodigoSucursal", "NumeroCuentaOrigen", "NumeroCuentaDestino", "Valor", "FechaOrigen", "FechaPago", "DNI", "Estado", "Tipo"])
        # ~ aca agregar otros cheques

#Funciones para validar los tipos de datos ingresados
def validar_fecha(fechaEntrada):
    try:
        d = datetime.strptime(fechaEntrada, "%Y-%m-%d")
        return True, d
    except ValueError:
        return False, None

def validar_entero(num):
    try:
        int(num)
        return True, num
    except ValueError:
        return False, None

def validar_dni(dni):
    try:
        #Controla que sea un strings de numeros
        entero = int(dni)
        if len(dni) == 8:
            return True, dni
        else:
            return False, None
    except ValueError:
        return False, None

def cargar_cheque(nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado, tipo):
    """Guarda un cheque en el archivo CSV"""

    #Valida que las fechas tengan el formato adecuado
    fecha_origen_valida, fecha_origen = validar_fecha(fecha_origen)
    fecha_pago_valida, fecha_pago = validar_fecha(fecha_pago)
    if not fecha_origen_valida or not fecha_pago_valida:
        print("Error: Las fechas no tienen el formato correcto (YYYY-MM-DD).")
        return

    # Valida los campos de numeros enteros (DNI, NroCheque, etc)
    nro_cheque_valid, nro_cheque = validar_entero(nro_cheque)
    numero_cuenta_origen_valid, numero_cuenta_origen = validar_entero(numero_cuenta_origen)
    numero_cuenta_destino_valid, numero_cuenta_destino = validar_entero(numero_cuenta_destino)
    valor_valid, valor = validar_entero(valor)
    if not (nro_cheque_valid and numero_cuenta_origen_valid and numero_cuenta_destino_valid and valor_valid):
        print("Error: Los valores numércios deben ser un números enteros.")
        return
    
    #Controla que el DNI tenga 8 digitos y sean numeros
    dni_valid, dni = validar_dni(dni)
    if not (dni_valid):
        print("Error: El DNI debe tener 8 caracteres numéricos.")
        return
    
    #Se abre el archivo para ver si se quiere agregar un nroCheque ya existente a un usuario
    with open(archivo_cheques, "r") as file:
        arch = csv.DictReader(file)
        for fila in arch:
            if (
                fila["NroCheque"] == nro_cheque and
                fila["NumeroCuentaOrigen"] == numero_cuenta_origen and
                fila["DNI"] == dni
            ):
                print("Error: El número de cheque ya existe en la misma cuenta para el DNI ingresado.")
                return

    # Si no se encuentra un cheque duplicado, agrega el cheque al archivo .CSV
    with open(archivo_cheques, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado, tipo])
    print("Cheque agregado con éxito.")

def listar_cheques(filtro=None, fecha_inicio=None, fecha_fin=None, tipo=None):
    """Ordena los cheques en el archivo CSV"""

    with open(archivo_cheques, "r") as file:
        reader = csv.DictReader(file)
        cheques = [cheque for cheque in reader]

    if filtro:
        cheques = [cheque for cheque in cheques if cheque["DNI"] == filtro]

    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        cheques = [cheque for cheque in cheques if fecha_inicio <= datetime.fromtimestamp(float(cheque["FechaPago"])) <= fecha_fin]
    
    if tipo:
        cheques = [cheque for cheque in cheques if cheque["Tipo"] == tipo]

    return cheques

def exportar_cheques(cheques, archivo_salida):
    """Esta funcion exporta los cheques a un archivo CSV """
    with open(archivo_salida, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cheques[0].keys())
        writer.writeheader()
        writer.writerows(cheques)

if __name__ == "__main__":
    while True:
        print("\nMenú:")
        print("1. Agregar cheque")
        print("2. Filtrar cheques por cliente, fecha y/o tipo de cheque")
        print("3. Exportar cheques filtrados")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        # ~ Limpia la consola
        os.system ("cls")

        if opcion == "1":
            nro_cheque = input("Número de cheque: ")
            codigo_banco = input("Código de banco: ")
            codigo_sucursal = input("Código de sucursal: ")
            numero_cuenta_origen = input("Número de cuenta de origen: ")
            numero_cuenta_destino = input("Número de cuenta de destino: ")
            valor = input("Valor: ")
            fecha_origen = input("Fecha de emisión (YYYY-MM-DD): ")
            fecha_pago = input("Fecha de pago (YYYY-MM-DD): ")
            dni = input("DNI del cliente: ")
            estado = input("Estado (pendiente/aprobado/rechazado): ")
            tipo = input("Tipo de Cheque (emitido/depositado): ")
            cargar_cheque(nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado, tipo)

        elif opcion == "2":
            dni = input("Ingrese el DNI del cliente (deje en blanco para omitir este filtro): ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD) (deje en blanco para omitir este filtro): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD) (deje en blanco para omitir este filtro): ")
            tipo = input("Ingrese el tipo de cheque (emitido/depositado) (deje en blanco para omitir este filtro): ")
            cheques_filtrados = listar_cheques(dni, fecha_inicio, fecha_fin, tipo)

            if not cheques_filtrados:
                print("No se encontraron cheques que cumplan con los criterios de búsqueda.")
            else:
                for cheque in cheques_filtrados:
                    print("\nDetalle del cheque >>>")
                    print(f"NroCheque: {cheque['NroCheque']}")
                    print(f"CodigoBanco: {cheque['CodigoBanco']}")
                    print(f"CodigoSucursal: {cheque['CodigoSucursal']}")
                    print(f"NumeroCuentaOrigen: {cheque['NumeroCuentaOrigen']}")
                    print(f"NumeroCuentaDestino: {cheque['NumeroCuentaDestino']}")
                    print(f"Valor: {cheque['Valor']}")
                    print(f"FechaOrigen: {datetime.fromtimestamp(time.mktime(datetime.strptime(cheque['FechaOrigen'],'%Y-%m-%d').timetuple())).strftime('%Y-%m-%d')}")
                    print(f"FechaPago: {datetime.fromtimestamp(time.mktime(datetime.strptime(cheque['FechaPago'],'%Y-%m-%d').timetuple())).strftime('%Y-%m-%d')}")
                    print(f"DNI: {cheque['DNI']}")
                    print(f"Estado: {cheque['Estado']}")
                    print(f"Tipo: {cheque['Tipo']}")

        elif opcion == "3":
            try:
                archivo_salida = input("Nombre del archivo de salida CSV: ")+".csv"
                exportar_cheques(cheques_filtrados, archivo_salida)
                print(f"Cheques exportados a {archivo_salida}")
            except NameError:
                print("Se debe filtrar los cheques antes de ser importados.")

        elif opcion == "4":
            break
