from modulo_a import crear_archivo_pacientes
from modulo2 import construir_indices, buscar_por_dni
from modulo3_reportes import listar_pacientes_ordenados
from modulo4_agenda import asignar_agenda, verificar_asignacion


def main():

    ruta = "pacientes.dat"

    pacientes = [
        {'dni': 40111222, 'apellido': 'Perez', 'nombre': 'Ana', 'telefono': '111', 'prioridad': 1},
        {'dni': 38999111, 'apellido': 'Gomez', 'nombre': 'Luis', 'telefono': '222', 'prioridad': 2},
        {'dni': 42000888, 'apellido': 'Lopez', 'nombre': 'Maria', 'telefono': '333', 'prioridad': 3},
    ]

    # 1. crear archivo
    crear_archivo_pacientes(ruta, pacientes)

    # 2. construir índices
    indice_dni, _ = construir_indices(ruta)

    # 3. búsqueda por DNI
    with open(ruta, "rb") as archivo:
        dni_buscar = 38999111
        print("Búsqueda por DNI:")
        print(buscar_por_dni(archivo, indice_dni, dni_buscar))
        print()

    # 4. reportes
    print("Orden por apellido:")
    print(listar_pacientes_ordenados(ruta, "apellido"))
    print()

    print("Orden por prioridad:")
    print(listar_pacientes_ordenados(ruta, "prioridad"))
    print()

    # 5. agenda (backtracking)
    pacientes_dia = [p["apellido"] for p in pacientes]

    franjas = [1, 2, 3, 4, 5, 6, 7, 8]

    disponibilidad = {
        "Perez": [1, 2, 3],
        "Gomez": [2, 3, 4],
        "Lopez": [3, 4, 5]
    }

    resultado = asignar_agenda(pacientes_dia, franjas, disponibilidad)

    print("Asignación de agenda:")
    print(resultado)
    print()

    if resultado:
        print("Verificación:")
        print(verificar_asignacion(resultado, disponibilidad))


if __name__ == "__main__":
    main()