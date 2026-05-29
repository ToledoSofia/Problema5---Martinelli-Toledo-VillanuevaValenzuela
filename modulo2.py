from modulo_a import leer_paciente, TAM_REGISTRO


def construir_indices(ruta):
    """
    Construye índices en memoria a partir del archivo de pacientes.

    Precondición:
        - ruta es la ruta de un archivo binario de pacientes.
        - El archivo contiene registros de tamaño TAM_REGISTRO.

    Postcondición:
        - Devuelve una tupla (indice_por_dni, indice_por_apellido).
        - indice_por_dni relaciona cada DNI con la posición de su registro en el archivo.
        - indice_por_apellido relaciona cada apellido con una lista de posiciones de registros.
        - El archivo se recorre una única vez.
    """

    indice_por_dni = {}
    indice_por_apellido = {}

    with open(ruta, "rb") as archivo:

        archivo.seek(0, 2)
        cantidad_registros = archivo.tell() // TAM_REGISTRO

        for k in range(cantidad_registros):

            paciente = leer_paciente(archivo, k)

            dni = paciente["dni"]
            apellido = paciente["apellido"]

            indice_por_dni[dni] = k

            if apellido not in indice_por_apellido:
                indice_por_apellido[apellido] = []

            indice_por_apellido[apellido].append(k)

    return indice_por_dni, indice_por_apellido


def buscar_por_dni(archivo, indice_por_dni, dni):
    """
    Busca un paciente utilizando el índice por DNI.

    Precondición:
        - archivo es un archivo binario abierto en modo lectura.
        - indice_por_dni es un diccionario que relaciona DNI con posiciones de registros.
        - dni es un entero.

    Postcondición:
        - Devuelve el paciente asociado al DNI indicado.
        - Si el DNI no existe, devuelve None.

    Complejidad:
        - O(1) promedio por acceso al diccionario.
        - Sin índice sería necesario recorrer el archivo secuencialmente, con complejidad O(n).
    """

    if dni not in indice_por_dni:
        return None

    posicion = indice_por_dni[dni]

    return leer_paciente(archivo, posicion)

