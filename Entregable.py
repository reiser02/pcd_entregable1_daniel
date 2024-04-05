from enum import Enum
import pytest

class EDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Persona:
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni

class Profesor(Persona):
    #Asignaturas es un conjunto para no permitir que hayan repetidas
    def __init__(self, nombre, dni, departamento):
        super().__init__(nombre, dni)
        self.creditos = None
        self.departamento = departamento
        self.asignaturas = set()

    def solicitar_asignaturas(self, listaAsignaturas):
        for e in listaAsignaturas:
            if self.creditos + e.creditos > 72:
                raise ValueError("Se excede el máximo de créditos que un profesor puede impartir")
            self.creditos += e.creditos
            self.asignaturas.add(e)

class Titular(Profesor):
    def __init__(self, nombre, dni, areaInvestivacion, departamento):
        super().__init__(nombre, dni, departamento)
        self.areaInvestivacion = areaInvestivacion
    
    def obtener_area_inv(self):
        return self.areaInvestivacion.area

class Asociado(Profesor):
    def __init__(self, nombre, dni, departamento, trabajoExterno):
        super().__init__(nombre, dni, departamento)
        self.trabajoExterno = trabajoExterno

class Asignatura():
    def __init__(self, nombre, creditos, curso):
        self.nombre = nombre
        self.creditos = creditos
        self.curso = curso

class Estudiante(Persona):
    #Asignaturas es un conjunto para no permitir que hayan repetidas
    def __init__(self, nombre, dni, curso):
        super().__init__(nombre, dni)
        self.curso = curso
        self.asignaturas = set()

    def add_asignaturas(self, listaAsignaturas):
        for e in listaAsignaturas:
            self.asignaturas.add(e)


class Universidad():
    def __init__(self):
        self.listaProfesores = list()
        self.listaAlumnos = list()
        self.listaAsignaturas = list()

    def add_profesor(self, nombre, dni, titular, departamento, areaInv=None, trabajoExterno=None):
        if not isinstance(departamento, EDepartamento):
            raise TypeError("Departamento no pertece a la clase EDepartamento")
        '''
        for p in self.listaProfesores():
            if dni == p.dni:
                return 
        '''
        if titular:
            if areaInv is None:
                raise ValueError("Si el profesor es titular, debe tener area de investigación")
            elif trabajoExterno is not None:
                raise ValueError("Si el profesor es titular, no debe tener un trabajo externo")
            t = Titular(nombre, dni, departamento, areaInv)
            self.listaProfesores.append(t)
        else:
            self.listaProfesores.append(Asociado(nombre, dni, departamento, trabajoExterno))



def test_add_profesor_titular():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", True, EDepartamento.DIIC, "software")
    assert len(universidad.listaProfesores) == 1


def test_add_profesor_asociado():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", False, EDepartamento.DIIC, trabajoExterno="Programador")
    assert len(universidad.listaProfesores) == 1






def test_exceso_creditos_profesor():
    with pytest.raises(ValueError):
        profesor = Titular("Jose", "23137838", 70)
        asignatura = Asignatura("PCD", 6, "Segundo")
        profesor.solicitar_asignatura(asignatura)

def test_asignatura_añadida_alumno():
    asignatura = Asignatura("PCD", 6, "Segundo")
    alumno = Estudiante("Carlos", "2344235", "Segundo")
    alumno.add_asignaturas([asignatura])
    assert len(alumno.asignaturas) == 1

def test_asignatura_añadida_profesor():
    profesor = Titular("Jose", "23137838", 70)
    asignatura = Asignatura("PCD", 6, "Segundo")
    profesor.solicitar_asignatura(asignatura)
    assert len(profesor.asignaturas) == 1

def test__del__alumno():
    asignatura = Asignatura("PCD", 6, "Segundo")
    alumno = Estudiante("Carlos", "2344235", "Segundo")
    alumno.add_asignaturas([asignatura])
    del alumno
    assert len(asignatura.listaMatriculados) == 0
