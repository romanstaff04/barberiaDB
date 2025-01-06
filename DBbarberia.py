import sqlite3 as sql
def createDb():
    conn = sql.connect("databaseBarberia")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("databaseBarberia")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            nombre TEXT NOT NULL,
            servicio TEXT NOT NULL,
            precio INTEGER NOT NULL
        )"""
    )
    print("tabla creada con exito")
    conn.commit()
    conn.close()


def dropTable():
    conn = sql.connect("databaseBarberia")
    cursor = conn.cursor()
    cursor.execute(
        """DROP TABLE barberos"""
    )
    conn.commit()
    conn.close()

def insertServicio(fecha, barbero, servicio, precio):
    conn = sql.connect("databaseBarberia")
    cursor = conn.cursor()
    query = """INSERT INTO servicios (fecha, nombre, servicio, precio) 
                VALUES (?, ?, ?, ?)"""
    cursor.execute(query, (fecha, barbero, servicio, precio))
    conn.commit()
    conn.close()

# Consultar datos
def consultar():
    conn = sql.connect("databaseBarberia")
    cursor = conn.cursor()
    cursor.execute(
            """SELECT * FROM servicios """
        )
    resultados = cursor.fetchall()
    for fila in resultados: #preguntar a chatgpt si resultados esta vacio, imprima: no tenes registros en la base de datos
        print(fila)
    conn.commit()
    conn.close()



consultar()