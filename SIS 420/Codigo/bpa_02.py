# Busqueda primero en anchura - Breadth First Search
from Nodos import Nodo

def busqueda_BPA_solucion(conecciones, estado_inicial, solucion):
    resuelto = False
    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    while (not resuelto) and len(nodos_frontera) != 0:
        # nodo = nodos_frontera[0]
        nodo_actual = nodos_frontera.pop(0)
        # extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodo_actual)
        if nodo_actual.get_estado() == solucion:
            resuelto = True
            return nodo_actual
        else:
            # expandir nodos hijo
            estado_nodo = nodo_actual.get_estado()
            lista_hijos = []
            for chld in conecciones[estado_nodo]:
                hijo = Nodo(chld)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)

            nodo_actual.set_hijo(lista_hijos)


if __name__ == "__main__":
    conecciones = {
        'Malaga': {'Salamanca', 'Madrid', 'Barcelona'},
        'Sevilla': {'Santiago', 'Madrid'},
        'Granada': {'Valencia'},
        'Valencia': {'Barcelona'},
        'Madrid': {'Salamanca', 'Sevilla', 'Malaga', 'Barcelona', 'Santander'},
        'Salamanca': {'Malaga', 'Madrid'},
        'Santiago': {'Sevilla', 'Santander', 'Barcelona'},
        'Santander': {'Santiago', 'Madrid'},
        'Zaragoza': {'Barcelona'},
        'Barcelona': {'Zaragoza', 'Santiago', 'Madrid', 'Malaga', 'Valencia'}
    }

    estado_inicial = 'Malaga'
    solucion = 'Santiago'
    nodo_solucion = busqueda_BPA_solucion(conecciones, estado_inicial, solucion)
    # mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_estado())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
