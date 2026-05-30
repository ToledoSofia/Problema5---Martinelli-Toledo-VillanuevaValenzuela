"""
SECCION DECLARATIVA:
MÓDULO 3 — Reportes ordenados

Implementa listado de pacientes ordenados por criterio usando merge sort estable.

Estructura del registro :
    FORMATO       = '<i30s24s16sB'
    TAM_REGISTRO  = struct.calcsize(FORMATO) 

Interfaz modulo 1 
    - FORMATO, TAM_REGISTRO 
    - desempaquetar_paciente(bytes_registro) dict con claves:
          'dni', 'apellido', 'nombre', 'telefono', 'prioridad'
"""

import struct
import os
import tempfile
import unicodedata
from modulo_a import desempaquetar_paciente, empaquetar_paciente

# ctes del modulo 1

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)  # 75 bytes




# SECCION ALGORITMICA:

def _normalizar(texto):
    """Normaliza texto para comparación: minúsculas sin acentos."""
    return"".join(char for char in unicodedata.normalize('NFD', texto.lower())
    if unicodedata.category(char) != "Mn")

# merge_sort estable:

def merge_sort(lista, funcion_clave):
    """
    Ordena la lista de forma estable usando merge sort.

    Precondición:
    - lista: list de cualquier elemento.
    - funcion_clave: funcion que recibe un paciente y devuelve el valor para comparar.

    Postcondición:
    - Devuelve una nueva lista ordenada ascendentemente según `funcion_clave`.
    - El orden relativo de elementos con igual clave se mantiene (estabilidad).
    Complejidad: O(n log n) tiempo, O(n) espacio auxiliar.
    """
    if len(lista) <= 1:
        return lista[:]

    mid = len(lista) >> 1
    izquierda = merge_sort(lista[:mid], funcion_clave) 
    derecha   = merge_sort(lista[mid:], funcion_clave)
    return _fusionar(izquierda, derecha, funcion_clave)


def _fusionar(izq, der, clave):
    """
    Fusiona dos listas ya ordenadas en una sola lista ordenada.
    Usa '<='  para mantener el orden original de elementos con clave igual: 
    en el empate agarra primero el de la izquierda --> ESTABILIDAD.
    """
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        # < : en empate se toma primero el de la izquierda
        # preserva orden original = estable
        if clave(izq[i]) <= clave(der[j]): #clave() devuelve el apellido normalizado o prioridad del paciente (solo para comparar, no lo muestra)
            # <= en empate agarra primero el de la  izquierda  preservando el orden original.
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado



# Listar pacientes ordenados

# funciones para las claves por si se quiere agregar otra después.
def apellido(paciente):
    return _normalizar(paciente["apellido"])

def prioridad(paciente):
    return paciente["prioridad"]


def listar_pacientes_ordenados(ruta, criterio):
    """
    Lee todos los pacientes del archivo binario y devuelve la lista ordenada

    Precondición:
    - ruta: path de un archivo binario de registros de pacientes.
    - criterio: "apellido" o "prioridad".
    Postcondición:
    - Devuelve list[dict] ordenada según criterio:
        apellido: orden alfabético ascendente por apellido.
        prioridad: orden por prioridad (1=alta … 3=baja); dentro de cada prioridad orden alfabético por apellido.
        - Sin modificar el archivo original

    Ordenamiento por prioridad (dos pasadas estables):
    - Pasada 1: merge_sort por apellido (alfabetico)
    - Pasada 2: merge_sort por prioridad: agrupa por prioridad; 
    la estabilidad garantiza que el sub-orden de la pasada 1 se mantenga dentro del grupo
      
    Errores:
    - ValueError: si criterio no es 'apellido' ni 'prioridad'
    - FileNotFoundError: si ruta no existe.
    """
    if criterio not in ('apellido', 'prioridad'):
        raise ValueError(f"Criterio invalido: '{criterio}'. Debe ser 'apellido' o 'prioridad'.")

    pacientes = _leer_todos(ruta)

    if criterio == 'apellido':
        return merge_sort(pacientes, apellido)

    # criterio == 'prioridad'
    por_apellido = merge_sort(pacientes, apellido) # ordena por apellido
    por_prioridad = merge_sort(por_apellido, prioridad) # ordena por prioridad conservando el orden de apellidos
    return por_prioridad


def _leer_todos(ruta):
    """
    Lee todos los registros del archivo binario.

    Precondición: ruta apunta a un archivo binario de registros de TAM_REGISTRO bytes.
    Postcondición: devuelve list[dict] con todos los pacientes.
    """
    pacientes = []
    with open(ruta, 'rb') as f:
        registro = f.read(TAM_REGISTRO)
        while len(registro) == TAM_REGISTRO: # si es menos de los bytes (o cero) es porque termino de recorrer
            pacientes.append(desempaquetar_paciente(registro)) #guarda el dict del paciente en la lista
            registro = f.read(TAM_REGISTRO)
    return pacientes


# (f) JUSTIFICACIÓN DE LA ESTABILIDAD

JUSTIFICACION_ESTABILIDAD = """
(f) Por qué la estabilidad del algoritmo de ordenamiento es relevante
para el criterio "prioridad":

El objetivo es ordenar una lista de pacientes por prioridad (1, 2, 3) y, dentro de cada grupo, ordenarlos
alfabeticamente por apellido.

Dos pasadas con el merge_sort estable:

  Pasada 1 --> ordenar por apellido:
      Se aplica merge_sort con clave=apellido.
      Resultado: los pacientes quedan en orden alfabetico sin importar prioridad.
      Esto "fija el orden alfabético que queremos mantener.

  Pasada 2 --> ordenar por prioridad:
      Se aplica merge_sort con clave=prioridad sobre la lista ya ordenada.
      Un algoritmo Estable garantiza que para dos pacientes con la misma
      prioridad, su orden relativo NO cambia respecto a la entrada.
      Como la entrada ya está en orden alfabetico, el resultado final tiene
      los grupos de prioridad en orden Y, dentro de cada grupo, los apellidos
      en orden alfabético.

Si el algoritmo no es estable, al ordenar por prioridad puede
intercambiar libremente pacientes con la misma prioridad, deshaciendo
el orden alfabético de la pasada 1.

La estabilidad de merge_sort se asegura usando comparación '<='  en el caso de empate, 
se toma primero el elemento de la mitad izquierda (que viene de posiciones anteriores en la lista de entrada).
"""


# CASOS DE PRUEBA

def crear_archivo(lista_pacientes):
    tf = tempfile.NamedTemporaryFile(suffix='.bin', delete=False)
    tf.close()
    with open(tf.name, 'wb') as f:
        for p in lista_pacientes:
            f.write(empaquetar_paciente(
                p['dni'], p['apellido'], p['nombre'],
                p['telefono'], p['prioridad']
            ))
    return tf.name

if __name__ == '__main__':
    pasa = 0
    falla = 0

    # PRUEBA merge_sort

    """
    Elementos con la misma clave deben mantener su orden original.
    Los tres pacientes tienen la misma prioridad (1).
    Orden original: Pérez, García, Álvarez.
    Tienen todos la misma prioridad, entonces deberian mantener el mismo orden.
    """
    pacientes = [
        {'dni': 1, 'apellido': 'Pérez',   'nombre': 'Ana',  'telefono': '111', 'prioridad': 1},
        {'dni': 2, 'apellido': 'García',  'nombre': 'Luis', 'telefono': '222', 'prioridad': 1},
        {'dni': 3, 'apellido': 'Álvarez', 'nombre': 'Juan', 'telefono': '333', 'prioridad': 1},
    ]
    resultado = merge_sort(pacientes, prioridad)
    dnis = [p['dni'] for p in resultado]
    if dnis != [1,2,3]:
        print(f"FALLA: merge_sort no es estable, orden de dnis:{dnis}")
        falla +=1
    else:
        print("[OK] merge_sort: estabilidad con claves iguales")
        pasa += 1


    # PRUEBA listar_pacientes_ordenados — criterio 'apellido'

    """Los apellidos deben quedar en orden alfabético ascendente. 
    Incluyendo apellidos con tildes y repetidos"""
    pacientes = [
        {'dni': 1, 'apellido': 'Rodríguez', 'nombre': 'Ana',    'telefono': '111', 'prioridad': 2},
        {'dni': 2, 'apellido': 'García',    'nombre': 'Luis',   'telefono': '222', 'prioridad': 1},
        {'dni': 3, 'apellido': 'Álvarez',   'nombre': 'María',  'telefono': '333', 'prioridad': 3},
        {'dni': 4, 'apellido': 'Pérez',     'nombre': 'Carlos', 'telefono': '444', 'prioridad': 1},
        {'dni': 5, 'apellido': 'Pérez',     'nombre': 'Juan', 'telefono': '555', 'prioridad': 1},
    ]
    ruta = crear_archivo(pacientes)
    try:
        resultado = listar_pacientes_ordenados(ruta, 'apellido')
        apellidos = [p['apellido'] for p in resultado]
        if apellidos == ['Álvarez', 'García', 'Pérez', 'Pérez', 'Rodríguez']:
            print("[OK] apellido: orden alfabético básico")
            pasa += 1
        else:
            print(f"Orden incorrecto: {apellidos}")
            falla +=1
    finally:
        os.unlink(ruta)



    # PRUEBA listar_pacientes_ordenados — criterio 'prioridad'

    """ Debe ordenarse por prioridad, dentro de cada prioridad los apellidos deben estar en orden alfabético."""
    pacientes = [
        {'dni': 1, 'apellido': 'Pérez',     'nombre': 'Ana',   'telefono': '111', 'prioridad': 1},
        {'dni': 2, 'apellido': 'Álvarez',   'nombre': 'Luis',  'telefono': '222', 'prioridad': 1},
        {'dni': 3, 'apellido': 'Rodríguez', 'nombre': 'María', 'telefono': '333', 'prioridad': 2},
        {'dni': 4, 'apellido': 'García',    'nombre': 'Juan',  'telefono': '444', 'prioridad': 2},
        {'dni': 5, 'apellido': 'Fernández', 'nombre': 'Rosa',  'telefono': '555', 'prioridad': 1},
    ]
    ruta = crear_archivo(pacientes)
    try:
        resultado = listar_pacientes_ordenados(ruta, 'prioridad')

        prio1 = [p['apellido'] for p in resultado if p['prioridad'] == 1]
        claves1 = [_normalizar(a) for a in prio1]

        prio2 = [p['apellido'] for p in resultado if p['prioridad'] == 2]
        claves2 = [_normalizar(a) for a in prio2]

        if claves1 == sorted(claves1) and claves2 == sorted(claves2): # comparación con sorted
            print(f"[OK] prioridad: sub orden alfabético P1: {prio1}, P2: {prio2}")
            pasa += 1
        else:
            print("FALLA: falla en el orden por prioridad")
            falla += 1
    finally:
        os.unlink(ruta)


    print("-----------------------------------------------")
    print(f"Resultado: {pasa}/3 aprobadas, {falla} fallidas")
    
