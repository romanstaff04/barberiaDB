import sqlite3 as sql

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

def fechaInforme(fecha):
    conn = sql.connect("databaseBarberia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM servicios WHERE DATE(fecha) = ? """, (fecha,))
    conn.commit()
    conn.close()