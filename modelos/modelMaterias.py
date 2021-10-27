#!/usr/bin/python3

import modelos.base_models as bm
from typing import Any


class Materias():
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
    def get_all():
        """
        Obtiene todas las materias de la base de datos.
        """
        return bm.selectDb("SELECT * FROM Materias", None)

    @staticmethod
    def materiaUsuario(idUsuario: int):
        """
        Obtiene las materias que ha cursado un usuario.
        """
        return bm.selectDb("SELECT * FROM Materias WHERE idMateria IN (SELECT id_materia FROM MateriaUsuarios WHERE id_usuario = ?)", [idUsuario])


    def insertarMateria(self):
        """
        Crea una materia en la base de datos.
        """
        fila = bm.insertDb("INSERT INTO Materias (idMateria, nombreMateria) VALUES (?, ?)",
        [self.idMateria, self.nombreMateria])

        return (fila == 1)


    def actualizarMateria(self):
        """
        Actualiza una materia en la base de datos.
        """
        fila = bm.updateDb("UPDATE Materias SET nombreMateria = ? WHERE idMateria = ?",
        [self.nombreMateria, self.idMateria])

        return (fila == 1)


    def eliminarMateria(self):
        """
        Elimina una materia de la base de datos.
        """
        fila = bm.deleteDb("DELETE FROM Materias WHERE idMateria = ?", [self.idMateria])

        return (fila == 1)


    def __str__(self):
        """
        Representación en string de la clase Materia.
        """
        return 'Materia: {} Id: {}'.format(self.nombreMateria, self.idMateria)