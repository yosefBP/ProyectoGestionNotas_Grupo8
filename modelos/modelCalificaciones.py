from os import stat
import modelos.base_models as bm
from typing import Any

class Calificaciones():
    """
    Clase que representa una calificación
    """
    idCalificacion = Any
    calificacion = Any
    retroalimentacion = Any
    id_usuario = Any
    id_actividad = Any

    def __init__(self, idCalificacion: int, calificacion: float, retroalimentacion: str,id_usuario: int, id_actividad: any ):
        """"
        Constructor de la clase Calificaciones
        """
        self.idCalificacion = idCalificacion
        self.calificacion = calificacion
        self.retroalimentacion = retroalimentacion
        self.id_usuario = id_usuario
        self.id_actividad = id_actividad
    
    @classmethod
    def  get_by_id(cls, calificacionID):
        """
        Obtiene una calificación por su id
        """
        getRow = bm.selectDb("SELECT * FROM Calificaciones WHERE idCalificacion = ?", [calificacionID])

        if getRow and len(getRow) > 0:
            return cls(getRow[0]['idCalificacion'], getRow[0]['calificacion'], getRow[0]['retroalimentacion'], getRow[0]['id_usuario'], getRow[0]['id_actividad'])

    @staticmethod
    def get_by_id_usuario_id_actividad(usuarioID: int, actividadID: int):
        """
        Obtiene una calificación según el usuario y la actividad
        """
        return bm.selectDb("SELECT calificacion FROM Calificaciones WHERE id_usuario = ? AND id_actividad = ?", [usuarioID] [actividadID])
    
    #@staticmethod
    #def notas_materia_usuario(usuarioID: int, materiaID: int):
        

    #    return

    def insertarCalificacion(self):
        """
        Crear una calificacion en la base de datos
        """
        fila = bm.insertDb("INSERT INTO Calificaciones (calificacion, retroalimentacion, id_usuario, id_actividad) VALUES (?, ?, ?, ?)",
        [self.calificacion, self.retroalimentacion, self.id_usuario, self.id_actividad])

        return (fila == 1)

    def actualizarCalificacion(self, nuevaCalificacion: float, nuevaRetroalimentacion: str):
        """
        Actualizar calificacion y retroalimentación en la base de datos
        """
        sql = "UPDATE Calificaciones SET calificacion = ?, retroalimentacion = ? WHERE id_usuario = ? AND id_actividad = ? VALUES (?, ?, ?, ?)"
        fila = bm.insertDb(sql, [nuevaCalificacion, nuevaRetroalimentacion, self.id_usuario, self.id_actividad])
        return (fila == 1)
    
    def eliminarCalificacion(usuarioID :int, actividadID: int):
        """
        Eliminar una calificacion de la base de datos según usuario y actividad
        """
        fila = bm.insertDb("DELETE FROM Calificaciones WHERE id_usuario = ? AND id_actividad = ? VALUES (?, ?) ", 
        [usuarioID, actividadID])
        return (fila == 1)


