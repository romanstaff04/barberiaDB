import sqlite3 as sql
from datetime import datetime  # Obtener la fecha actual
# Crear la tabla de servicios si no existe
def crear_tabla():
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

# Insertar un servicio en la tabla
def insertServicio(fecha, barbero, servicio, precio):
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servicios (fecha, barbero, servicio, precio)
        VALUES (?, ?, ?, ?)
    """, (fecha, barbero, servicio, precio))
    conn.commit()
    conn.close()

# Consultar servicios de un día específico
def getServiciosDelDia(fecha):
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
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato compatible con la base de datos
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