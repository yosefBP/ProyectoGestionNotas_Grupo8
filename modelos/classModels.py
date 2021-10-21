# sql statement handler class

import modelos.base_models as bm
from typing import Any


class Usuarios():
    idUsuario = Any
    nombreUsuario = Any
    apellidoUsuario = Any
    correoUsuario = Any
    telefonoUsuario = Any
    direccionUsuario = Any
    password = Any
    rol_id  = Any

    def __init__(self, idUsuario, nombreUsuario, apellidoUsuario, correoUsuario, telefonoUsuario, direccionUsuario, password, rol_id ):
        self.idUsuario = idUsuario
        self.nombreUsuario = nombreUsuario
        self.apellidoUsuario = apellidoUsuario
        self.correoUsuario = correoUsuario
        self.telefonoUsuario = telefonoUsuario
        self.direccionUsuario = direccionUsuario
        self.password = password
        self.rol_id  = rol_id 

         
    @classmethod
    def get_by_id(cls, idUsuario):
        getRow = bm.selectDb("SELECT * FROM Usuarios WHERE idUsuario = ?", [idUsuario])

        if getRow and len(getRow) > 0:
            return cls(getRow[0]['idUsuario'], getRow[0]['nombreUsuario'], getRow[0]['apellidoUsuario'], getRow[0]['correoUsuario'],
             getRow[0]['telefonoUsuario'], getRow[0]['direccionUsuario'], getRow[0]['password'], getRow[0]['rol_id'])

    def insertarUsuario(self):
        numFilas = bm.insertDb("INSERT INTO Usuarios (idUsuario, nombreUsuario, apellidoUsuario, correoUsuario, telefonoUsuario, direccionUsuario, password, rol_id ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [self.idUsuario, self.nombreUsuario, self.apellidoUsuario, self.correoUsuario, self.telefonoUsuario, self.direccionUsuario, self.password, self.rol_id])

        return (numFilas > 0)

    def eliminarUsuario(self):
        sql = "DELETE FROM Usuarios WHERE idUsuario = ?"
        afectadas = bm.insertDb(sql, [self.idUsuario])
        return (afectadas >0)

    @staticmethod
    def get_all():
        return bm.selectDb("SELECT * FROM Usuarios", None)