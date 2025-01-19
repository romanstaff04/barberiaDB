from datetime import datetime  # Obtener la fecha actual
import sys  # forzar a finalizar el programa 
import DBbarberia as db  # Módulo de la base de datos

class Barberia:
    servicios = { # servicios que realiza la barberia con sus respectivos precios
        "barba": 5000,
        "pelo": 6000,
        "cortebarba": 7000
    }
    barberos = ["Santiago", "Alejandro2", "Brian", "Ángel", "Alejandro"] #nombres barberos

    def __init__(self):
        self.cortes_totales = 0
        self.totalFacturado = 0
        self.fecha_actual = datetime.now().strftime("%Y-%m-%d")
        db.crear_tabla()  # Asegurar que la tabla existe al iniciar

    def menu(self):
        while True:
            print("\n--- Menú Principal ---")
            print("1. Registrar un servicio")
            print("2. Ver informe del día")
            print("3. Anular ultimo servicio")
            print("4. Salir")
            print("5. Archivo TXT")
            print("6. Ganancia Barbero")
            opcion = int(input("Ingrese una opción: "))
            if opcion == 1:
                self.registrar_servicio()
            elif opcion == 2:
                self.informe_del_dia()
            elif opcion == 3:
                self.anularUltimoServicio()
            elif opcion == 4:
                print("¡Gracias por usar el sistema! Hasta luego.")
                sys.exit()
            elif opcion == 5:
                self.finDiaLaboral()
                sys.exit()
            elif opcion == 6:
                print("Barberos")
                print("1. Santiago")
                print("2. Alejandro2")
                print("3. Brian")
                print("4. Angel")
                print("5. Ale")
                opcion = int(input("Elija el barbero: "))
                if opcion < 1 or opcion > 5:
                    print("Error, Barbero no valido.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def registrar_servicio(self):
        print("\n--- Registrar Servicio ---")
        for indice, barbero in enumerate(self.barberos, start=1):
            print(f"{indice}. {barbero}")
        print("6. Volver al menú principal")
        try:
            opcion = int(input("Seleccione un barbero: "))
            if opcion == 6:
                return
            elif opcion < 1 or opcion > len(self.barberos):
                print("Opción inválida. Intente nuevamente.")
                return

            barbero_seleccionado = self.barberos[opcion - 1]
            print("Servicios disponibles:")
            for servicio, precio in self.servicios.items():
                print(f"- {servicio.capitalize()}: ${precio}")

            servicio_elegido = input("Ingrese el servicio realizado: ").lower()
            if servicio_elegido not in self.servicios:
                print("Servicio no válido. Intente nuevamente.")
                return
            precio = self.servicios[servicio_elegido]
            confirmacion = input(f"¿Registrar {servicio_elegido} para {barbero_seleccionado} por ${precio}? (s/n): ").lower()
            if confirmacion == "s":
                db.insertServicio(self.fecha_actual, barbero_seleccionado, servicio_elegido, precio)
                print("Servicio registrado exitosamente.")
            else:
                print("Registro cancelado.")
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")

    def anularUltimoServicio(self):
        opcion = input("estas seguro que queres anular el ultimo servicio registrado?: s/n").lower()
        if opcion == "s":
            db.anularUltimoRegistro()
            print("anulado correctamente")
            return
        print("anulacion cancelada")
        sys.exit()

    def informe_del_dia(self):
        print("\n--- Informe del Día ---")
        servicios = db.getServiciosDelDia(self.fecha_actual)
        if servicios:
            print(f"Servicios realizados el {self.fecha_actual}:")
            for barbero, servicio, precio, fecha in servicios:
                print(f"- Barbero: {barbero}, Servicio: {servicio}, Precio: ${precio}, Fecha: {fecha}")
                self.totalFacturado += precio #cada servicio aumenta la facturacion
                self.cortes_totales += 1 #cada servicio aumenta los cortes totales
            print(f"Facturado = {self.totalFacturado}")
            print(f"Cortes Totales = {self.cortes_totales}")
            sys.exit()
        else:
            print("No se registraron servicios hoy.")

    def finDiaLaboral(self):
        resultados = db.finDiaLaboral2()
        if resultados:
            for fecha, cortes_totales_en_el_dia, total_facturado, ganancia_dueno in resultados:
                print(f"Fecha: {fecha}")
                print(f"Cortes Totales: {cortes_totales_en_el_dia}")
                print(f"Total facturado: ${total_facturado}")
                print(f"Ganancia del dueño: ${ganancia_dueno}")
            self.guardarFinDiaLaboralEnTXT()
            db.detalleServicios() #funcion que contiene una consulta a la DB
        else:
            print("no se registraron servicios para el dia de hoy")


    def guardarFinDiaLaboralEnTXT(self): #funcion para guardar el informe de la jornada laboral en un archivo "txt"
        resultados = db.finDiaLaboral2() #esta funcion contiene una consulta para extraer los datos de la db
        resultados2= db.detalleServicios() #esta funcion contiene una consulta para extraer los datos de la db
        if resultados:
            nombreArchivo= f"finJornada {datetime.now().strftime('%Y-%m-%d')}.txt" # Nombre del archivo con la fecha actual 
            
            with open(nombreArchivo, "a") as archivo:  # Usa "a" para agregar datos al archivo
                archivo.write("--- Informe del Día ---\n")
                for fecha, cortes_totales_en_el_dia, total_facturado, ganancia_dueno in resultados:
                    archivo.write(f"Fecha: {fecha}\n")
                    archivo.write(f"Cortes Totales: {cortes_totales_en_el_dia}\n")
                    archivo.write(f"Total Facturado: ${total_facturado:.2f}\n")
                    archivo.write(f"Ganancia del Dueño: ${ganancia_dueno:.2f}\n")
                for servicio, total in resultados2:
                    archivo.write(f"{servicio}: { total}")
                    archivo.write("\n")
                    #archivo.write(f"{total}")
            print(f"Informe del día guardado en {nombreArchivo}.")
        else:
            print("No se registraron servicios para el día de hoy.")

# Ejecutar el programa
if __name__ == "__main__":
    barberia = Barberia()
    barberia.menu()