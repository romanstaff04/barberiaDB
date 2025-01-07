from datetime import datetime  # Obtener la fecha actual
import sys  # Finalizar el programa en caso de error
import DBbarberia as db  # Módulo de la base de datos
class Barberia:
    servicios = { # servicios que realiza la barberia con sus respectivos precios
        "barba": 5000,
        "pelo": 6000,
        "cortebarba": 7000
    }
    barberos = ["Santiago", "Alejandro2", "Brian", "Ángel", "Alejandro"] #nombre barberos

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
            print("3. Salir")
            opcion = int(input("Ingrese una opción: "))
            if opcion == 1:
                self.registrar_servicio()
            elif opcion == 2:
                self.informe_del_dia()
            elif opcion == 3:
                print("¡Gracias por usar el sistema! Hasta luego.")
                sys.exit()
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

    def informe_del_dia(self):
        print("\n--- Informe del Día ---")
        servicios = db.getServiciosDelDia(self.fecha_actual)
        if servicios:
            print(f"Servicios realizados el {self.fecha_actual}:")
            for barbero, servicio, precio, fecha in servicios:
                print(f"- Barbero: {barbero}, Servicio: {servicio}, Precio: ${precio}, Fecha: {fecha}")
                self.totalFacturado += precio #cada servicio aumenta la facturacion
                self.cortes_totales += 1 #cada servicio aumenta los cortes totales
            gananciaDueño = self.totalFacturado * 0.6 # calculamos la ganancia del dueño que: del precio del servicio se queda con un 60%
            print(f"Facturado = {self.totalFacturado}")
            print(f"Cortes Totales = {self.cortes_totales}")
            print(f"Ganancia dueño = ${gananciaDueño}")
            sys.exit()
            #db.fechaInforme(self.fecha_actual)
        else:
            print("No se registraron servicios hoy.")


# Ejecutar el programa
if __name__ == "__main__":
    barberia = Barberia()
    barberia.menu()