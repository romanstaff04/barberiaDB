import sqlite3 as sql
from datetime import datetime  # Obtener la fecha actual

def crear_tabla():
    """
    Crea la tabla
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME NOT NULL,
            barbero TEXT NOT NULL,
            servicio TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertServicio(fecha, barbero, servicio, precio):
    """
    Inserta los servicios a la DB
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servicios (fecha, barbero, servicio, precio)
        VALUES (?, ?, ?, ?)
    """, (fecha, barbero, servicio, precio))
    conn.commit()
    conn.close()


def anularUltimoRegistro():
    """
    Anula el ultimo servicio registrado
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    #Buscar el ID del último registro
    cursor.execute("""
        SELECT id 
        FROM servicios
        ORDER BY id DESC
        LIMIT 1
    """)
    ultimo_registro = cursor.fetchone()
    if ultimo_registro:
        # Eliminar el último registro
        cursor.execute("""
            DELETE FROM servicios
            WHERE id = ?
        """, (ultimo_registro[0],))
        conn.commit()
        print(f"Registro con ID {ultimo_registro[0]} eliminado correctamente.")
    else:
        print("No hay registros para eliminar.")
    conn.close()

def getServiciosDelDia(fecha):
    """
    Consulta los servicios de un dia especifico.
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT barbero, servicio, precio, fecha 
        FROM servicios 
        WHERE DATE(fecha) = ?
    """, (fecha,))
    servicios = cursor.fetchall()
    conn.close()
    return servicios

def finDiaLaboral2():
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d") 
    cursor.execute("""
        SELECT
            fecha,
            COUNT(servicio) AS cortes_totales_en_el_dia,
            SUM(precio) AS total_facturado,
            SUM(precio) * 0.6 AS ganancia_dueno
        FROM servicios
        WHERE fecha = ?;
    """, (fecha_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def detalleServicios():
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT
            servicio,
            COUNT(servicio) as "total"
            FROM servicios
            WHERE fecha = ?
            GROUP BY servicio;
    """, (fecha_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def gananciaBarbero(barbero, fecha):
    """
    Imprime los servicios realizados por el barbero pero sin la sumatoria total
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
	        fecha,
	        barbero,
	        servicio,
	        COUNT(servicio),
	        SUM(precio) * 0.4 AS "ganancia_barbero"
        FROM servicios
        WHERE barbero = ? AND fecha = ?
        GROUP BY servicio;
    """, (barbero, fecha))
    resultado = cursor.fetchall() #devuelve una lista de filas
    conn.close()
    if resultado:
        for fila in resultado: #imprime los resultados de la consulta
            print(f"Fecha: {fila[0]}, Barbero: {fila[1]}, Servicio {fila[2]}, Total_Servicios {fila[3]}, Ganancia_barbero {fila[4]}")
    else:
        print(f"no existen registros para {barbero}")

def gananciaTotalBarbero(barbero):
    """
    Calcula la ganancia economica total del barbero con la sumatoria (de los servicios que hizo, se queda con un 40%)
    """
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
	        SUM(precio) * 0.4 AS "ganancia_total"
        FROM servicios
        WHERE barbero = ?;
    """, (barbero,))
    resultado = cursor.fetchone() #devuelve una sola fila
    conn.close()
    if resultado:
        print(f"Total ${resultado}")