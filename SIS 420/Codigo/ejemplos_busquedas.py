from busquedas_01 import *

INICIO = (4, 1, 0, 2, 7, 3, 8, 5, 6)
OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def encontrar_ubicacion(filas, elemento_a_encontrar):
    '''Encuentra la posicion de una pieza en el puzzle.
       Devuelve una tupla: fila, columna'''
    for infi, elemento in enumerate(filas):
        if elemento == elemento_a_encontrar:
            return infi // 3, infi % 3

# Se crea un cache para las posiciones del estado_objetivo position de cada piesa, 
# para no tener que recalcularlos cada vez

posiciones_objetivo = {}
filas_objetivo = {str(c) for c in OBJETIVO}

for numero in '123456780':
    posiciones_objetivo[numero] = encontrar_ubicacion(filas_objetivo, numero)

class EigthPuzzleProblema(Problema):
    def __init__(self, estado_inicial, estado_objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define estado_objetivo estado and initialize a problem """
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        Problema.__init__(self, estado_inicial, estado_objetivo)

    def encontrar_cuadro_vacio(self, estado):
        """Devuelve el indice del cuadrado vacio en un estado"""
        return estado.index(0)
    
    def acciones(self, estado):
        """Devuelve las acciones que pueden se ejecutadas en un estado.
        El resultado sera una lista, ya que solo hay cuatro acciones posibles 
        en un determinado estado."""
        
        acciones_posibles = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        indice_cuadro_vacio = self.encontrar_cuadro_vacio(estado)

        if indice_cuadro_vacio % 3 == 0:
            acciones_posibles.remove('LEFT')
        if indice_cuadro_vacio < 3:
            acciones_posibles.remove('UP')
        if indice_cuadro_vacio % 3 == 2:
            acciones_posibles.remove('RIGHT')
        if indice_cuadro_vacio > 5:
            acciones_posibles.remove('DOWN')

        return acciones_posibles

    def resultado(self, estado, accion):
        """Dado un estado y accion, devuelve un nuevo estado que es resultado de ejecutar la accion.
        Accion es asumida para
        Se asume que la acción es un accion válido en el estado """

        # vacio es el indice del cuadrado en blanco
        indice_cuadro_vacio = self.encontrar_cuadro_vacio(estado)
        estado_nuevo = list(estado)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        indice_vecino = indice_cuadro_vacio + delta[accion]
        estado_nuevo[indice_cuadro_vacio], estado_nuevo[indice_vecino] = estado_nuevo[indice_vecino], estado_nuevo[indice_cuadro_vacio]

        return tuple(estado_nuevo)

    def es_objetivo(self, estado):
        '''Devuelve verdadero si un estado es estado objetivo.'''
        return estado == self.estado_objetivo

    def costo(self, estado1, accion, estado2):
        '''Devuelve el costo de ejecutar una accion. '''
        return 1

    def comprobar_solubilidad(self, estado):
        """ Verifica si estado es soluble """

        inversion = 0
        for i in range(len(estado)):
            for j in range(i + 1, len(estado)):
                if (estado[i] > estado[j]) and estado[i] != 0 and estado[j]!= 0:
                    inversion += 1
        
        return inversion % 2 == 0
    
    #def h(self, nodo):
    #    '''Devuelve una estimacion de la distancia de un estado al estado_objetivo.
    #       Se utilizara la distancia manhattan.
    #    '''
    #    filas = {str(c) for c in nodo.estado}
    #    distancia = 0

    #    for numero in '123456780':
    #        fila_n, columna_n = encontrar_ubicacion(filas, numero)
    #        fila_n_objetivo, columna_n_objetivo = posiciones_objetivo[numero]

    #        distancia += abs(fila_n - fila_n_objetivo) + abs(columna_n - columna_n_objetivo)

    #    return distancia

    def h(self, nodo):
        """ Devuelve un valor de heuristica para un estado.
        La funcion heuristica usada es:
        h(n) = cantidad de cuadros mal ubicados"""

        return sum(s != g for (s, g) in zip(nodo.estado, self.estado_objetivo))

#eight_puzzle = EigthPuzzleProblema((1, 0, 6, 8, 7, 5, 4, 2, 3), (1, 2, 3, 4, 5, 6, 7, 8, 0))
eight_puzzle = EigthPuzzleProblema(INICIO, OBJETIVO)

#def test_encontrar_limite_minimo():
#    assert romania_problem.find_min_edge() == 70

def test_busqueda_arbol_primero_anchura():
    return busqueda_arbol_primero_anchura(eight_puzzle)

def test_busqueda_arbol_primero_profundidad():
    return busqueda_arbol_primero_profundidad(eight_puzzle)

def test_busqueda_grafo_primero_profundidad():
    return busqueda_grafo_primero_profundidad(eight_puzzle)

def test_busqueda_primero_anchura():
    return busqueda_primero_anchura(eight_puzzle)

def test_busqueda_costo_uniforme():
    return busqueda_costo_uniforme(eight_puzzle)

def test_busqueda_profundidad_limitada():
    return busqueda_profundidad_limitada(eight_puzzle)

def test_busqueda_profundidad_iterativa():
    return busqueda_profundidad_iterativa(eight_puzzle)

def test_busqueda_grafo_primero_mejor():
    return busqueda_grafo_primero_mejor(eight_puzzle, lambda nodo: nodo.estado)

def test_busqueda_a_estrella():
    return busqueda_a_estrella(eight_puzzle)

def main():
    #nodo_solucion = test_busqueda_arbol_primero_anchura()
    #nodo_solucion = test_busqueda_arbol_primero_profundidad()
    #nodo_solucion = test_busqueda_grafo_primero_profundidad()
    #nodo_solucion = test_busqueda_primero_anchura()
    #nodo_solucion = test_busqueda_costo_uniforme()
    #nodo_solucion = test_busqueda_profundidad_limitada()
    #nodo_solucion = test_busqueda_profundidad_iterativa()
    #nodo_solucion = test_busqueda_grafo_primero_mejor()
    nodo_solucion = test_busqueda_a_estrella()
    
    # Mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.padre is not None:
        resultado.append(nodo.estado)
        nodo = nodo.padre
    resultado.append(INICIO)
    resultado.reverse()
    for e in resultado:
        print(e[:3])
        print(e[3:6])
        print(e[6:])
        print('\n')

if __name__ == '__main__':
    main()