# Búsqueda Coste Uniforme - Uniform Cost Search
from Nodos import Nodo

def Comparar(nodo):
    return nodo.get_costo()

def busqueda_BCU(conecciones, estado_inicial, solucion):
    resuelto = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_raiz = Nodo(estado_inicial)
    nodo_raiz.set_costo(0)
    nodos_frontera.append(nodo_raiz)
    while (not resuelto) and len(nodos_frontera) != 0:
        # Ordenar lista de nodos frontera
        nodos_frontera = sorted(nodos_frontera, key=Comparar)
        nodo_actual = nodos_frontera[0]
        # Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo_actual.get_estado() == solucion:
            # Solucion encontrada
            resuelto = True
            return nodo_actual
        else:
            # Expandir nodos hijo (ciudades con conexion)
            datos_nodo = nodo_actual.get_estado()
            lista_hijos = []
            for achild in conecciones[datos_nodo]:
                hijo = Nodo(achild)
                costo = conecciones[datos_nodo][achild]
                hijo.set_costo(nodo_actual.get_costo() + costo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados):
                    # Si está en la lista lo sustituimos con el nuevo valor de coste si es menor
                    if hijo.en_lista(nodos_frontera):
                        for n in nodos_frontera:
                            if n.equal(hijo) and n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)
            nodo_actual.set_hijo(lista_hijos)


if __name__ == "__main__":
    conecciones = {
        'Malaga': {'Granada': 125, 'Madrid': 513},
        'Sevilla': {'Madrid': 514},
        'Granada': {'Malaga': 125, 'Madrid': 423, 'Valencia': 491},
        'Valencia': {'Granada': 491, 'Madrid': 356, 'Zaragoza': 309, 'Barcelona': 346},
        'Madrid': {'Salamanca': 203, 'Sevilla': 514, 'Malaga': 513, 'Granada': 423, 'Barcelona': 603, 'Santander': 437,
                   'Valencia': 356, 'Zaragoza': 313, 'Santiago': 599},
        'Salamanca': {'Santiago': 390, 'Madrid': 203},
        'Santiago': {'Salamanca': 390, 'Madrid': 599},
        'Santander': {'Madrid': 437, 'Zaragoza': 394},
        'Zaragoza': {'Barcelona': 296, 'Valencia': 309, 'Madrid': 313},
        'Barcelona': {'Zaragoza': 296, 'Madrid': 603, 'Valencia': 396}
    }
    estado_inicial = 'Malaga'
    solucion = 'Santiago'
    nodo_solucion = busqueda_BCU(conecciones, estado_inicial, solucion)
    # Mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_estado())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
    print("Costo: %s" % str(nodo_solucion.get_costo()))
