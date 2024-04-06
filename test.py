from Entregable import Universidad, Asignatura, Titular, Estudiante, EDepartamento
import pytest

def test_add_profesor_titular():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", True, EDepartamento.DIIC, "software")
    assert len(universidad.listaProfesores) == 1

def test_add_profesor_asociado():
    universidad = Universidad()
    universidad.add_profesor("Jose", "1234", False, EDepartamento.DIIC, trabajoExterno="Programador")
    assert len(universidad.listaProfesores) == 1

def test_add_alumno():
    universidad = Universidad()
    universidad.add_alumno("Carlos", "3423", 1)
    assert len(universidad.listaAlumnos) == 1

def test_add_alumno_mismo_dni():
    universidad = Universidad()
    universidad.add_alumno("Carlos", "3423", 1)
    universidad.add_alumno("Felipe", "3423", 3)
    assert len(universidad.listaAlumnos) == 1

def test_add_asignatura():
    universidad = Universidad()
    universidad.add_asignatura(1234, 6, 1)
    assert len(universidad.listaAsignaturas) == 1

def test_add_asignatura_profesor():
    profesor = Titular("Jose", "1234", EDepartamento.DIIC, "software")
    asignatura = Asignatura("PCD", 6, 2)
    profesor.add_asignatura(asignatura)
    assert len(profesor.asignaturas) == 1

def test_exceso_creditos_profesor():
    with pytest.raises(ValueError):
        profesor = Titular("Jose", "1234", EDepartamento.DIIC, "software")
        asignatura = Asignatura("PCD", 73, 2)
        profesor.add_asignatura(asignatura)

def test_add_asignatura_alumno():
    alumno = Estudiante("Carlos", "1234", 2)
    asignatura = Asignatura(3412, 6, 1)
    alumno.add_asignatura(asignatura)
    assert len(alumno.asignaturas) == 1