from datetime import datetime  # Obtener la fecha actual
import sys  # Finalizar el programa en caso de error
import DBbarberia as db #modulo de la base de datos


class Barberia:
    servicios = {
        "barba": 5000,
        "pelo": 6000,
        "cortebarba": 7000
    }
    barberos = ["Santiago", "Alejandro2", "Brian", "Ángel", "Alejandro"]  # Lista con los nombres de los barberos
    # --------------------------------------------------------------------------
    def __init__(self):
        self.cortes_totales = 0
        self.ingresos_totales = 0
        self.ganancia_barberos = {barbero: 0 for barbero in self.barberos}
        self.ganancia_dueno = 0
        self.fecha_actual = datetime.now()
    # --------------------------------------------------------------------------
    def menu(self):
        print("1. Registrar un servicio")
        print("2. Anular el último servicio")
        print("3. Ver informe del día")
        print("4. Salir")
        opcion = int(input("Ingrese una opción: "))
        if opcion == 1:
            self.registrar_servicio()
        elif opcion == 2:
            self.anular_ultimo_servicio()
        elif opcion == 3:
            self.ver_informe_del_dia()
        elif opcion == 4:
            print("¡Gracias por usar el sistema! Hasta luego.")
            sys.exit()
        else:
            print("Opción inválida. Intente nuevamente.")
    # ------------------------------------------------------------------------
    def registrar_servicio(self):
        print("Barberos disponibles:")
        for indice, barbero in enumerate(self.barberos, start=1):
            print(f"{indice}. {barbero}")
        print("6. Volver al menú principal")
        try:
            opcion = int(input("Seleccione un barbero: "))
            if opcion == 6:
                print("Regresando al menú principal...")
                self.menu()
                return
            elif opcion < 1 or opcion > len(self.barberos):
                print("Opción inválida. Intente nuevamente.")
                return
            barbero_seleccionado = self.barberos[opcion - 1]  # Accede al barbero correspondiente
            print(f"Has seleccionado a {barbero_seleccionado}")
            print("Servicios disponibles:")

            for servicio, precio in self.servicios.items():
                print(f"- {servicio.replace('_', ' ').capitalize()}: ${precio}") #capitalize convierte la primera letra de una cadena en mayúscula y el resto en minúsculas.

            servicio_elegido = input("Ingrese el servicio realizado: ").lower() #todo a minusculas para que no genere error
            if servicio_elegido not in self.servicios:
                print("error")
                return
            self.cortes_totales += 1
            precio = self.servicios[servicio_elegido]
            self.ingresos_totales += precio
            self.ganancia_barberos[barbero_seleccionado] += precio * 0.4  # 40% para el barbero
            self.ganancia_dueno += precio * 0.6  # 60% para el dueño
            # Insertar datos en la base de datos
            confirmacion = input(f"{servicio_elegido} para {barbero_seleccionado}, confirmas? s/n").lower()
            if confirmacion != "s":
                print("servicio cancelado: ")
                return
            else:
                db.insertServicio(self.fecha_actual, barbero_seleccionado, servicio_elegido, precio)
                print(f"Servicio registrado exitosamente para {barbero_seleccionado}.")
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
    # ------------------------------------------------------------------------
    def anular_ultimo_servicio(self):
        pass
    # ------------------------------------------------------------------------
    def ver_informe_del_dia(self):
        self.finalizacion_dia_laboral()
    # ------------------------------------------------------------------------
    def finalizacion_dia_laboral(self):
        print(f"Fecha: {self.fecha_actual}")
        print(f"Cortes totales: {self.cortes_totales}")
        print(f"Facturación total: ${self.ingresos_totales}")
        print(f"Ganancia del dueño: ${self.ganancia_dueno}")
        print(f"Ganancias de los barberos: {self.ganancia_barberos}")

# Crear instancia de la clase
barberia = Barberia()
barberia.menu()