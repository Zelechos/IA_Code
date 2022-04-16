# Puzle lineal con Busqueda en Profundidad - Deep First Search
from Nodos import Nodo


def busqueda_BPP(estado_inicial, solucion):
    resuelto = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_raiz = Nodo(estado_inicial)
    nodos_frontera.append(nodo_raiz)
    while (not resuelto) and len(nodos_frontera) != 0:
        nodo_actual = nodos_frontera.pop()
        # Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodo_actual)
        if nodo_actual.get_estado() == solucion:
            # Solucion encontrada
            resuelto = True
            return nodo_actual
        else:
            # Expandir nodos hijos
            datos_nodo = nodo_actual.get_estado()
            # Operador Izquierdo
            hijo = [datos_nodo[1], datos_nodo[0], datos_nodo[2], datos_nodo[3]]
            hijo_izquierda = Nodo(hijo)
            if not hijo_izquierda.en_lista(nodos_visitados) and not hijo_izquierda.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izquierda)
            # Operador Central
            hijo = [datos_nodo[0], datos_nodo[2], datos_nodo[1], datos_nodo[3]]
            hijo_centro = Nodo(hijo)
            if not hijo_centro.en_lista(nodos_visitados) and not hijo_centro.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_centro)
            # Operador Derecho
            hijo = [datos_nodo[0], datos_nodo[1], datos_nodo[3], datos_nodo[2]]
            hijo_derecha = Nodo(hijo)
            if not hijo_derecha.en_lista(nodos_visitados) and not hijo_derecha.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_derecha)
            nodo_actual.set_hijo([hijo_izquierda, hijo_centro, hijo_derecha])

if __name__ == "__main__":
    estado_inicial = [4, 3, 2, 1]
    solucion = [1, 2, 3, 4]
    nodo_solucion = busqueda_BPP(estado_inicial, solucion)
    # Mostrar resultado
    resultado = []
    nodo_actual = nodo_solucion
    while nodo_actual.get_padre() is not None:
        resultado.append(nodo_actual.get_estado())
        nodo_actual = nodo_actual.get_padre()
    
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
