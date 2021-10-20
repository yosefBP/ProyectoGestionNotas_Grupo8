import sqlite3
from sqlite3 import Error

def conectarDb():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect('db/appNotas.db')
        return conn
    except Error as e:
        print("Fallo la coneccion a la base de datos Error:\n" + e)
    return None

def crearUsuario(usuario):
    """ create a new user into the database """
    try:
        conexion = conectarDb()
        if conexion:
            sql = ''' INSERT INTO usuarios(nombre, apellido, correo, contrasena)
                      VALUES(?,?,?,?) '''
            cursorObjeto = conexion.cursor()
            numFilas = cursorObjeto.execute(sql, usuario).rowcount
            conexion.commit()
            conexion.close()
            return numFilas
        else:
            print("No se pudo conectar a la base de datos")
            return -1
    except Error as e:
        print("Fallo al crear el usuario Error:\n" + e)