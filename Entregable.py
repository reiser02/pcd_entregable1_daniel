from enum import Enum

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
        self.creditos = 0
        self.departamento = departamento
        self.asignaturas = list()

    def add_asignatura(self, asignatura):
        for e in self.asignaturas:
            if asignatura is e:
                return
            
        if self.creditos + asignatura.creditos > 72:
            raise ValueError("Se excede el máximo de créditos que un profesor puede impartir")
        self.creditos += asignatura.creditos
        self.asignaturas.append(asignatura)

class Titular(Profesor):
    def __init__(self, nombre, dni, departamento, areaInvestivacion):
        super().__init__(nombre, dni, departamento)
        self.areaInvestivacion = areaInvestivacion
    
    def obtener_area_inv(self):
        return self.areaInvestivacion.area
    
    def __str__(self):
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Departamento: {self.departamento}\n")
        print(f"Area de investigación: {self.areaInvestivacion}\n")
        print(f"Creditos: {self.creditos}\n")
        print(f"Asignaturas: ")
        for a in self.asignaturas:
            print(a.codigo)

class Asociado(Profesor):
    def __init__(self, nombre, dni, departamento, trabajoExterno):
        super().__init__(nombre, dni, departamento)
        self.trabajoExterno = trabajoExterno

    def __str__(self):
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Departamento: {self.departamento}\n")
        print(f"Trabajo externo: {self.trabajoExterno}\n")
        print(f"Creditos: {self.creditos}\n")
        print(f"Asignaturas: ")
        for a in self.asignaturas:
            print(a.codigo)

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

class Estudiante(Persona):
    def __init__(self, nombre, dni, curso):
        super().__init__(nombre, dni)
        self.curso = curso
        self.asignaturas = list()

    def add_asignatura(self, asignatura):
        for e in self.asignaturas:
            if asignatura is e:
                return
        
        self.asignaturas.append(asignatura)

    def __str__(self):
        cursos = ["Primero", "Segundo", "Tercero", "Cuarto"]
        print(f"Nombre: {self.nombre}\n")
        print(f"DNI: {self.dni}\n")
        print(f"Curso: {cursos[self.curso]}\n")
        print(f"Asignaturas: ")
        for a in self.asignaturas:
            print(a.codigo)


class Universidad():
    def __init__(self):
        self.listaProfesores = list()
        self.listaAlumnos = list()
        self.listaAsignaturas = list()

    def add_profesor(self, nombre, dni, titular, departamento, areaInv=None, trabajoExterno=None):
        if not isinstance(departamento, EDepartamento):
            raise TypeError("Departamento no pertece a la clase EDepartamento")
        
        for p in self.listaProfesores:
            if dni == p.dni:
                return 
        
        if titular:
            if areaInv is None:
                raise ValueError("Si el profesor es titular, debe tener area de investigación")
            elif trabajoExterno is not None:
                raise ValueError("Si el profesor es titular, no debe tener un trabajo externo")
            self.listaProfesores.append(Titular(nombre, dni, departamento, areaInv))
        else:
            self.listaProfesores.append(Asociado(nombre, dni, departamento, trabajoExterno))

    def add_alumno(self, nombre, dni, curso):
        for a in self.listaAlumnos:
            if dni == a.dni:
                return
        
        self.listaAlumnos.append(Estudiante(nombre, dni, curso))

    def add_asignatura(self, codigo, creditos, curso):
        for a in self.listaAsignaturas:
            if codigo == a.codigo:
                return
            
        self.listaAsignaturas.append(Asignatura(codigo, creditos, curso))

    def add_asignatura_profesor(self, dni, codigo):
        for p in self.listaProfesores:
            if dni == p.dni:
                for a in self.listaAsignaturas:
                    if codigo == a.codigo:
                        p.add_asignatura(a)
                        break

    def add_asignatura_alumno(self, dni, codigo):
        for a in self.listaAlumnos:
            if dni == a.dni:
                for asig in self.listaAsignaturas:
                    if codigo == asig.codigo:
                        a.add_asignatura(asig)
                        break

    def obtener_profesor(self, dni):
        for p in self.listaProfesores:
            if dni == p.dni:
                return p

    def obtener_alumno(self, dni):
        for a in self.listaAlumnos:
            if dni == a.dni:
                return a

    def obtener_asignatura(self, codigo):
        for a in self.listaAsignaturas:
            if codigo == a.codigo:
                return a