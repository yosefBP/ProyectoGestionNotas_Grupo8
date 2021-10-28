#!/usr/bin/python3

import modelos.base_models as bm
from typing import Any


class Docentes():
    """
    Clase que representa una materia.
    """
    idMateria = Any
    nombreMateria = Any
    idDocente = Any


    def __init__(self, idMateria: int, nombreMateria: str, idDocente: int):
        """
        Constructor de la clase Materia.
        """
        self.idMateria = idMateria
        self.nombreMateria = nombreMateria
        self.idDocente = idDocente


    @classmethod
    def get_by_id(cls, idMateria: int):
        """
        Obtiene una materia por su id.
        """
        getRow = bm.selectDb("SELECT * FROM Materias WHERE idMateria = ?", [idMateria])

        if getRow and len(getRow) > 0:
            return cls(getRow[0]['idMateria'], getRow[0]['nombreMateria'])


    @staticmethod
    def listaDocentes():
        """
        Obtiene todas las materias de la base de datos.
        """
        listaDocentes = []
        dicDocente = {}
        docentes = bm.selectDb("SELECT idUsuario, nombreUsuario FROM Usuarios WHERE rol_id = ? AND idusuario IN (SELECT id_usuario FROM MateriaUsuarios)", [1])
        print(docentes[0]['idUsuario'])
        dicDocente.setdefault(docentes[0]['idUsuario'], docentes[0]['nombreUsuario'])
        print(dicDocente)
        return docentes

    @staticmethod
    def materiaDocente(idUsuario: int):
        """
        Obtiene las materias que ha cursado un usuario.
        """
        return bm.selectDb("SELECT * FROM Materias WHERE idMateria IN (SELECT id_materia FROM MateriaUsuarios WHERE id_usuario = ?)", [idUsuario])


    def insertarMateria(self):
        """
        Crea un docente en la base de datos.
        """
        fila = bm.insertDb("INSERT INTO Materias (idMateria, nombreMateria) VALUES (?, ?)",
        [self.idMateria, self.nombreMateria])

        return (fila == 1)


    def actualizarMateria(self):
        """
        Actualiza un docente en la base de datos.
        """
        fila = bm.updateDb("UPDATE Materias SET nombreMateria = ? WHERE idMateria = ?",
        [self.nombreMateria, self.idMateria])

        return (fila == 1)


    def eliminarMateria(self):
        """
        Elimina un docente de la base de datos.
        """
        fila = bm.deleteDb("DELETE FROM Materias WHERE idMateria = ?", [self.idMateria])

        return (fila == 1)


    def __str__(self):
        """
        Representación en string de la clase Docente.
        """
        return 'Materia: {} Id: {}'.format(self.nombreMateria, self.idMateria)
