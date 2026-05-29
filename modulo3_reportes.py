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
import unicodedata


# ctes del modulo 1

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)  # 75 bytes



# Funciones del modulo 1
# (solo para probar en este módulo)
def _empaquetar_paciente(dni, apellido, nombre, telefono, prioridad):
    return struct.pack(
        FORMATO,
        dni,
        apellido.encode('utf-8')[:30].ljust(30, b'\x00'),
        nombre.encode('utf-8')[:24].ljust(24, b'\x00'),
        telefono.encode('utf-8')[:16].ljust(16, b'\x00'),
        prioridad
    )

def _desempaquetar_paciente(registro):
    dni, apellido_b, nombre_b, telefono_b, prioridad = struct.unpack(FORMATO, registro)
    return {
        'dni':       dni,
        'apellido':  apellido_b.rstrip(b'\x00').decode('utf-8'),
        'nombre':    nombre_b.rstrip(b'\x00').decode('utf-8'),
        'telefono':  telefono_b.rstrip(b'\x00').decode('utf-8'),
        'prioridad': prioridad
    }



# SECCION ALGORITMICA:

def _normalizar(texto):
    """Normaliza texto para comparación: minúsculas sin acentos."""
    return unicodedata.normalize('NFD', texto.lower())

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
            pacientes.append(_desempaquetar_paciente(registro)) #guarda el dict del paciente en la lista
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
# ...
