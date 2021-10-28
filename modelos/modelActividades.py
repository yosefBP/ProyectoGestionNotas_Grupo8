#!/usr/bin/python3

import modelos.base_models as bm
from typing import Any
from werkzeug.security import generate_password_hash,check_password_hash

                                ## Clase Actividad
class Actividades():
    #atributos
    idActividad= any
    actividad= any
    id_materia= any

    # metodo constructor 
    def __init__(self, p_idActividad, p_actividad, p_id_materia):
        self.idActividad = p_idActividad
        self.actividad = p_actividad
        self.id_materia = p_id_materia
    
    @classmethod
    def get_by_id(cls, idActividad:int):
    
        #Obtiene una Actividad por su id.
        getRow = bm.selectDb("SELECT * FROM Actividades WHERE idActividad = ?", [idActividad])

        if getRow and len(getRow) > 0:
			#llamamos al constructor de la clase par
			#devolvemos una instancia de Actividades
            return cls(getRow[0]['idActividad'], getRow[0]['actividad']), getRow[0]['id_materia']
	    
    def insertar(self):
        #Inserta en la base de datos una Actividad, a partir de los valores del objeto Actividades.
        #Crea una Actividad en la base de datos.
		# Hay que crear una instancia de Actividad en app.py para llamar este metodo        
        fila = bm.insertDb("INSERT INTO Actividades (actividad) VALUES (?)", [self.actividad])

        return (fila == 1)
