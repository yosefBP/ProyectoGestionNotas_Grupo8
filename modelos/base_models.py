import sqlite3
from sqlite3 import Error

def conectarDb():
    """ create a database connection to a SQLite database """
    try:
        conexion = sqlite3.connect('./db/appNotas.db')
        return conexion
    except Error as e:
        print("Fallo la coneccion a la base de datos Error:\n" + e)
    return None

def insertDb(_sql, args):
    """ insert into the database """
    try:
        conexion = conectarDb()
        if conexion:
            cursorObjeto = conexion.cursor()

            numFilas = cursorObjeto.execute(_sql, args).rowcount
            cursorObjeto.close()
            conexion.commit()
            conexion.close()

            return numFilas
        else:
            print("No se pudo conectar a la base de datos")
            return -1
    except Error as e:
        print("Fallo al Insertar en la base de datos:\n" + e)
        return -1

def selectDb(_sql, args):
    """ Select into the database """
    try:
        conexion = conectarDb()
        if conexion:
            conexion.row_factory = dict_factory
            cursorObjeto = conexion.cursor()
            if args:
                cursorObjeto.execute(_sql, args)
            else:
                cursorObjeto.execute(_sql)

            filas = cursorObjeto.fetchall()
            cursorObjeto.close()
            conexion.close()

            return filas
        else:
            print("No se pudo conectar a la base de datos")
            return None
    except Error as e:
        print("Fallo al ejecutar el Select en la base de datos:\n" + e)
        return None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d