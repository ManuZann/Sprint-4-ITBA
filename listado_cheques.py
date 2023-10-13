import csv
import os
from datetime import datetime

# ~ el archivo CSV
# ~ archivo_cheques = 'cheques.csv'
archivo_cheques = input("Nombre del archivo CSV que desea consultar (Recuerde agregar el .csv al final)")

# ~ Verifica si el archivo CSV existe y si no existe lo crea
if not os.path.isfile(archivo_cheques):
    with open(archivo_cheques, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NroCheque", "CodigoBanco", "CodigoSucursal", "NumeroCuentaOrigen", "NumeroCuentaDestino", "Valor", "FechaOrigen", "FechaPago", "DNI", "Estado"])
        # ~ aca agregar otros cheques

def cargar_cheque(nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado):
    """Guarda un cheque en el archivo CSV"""
    with open(archivo_cheques, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado])

def listar_cheques(filtro=None, fecha_inicio=None, fecha_fin=None):
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
        print("2. Filtrar cheques por cliente y/o fecha")
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
            cargar_cheque(nro_cheque, codigo_banco, codigo_sucursal, numero_cuenta_origen, numero_cuenta_destino, valor, fecha_origen, fecha_pago, dni, estado)
            print("Cheque agregado con éxito.")

        elif opcion == "2":
            dni = input("Ingrese el DNI del cliente (deje en blanco para omitir este filtro): ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD) (deje en blanco para omitir este filtro): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD) (deje en blanco para omitir este filtro): ")
            cheques_filtrados = listar_cheques(dni, fecha_inicio, fecha_fin)

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
                    print(f"FechaOrigen: {datetime.fromtimestamp(float(cheque['FechaOrigen'])).strftime('%Y-%m-%d')}")
                    print(f"FechaPago: {datetime.fromtimestamp(float(cheque['FechaPago'])).strftime('%Y-%m-%d')}")
                    print(f"DNI: {cheque['DNI']}")
                    print(f"Estado: {cheque['Estado']}")

        elif opcion == "3":
            archivo_salida = input("Nombre del archivo de salida CSV: ")
            exportar_cheques(cheques_filtrados, archivo_salida)
            print(f"Cheques exportados a {archivo_salida}.")

        elif opcion == "4":
            break
