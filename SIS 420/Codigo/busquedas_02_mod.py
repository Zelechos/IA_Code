import heapq
from collections import deque
import random
try:
    from itertools import izip
except ImportError:
    izip = zip

class ListaLIFO(deque):
    '''Lista que saca del final.'''

    def sorted(self):
        return list(self)[::-1]

class ListaFIFO(deque):
    '''Lista que saca del inicio.'''
    def pop(self):
        return super(ListaFIFO, self).popleft()

    def sorted(self):
        return list(self)

class ColaPrioridadLimitada(object):
    def __init__(self, limite=None, *args):
        self.limite = limite
        self.queue = list()

    def __getitem__(self, val):
        return self.queue[val]

    def __len__(self):
        return len(self.queue)

    def append(self, x):
        heapq.heappush(self.queue, x)
        if self.limite and len(self.queue) > self.limite:
            self.queue.remove(heapq.nlargest(1, self.queue)[0])

    def pop(self):
        return heapq.heappop(self.queue)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def clear(self):
        for x in self:
            self.queue.remove(x)

    def remove(self, x):
        self.queue.remove(x)

    def sorted(self):
        return heapq.nsmallest(len(self.queue), self.queue)

class TransformarInversaMuestra(object):
    def __init__(self, pesos, objetos):
        assert pesos and objetos and len(pesos) == len(objetos)
        self.objetos = objetos
        tot = float(sum(pesos))
        if tot == 0:
            tot = len(pesos)
            pesos = [1 for x in pesos]
        acumulado = 0
        self.probs = []
        for w, x in izip(pesos, objetos):
            p = w / tot
            acumulado += p
            self.probs.append(acumulado)

    def muestra(self):
        objetivo = random.random()
        i = 0
        while i + 1 != len(self.probs) and objetivo > self.probs[i]:
            i += 1
        return self.objetos[i]

def _generic_arg(iterable, funcion, mejor_funcion):
    valores = [funcion(x) for x in iterable]
    mejor_valor = mejor_funcion(valores)
    candidatos = [x for x, value in zip(iterable, valores) if value == mejor_valor]
    return random.choice(candidatos)

def argmin(iterable, funcion):
    return _generic_arg(iterable, funcion, min)

def argmax(iterable, funcion):
    return _generic_arg(iterable, funcion, max)

class ProblemaBusqueda(object):
    '''Clase base abstracta, para representar y manipular los espacio de busqueda
    de un problema. IEn esta clase, el espacio de búsqueda debe representarse 
    implícitamente como un gráfico.
    Cada estado corresponde con un estado del problema(es decir, una configuración válida) 
    y cada accion del problema(es decir, una transformación válida a una configuración) corresponde con un limite o frontera.
    Para utilizar esta clase se debe implementar metodos requeridos by el algoritmo de busqueda
    que se utilizara.'''

    def __init__(self, estado_inicial=None):
        self.estado_inicial = estado_inicial

    def acciones(self, estado):
        '''Devuelve las acciones disponibles para realizar a partir 'estado.
        El valor devuelto es íterador sobre acciones.
        Las acciones son específicas del problema y no se debe asumir nada sobre ellas.
        '''
        raise NotImplementedError

    def resultado(self, estado, accion):
        '''Debuelve un nuevo estado despues de aplicar una accion a estado.'''
        raise NotImplementedError

    def costo(self, estado, accion, estado2):
        '''Devuelve el costo de aplicar una accion para alcanzar el estado2 a partir de estado.
            El valor devuelto es un numero (intero o de punto flotante),
            por defecto la funcion devuelve 1.
        '''
        return 1

    def es_objetivo(self, estado):
        '''Devuelve True si estado es el estado_objetivo y false caso contrario'''
        raise NotImplementedError

    def valor(self, estado):
        '''Devuelve el valor de `estado`, para motivos de optimizacion.
           valor es un numero (entero o punto flotante).'''
        raise NotImplementedError

    def heuristica(self, estado):
        '''DEvuelve un estimado del costo faltante para alcanzar la solucion a partir de `estado`.'''
        return 0

    def estado_representacion(self, estado):
        """
        Devuelve un string de representacion de un estado.
        Por defecto devuelve str(estado).
        """
        return str(estado)

    def accion_representacion(self, accion):
        """
        Devuelve un string de representacion de una acción.
        Por defecto devuelve str(acción).
        """
        return str(accion)

class NodoBusqueda(object):
    '''Nodo para el proceso de busqueda.'''

    def __init__(self, estado, padre=None, accion=None, costo=0, problema=None, profundidad=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo
        self.problema = problema or padre.problema
        self.profundidad = profundidad

    def expandir(self, busqueda_local=False):
        '''Crear sucesores.'''
        nodos_nuevos = []
        for accion in self.problema.acciones(self.estado):
            estado_nuevo = self.problema.resultado(self.estado, accion)
            costo = self.problema.costo(self.estado,
                                     accion,
                                     estado_nuevo)
            fabrica_nodos = self.__class__
            nodos_nuevos.append(fabrica_nodos(estado=estado_nuevo,
                                         padre=None if busqueda_local else self,
                                         problema=self.problema,
                                         accion=accion,
                                         costo=self.costo + costo,
                                         profundidad=self.profundidad + 1))
        return nodos_nuevos

    def camino(self):
        '''Camino (lista de nodos y acciones) desde el nodo raiz al nodo actual.'''
        nodo = self
        camino = []
        while nodo:
            camino.append((nodo.accion, nodo.estado))
            nodo = nodo.padre
        return list(reversed(camino))

    def __eq__(self, otro):
        return isinstance(otro, NodoBusqueda) and self.estado == otro.estado

    def estado_representacion(self):
        return self.problema.estado_representacion(self.estado)

    def accion_representacion(self):
        return self.problema.accion_representacion(self.accion)

    def __repr__(self):
        return 'Node <%s>' % self.estado_representacion().replace('\n', ' ')

    def __hash__(self):
        return hash((
            self.estado,
            self.padre,
            self.accion,
            self.costo,
            self.profundidad,
        ))

class NodoBusquedaCostoOrdenado(NodoBusqueda):
    def __lt__(self, otro):
        return self.costo < otro.costo


class NodoBusquedaValorOrdenado(NodoBusqueda):
    def __init__(self, *args, **kwargs):
        super(NodoBusquedaValorOrdenado, self).__init__(*args, **kwargs)
        self.valor = self.problema.valor(self.estado)

    def __lt__(self, otro):
        # el valor debe funcionar invertido, porque heapq clasifica 1-9
        # y se necesita ordenar 9-1
        return -self.valor < -otro.valor

class NodoBusquedaHeuristicaOrdenado(NodoBusqueda):
    def __init__(self, *args, **kwargs):
        super(NodoBusquedaHeuristicaOrdenado, self).__init__(*args, **kwargs)
        self.heuristica = self.problema.heuristica(self.estado)

    def __lt__(self, otro):
        return self.heuristica < otro.heuristica

class NodoBusquedaEstrellaOrdenado(NodoBusquedaHeuristicaOrdenado):
    def __lt__(self, otro):
        return self.heuristica + self.costo < otro.heuristica + otro.costo

class ProblemaCsp(object):
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones

        # variable-based restricciones dict
        self.var_restricciones = dict([(v, [restriccion
                                         for restriccion in restricciones
                                         if v in restriccion[0]])
                                    for v in variables])

        # calcula el grado de cada variable
        self.var_grados = dict([(v, len(self.var_restricciones[v]))
                                 for v in variables])

def primero_anchura(problema, busqueda_en_grafo=False, viewer=None):
    '''
    Busqueda primero en anchura.

    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo.
    '''
    return _buscar(problema,
                   ListaFIFO(),
                   busqueda_en_grafo=busqueda_en_grafo)


def primero_profundidad(problema, busqueda_en_grafo=False, viewer=None):
    '''
    Primero en profundidad.
    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo.
    '''
    return _buscar(problema,
                   ListaLIFO(),
                   busqueda_en_grafo=busqueda_en_grafo)

def primero_profundidad_limitada(problema, limite_profundidad, busqueda_en_grafo=False, viewer=None):
    '''
    Busqueda primero en profundidad limitada.

    limite_profundidad es la maxima profundidad permitida, empieza en 0 el estado inicial.
    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo.
    '''
    return _buscar(problema,
                   ListaLIFO(),
                   busqueda_en_grafo=busqueda_en_grafo,
                   limite_profundidad=limite_profundidad)


def primero_profundidad_limitada_iterativa(problema, busqueda_en_grafo=False):
    '''
    Busqueda primero en profundidad limitada iterativa.

    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo.
    '''
    solucion = None
    limite = 0

    while not solucion:
        solucion = primero_profundidad_limitada(problema,
                                       limite_profundidad=limite,
                                       busqueda_en_grafo=busqueda_en_grafo,
                                       viewer=viewer)
        limite += 1

    if viewer:
        viewer.event('no_more_runs', solucion, 'returned after %i runs' % limite)

    return solucion


def costo_uniforme(problema, busqueda_en_grafo=False):
    '''
    Busqueda costo uniforme.

    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo.
    '''
    return _buscar(problema,
                   ColaPrioridadLimitada(),
                   busqueda_en_grafo=busqueda_en_grafo,
                   fabrica_nodos=NodoBusquedaCostoOrdenado,
                   reemplazar_grafo_cuando_mejor=True)


def voraz(problema, busqueda_en_grafo=False, viewer=None):
    '''
    Busqueda voraz.

    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo, ProblemaBusqueda.costo,
    ProblemaBusqueda.heuristica.
    '''
    return _buscar(problema,
                   ColaPrioridadLimitada(),
                   busqueda_en_grafo=busqueda_en_grafo,
                   fabrica_nodos=NodoBusquedaHeuristicaOrdenado,
                   reemplazar_grafo_cuando_mejor=True)


def aestrella(problema, busqueda_en_grafo=False, viewer=None):
    '''
    Busuqeda A*.

    Si se establece busqueda_en_grafo=True, se eliminara la busqueda en estados repetidos.
    Requiere redefinir las funciones de la clase ProblemaBusqueda:
    ProblemaBusqueda.acciones, ProblemaBusqueda.resultado, y
    ProblemaBusqueda.es_objetivo, ProblemaBusqueda.costo,
    ProblemaBusqueda.heuristica.
    '''
    return _buscar(problema,
                   ColaPrioridadLimitada(),
                   busqueda_en_grafo=busqueda_en_grafo,
                   fabrica_nodos=NodoBusquedaEstrellaOrdenado,
                   reemplazar_grafo_cuando_mejor=True)


def _buscar(problema, frontera, busqueda_en_grafo=False, limite_profundidad=None,
            fabrica_nodos=NodoBusqueda, reemplazar_grafo_cuando_mejor=False):
    '''
    Algoritmo basico de busqueda, base de todos los demas algoritmos de busqueda.
    '''
    memoria = set()
    nodo_inicio = fabrica_nodos(estado=problema.estado_inicial, problema=problema)
    frontera.append(nodo_inicio)

    while frontera:
        nodo = frontera.pop()

        if problema.es_objetivo(nodo.estado):
            return nodo
    
        memoria.add(nodo.estado)

        if limite_profundidad is None or nodo.profundidad < limite_profundidad:
            expandido = nodo.expandir()
    
            for n in expandido:
                if busqueda_en_grafo:
                    otros = [x for x in frontera if x.estado == n.estado]
                    assert len(otros) in (0, 1)
                    if n.estado not in memoria and len(otros) == 0:
                        frontera.append(n)
                    elif reemplazar_grafo_cuando_mejor and len(otros) > 0 and n < otros[0]:
                        frontera.remove(otros[0])
                        frontera.append(n)
                else:
                    frontera.append(n)