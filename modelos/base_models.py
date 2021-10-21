import sqlite3
from sqlite3 import Error

def conectarDb():
    """ create a database connection to a SQLite database """
    try:
        conexion = sqlite3.connect('db/appNotas.db')
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
            conexion.row_factory = sqlite3.Row
            cursorObjeto = conexion.cursor()
            cursorObjeto.execute(_sql, args)
            filas = cursorObjeto.fetchall()
            conexion.close()
            return filas
        else:
            print("No se pudo conectar a la base de datos")
            return None
    except Error as e:
        print("Fallo al ejecutar el Select en la base de datos:\n" + e)
        return None