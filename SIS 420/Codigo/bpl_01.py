# Puzle lineal con Busqueda en Profundidad Recursiva
from Nodos import Nodo


def busqueda_BPL(estado_inicial, estado_objetivo, limite):
    nodos_explorados = []
    nodo_inicial = Nodo(estado_inicial)
    return BPLR(nodo_inicial, estado_objetivo, limite, nodos_explorados)

def BPLR(nodo_actual, estado_objetivo, limite, nodos_explorados):
    if nodo_actual.get_estado() == estado_objetivo:
        return nodo_actual
    else:
        if limite == 0:
            return None
        else:
            # Expandir nodos sucesores (hijos)
            datos_nodo = nodo_actual.get_estado()
            hijo = [datos_nodo[1], datos_nodo[0], datos_nodo[2], datos_nodo[3]]
            hijo_izquierda = Nodo(hijo)
            hijo = [datos_nodo[0], datos_nodo[2], datos_nodo[1], datos_nodo[3]]
            hijo_centro = Nodo(hijo)
            hijo = [datos_nodo[0], datos_nodo[1], datos_nodo[3], datos_nodo[2]]
            hijo_derecha = Nodo(hijo)
            nodo_actual.set_hijo([hijo_izquierda, hijo_centro, hijo_derecha])

            for nodo_hijo in nodo_actual.get_hijo():
                if not nodo_hijo.get_estado() in nodos_explorados:
                    # Llamada Recursiva
                    Solution = BPLR(nodo_hijo, estado_objetivo, limite - 1, nodos_explorados)
                    if Solution is not None:
                        return Solution

if __name__ == "__main__":
    estado_inicial = [1, 2, 4, 3]
    estado_objetivo = [1, 2, 3, 4]
    limite = 5
 
    nodo_solucion = busqueda_BPL(estado_inicial, estado_objetivo, limite)
    nodo_actual = nodo_solucion
    # Mostrar Resultado
    resultado = []
    while nodo_actual.get_padre() is not None:
        resultado.append(nodo_actual.get_estado())
        nodo_actual = nodo_actual.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
