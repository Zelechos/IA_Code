# Puzle lineal con Busqueda en Profundidad Recursiva
from Nodos import Nodo


def busqueda_BPPR(nodo_inicial, solucion, visitado):
    visitado.append(nodo_inicial.get_estado())
    if nodo_inicial.get_estado() == solucion:
        return nodo_inicial
    else:
        # Expandir nodos sucesores (hijos)
        datos_nodo = nodo_inicial.get_estado()
        hijo = [datos_nodo[1], datos_nodo[0], datos_nodo[2], datos_nodo[3]]
        hijo_izquierda = Nodo(hijo)
        hijo = [datos_nodo[0], datos_nodo[2], datos_nodo[1], datos_nodo[3]]
        hijo_centro = Nodo(hijo)
        hijo = [datos_nodo[0], datos_nodo[1], datos_nodo[3], datos_nodo[2]]
        hijo_derecha = Nodo(hijo)
        nodo_inicial.set_hijo([hijo_izquierda, hijo_centro, hijo_derecha])

        for nodo_hijo in nodo_inicial.get_hijo():
            if not nodo_hijo.get_estado() in visitado:
                # Llamada Recursiva
                Solution = busqueda_BPPR(nodo_hijo, solucion, visitado)
                if Solution is not None:
                    return Solution
        return None

if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    nodo_solucion = None
    visitado = []
    nodo_inicial = Nodo(estado_inicial)
    nodo_actual = busqueda_BPPR(nodo_inicial, solucion, visitado)

    # Mostrar Resultado
    resultado = []
    while nodo_actual.get_padre() is not None:
        resultado.append(nodo_actual.get_estado())
        nodo_actual = nodo_actual.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
