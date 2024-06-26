from enum import Enum
import pytest

class EDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Persona:
    def __init__(self, nombre, dni, sexo):
        self.nombre = nombre
        self.dni = dni

        if sexo != "V" and sexo != "M":
            raise ValueError("El argumento sexo solo puede ser V o M")
        self.sexo = sexo

class Profesor(Persona):
    def __init__(self, nombre, dni, sexo, departamento):
        super().__init__(nombre, dni, sexo)
        self.creditos = 0
        self.departamento = departamento
        self.asignaturas = list()

    #Añade una asignatura a la lista de asignaturas si no está ya y si no se excede el máximo de créditos
    def add_asignatura(self, codAsignatura, creditos):
        if codAsignatura in self.asignaturas:
            return
            
        if self.creditos + creditos > 72:
            raise ValueError("Se excede el máximo de créditos que un profesor puede impartir")
        self.creditos += creditos
        self.asignaturas.append(codAsignatura)

    '''
    Ya que el enunciado dice que se tiene que poder eliminar a un profesor de un departamento,
    al cambiarlo se le estaría borrando se su anterior departamento.
    '''
    def cambiar_departamento(self, departamento):
        '''
        Así se obliga a que sea instancia de EDepartamento y no hay problemas con que se ponga None y se quede
        sin departamento
        '''
        if not isinstance(departamento, EDepartamento):
            raise TypeError("Departamento no pertece a la clase EDepartamento")
        
        self.departamento = departamento

class Titular(Profesor):
    def __init__(self, nombre, dni, sexo, departamento, areaInvestivacion):
        super().__init__(nombre, dni, sexo, departamento)
        self.areaInvestivacion = areaInvestivacion
    
    def obtener_area_inv(self):
        return self.areaInvestivacion.area
    
    def __str__(self):
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Sexo: {self.sexo}\n")
        print(f"Departamento: {self.departamento}\n")
        print(f"Area de investigación: {self.areaInvestivacion}\n")
        print(f"Creditos: {self.creditos}\n")
        print(f"Asignaturas: {self.asignaturas}")
        return "\n"

class Asociado(Profesor):
    def __init__(self, nombre, dni, sexo, departamento, trabajoExterno):
        super().__init__(nombre, dni, sexo, departamento)
        self.trabajoExterno = trabajoExterno

    def __str__(self):
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Sexo: {self.sexo}\n")
        print(f"Departamento: {self.departamento}\n")
        print(f"Trabajo externo: {self.trabajoExterno}\n")
        print(f"Creditos: {self.creditos}\n")
        print(f"Asignaturas: {self.asignaturas}")
        return "\n"

class Asignatura():
    def __init__(self, codigo, creditos, curso):
        self.codigo = codigo
        self.creditos = creditos
        self.curso = curso

    def __str__(self):
        cursos = ["Primero", "Segundo", "Tercero", "Cuarto"]
        print(f"Codigo: {self.codigo}\n")
        print(f"Creditos: {self.creditos}\n")
        print(f"Asignaturas: {cursos[self.curso]}\n")
        return "\n"

class Estudiante(Persona):
    def __init__(self, nombre, dni, sexo, curso):
        super().__init__(nombre, dni, sexo)
        self.curso = curso
        self.asignaturasMatriculadas = list()
        self.asignaturasAprobadas = list()

    def add_asignatura(self, codAsignatura):
        '''
        Si el código está en una de las dos listas, entonces la asignatura no se tiene que añadir.
        '''
        if codAsignatura in self.asignaturasMatriculadas or codAsignatura in self.asignaturasAprobadas:
            return
        
        self.asignaturasMatriculadas.append(codAsignatura)

    def aprobar_asignatura(self, codAsignatura):
        '''
        Como list().remove tiene una excepción si no el existe el valor, lo meto en un try except.
        '''
        try:
            self.asignaturasMatriculadas.remove(codAsignatura)
            self.asignaturasAprobadas.append(codAsignatura)
        except Exception as e:
            print("Excepción: ", e)

    def __str__(self):
        cursos = ["Primero", "Segundo", "Tercero", "Cuarto"]
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Sexo: {self.sexo}\n")
        print(f"Curso: {cursos[self.curso]}\n")
        print(f"Asignaturas matriculadas: {self.asignaturasMatriculadas}")
        print(f"Asignaturas aprobadas: {self.asignaturasAprobadas}")
        return "\n"


class Universidad():
    def __init__(self):
        '''
        He optado por el uso de diccionarios indexados por dni o código de asignatura en lugar de listas
        para evitar recorrer las listas cada vez que sea necesario buscar a un profesor, alumno o asignatura.
        '''
        self.dictProfesores = dict()
        self.dictAlumnos = dict()
        self.dictAsignaturas = dict()

    def add_profesor(self, nombre, dni, sexo, titular, departamento, areaInv=None, trabajoExterno=None):
        if not isinstance(departamento, EDepartamento):
            raise TypeError("Departamento no pertece a la clase EDepartamento")
        
        #Así hago que acabe el método en caso de que ya exista un profesor con ese dni
        if dni in self.dictProfesores:
            return
        
        #Comprobación de los requisitos que se imponen y excepciones en caso de no cumplirse
        if titular:
            if areaInv is None:
                raise ValueError("Si el profesor es titular, debe tener area de investigación")
            elif trabajoExterno is not None:
                raise ValueError("Si el profesor es titular, no debe tener un trabajo externo")
            self.dictProfesores[dni] = Titular(nombre, dni, sexo, departamento, areaInv)
        else:
            if areaInv is not None:
                raise ValueError("Si el profesor es asociado, no debe tener area de investigación")
            elif trabajoExterno is None:
                raise ValueError("Si el profesor es asociado, debe tener un trabajo externo")
            self.dictProfesores[dni] = Asociado(nombre, dni, sexo, departamento, trabajoExterno)

    def add_alumno(self, nombre, dni, sexo, curso):
        #Si ya existe un alumno con ese dni, acaba la función
        if dni in self.dictAlumnos:
            return
        
        self.dictAlumnos[dni] = Estudiante(nombre, dni, sexo, curso)

    def add_asignatura(self, codigo, creditos, curso):
        #Si ya existe una asignatura con ese código, acaba la función
        if codigo in self.dictProfesores:
            return
            
        self.dictAsignaturas[codigo] = Asignatura(codigo, creditos, curso)

    def add_asignatura_profesor(self, dni, codigo):
        #Controlada la excepción en caso de que la clave por la que se indexa no exista.
        try:
            profesor = self.dictProfesores[dni]
        except Exception as e:
            print(f"El profesor con dni: {dni} no existe", e)

        try:
            asignatura = self.dictAsignaturas[codigo]
        except Exception as e:
            print(f"La asigntura con codigo: {codigo} no existe", e)

        profesor.add_asignatura(codigo, asignatura.creditos)

    def add_asignatura_alumno(self, dni, codigo):
        #Controlada la excepción en caso de que la clave por la que se indexa no exista.
        try:
            alumno = self.dictAlumnos[dni]
        except Exception as e:
            print(f"El alumno con dni: {dni} no existe", e)

        try:
            asignatura = self.dictAsignaturas[codigo]
        except Exception as e:
            print(f"La asigntura con codigo: {codigo} no existe", e)

        alumno.add_asignatura(codigo, asignatura.creditos)

    def eliminar_alumno(self, dni):
        try:
            self.dictAlumnos.pop(dni)
        except Exception as e:
            print(f"No existe el alumno con dni: {dni}", e)

    def cambiar_departamento(self, dni, departamento):
        #Controlada la excepción en caso de que la clave por la que se indexa no exista.
        try:
            profesor = self.dictProfesores[dni]
        except Exception as e:
            print(f"El profesor con dni: {dni} no existe", e)

        profesor.cambiar_departamento(departamento)


    def obtener_profesor(self, dni):
        try:
            return self.dictProfesores[dni]
        except Exception as e:
            print(f"El profesor con dni: {dni} no existe", e)

    def obtener_alumno(self, dni):
        try:
            return self.dictAlumnos[dni]
        except Exception as e:
            print(f"El alumno con dni: {dni} no existe", e)

    def obtener_asignatura(self, codigo):
        try:
            return self.dictAsignaturas[codigo]
        except Exception as e:
            print(f"La asigntura con codigo: {codigo} no existe", e)

    def __str__(self):
        print(f"dictProfesores: {self.dictProfesores} \n")
        print(f"dictAlumnos: {self.dictAlumnos} \n")
        print(f"dictAsignaturas: {self.dictAsignaturas} \n")
        return "\n"


def test_add_profesor_titular():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", "V", True, EDepartamento.DIIC, "software")
    assert len(universidad.dictProfesores) == 1

def test_add_profesor_asociado():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", "V", False, EDepartamento.DIIC, trabajoExterno="Programador")
    assert len(universidad.dictProfesores) == 1

def test_add_alumno():
    universidad = Universidad()
    universidad.add_alumno("Carlos", "3423", "V", 1)
    assert len(universidad.dictAlumnos) == 1

def test_add_alumno_mismo_dni():
    universidad = Universidad()
    universidad.add_alumno("Carlos", "3423", "V", 1)
    universidad.add_alumno("Felipe", "3423", "V", 3)
    assert len(universidad.dictAlumnos) == 1

def test_add_asignatura():
    universidad = Universidad()
    universidad.add_asignatura(1234, 6, 1)
    assert len(universidad.dictAsignaturas) == 1

def test_add_asignatura_profesor():
    profesor = Titular("Jose", "1234", "V", EDepartamento.DIIC, "software")
    asignatura = Asignatura("3124", 6, 2)
    profesor.add_asignatura(asignatura.codigo, asignatura.creditos)
    assert len(profesor.asignaturas) == 1

def test_exceso_creditos_profesor():
    with pytest.raises(ValueError):
        profesor = Titular("Jose", "1234", "V", EDepartamento.DIIC, "software")
        asignatura = Asignatura("3124", 73, 2)
        profesor.add_asignatura(asignatura.codigo, asignatura.creditos)

def test_add_asignatura_alumno():
    alumno = Estudiante("Carlos", "1234", "V", 2)
    asignatura = Asignatura("3124", 6, 1)
    alumno.add_asignatura(asignatura.codigo)
    assert len(alumno.asignaturasMatriculadas) == 1

def test_aprobar_asignatura():
    alumno = Estudiante("Carlos", "1234", "V", 2)
    asignatura = Asignatura("3124", 6, 1)
    alumno.add_asignatura(asignatura.codigo)
    alumno.aprobar_asignatura(asignatura.codigo)
    assert len(alumno.asignaturasMatriculadas) == 0 and len(alumno.asignaturasAprobadas) == 1

'''
No entiendo por qué el test sale mal, pero se puede comprobar con el print que el método
funciona correctamente.
'''
def test_cambiar_departamento():
    profesor = Titular("Jose", "1234", "V", EDepartamento.DIIC, "software")
    profesor.cambiar_departamento(EDepartamento.DITEC)
    print(profesor.departamento)
    raise profesor.departamento == EDepartamento.DITEC

if __name__ == "__main__":
    titular = Titular("Jose", "1234", "V", EDepartamento.DIIC, "software")
    asociado = Asociado("Hernesto", "1235", "V", EDepartamento.DITEC, "Programador")
    alumno = Estudiante("Carlos", "1236", "V", 2)
    asignatura = Asignatura("3124", 6, 1)
    universidad = Universidad()

    print(titular)
    print(asociado)
    print(alumno)
    print(asignatura)
    print(universidad)
