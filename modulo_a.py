import struct

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)


def _ajustar_cadena(texto, longitud):
    """
    Ajusta una cadena a una longitud fija para almacenamiento binario.

    Precondición:
        - texto es un string.
        - longitud es un entero positivo.

    Postcondición:
        - Devuelve la cadena codificada en UTF-8.
        - Si excede la longitud máxima, se trunca.
        - Si es más corta, struct.pack agrega relleno con bytes nulos.
    """

    while len(texto.encode("utf-8")) > longitud:
        texto = texto[:-1]

    return texto.encode("utf-8")



# Modulo 1 — Persistencia binaria de pacientes

def empaquetar_paciente(dni, apellido, nombre, telefono, prioridad):
    """
    Empaqueta los datos de un paciente en un registro binario de longitud fija.

    Precondición:
        - dni es un entero.
        - apellido, nombre y telefono son strings.
        - prioridad es un entero entre 1 y 3.

    Postcondición:
        - Devuelve un objeto bytes de tamaño TAM_REGISTRO.
        - Las cadenas se codifican en UTF-8.
        - Las cadenas largas se truncan automáticamente.
    """
    
# Prólogo
    apellido_bytes = _ajustar_cadena(apellido, 30)
    nombre_bytes = _ajustar_cadena(nombre, 24)
    telefono_bytes = _ajustar_cadena(telefono, 16)

# Resolución
    registro = struct.pack(FORMATO, dni, apellido_bytes, nombre_bytes, telefono_bytes, prioridad)

# Epílogo
    return registro



def desempaquetar_paciente(registro_bytes):
    """
    Desempaqueta un registro binario y devuelve los datos del paciente.

    Precondición:
        - registro_bytes tiene tamaño TAM_REGISTRO.

    Postcondición:
        - Devuelve un diccionario con los datos del paciente.
        - El relleno de bytes nulos es removido.
        - Las cadenas se decodifican desde UTF-8.
    """

 # Prólogo
    datos = struct.unpack(FORMATO, registro_bytes)

# Resolución
    dni, apellido, nombre, telefono, prioridad = datos

    paciente = {"dni": dni,
                "apellido": apellido.decode("utf-8").rstrip("\x00"),
                "nombre": nombre.decode("utf-8").rstrip("\x00"),
                "telefono": telefono.decode("utf-8").rstrip("\x00"),
                "prioridad": prioridad}

# Epílogo
    return paciente


# Creación del archivo y lectura por acceso directo


def crear_archivo_pacientes(ruta, lista_pacientes):
    """
    Crea un archivo binario de pacientes de longitud fija.

    Precondición:
        - ruta es un string válido.
        - lista_pacientes es una lista de diccionarios.
        - Cada diccionario contiene:
            dni, apellido, nombre, telefono y prioridad.

    Postcondición:
        - Se crea o sobrescribe el archivo indicado.
        - Cada paciente queda almacenado en un registro binario.

    Efectos secundarios:
        - Escritura de archivo binario.
    """

# Prólogo
    with open(ruta, 'wb') as archivo:


# Resolución
        for paciente in lista_pacientes:
            registro = empaquetar_paciente(paciente['dni'],
                paciente['apellido'],
                paciente['nombre'],
                paciente['telefono'],
                paciente['prioridad'])
            
            archivo.write(registro)




def leer_paciente(archivo, k):
    """
    Lee el paciente ubicado en la posición k del archivo.

    Precondición:
        - archivo es un archivo binario abierto en modo lectura.
        - k es un entero mayor o igual a 0.
        - El registro k existe en el archivo.

    Postcondición:
        - Devuelve un diccionario con los datos del paciente.
        - La lectura se realiza mediante acceso directo por offset.

    Efectos secundarios:
        - Modifica la posición del cursor del archivo.
    """


# Prólogo
    offset = k * TAM_REGISTRO
    archivo.seek(offset)

# Resolución
    registro_bytes = archivo.read(TAM_REGISTRO)
    paciente = desempaquetar_paciente(registro_bytes)

# Epílogo
    return paciente



# Casos de prueba
if __name__ == '__main__':
    pacientes = [{ 'dni': 40111222,
            'apellido': 'Gomez',
            'nombre': 'Ana',
            'telefono': '1122334455',
            'prioridad': 1},
        
        {'dni': 38999111,
        'apellido': 'Perez',
        'nombre': 'Juan',
        'telefono': '1166778899',
        'prioridad': 2},

        {'dni': 42000888,
        'apellido': 'Rodriguez',
        'nombre': 'Lucia',
        'telefono': '1144556677',
        'prioridad': 3}]

    ruta_archivo = 'pacientes.dat'


    # Crear archivo binario
    crear_archivo_pacientes(ruta_archivo, pacientes)


    # Leer pacientes por acceso directo
    with open(ruta_archivo, 'rb') as archivo:

        paciente_0 = leer_paciente(archivo, 0)
        paciente_1 = leer_paciente(archivo, 1)
        paciente_2 = leer_paciente(archivo, 2)


    print('Paciente 0:')
    print(paciente_0)
    print()

    print('Paciente 1:')
    print(paciente_1)
    print()

    print('Paciente 2:')
    print(paciente_2)
    print()


    # Verificación del tamaño del archivo
    with open(ruta_archivo, 'rb') as archivo:

        archivo.seek(0, 2)
        tamanio = archivo.tell()


    print('Tamaño del registro:', TAM_REGISTRO)
    print('Tamaño total del archivo:', tamanio)
    print('Cantidad esperada:', len(pacientes) * TAM_REGISTRO)
