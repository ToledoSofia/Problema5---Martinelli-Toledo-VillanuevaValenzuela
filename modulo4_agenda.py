
# BACKTRACKING

def asignar_agenda(pacientes_del_dia, franjas, disponibilidad):
    """
    Asigna cada paciente a una franja horaria usando backtracking.

    Precondición:
        - pacientes_del_dia: list de nombres/ids de pacientes a asignar.
        - franjas: list de franjas horarias disponibles (ej: [1,2,3,4,5,6,7,8]).
        - disponibilidad: dict {paciente: [lista de franjas en las que puede asistir]}.

    Postcondición:
        - Devuelve un dict {paciente: franja} donde cada paciente está asignado
          a una franja compatible y no hay dos pacientes en la misma franja.
        - Devuelve None si no existe ninguna asignación válida.

    Estrategia:
        Se asignan los pacientes de a uno por vez (en el orden de pacientes_del_dia).
        Para cada paciente se prueban todas sus franjas disponibles.
        Poda: se descarta una franja si ya está ocupada por otro paciente.
        Si ninguna franja funciona para el paciente actual, se retrocede (backtrack)
        y se prueba otra franja para el paciente anterior.
    """
    asignacion = {}
    franjas_ocupadas = set()
    return _backtrack(pacientes_del_dia, franjas, disponibilidad, asignacion, franjas_ocupadas, 0)

def _backtrack(pacientes, franjas, disponibilidad, asignacion, franjas_ocupadas, indice):
    """
    Función recursiva de backtracking.

    Precondición:
        - pacientes: lista completa de pacientes del día.
        - disponibilidad: dict {paciente: [franjas posibles]}.
        - asignacion: dict parcial {paciente: franja} construido hasta ahora.
        - franjas_ocupadas: set de franjas ya asignadas.
        - indice: posición del paciente actual en la lista.

    Postcondición:
        - Si encuentra una asignación completa válida, la devuelve.
        - Si no encuentra ninguna, devuelve None.
        """
    if indice == len(pacientes):
        return dict(asignacion)

    paciente_actual = pacientes[indice]

    for franja in disponibilidad[paciente_actual]:
        if franja in franjas and franja not in franjas_ocupadas:
            asignacion[paciente_actual] = franja
            franjas_ocupadas.add(franja)

            resultado = _backtrack(pacientes, franjas, disponibilidad, asignacion, franjas_ocupadas, indice + 1)

            if resultado is not None:
                return resultado

            del asignacion[paciente_actual]
            franjas_ocupadas.remove(franja)

    return None

# aux para test
def verificar_asignacion(asignacion, disponibilidad):
    """
    Verifica que una asignación respete todas las restricciones.

    Precondición:
        - asignacion: dict {paciente: franja}.
        - disponibilidad: dict {paciente: [franjas posibles]}.

    Postcondición:
        - Devuelve True si la asignación es válida, False si no.
    """
    # No hay franjas repetidas
    franjas_usadas = list(asignacion.values())
    if len(franjas_usadas) != len(set(franjas_usadas)):
        return False

    # Cada paciente está en una franja compatible
    for paciente, franja in asignacion.items():
        if franja not in disponibilidad[paciente]:
            return False

    return True


# CASOS DE PRUEBA

if __name__ == '__main__':

    pasa = 0
    falla = 0

    # Prueba 1: hay solución 
    """
    Cada paciente tiene franjas disponibles distintas,
    existe al menos una asignación válida.
    """
    franjas = [1, 2, 3, 4, 5, 6, 7, 8]

    pacientes_dia = ['Ana', 'Luis', 'María']

    disponibilidad_caso1 = {
        'Ana':   [1, 2, 3],
        'Luis':  [2, 3, 4],
        'María': [3, 4, 5],
    }

    resultado = asignar_agenda(pacientes_dia, franjas, disponibilidad_caso1)

    if resultado is None:
        print("FALLA caso 1: debería tener solución pero devolvió None")
        falla += 1
    elif verificar_asignacion(resultado, disponibilidad_caso1):
        print(f"[OK] caso con solución: {resultado}")
        pasa += 1
    else:
        print(f"FALLA caso 1: asignación inválida: {resultado}")
        falla += 1


    # Prueba 2: sin solución 
    """
    Todos solo pueden ir a la franja 1.
    Es imposible asignarlos sin repetir franja.
    """
    pacientes_dia2 = ['Carlos', 'Rosa', 'Juan']

    disponibilidad_caso2 = {
        'Carlos': [1],
        'Rosa':   [1],
        'Juan':   [1],
    }

    resultado2 = asignar_agenda(pacientes_dia2, franjas, disponibilidad_caso2)

    if resultado2 is None:
        print("[OK] caso sobre-restringido: devolvió None correctamente")
        pasa += 1
    else:
        print(f"FALLA caso 2: debería devolver None pero devolvió: {resultado2}")
        falla += 1


    # Prueba 3: un solo paciente
    """
    Un solo paciente con varias franjas disponibles.
    Se asigna cualquiera.
    """
    pacientes_dia3 = ['Pedro']
    disponibilidad_caso3 = {
        'Pedro': [3, 5, 7],
    }

    resultado3 = asignar_agenda(pacientes_dia3, franjas, disponibilidad_caso3)

    if resultado3 is None:
        print("FALLA prueba 3: un paciente con franjas disponibles debería tener solución")
        falla += 1
    elif resultado3['Pedro'] in disponibilidad_caso3['Pedro']:
        print(f"[OK] caso un paciente: {resultado3}")
        pasa += 1
    else:
        print(f"FALLA prueba 3: franja asignada no está en la disponibilidad: {resultado3}")
        falla += 1


    print(f"Resultado: {pasa}/3 aprobadas, {falla} fallidas")

    # Fuerza bruta vs backtracking
    """
    Prueba 1 (3 pacientes):
      Fuerza bruta: Ana tiene 3 opciones, Luis 3, María 3 = 27 combinaciones para revisar.
      Backtracking: al asignar Ana=1 y Luis=2, María prueba 3,4,5 y encuentra solucion rápido.
      Si Ana=1 y Luis=1 -> poda (franja ocupada), no se llega a María.
      La poda evita explorar ramas completas en cuanto hay conflicto.
    """
    
